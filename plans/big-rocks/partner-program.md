---
status: active
owner: Dylan Ram
horizon: FY27 H2
owned-skills: none yet
---

# Big Rock: Partner Program

## Objective

Own the program mechanics that decide where every partner stands and what
that standing is worth: the Partner Value Score, tier thresholds, and the
benefits-eligibility table in `data/DATA_DICTIONARY.md`. The program is the
contract between the company and its partners — tier moves and benefits
decisions must be explainable from the score, never negotiated ad hoc.

This rock also owns **priority motions**: the business shifts emphasis
(migrations one half, solution development the next), and `active_motion`
enrollment plus any score weighting for the current motion are decided here.

## Milestones

- [x] Define the Partner Value Score formula and component caps in the data dictionary (2026-06-10)
- [x] Add deal registration and sourced/influenced revenue split to the gold layer (2026-06-10)
- [x] Publish the benefits-eligibility table per tier (2026-06-10)
- [ ] Ship `/tier-review` — half-close memo for any partner within ±3 points of a threshold: score components, trajectory, benefits delta if moved
- [ ] Ship `/benefits-audit` — sweep for partners consuming benefits above their tier or leaving entitled benefits unused
- [ ] Decide whether approved deal regs in the current priority motion earn a score multiplier (open question below)
- [ ] FY27 H2 motion review: confirm or rotate the `active_motion` enrollments

## Owned Skills

None shipped yet. `/tier-review` and `/benefits-audit` are proposed above;
per the operating model they ship only after this plan's milestones say so.

## Open Questions

- Should deal regs inside the active priority motion (e.g. migrations) count
  extra toward the Partner Value Score, or does that distort the score's
  comparability across halves?
- Tier-drop grace period: move partners down at half-close immediately, or
  hold one half with a remediation plan?
- Vector Integrations and Analytics Corp both sit exactly at PVS 40 — the
  Premier floor. The first `/tier-review` should use them as test cases.

## Improvement Log

- **2026-06-10** — Created when the walkthrough restructure surfaced that
  tiering, benefits, and deal-reg mechanics had no owning rock: the scorecard
  rock computed tiers but nothing owned what a tier *means*. Program
  definitions moved into the data dictionary with this rock as owner.
