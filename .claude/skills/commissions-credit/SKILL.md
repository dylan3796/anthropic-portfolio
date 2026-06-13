---
name: commissions-credit
description: Codify the partner team's plain-English coverage sheet into effective-dated crediting rules, then verify them against the deal book so commissions actuals credit the right person on the right line for the right months. Use when the coverage sheet changes (new hire, territory handoff, split) or before a comp run.
allowed-tools: Read, Grep, Bash(python3:*), Write, Edit
---

# Commissions Crediting

Owned by big rock: [`plans/big-rocks/partner-compensation.md`](../../../plans/big-rocks/partner-compensation.md)

The one place plain-English coverage becomes governed crediting rules. The
**AI half** is this skill: read what managers wrote in `coverage_assignments.csv`
and turn intent into structured, effective-dated rules. The **deterministic half**
is `crediting/engine.py`: it applies those rules to deals and is unit-tested — no
model does the money math. Keep that boundary.

## Inputs

- `data/coverage_assignments.csv` — the coverage sheet managers maintain (the
  "Google Sheet"). Columns: `rep_name`, `role` (PSM/PAM — see the CLAUDE.md
  glossary), `start_date`, `end_date` (blank = open), `coverage` (plain English),
  `notes`.
- `data/DATA_DICTIONARY.md` — segment, region, and motion enumerations. Match
  predicates must use these exact values; never invent a territory dimension.

## Steps

1. Read the coverage sheet and the dictionary's enumerations.
2. For each row, codify the plain-English `coverage` into a structured rule:
   - `match`: any of `segment`, `region`, `motion`, `partner_name` as value
     lists. An omitted dimension is a wildcard (covers all).
   - `effective_start` / `effective_end` from the dates. Resolve handoffs:
     when one row says it takes over from another ("taking over the SMB book
     from Sam"), set the outgoing rep's `effective_end` to the day before the
     incoming rep's `start_date` so there is no gap and no double-coverage.
   - `credit_share`: 1.0 unless the sheet describes a split; co-coverage that
     should split must say so.
   - `source`: quote the sheet row you codified, so every rule is traceable.
3. Write the result to `data/crediting_rules.json` as
   `{ "generated_by": ..., "fiscal_year": ..., "rules": [...] }`.
4. **Verify before trusting it.** Run the engine against the deal book and
   report:
   - the credited lines (rep · role · deal · month · amount), and
   - any **uncredited deals** — a deal matching no rule is a coverage gap, not a
     zero. Surface it loudly.
   ```bash
   python3 -c "from crediting.engine import apply_rules, load_rules, load_deals; \
   lines, gaps = apply_rules(load_rules(), load_deals()); \
   print(len(lines), 'credited lines;', len(gaps), 'uncredited:', [d['deal_id'] for d in gaps])"
   ```
5. Run the golden tests so a codification change can't silently break the money
   math: `python3 tests/test_crediting.py`.
6. **Show the rules diff and the verification output, then ask before writing.**

## Don'ts

- Never let an LLM compute credited amounts — that path is `crediting/engine.py`,
  and it is tested. This skill only authors rules.
- Never leave a deal uncredited silently. If the sheet doesn't cover something,
  report the gap and stop; don't paper over it with a catch-all rule.
- Never invent segment/region/motion values not in the data dictionary.
