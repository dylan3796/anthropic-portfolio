---
name: scorecard-refresh
description: Recompute partner tiers and health flags from the thresholds in the data dictionary, report deltas, and update partner_metrics.csv after confirmation. Use after metrics change or on a periodic refresh.
allowed-tools: Read, Grep, Bash(python3:*), Edit, Write
---

# Scorecard Refresh

Owned by big rock: [`plans/big-rocks/partner-scorecard.md`](../../../plans/big-rocks/partner-scorecard.md)

This is the only skill in this repo permitted to write data. The write target
is exactly one file: `data/partner_metrics.csv`. Touch nothing else.

## Steps

1. Read the tiering thresholds and health-flag rules from
   `data/DATA_DICTIONARY.md`. They live there, not here — if this skill and
   the dictionary ever disagree, the dictionary wins and this file needs a fix
   (flag it for `/improve-setup`).
2. Run the recompute with `python3` over `data/partner_metrics.csv`:
   - `partner_value_score` from the component formula (revenue, deal regs,
     certifications, NPS — each capped per the dictionary).
   - `tier` from the Partner Value Score thresholds. Partners within ±3
     points of a threshold get flagged for tier review, not auto-moved —
     note them in the delta report.
   - `health_flag` from NPS and QBR-recency rules, using today's date.
3. Report a **delta table** before changing anything: only partners whose
   `tier` or `health_flag` would change, with old → new values and the rule
   that fired. If nothing changes, say so and stop.
4. **Ask for explicit confirmation** before writing. On confirmation, update
   only the changed cells in `data/partner_metrics.csv`, preserving column
   order and formatting.
5. After a confirmed write, remind the user to check the scorecard plan's
   milestones — a refresh that produces new red flags may warrant a QBR
   coverage milestone update.

## Don'ts

- Never write without showing the delta table and getting a yes.
- Never edit thresholds inline to make a result "look right" — threshold
  changes are proposals against `data/DATA_DICTIONARY.md` via the scorecard plan.
