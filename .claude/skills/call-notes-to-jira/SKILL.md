---
name: call-notes-to-jira
description: Turn raw partner-call notes into tracked Jira tickets — follow-ups like a stalled deal-reg to chase, a missing certification to schedule, or an exec intro to tee up — each tagged to the partner and the owning rep. Use after a partner call when the follow-ups are still buried in notes.
allowed-tools: Read, Grep, Bash(python3:*)
---

# Call Notes → Jira Tickets

Owned by big rock: [`plans/big-rocks/partner-engagement.md`](../../../plans/big-rocks/partner-engagement.md)

This skill drafts ready-to-file tickets from unstructured notes; it does not
invent the work. Filing into Jira runs through whatever integration the session
has (a Jira MCP server or CLI). If none is configured, output the tickets as
markdown the rep can paste in.

## Inputs

- The call notes — pasted as the argument, or a path to a notes file.
- Optionally a partner name. If given, it must match `partner_name` in
  `data/partner_metrics.csv`; if missing, infer it from the notes and confirm
  against the book before tagging anything.

## Steps

1. Read `data/partner_metrics.csv` and `data/DATA_DICTIONARY.md` so every
   ticket is tagged to a real partner and uses the dictionary's vocabulary
   (tier, motion, the owning PSM/PAM).
2. Extract action items from the notes — only commitments and follow-ups, not
   discussion. Typical shapes:
   - a deal registration to chase or renew before its 90-day window lapses
   - a certification gap to schedule (ties to `certified_engineers`)
   - an exec intro or QBR to tee up
   - a benefits or tier question to route to the program owner
3. For each action, draft a ticket:
   - **summary** — one imperative line ("Schedule Security cert for <partner>")
   - **partner / tier / motion** — from the book
   - **owner** — the PSM for revenue follow-ups, the PAM for relationship and
     enablement follow-ups (see the roles in `CLAUDE.md`); if unclear, say so
   - **why now** — the trigger from the notes (a date, a risk, a commitment)
4. Surface anything ambiguous instead of inventing it: an unrecognized partner
   name, an action with no clear owner, a commitment with no date.
5. If a Jira integration is available, create the tickets and return their
   keys; otherwise output the markdown ticket list for the rep to file.

## Don'ts

- Don't invent action items the notes don't support, or assign an owner you
  can't justify from the roles in `CLAUDE.md`.
- Don't tag a partner that isn't in `data/partner_metrics.csv` — confirm first.
- Don't restate metric definitions; read them from the dictionary.
