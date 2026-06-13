"""Golden tests for the deterministic commission-crediting engine.

These are the evals on the money path: the AI may author the rules, but the
arithmetic that decides who gets paid is pinned by tests. Run either way:

    python3 tests/test_crediting.py      # no dependencies
    python3 -m pytest tests/             # if pytest is installed
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crediting.engine import apply_rules, load_deals, load_rules  # noqa: E402

WEST_SMB = {"segment": ["SMB"], "region": ["West"], "motion": ["Core Co-Sell"]}


def _deal(deal_id, close_date, amount=100000, **over):
    deal = {
        "deal_id": deal_id,
        "partner_name": "Harbor Technologies",
        "segment": "SMB",
        "region": "West",
        "motion": "Core Co-Sell",
        "close_date": close_date,
        "amount": str(amount),
    }
    deal.update({k: str(v) for k, v in over.items()})
    return deal


def test_midquarter_hire_is_not_credited_before_their_start_date():
    rules = [{"rep": "Maria Lopez", "role": "PSM", "effective_start": "2026-03-15",
              "effective_end": None, "match": WEST_SMB, "credit_share": 1.0}]
    lines, uncredited = apply_rules(rules, [_deal("D1", "2026-03-01"),
                                            _deal("D2", "2026-03-20")])
    assert {l.deal_id for l in lines} == {"D2"}
    assert [d["deal_id"] for d in uncredited] == ["D1"]


def test_territory_handoff_switches_rep_at_the_boundary():
    rules = [
        {"rep": "Sam Park", "role": "PSM", "effective_start": "2025-02-01",
         "effective_end": "2026-03-14", "match": WEST_SMB, "credit_share": 1.0},
        {"rep": "Maria Lopez", "role": "PSM", "effective_start": "2026-03-15",
         "effective_end": None, "match": WEST_SMB, "credit_share": 1.0},
    ]
    lines, _ = apply_rules(rules, [_deal("J", "2026-03-10"), _deal("K", "2026-03-20")])
    assert {l.deal_id: l.rep for l in lines} == {"J": "Sam Park", "K": "Maria Lopez"}


def test_overlapping_coverage_splits_the_credit():
    rules = [
        {"rep": "Sam Park", "role": "PSM", "effective_start": "2025-02-01",
         "effective_end": None, "match": WEST_SMB, "credit_share": 0.5},
        {"rep": "Maria Lopez", "role": "PSM", "effective_start": "2025-02-01",
         "effective_end": None, "match": WEST_SMB, "credit_share": 0.5},
    ]
    lines, _ = apply_rules(rules, [_deal("D", "2026-08-10", amount=100000)])
    assert sorted(l.credited_amount for l in lines) == [50000.0, 50000.0]
    assert {l.rep for l in lines} == {"Sam Park", "Maria Lopez"}


def test_month_is_derived_from_the_close_date():
    rules = [{"rep": "Maria Lopez", "role": "PSM", "effective_start": "2026-01-01",
              "effective_end": None, "match": WEST_SMB, "credit_share": 1.0}]
    lines, _ = apply_rules(rules, [_deal("D", "2026-09-30")])
    assert lines[0].month == "2026-09"


def test_real_fixtures_load_and_every_deal_is_credited():
    lines, uncredited = apply_rules(load_rules(), load_deals())
    assert lines, "expected credited lines from the sample deal book"
    assert not uncredited, f"coverage gap: {[d['deal_id'] for d in uncredited]}"


def test_smb_deal_credits_both_the_psm_and_the_pam():
    # Multi-stakeholder: the same SMB deal lands on a PSM revenue line and a PAM
    # coverage line. D-1006 closed 2026-03-25, after the Sam -> Maria handoff.
    lines, _ = apply_rules(load_rules(), load_deals())
    d1006 = {(l.rep, l.role) for l in lines if l.deal_id == "D-1006"}
    assert ("Maria Lopez", "PSM") in d1006
    assert ("Alex Kim", "PAM") in d1006
    assert ("Sam Park", "PSM") not in d1006  # handed off before this deal closed


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(tests)} passed")
