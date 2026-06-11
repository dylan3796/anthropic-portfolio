---
status: active
owner: Dylan Ram
horizon: FY27 H1
owned-skills: scorecard-refresh, partner-qbr
---

# Big Rock: Partner Scorecard

## Objective

One trusted view of partner health that executives, partner managers, and
partners themselves can all read the same way. The scorecard turns the raw
metrics in `data/partner_metrics.csv` into tiers and health flags using the
thresholds in `data/DATA_DICTIONARY.md`, and feeds the QBR motion so reviews
start from data instead of anecdotes.

## Milestones

- [x] Define scorecard columns and thresholds in the data dictionary (2026-04-29)
- [x] Seed `partner_metrics.csv` with the full partner book (2026-05-06)
- [x] Ship `/scorecard-refresh` to recompute tiers and health flags from thresholds (2026-05-21)
- [x] Ship `/partner-qbr` to draft QBR briefs from scorecard data (2026-05-27)
- [ ] Add quarter-over-quarter deltas (requires snapshotting the CSV per quarter)
- [ ] Health push: Summit Advisory and Lakeshore Consulting are flagged red — review with their PSMs and offer a partner-scoped QBR brief if either requests one

## Owned Skills

- [`/scorecard-refresh`](../../.claude/skills/scorecard-refresh/SKILL.md) —
  recomputes `tier` and `health_flag` from dictionary thresholds, reports
  deltas, writes only with confirmation.
- [`/partner-qbr`](../../.claude/skills/partner-qbr/SKILL.md) — pulls the QBR
  data cut for a scope: the whole org (default), a region/segment, or a single
  partner on request, benchmarked against book or tier medians.

## Open Questions

- Should `health_flag` incorporate pipeline coverage (sourced_pipeline /
  attributed_revenue ratio) or stay NPS + QBR recency only?
- Who owns updating `last_qbr_date` — the partner manager, or should
  `/partner-qbr` update it when a brief is generated?

## Improvement Log

- **2026-06-10** — Tiering moved from ad-hoc revenue/certification thresholds
  to the Partner Value Score. The formula, thresholds, and benefits table are
  owned by the partner-program rock via the data dictionary; this rock's
  `/scorecard-refresh` computes, it doesn't decide.
- **2026-06-05** — Retro found three sessions where the fiscal calendar had to
  be re-explained while discussing scorecard figures; the FY convention was
  promoted into `CLAUDE.md` so every session starts with it
  (see `retros/2026-06-05-retro.md`).
