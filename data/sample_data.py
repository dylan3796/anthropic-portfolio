"""Attribution deal fixture.

The single scenario `/attribution-compare` runs when no deal is passed. Kept
deliberately small — the canonical model weights live in the attribution plan,
not here (see plans/big-rocks/partner-attribution.md), and the partner book of
record is data/partner_metrics.csv.
"""

# Default deal for the /attribution-compare skill: four partners, four
# touchpoint types, one $150K close.
SAMPLE_DEAL = {
    "deal_name": "Enterprise Analytics Platform",
    "deal_value": 150000,
    "touchpoints": [
        {"partner": "Acme Consulting", "type": "Referral", "days_before_close": 90},
        {"partner": "DataTech SI", "type": "Implementation", "days_before_close": 45},
        {"partner": "Cloud Partners", "type": "Influence", "days_before_close": 30},
        {"partner": "Integration Pro", "type": "Technical Demo", "days_before_close": 14},
    ],
}
