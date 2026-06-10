# Data Dictionary

Single source of truth for metric definitions in this repo. Any skill, plan, or
dashboard that references a metric must use the exact names and definitions below.
If a definition changes, update it here first, then propagate (the `/improve-setup`
skill checks for drift).

> All figures in this repo are **synthetic sample data** built for portfolio
> demonstration. They mirror the shape of real partner-ops datasets without
> containing any confidential information.

## Conventions

- **Fiscal calendar:** Feb 1 – Jan 31 (Databricks-style). "FY26" = Feb 2025 – Jan 2026.
- **Currency:** USD, formatted `$XXX,XXX` (no decimals) in all outputs.
- **Attribution source of truth:** the rules documented in
  [`plans/big-rocks/partner-attribution.md`](../plans/big-rocks/partner-attribution.md).
  Never invent new attribution weights inline — propose changes against that plan.
- **Tier order:** Strategic > Premier > Select.

## `partner_metrics.csv`

| Column | Type | Definition | Owner | Computed by |
|---|---|---|---|---|
| `partner_name` | string | Canonical partner name. Must match names used in `sample_data.py` where overlapping. | Partner Ops | manual |
| `segment` | enum | Primary customer segment the partner serves: `Enterprise`, `Mid-Market`, `SMB`. | Partner Ops | manual |
| `tier` | enum | Program tier per the Partner Value Score composite: `Strategic`, `Premier`, `Select`. | Partner Strategy | `/scorecard-refresh` |
| `attributed_revenue_fy26` | int (USD) | Revenue attributed to the partner in FY26 under the production attribution model (currently Role-Weighted). | Partner Ops | attribution engine |
| `sourced_pipeline` | int (USD) | Open pipeline where the partner is the originating source (first touch = referral or sourced lead). | Partner Ops | attribution engine |
| `certified_engineers` | int | Count of partner engineers holding a current certification. | Partner Enablement | manual |
| `nps` | int | Most recent partner-satisfaction NPS (-100 to 100). | Partner Programs | survey pipeline |
| `last_qbr_date` | date (ISO) | Date of the most recent quarterly business review. | Partner Managers | `/partner-qbr` |
| `health_flag` | enum | `green` / `yellow` / `red` composite health signal. See thresholds below. | Partner Strategy | `/scorecard-refresh` |

## Tiering thresholds (used by `/scorecard-refresh`)

| Tier | Rule |
|---|---|
| Strategic | `attributed_revenue_fy26 >= $1,800,000` AND `certified_engineers >= 30` |
| Premier | `attributed_revenue_fy26 >= $600,000` OR (`sourced_pipeline >= $1,200,000` AND `certified_engineers >= 15`) |
| Select | everything else |

## Health flag rules (used by `/scorecard-refresh`)

| Flag | Rule |
|---|---|
| `red` | `nps < 50` AND `last_qbr_date` older than 120 days |
| `yellow` | `nps < 55` OR `last_qbr_date` older than 120 days |
| `green` | otherwise |
