# dylanram.com — cutover runbook

The build is already parameterized; going live is four short steps done in
this order (the order matters: the Worker learns the new origin *before* any
page is served from it, so chat never 403s mid-cutover).

Bought a different name than `dylanram.com`? Same steps — but first replace
the name in `worker/worker.js` `ALLOWED_ORIGINS` and in step 3 below.

## 1. Buy the domain

Any registrar works. Cloudflare Registrar is the natural fit (at-cost pricing,
and DNS then lives in the same dashboard as the chat Worker).

## 2. Redeploy the Worker

`ALLOWED_ORIGINS` already includes `https://dylanram.com` and
`https://www.dylanram.com`, so this is only needed if the Worker was deployed
before those lines landed:

```bash
cd worker && wrangler deploy
```

## 3. Point DNS at GitHub Pages

At the registrar's DNS panel:

| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | dylan3796.github.io |

(If the registrar proxies traffic — Cloudflare's orange cloud — turn the proxy
**off** for these records until the GitHub certificate is issued, then turn it
back on if wanted.)

## 4. Flip the build and ship it

In `build_site.py`, set:

```python
DOMAIN = "dylanram.com"
```

then:

```bash
python3 build_site.py     # writes docs/CNAME + canonical/og:url tags
git add -A docs build_site.py && git commit -m "Go live on dylanram.com" && git push
```

Committing `docs/CNAME` to the publishing branch is what configures Pages —
no dashboard clicking needed. Then in repo **Settings → Pages**, wait for the
certificate check to pass and tick **Enforce HTTPS**.

## Verify

- `https://dylanram.com` and `https://www.dylanram.com` both load the site.
- `https://dylan3796.github.io/anthropic-portfolio/` 301-redirects to the domain.
- All four resume downloads work from the new origin.
- The chat answers from the new origin (Worker CORS — the pinned test:
  `node tests/worker_harness.mjs`).
- Old links keep working: the github.io redirect means nothing sent out
  before cutover breaks.
