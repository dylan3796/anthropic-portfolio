# Ask Dylan — the chat backend

The portfolio is a static page on GitHub Pages, so it can't hold an API key: anything
shipped to a browser gets scraped and billed to whoever owns it. This Worker holds the
key and is the only thing that talks to a model provider.

The site works without it. When this Worker is unset, unreachable, or rate-limited, the
page falls back to local grounded retrieval — the visitor still gets cited answers, just
not a conversation.

## Deploy

```bash
cd worker
npm install -g wrangler         # once
wrangler login                  # opens a browser

# 1. rate-limit storage — paste the printed id into wrangler.toml
wrangler kv namespace create RATE_LIMIT

# 2. the provider key (never goes in a file)
wrangler secret put PROVIDER_API_KEY

# 3. ship it
wrangler deploy
```

Wrangler prints a URL like `https://ask-dylan.<subdomain>.workers.dev`. Put it in
`build_site.py` as `CHAT_ENDPOINT`, rerun `python3 build_site.py`, and commit — the
site starts using it on the next deploy.

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
