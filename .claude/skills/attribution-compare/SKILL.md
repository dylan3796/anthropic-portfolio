---
name: attribution-compare
description: Compare attribution models for a deal scenario. Use when deciding how partner credit should be split on a deal, or when evaluating attribution model trade-offs. Accepts a deal value and touchpoints; defaults to the sample deal in data/sample_data.py.
allowed-tools: Read, Grep, Bash(python3:*)
---

# Attribution Model Comparison

Owned by big rock: [`plans/big-rocks/partner-attribution.md`](../../../plans/big-rocks/partner-attribution.md)
— that plan holds the **canonical model weights**. Read it first; never
restate or invent weights here.

## Inputs

From the user's arguments, extract:
- `deal_value` (USD)
- `touchpoints`: list of `{partner, type, days_before_close}` where type is
  one of: Referral, Implementation, Technical Demo, Influence.

If no arguments are given, use `SAMPLE_DEAL` from `data/sample_data.py`
($150,000 Enterprise Analytics Platform, 4 touchpoints).

## Steps

1. Read the canonical weights table in `plans/big-rocks/partner-attribution.md`.
2. Compute the split for all six models (Equal, Role-Weighted, Time Decay,
   First Touch, Last Touch, U-Shaped). Use `python3` inline for the math —
   especially Time Decay normalization — rather than mental arithmetic.
3. Enforce the split cap: each model's attributions must sum to exactly
   `deal_value`. If rounding breaks this, adjust the largest share.
4. Output:
   - A markdown table: rows = partners, columns = models, cells formatted `$XXX,XXX`.
   - A short recommendation: which model fits this deal's shape and why
     (e.g., implementation-heavy deals favor Role-Weighted; long nurture
     cycles distort Last Touch).
5. Note that Role-Weighted is the current production model, so flag any
   partner whose credit would swing more than 2x between Role-Weighted and
   the recommended model.

## Don'ts

- Don't write any files; this skill is read-only analysis.
- Don't propose new models here — open-question them in the attribution plan.
