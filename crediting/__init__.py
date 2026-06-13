"""Deterministic commission-crediting engine for the partner-compensation rock.

The AI half of the system (the /commissions-credit skill) authors the rules in
data/crediting_rules.json. This package is the deterministic half that applies
them — kept out of the LLM's hands on purpose, and unit-tested in tests/.
"""

from crediting.engine import CreditLine, apply_rules, load_deals, load_rules

__all__ = ["CreditLine", "apply_rules", "load_deals", "load_rules"]
