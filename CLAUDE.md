# CLAUDE.md

This file is read by Claude Code at the start of every session. It is the
bootstrap layer of this repo's operating model: identity, conventions, and
the rules for how work gets done here.

## What this repo is

Two things at once:

1. **A portfolio site** — a Streamlit app (`app.py`) presenting Dylan Ram's
   GTM / Partner Strategy & Ops background.
2. **A reference Claude Code setup** — a working demonstration of running
   Claude Code as an operating system: persistent memory (this file), a data
   layer, long-horizon plans against big rocks, per-rock skills, and a
   recursive self-improvement loop. The architecture is documented in
   `docs/claude-code-architecture.md`.

## Repo map

```
app.py                       Streamlit portfolio app (single page)
data/sample_data.py          Attribution demo data used by app.py
data/partner_metrics.csv     Synthetic partner scorecard data (skills consume this)
data/DATA_DICTIONARY.md      Metric definitions — the source of truth for all metrics
plans/big-rocks/             One long-lived plan per strategic initiative
.claude/skills/              Skills, each owned by a big rock (plus one meta-skill)
.claude/agents/              Subagents (big-rock-planner)
.claude/hooks/               SessionStart context injection, Stop session logging
retros/                      Session log + dated retros from the improvement loop
docs/                        Architecture documentation
```

## Conventions

- **Fiscal calendar:** Feb 1 – Jan 31. "FY26" = Feb 2025 – Jan 2026. Never
  assume calendar years for revenue figures.
- **Currency:** format as `$XXX,XXX`, USD, no decimals.
- **Metric names:** must match `data/DATA_DICTIONARY.md` exactly. If a metric
  isn't defined there, define it there before using it anywhere else.
- **Attribution logic:** the source of truth is
  `plans/big-rocks/partner-attribution.md`. Don't invent attribution weights
  inline.
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
- Data sanity: `python3 -c "import pandas as pd; print(pd.read_csv('data/partner_metrics.csv'))"`
- Hooks: `bash .claude/hooks/session_context.sh` should print current big-rock
  status and scorecard headlines with exit code 0.
