# Ask Dylan — the chat backend

The portfolio is a static page on GitHub Pages, so it can't hold an API key: anything
shipped to a browser gets scraped and billed to whoever owns it. This Worker holds the
key and is the only thing that talks to a model provider.

The site works without it. When this Worker is unset, unreachable, or rate-limited, the
page falls back to local grounded retrieval — the visitor still gets cited answers, just
not a conversation.

## Deploy

```bash
cd worker && ./setup.sh
```

It logs you in, creates the rate-limit storage and wires the id into
`wrangler.toml`, takes your API key, deploys, and offers to point the site at the
new URL and rebuild. Two prompts need you: the browser login and the key. Safe to
re-run — it skips whatever is already done.

Then commit and push; the site goes live with chat and the fit check on.

<details><summary>Doing it by hand instead</summary>

```bash
npx wrangler login
npx wrangler kv namespace create RATE_LIMIT   # paste the id into wrangler.toml
npx wrangler secret put PROVIDER_API_KEY
npx wrangler deploy
```

Then `python3 configure.py chat https://ask-dylan.<subdomain>.workers.dev`.
</details>

## Choosing a model

`PROVIDER` in `wrangler.toml` selects a preset. Every provider except Anthropic speaks
the OpenAI-compatible `/chat/completions` shape, so switching is config, not code.

| `PROVIDER`  | Model                | Notes |
|-------------|----------------------|-------|
| `deepseek`  | `deepseek-chat`      | Default. Cheapest of these by a wide margin. |
| `moonshot`  | `moonshot-v1-8k`     | Kimi. |
| `qwen`      | `qwen-plus`          | Alibaba DashScope, OpenAI-compatible endpoint. |
| `zhipu`     | `glm-4-flash`        | GLM. |
| `openai`    | `gpt-4o-mini`        | |
| `anthropic` | `claude-haiku-4-5`   | Different request shape; the Worker handles it. |

Override either field for a model a preset doesn't name:

```toml
[vars]
PROVIDER_BASE_URL = "https://api.deepseek.com/v1"
PROVIDER_MODEL    = "deepseek-reasoner"
```

Then `wrangler deploy` again. Swapping providers means a new `PROVIDER_API_KEY`.

## What stops a stranger draining the budget

| Guard | Limit | Where |
|---|---|---|
| Origin allowlist | the portfolio's domains only | `ALLOWED_ORIGINS` |
| Per-IP rate limit | 30 messages/hour | KV, 1h window |
| Global daily cap | 600 messages/day | KV, 24h window |
| Input size | 1200 chars/message, 8000 total, 16 turns | `sanitize()` |
| Output size | 700 tokens | `max_tokens` |
| JD fit check | 6000-char cap, 5/IP/hour, 1100 output tokens | `{mode:'jd'}` branch |

The origin check is a speed bump, not a wall — a header is trivially forged. The rate
limits are the real defense, so **don't deploy without the KV namespace bound.**

Also set a hard spend cap in the provider's own billing console. It's the only limit
that can't be defeated by a bug in this file.

## Cost

Roughly $0.15–$0.60/month at a few hundred messages, depending on provider. The daily
cap is the ceiling: 600 messages/day is the most the Worker will ever buy.

## Changing what it knows

Don't edit `corpus.js` — it's generated. The facts live in `site_qa.py` (`FACTS` for
what it answers, `DECLINE` for what it refuses, `SYSTEM_PROMPT` for how it behaves).
Edit there, run `python3 build_site.py`, and redeploy. One corpus feeds both the chat
and the offline fallback, so they can never drift apart.
