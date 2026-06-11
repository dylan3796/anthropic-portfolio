---
name: partner-qbr
description: Pull the QBR data cut for a slice of the partner book — the whole org (default), a region or segment, or a single partner when one requests a review. Use when preparing QBR material or when asked for a partner health summary.
allowed-tools: Read, Grep
---

# QBR Data Brief

Owned by big rock: [`plans/big-rocks/partner-scorecard.md`](../../../plans/big-rocks/partner-scorecard.md)

## Inputs

A scope. QBRs run for the whole org — sometimes cut by region or segment,
occasionally for a single partner when they request a review. Default to the
whole book. If a partner name is given it must match `partner_name` in
`data/partner_metrics.csv`; if ambiguous or missing, list the available
partners and ask.

## Steps

1. Read `data/partner_metrics.csv` and `data/DATA_DICTIONARY.md`.
2. Filter to the scope. For org or segment cuts, aggregate the numeric
   metrics and benchmark against whole-book medians. For a single partner,
   benchmark against the median of each numeric metric across partners in
   the **same tier**.
3. Draft the brief in this structure:

   ```markdown
   # QBR Brief: <scope> — <date>

   ## Snapshot
   (partners in scope, tier mix, health-flag mix)

   ## Performance vs. benchmark
   (table: metric | scope | benchmark | delta — currency as $XXX,XXX)

   ## Risks
   (health-flag drivers per the dictionary rules; any metric > 25% below
   the benchmark)

   ## Asks & next steps
   (2-4 concrete items, e.g. certification push where certified_engineers
   lags, pipeline review where sourced_pipeline is thin)
   ```

4. Keep it to one page. Fiscal references use the Feb–Jan calendar.

## Don'ts

- Don't modify the CSV (updating `last_qbr_date` after a review actually
  happens is an open question owned by the scorecard plan, not this skill).
- Don't treat QBRs as a per-partner cadence — there is no "overdue" clock.
  A partner-scoped brief happens because the partner asked, not because a
  date lapsed.
- Don't speculate beyond the data; if a section has no signal, say so.
