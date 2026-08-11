# CLAUDE.md

This file is read by Claude Code at the start of every session. It is the
bootstrap layer of this repo's operating model: identity, conventions, and
the rules for how work gets done here.

## What this repo is

Two things at once:

1. **A walkthrough site** — a Streamlit app (`app.py`) presenting how to run
   agentic AI as an operating system at an org: tenets, architecture,
   self-serve analytics, AI-embedded GTM, and team adoption.
2. **A reference Claude Code setup** — a working demonstration of running
   Claude Code as an operating system: persistent memory (this file), a data
   layer, long-horizon plans against big rocks, per-rock skills, and a
   recursive self-improvement loop. The architecture is documented in
   `docs/claude-code-architecture.md`.

## Repo map

```
app.py                       Streamlit portfolio app (single page)
data/partner_metrics.csv     Synthetic partner scorecard data (the gold table)
data/coverage_assignments.csv  Plain-English coverage sheet (the "Google Sheet")
data/crediting_rules.json    Codified crediting rules — output of /commissions-credit
data/commission_deals.csv    Closed deals the crediting engine runs actuals against
data/DATA_DICTIONARY.md      Metric & schema definitions — source of truth for all metrics
crediting/engine.py          Deterministic crediting engine (the money path; no LLM)
tests/                       Golden tests / evals — pin the crediting math
notebooks/                   Analysis artifacts (e.g. scorecard tier/health refresh)
build_site.py                Builds the public one-link portfolio into docs/
site_qa.py                   The "Run the screen" corpus, persona, and answer engine
worker/                      Cloudflare Worker fronting the chat model (holds the API key)
plans/big-rocks/             One long-lived plan per strategic initiative
.claude/skills/              Skills, each owned by a big rock (plus one meta-skill)
.claude/agents/              Subagents (big-rock-planner)
.claude/hooks/               SessionStart context injection, Stop session logging
retros/                      Session log + dated retros from the improvement loop
docs/                        Architecture documentation
```

## Domain glossary

The roles, segments, and motions every session should assume. Metric
*definitions* live in `data/DATA_DICTIONARY.md`; this is the vocabulary, kept in
memory so Claude never has to ask who a PSM is.

- **PSM — Partner Sales Manager.** Quota-carrying co-sell seller. Owns
  partner-sourced pipeline and attributed revenue for the partners/territory
  they cover; credited on the revenue line.
- **PAM — Partner Account Manager.** Owns the partner *relationship* —
  enablement, certifications, QBRs, health. Credited on the coverage line, not
  on sourced revenue.
- **Territory** = segment × region × motion. Coverage is **effective-dated**:
  reps join, leave, and hand off mid-period (owned by the partner-compensation
  rock).
- **Segments:** Enterprise > Mid-Market > SMB (the customer segment a partner serves).
- **Regions:** East, Central, West.
- **Motions:** Migrations, Solution Development, Core Co-Sell — the priority GTM
  motion a partner is enrolled in (owned by the partner-program rock).
- **Tiers:** Strategic > Premier > Select (derived from the Partner Value Score).

## Conventions

- **Fiscal calendar:** Feb 1 – Jan 31. "FY26" = Feb 2025 – Jan 2026. Never
  assume calendar years for revenue figures.
- **Currency:** format as `$XXX,XXX`, USD, no decimals.
- **Metric names:** must match `data/DATA_DICTIONARY.md` exactly. If a metric
  isn't defined there, define it there before using it anywhere else.
- **Attribution logic:** the source of truth is
  `plans/big-rocks/partner-attribution.md`. Don't invent attribution weights
  inline.
- **Crediting math stays in code.** `/commissions-credit` (an LLM) only authors
  rules in `data/crediting_rules.json`. Applying rules to deals — the money — is
  `crediting/engine.py`, and it is unit-tested. Never compute credited amounts
  in a prompt.
- **App style:** match existing patterns in `app.py` — `narrative-quote` and
  `experience-card` CSS classes, Anthropic-inspired palette (`#D97757` accent,
  `#FAFAF9` background), no emoji in section headings, no new dependencies
  without a strong reason.

## Operating model

1. **Big rocks first.** Before working on any strategic initiative, read its
   plan in `plans/big-rocks/`. If the work doesn't map to an existing rock,
   ask whether it should become one (use the `big-rock-planner` agent to
   draft the plan doc).
2. **Skills belong to rocks.** Every domain skill in `.claude/skills/` is
   listed in the `owned-skills` header of exactly one big-rock plan. New
   skills get proposed in a rock's plan before they get built.
3. **Plans are living documents.** When a milestone lands, check it off in
   the plan and note the date. Stale plans are a friction signal the
   improvement loop will flag.
4. **Close the loop.** After a session that produced meaningful work or
   meaningful friction, run `/improve-setup`. It reviews the session log and
   proposes edits to this file, the skills, and the plans — that's how this
   setup compounds.

## Verification

- App: `streamlit run app.py` (port 8501)
- Crediting math: `python3 tests/test_crediting.py` (golden tests, no deps) —
  must stay green after any change to `crediting/` or `crediting_rules.json`.
- Site + chat: `python3 tests/test_site_qa.py` (needs node) — retrieval answers,
  chat client fallback, and the Worker's origin/rate/size guards. Must stay green
  after any change to `site_qa.py` or `worker/`.
- Site build: `python3 build_site.py` regenerates `docs/` and `worker/corpus.js`.
  The corpus is generated — edit `site_qa.py`, never `worker/corpus.js`.
- Data sanity: `python3 -c "import pandas as pd; print(pd.read_csv('data/partner_metrics.csv'))"`
- Hooks: `bash .claude/hooks/session_context.sh` should print current big-rock
  status and scorecard headlines with exit code 0.
