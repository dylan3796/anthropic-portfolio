"""Deterministic commission-crediting engine.

The AI half of this system (the ``/commissions-credit`` skill) turns plain-English
coverage — "Maria takes over the SMB book from Sam on March 15" — into the
structured, effective-dated rules in ``data/crediting_rules.json``.

This module is the deterministic half: given those rules and a set of closed
deals, it decides exactly who is credited, on which line, for which month. The
money math is code, not a prompt, so it is reproducible and unit-tested
(see ``tests/test_crediting.py``).
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# Dimensions a rule may constrain. An omitted/empty dimension is a wildcard.
MATCH_DIMENSIONS = ("segment", "region", "motion", "partner_name")


def _parse_date(value):
    return date.fromisoformat(value) if value else None


@dataclass(frozen=True)
class CreditLine:
    rep: str
    role: str
    deal_id: str
    month: str          # YYYY-MM, derived from the deal close date
    credited_amount: float
    share: float


def _rule_covers(rule, deal) -> bool:
    """True if this rule is in effect on the close date and matches the deal."""
    close = _parse_date(deal["close_date"])
    start = _parse_date(rule.get("effective_start"))
    end = _parse_date(rule.get("effective_end"))
    if start and close < start:
        return False
    if end and close > end:
        return False
    match = rule.get("match", {})
    for dim in MATCH_DIMENSIONS:
        allowed = match.get(dim)
        if allowed and deal.get(dim) not in allowed:
            return False
    return True


def apply_rules(rules, deals):
    """Apply crediting rules to deals.

    Returns ``(credit_lines, uncredited_deals)``. A deal may be credited to more
    than one rep — a PSM on the revenue line and a PAM on the coverage line, or a
    deliberate split. A deal that matches no active rule is returned as
    *uncredited* rather than silently dropped: an uncredited deal at actuals time
    is a crediting gap, not a zero.
    """
    lines: list[CreditLine] = []
    uncredited: list[dict] = []
    for deal in deals:
        amount = float(deal["amount"])
        close = _parse_date(deal["close_date"])
        month = f"{close.year:04d}-{close.month:02d}"
        matched = [r for r in rules if _rule_covers(r, deal)]
        if not matched:
            uncredited.append(deal)
            continue
        for rule in matched:
            share = float(rule.get("credit_share", 1.0))
            lines.append(
                CreditLine(
                    rep=rule["rep"],
                    role=rule.get("role", ""),
                    deal_id=deal["deal_id"],
                    month=month,
                    credited_amount=round(amount * share, 2),
                    share=share,
                )
            )
    return lines, uncredited


def load_rules(path=None):
    path = Path(path) if path else DATA / "crediting_rules.json"
    data = json.loads(path.read_text())
    return data["rules"] if isinstance(data, dict) else data


def load_deals(path=None):
    path = Path(path) if path else DATA / "commission_deals.csv"
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))
