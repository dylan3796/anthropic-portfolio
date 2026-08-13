/**
 * Ask-Dylan backend — a Cloudflare Worker that fronts a chat model.
 *
 * The portfolio is a static page, so it cannot hold an API key: anything shipped
 * to the browser is scraped and billed to whoever owns it. This Worker holds the
 * key instead and is the only thing that talks to the provider.
 *
 * It is deliberately provider-agnostic. Every provider below speaks the
 * OpenAI-compatible /chat/completions shape, so switching models is two
 * environment variables rather than a rewrite. Anthropic uses a different
 * request shape and gets its own branch.
 *
 * The threat model is a stranger on the internet with the endpoint URL. Defenses,
 * in order of how much they matter:
 *   1. Origin allowlist  — only the portfolio may call it
 *   2. Per-IP rate limit — one visitor cannot drain the budget
 *   3. Global daily cap  — the whole internet cannot either
 *   4. Hard size caps    — bounded input and output on every request
 *
 * The site falls back to local retrieval whenever this Worker is unreachable,
 * rate-limited, or unconfigured, so the page never breaks.
 */

import { SYSTEM_PROMPT, JD_INSTRUCTION } from './corpus.js';

const ALLOWED_ORIGINS = [
  // Pre-registered custom domain (harmless until DNS exists; keep in sync
  // with DOMAIN in build_site.py — see DOMAIN-SETUP.md).
  'https://dylanram.com',
  'https://www.dylanram.com',
  'https://dylan3796.github.io',
  'https://claude.ai',
  'http://localhost:8000',
  'http://127.0.0.1:8000',
];

const LIMITS = {
  perIpPerHour: 30,        // one visitor's share
  globalPerDay: 600,       // the whole site's share
  maxMessages: 16,         // conversation turns kept
  maxCharsPerMessage: 1200,
  maxTotalChars: 8000,
  maxOutputTokens: 700,
  // JD fit-check mode: a pasted job description is legitimately larger and
  // costs several chat calls' worth of tokens, so it gets its own input cap,
  // output budget, and a stricter per-IP limit — NOT a raised global cap.
  jdMaxChars: 6000,
  jdPerIpPerHour: 5,
  jdMaxOutputTokens: 1100,
};

// OpenAI-compatible by default; `anthropic` is the one shape that differs.
const PRESETS = {
  deepseek: { url: 'https://api.deepseek.com/v1', model: 'deepseek-chat' },
  moonshot: { url: 'https://api.moonshot.cn/v1', model: 'moonshot-v1-8k' },
  qwen: { url: 'https://dashscope.aliyuncs.com/compatible-mode/v1', model: 'qwen-plus' },
  zhipu: { url: 'https://open.bigmodel.cn/api/paas/v4', model: 'glm-4-flash' },
  openai: { url: 'https://api.openai.com/v1', model: 'gpt-4o-mini' },
  anthropic: { url: 'https://api.anthropic.com/v1', model: 'claude-haiku-4-5' },
};

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.some((o) => origin === o || origin?.startsWith(o));
  return {
    'Access-Control-Allow-Origin': allowed ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

/** Fixed-window counter in KV. Returns true when the caller is over budget. */
async function overLimit(kv, key, cap, ttlSeconds) {
  if (!kv) return false; // no KV bound — per-request caps still apply
  const current = parseInt((await kv.get(key)) || '0', 10);
  if (current >= cap) return true;
  // expirationTtl refreshes the window on each write, which is fine for a
  // coarse abuse guard and avoids a second read to track window start.
  await kv.put(key, String(current + 1), { expirationTtl: ttlSeconds });
  return false;
}

function sanitize(messages) {
  if (!Array.isArray(messages)) return null;
  const cleaned = [];
  let total = 0;
  for (const m of messages.slice(-LIMITS.maxMessages)) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant')) continue;
    const content = String(m.content ?? '').slice(0, LIMITS.maxCharsPerMessage).trim();
    if (!content) continue;
    total += content.length;
    if (total > LIMITS.maxTotalChars) break;
    cleaned.push({ role: m.role, content });
  }
  // A turn must end with the visitor speaking, or there is nothing to answer.
  if (!cleaned.length || cleaned[cleaned.length - 1].role !== 'user') return null;
  return cleaned;
}

async function callProvider(env, messages, opts = {}) {
  const preset = PRESETS[env.PROVIDER || 'deepseek'] || PRESETS.deepseek;
  const baseUrl = (env.PROVIDER_BASE_URL || preset.url).replace(/\/$/, '');
  const model = env.PROVIDER_MODEL || preset.model;
  const isAnthropic = baseUrl.includes('api.anthropic.com');

  const systemPrompt = opts.jd ? `${SYSTEM_PROMPT}\n\n${JD_INSTRUCTION}` : SYSTEM_PROMPT;
  const maxTokens = opts.jd ? LIMITS.jdMaxOutputTokens : LIMITS.maxOutputTokens;
  const endpoint = isAnthropic ? `${baseUrl}/messages` : `${baseUrl}/chat/completions`;
  const headers = { 'Content-Type': 'application/json' };
  let payload;

  if (isAnthropic) {
    headers['x-api-key'] = env.PROVIDER_API_KEY;
    headers['anthropic-version'] = '2023-06-01';
    payload = {
      model,
      max_tokens: maxTokens,
      system: [{ type: 'text', text: systemPrompt, cache_control: { type: 'ephemeral' } }],
      messages,
    };
  } else {
    headers.Authorization = `Bearer ${env.PROVIDER_API_KEY}`;
    payload = {
      model,
      max_tokens: maxTokens,
      messages: [{ role: 'system', content: systemPrompt }, ...messages],
    };
  }

  const res = await fetch(endpoint, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(45000),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    throw Object.assign(new Error(`provider ${res.status}`), {
      status: res.status,
      detail: detail.slice(0, 300),
    });
  }

  const data = await res.json();
  const reply = isAnthropic
    ? (data.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('')
    : data.choices?.[0]?.message?.content;

  if (!reply) throw new Error('empty completion');
  return reply.trim();
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }
    if (request.method !== 'POST') {
      return json({ error: 'method_not_allowed' }, 405, origin);
    }
    if (origin && !ALLOWED_ORIGINS.some((o) => origin === o || origin.startsWith(o))) {
      return json({ error: 'forbidden_origin' }, 403, origin);
    }
    if (!env.PROVIDER_API_KEY) {
      return json({ error: 'not_configured' }, 503, origin);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'bad_json' }, 400, origin);
    }

    const isJd = body.mode === 'jd';
    let messages;
    if (isJd) {
      // Single-turn by design: a fit check maps one document, it doesn't chat.
      const jd = String(body.jd ?? '').slice(0, LIMITS.jdMaxChars).trim();
      if (jd.length < 80) return json({ error: 'bad_jd' }, 400, origin);
      messages = [{ role: 'user', content: jd }];
    } else {
      messages = sanitize(body.messages);
      if (!messages) return json({ error: 'bad_messages' }, 400, origin);
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const day = new Date(request.headers.get('CF-Request-Date') || Date.now())
      .toISOString()
      .slice(0, 10);

    if (isJd && await overLimit(env.RATE_LIMIT, `jd:${ip}`, LIMITS.jdPerIpPerHour, 3600)) {
      return json({ error: 'rate_limited', scope: 'jd' }, 429, origin);
    }
    if (await overLimit(env.RATE_LIMIT, `ip:${ip}`, LIMITS.perIpPerHour, 3600)) {
      return json({ error: 'rate_limited', scope: 'ip' }, 429, origin);
    }
    if (await overLimit(env.RATE_LIMIT, `day:${day}`, LIMITS.globalPerDay, 86400)) {
      return json({ error: 'rate_limited', scope: 'global' }, 429, origin);
    }

    try {
      const reply = await callProvider(env, messages, { jd: isJd });
      return json({ reply }, 200, origin);
    } catch (err) {
      // Never leak the provider's error body — it can echo request content.
      console.error('provider call failed', err.status || '', err.detail || err.message);
      const status = err.status === 429 ? 429 : 502;
      return json({ error: status === 429 ? 'rate_limited' : 'upstream_error' }, status, origin);
    }
  },
};
