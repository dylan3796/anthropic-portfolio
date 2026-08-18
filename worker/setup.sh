#!/usr/bin/env bash
# One-command setup for the chat backend.
#
# Everything that can be automated is. You supply two things a script can't:
# a browser login, and the provider API key.
#
#     cd worker && ./setup.sh
#
# Safe to re-run: it skips steps that are already done, so if a step fails you
# fix that one thing and run it again.

set -euo pipefail

cd "$(dirname "$0")"
TOML="wrangler.toml"
SITE_QA="../site_qa.py"
PLACEHOLDER="PASTE_YOUR_KV_NAMESPACE_ID_HERE"

bold() { printf "\n\033[1m%s\033[0m\n" "$1"; }
ok()   { printf "  \033[32m✓\033[0m %s\n" "$1"; }
info() { printf "  %s\n" "$1"; }
die()  { printf "\n\033[31m✗ %s\033[0m\n" "$1" >&2; exit 1; }

command -v node >/dev/null || die "Node.js is required. Install it from nodejs.org, then re-run."

WRANGLER="npx --yes wrangler@latest"

# ---------------------------------------------------------------- 1. login
bold "1/5  Cloudflare login"
if $WRANGLER whoami >/dev/null 2>&1; then
  ok "already logged in"
else
  info "A browser window will open — approve access, then come back here."
  $WRANGLER login || die "login failed"
  ok "logged in"
fi

# ------------------------------------------------------------ 2. KV namespace
bold "2/5  Rate-limit storage"
if grep -q "$PLACEHOLDER" "$TOML"; then
  info "creating KV namespace…"
  OUT=$($WRANGLER kv namespace create RATE_LIMIT 2>&1) || { echo "$OUT"; die "could not create the KV namespace"; }
  # wrangler prints the id in the block it tells you to paste; grab the first
  # 32-hex-char id it emits.
  KV_ID=$(printf '%s' "$OUT" | grep -oE '[0-9a-f]{32}' | head -1)
  [ -n "$KV_ID" ] || { echo "$OUT"; die "created it, but could not read the id from wrangler's output — paste it into $TOML manually"; }
  # portable in-place edit (BSD and GNU sed disagree about -i)
  sed "s/$PLACEHOLDER/$KV_ID/" "$TOML" > "$TOML.tmp" && mv "$TOML.tmp" "$TOML"
  ok "created and wired into $TOML ($KV_ID)"
else
  ok "already configured"
fi

# --------------------------------------------------------------- 3. provider
bold "3/5  Model provider"
CURRENT=$(grep -E '^PROVIDER *=' "$TOML" | head -1 | cut -d'"' -f2)
info "currently: $CURRENT   (options: deepseek moonshot qwen zhipu openai anthropic)"
printf "  press Enter to keep it, or type another: "
read -r PICK || PICK=""
if [ -n "$PICK" ] && [ "$PICK" != "$CURRENT" ]; then
  sed "s/^PROVIDER *= *\".*\"/PROVIDER = \"$PICK\"/" "$TOML" > "$TOML.tmp" && mv "$TOML.tmp" "$TOML"
  CURRENT="$PICK"
  ok "set to $CURRENT"
fi
info "get a key from that provider's console if you don't have one yet"

# ------------------------------------------------------------------ 4. secret
bold "4/5  API key"
if $WRANGLER secret list 2>/dev/null | grep -q PROVIDER_API_KEY; then
  ok "already stored"
  printf "  replace it? [y/N] "
  read -r REPLACE || REPLACE=""
  case "$REPLACE" in [yY]*) $WRANGLER secret put PROVIDER_API_KEY ;; esac
else
  info "paste your $CURRENT key at the prompt (it is not echoed, and never touches a file)"
  $WRANGLER secret put PROVIDER_API_KEY || die "could not store the key"
  ok "stored"
fi

# ------------------------------------------------------------------ 5. deploy
bold "5/5  Deploy"
DEPLOY_OUT=$($WRANGLER deploy 2>&1) || { echo "$DEPLOY_OUT"; die "deploy failed"; }
echo "$DEPLOY_OUT" | grep -iE "https://[^ ]*workers\.dev" || true
URL=$(printf '%s' "$DEPLOY_OUT" | grep -oE 'https://[a-z0-9.-]*workers\.dev' | head -1)
[ -n "$URL" ] || die "deployed, but could not read the URL — copy it from the output above"
ok "live at $URL"

# ------------------------------------------------------- wire up the website
bold "Turn it on for the site"
if grep -q "^CHAT_ENDPOINT = \"\"" "$SITE_QA"; then
  printf "  point the site at this Worker now? [Y/n] "
  read -r WIRE || WIRE=""
  case "$WIRE" in
    [nN]*) info "skipped — set CHAT_ENDPOINT in site_qa.py when ready" ;;
    *)
      sed "s|^CHAT_ENDPOINT = \"\"|CHAT_ENDPOINT = \"$URL\"|" "$SITE_QA" > "$SITE_QA.tmp" \
        && mv "$SITE_QA.tmp" "$SITE_QA"
      (cd .. && python3 build_site.py >/dev/null)
      ok "site rebuilt with chat + fit check enabled"
      printf "\n  Commit and push to go live:\n"
      printf "    git add -A && git commit -m 'Turn on the live chat' && git push\n"
      ;;
  esac
else
  ok "site already points at a Worker"
fi

bold "Done"
info "One last thing, and it matters: set a hard spend cap in your $CURRENT"
info "billing console. It's the only limit a bug in my code can't defeat."
