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
- **Program source of truth:** tier thresholds, the Partner Value Score formula,
  and benefits eligibility live in this file and are owned by
  [`plans/big-rocks/partner-program.md`](../plans/big-rocks/partner-program.md).
- **Tier order:** Strategic > Premier > Select.

## `partner_metrics.csv`

| Column | Type | Definition | Owner | Computed by |
|---|---|---|---|---|
| `partner_name` | string | Canonical partner name. Must match names used in `sample_data.py` where overlapping. | Partner Ops | manual |
| `segment` | enum | Primary customer segment the partner serves: `Enterprise`, `Mid-Market`, `SMB`. | Partner Ops | manual |
| `active_motion` | enum | The priority GTM motion the partner is currently enrolled in: `Migrations`, `Solution Development`, `Core Co-Sell`. Set each half per business priorities. | Partner Strategy | manual |
| `tier` | enum | Program tier derived from `partner_value_score` per the thresholds below: `Strategic`, `Premier`, `Select`. | Partner Program | `/scorecard-refresh` |
| `partner_value_score` | int (0–100) | Composite Partner Value Score. See formula below. | Partner Program | `/scorecard-refresh` |
| `sourced_revenue_fy26` | int (USD) | FY26 closed-won revenue on opportunities the partner originated (approved deal registration or sourced lead = first touch). Credited at 100%. | Partner Sales | attribution engine |
| `influenced_revenue_fy26` | int (USD) | FY26 closed-won revenue on opportunities the partner touched but did not source. Total deal value of influenced opps — partial credit flows into attributed revenue per the production model. | Partner Sales | attribution engine |
| `attributed_revenue_fy26` | int (USD) | Sourced revenue at 100% plus the partner's Role-Weighted share of influenced revenue, under the production attribution model. The headline revenue number for tiers and comp. | Partner Ops | attribution engine |
| `sourced_pipeline` | int (USD) | Open pipeline where the partner is the originating source (first touch = approved deal reg or sourced lead). | Partner Sales | attribution engine |
| `deal_regs_submitted_fy26` | int | Deal registrations filed by the partner in the PRM during FY26. | Partner Sales | PRM export |
| `deal_regs_approved_fy26` | int | Submitted registrations that passed conflict review (net-new opportunity, partner-originated, no competing reg). Approval grants a 90-day protection window and the tier's deal-reg margin. | Partner Sales | PRM export |
| `certified_engineers` | int | Count of partner engineers holding a current certification. | Partner Enablement | manual |
| `nps` | int | Most recent partner-satisfaction NPS (-100 to 100). | Partner Program | survey pipeline |
| `last_qbr_date` | date (ISO) | Date of the most recent quarterly business review. | Partner Managers | `/partner-qbr` |
| `health_flag` | enum | `green` / `yellow` / `red` composite health signal. See thresholds below. | Partner Management | `/scorecard-refresh` |

## Partner Value Score (used by `/scorecard-refresh`)

A 0–100 composite of what the program actually values: revenue performance,
sourcing discipline, technical investment, and relationship health. Components
are capped so no single dimension can buy a tier.

| Component | Weight | Formula |
|---|---|---|
| Revenue | 40 pts | `min(attributed_revenue_fy26 / $2,500,000, 1) × 40` |
| Deal registration | 20 pts | `min(deal_regs_approved_fy26 / 40, 1) × 20` |
| Technical capacity | 20 pts | `min(certified_engineers / 40, 1) × 20` |
| Satisfaction | 20 pts | `max(nps, 0) / 100 × 20` |

`partner_value_score` = sum of components, rounded to the nearest integer.

## Tiering thresholds (used by `/scorecard-refresh`)

| Tier | Rule |
|---|---|
| Strategic | `partner_value_score >= 70` |
| Premier | `partner_value_score >= 40` |
| Select | everything else |

Tier moves are evaluated at half-close. Partners within ±3 points of a
threshold get flagged for a tier review rather than moved automatically.

## Benefits eligibility by tier

What a tier is worth — the program's contract with the partner. Benefits
questions ("what is this partner eligible for?") resolve against this table.

| Benefit | Strategic | Premier | Select |
|---|---|---|---|
| Deal-reg margin on approved regs | 20% | 15% | 10% |
| Market development funds (annual) | $150,000 | $50,000 | — |
| Partner manager coverage | named PSM | pooled PSM | portal-led |
| Co-sell desk SLA | 24 hours | 72 hours | best effort |
| Certification vouchers (annual) | 40 | 15 | 5 |
| Product roadmap briefings | quarterly | semi-annual | — |

## Health flag rules (used by `/scorecard-refresh`)

| Flag | Rule |
|---|---|
| `red` | `nps < 50` AND `last_qbr_date` older than 120 days |
| `yellow` | `nps < 55` OR `last_qbr_date` older than 120 days |
| `green` | otherwise |
