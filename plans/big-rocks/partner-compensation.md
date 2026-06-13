---
status: active
owner: Dylan Ram
horizon: FY27 H1
owned-skills: commissions-credit
---

# Big Rock: Partner Compensation & Crediting

## Objective

Make partner-team crediting correct, reproducible, and auditable end to end.
Coverage in the partner world is genuinely messy — reps join mid-quarter, hand
off territories, and cover overlapping slices of segment × region × motion — and
that mess is maintained by managers in plain English, not in rules. The end
state: a manager writes "Maria takes over the SMB book from Sam on March 15,"
the system codifies it into effective-dated crediting rules, and when finance
runs actuals the right person shows up on the right line for the right months.

The design boundary is deliberate and is the point of this rock: **the AI does
the ambiguous codification (plain English → structured rules); deterministic,
unit-tested code does the money math (rules → credited lines).** Comp is not a
place for a model to do arithmetic.

## Architecture

```
data/coverage_assignments.csv   plain-English coverage sheet (the "Google Sheet")
        │  /commissions-credit  (AI: parse intent, resolve handoffs/overlaps, date)
        ▼
data/crediting_rules.json       structured, effective-dated crediting rules
        │  crediting/engine.py  (deterministic, tested — no LLM in the money path)
        ▼
credited lines                  rep · role · deal · month · amount  (+ uncredited gaps)
        ▲
data/commission_deals.csv       closed deals to run actuals against
```

## Milestones

- [x] Define the coverage sheet, rules, and deals schemas in the data dictionary (2026-06-13)
- [x] Ship `crediting/engine.py` — deterministic rule application with golden tests in `tests/` (2026-06-13)
- [x] Ship `/commissions-credit` — codify the plain-English sheet into `crediting_rules.json`, then verify against the deal book (2026-06-13)
- [ ] Surface uncredited deals as a first-class report (a gap at actuals time is a crediting hole, never a silent zero)
- [ ] Add ramp/proration: a mid-quarter hire's quota and credit prorate from start date
- [ ] Dispute ledger: where do manual crediting overrides live, and how do they survive the next codification run?

## Owned Skills

- [`/commissions-credit`](../../.claude/skills/commissions-credit/SKILL.md) —
  reads `data/coverage_assignments.csv`, codifies it into effective-dated rules
  in `data/crediting_rules.json`, and verifies the result against
  `data/commission_deals.csv` via the deterministic engine before writing.

## Open Questions

- When two reps legitimately co-cover a territory, is the default an even split,
  or weighted by role (PSM vs. PAM credit on different comp lines)?
- Handoff boundary: does the *outgoing* rep keep deals that closed before the
  handoff date, or deals they sourced regardless of close date? (Current rule:
  close date governs.)
- Should `/commissions-credit` ever write `crediting_rules.json` without a human
  reviewing the diff? (Current answer: no — same guardrail as any writing skill.)

## Improvement Log

- **2026-06-13** — Created as the headline system for the setup. Replaced the
  scorecard-refresh skill as the flagship: crediting is a real multi-stakeholder
  workflow (managers author coverage, the agent codifies, finance runs actuals,
  reps are credited) and demonstrates the AI/deterministic boundary that the
  scorecard analysis did not.
