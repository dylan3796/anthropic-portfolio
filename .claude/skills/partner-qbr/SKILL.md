---
name: partner-qbr
description: Draft a quarterly business review brief for a named partner using scorecard data. Use when preparing for a partner QBR or when asked for a partner health summary.
allowed-tools: Read, Grep
---

# Partner QBR Brief

Owned by big rock: [`plans/big-rocks/partner-scorecard.md`](../../../plans/big-rocks/partner-scorecard.md)

## Inputs

A partner name (must match `partner_name` in `data/partner_metrics.csv`).
If the name is ambiguous or missing, list the available partners and ask.

## Steps

1. Read `data/partner_metrics.csv` and `data/DATA_DICTIONARY.md`.
2. Pull the partner's row, then compute tier benchmarks: the median of each
   numeric metric across partners in the **same tier**.
3. Draft the brief in this structure:

   ```markdown
   # QBR Brief: <Partner> — <date>

   ## Snapshot
   (tier, segment, health flag, days since last QBR)

   ## Performance vs. <tier> benchmarks
   (table: metric | partner | tier median | delta — currency as $XXX,XXX)

   ## Risks
   (health-flag drivers per the dictionary rules: NPS trend, QBR recency,
   any metric > 25% below tier median)

   ## Asks & next steps
   (2-4 concrete items, e.g. certification push if certified_engineers lags,
   QBR scheduling if overdue, pipeline review if sourced_pipeline is thin)
   ```

4. Keep it to one page. Fiscal references use the Feb–Jan calendar.

## Don'ts

- Don't modify the CSV (updating `last_qbr_date` after a QBR actually happens
  is an open question owned by the scorecard plan, not this skill).
- Don't speculate beyond the data; if a section has no signal, say so.
