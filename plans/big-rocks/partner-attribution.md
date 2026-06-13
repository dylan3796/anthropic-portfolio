---
status: active
owner: Dylan Ram
horizon: FY27 H1
owned-skills: none yet
---

# Big Rock: Partner Attribution

## Objective

Establish a defensible, explainable answer to "which partner deserves credit
for this revenue?" — the foundation every downstream partner metric (tiers,
quotas, scorecards) is built on. The production model must be configurable,
auditable, and comparable against alternatives before anyone trusts it for
comp or tiering decisions.

This rock is the **source of truth for attribution logic** in this repo. The
weights below are the canonical definitions; skills and the data dictionary
reference them rather than restating them.

## Attribution models (canonical weights)

| Model | Rule |
|---|---|
| Equal Split | credit divided evenly across all touchpoints |
| Role-Weighted | Referral 15%, Implementation 40%, Technical Demo 30%, Influence 15% (production model for `attributed_revenue_fy26`) |
| Time Decay | weight ∝ `0.5 ^ (days_before_close / 30)`, normalized across touchpoints |
| First Touch | 100% to the earliest touchpoint |
| Last Touch | 100% to the latest touchpoint |
| U-Shaped | 40% first, 40% last, 20% split across middle touchpoints |

## Milestones

- [x] Inventory candidate models and document canonical weights (2026-04-22)
- [x] Ship `/attribution-compare` so any deal scenario can be run through all six models side by side (2026-05-19)
- [x] Adopt Role-Weighted as the production model for FY26 attributed revenue (2026-05-19)
- [ ] Tune the Time Decay half-life (30 days is a placeholder; test 21/30/45 against sample deals)
- [ ] Add split-cap enforcement note: attributed credit across partners must never exceed 100% of deal value
- [ ] Decide whether sourced pipeline should use First Touch or Role-Weighted (open question below)

## Owned Skills

None. `/attribution-compare` was retired (2026-06-13) — model selection is
settled on Role-Weighted for production, so a standing side-by-side comparison
skill stopped earning its keep. The **canonical weights above** remain the
source of truth that the data dictionary and crediting reference.

## Open Questions

- Should `sourced_pipeline` attribution stay First Touch (simple, gameable) or
  move to Role-Weighted (consistent with revenue, harder to explain to partners)?
- Do we need a manual-override ledger for disputed attributions, and where
  would it live?

## Improvement Log

- **2026-06-13** — Retired `/attribution-compare` and its fixture
  (`data/sample_data.py`). The comparison did its job — Role-Weighted is the
  adopted production model — and a standing side-by-side skill was friction
  without a recurring use. Attribution *logic* still lives here; only the
  comparison skill was removed.
- **2026-05-19** — `/attribution-compare` initially hardcoded the sample deal;
  retro feedback ("had to re-explain how to pass a custom deal twice") led to
  the skill accepting deal value + touchpoints as arguments with the sample
  deal as default.
- **2026-06-05** — Retro moved the canonical weight table from the skill into
  this plan so there is exactly one place attribution logic is defined
  (see `retros/2026-06-05-retro.md`).
