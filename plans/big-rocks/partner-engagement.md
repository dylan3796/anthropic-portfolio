---
status: active
owner: Dylan Ram
horizon: FY27 H2
owned-skills: call-notes-to-jira
---

# Big Rock: Partner Engagement (Field Execution)

## Objective

Close the gap between what happens in a partner conversation and what actually
gets tracked and done. Co-sell runs on calls, QBRs, and hallway commitments,
and the follow-ups that matter — a deal-reg to chase, a certification to
schedule, an exec intro to make — too often die in someone's notebook. This
rock owns the execution layer that turns partner-facing signal into tracked,
owned action, grounded in the same partner book and vocabulary every other
rock reads.

## Milestones

- [x] Ship `/call-notes-to-jira` — turn raw call notes into ready-to-file Jira tickets, each tagged to a partner in the book and an owning PSM/PAM (2026-06-13)
- [ ] Wire a Jira integration (MCP or CLI) so the skill can file tickets, not just draft them
- [ ] Ship `/next-best-action` — rank a seller's next moves from their book: blocked deal-regs, certification gaps, partner relationships mapping into open pipeline
- [ ] Close the loop: reconcile filed tickets back against deal-reg and certification status so follow-ups don't go stale

## Owned Skills

- [`/call-notes-to-jira`](../../.claude/skills/call-notes-to-jira/SKILL.md) —
  drafts tracked tickets from unstructured call notes; tags each to a real
  partner and the owning rep, and files them when a Jira integration is present.

`/next-best-action` is proposed above and ships when its milestone is in flight.

## Open Questions

- Should the skill file tickets directly, or always stop at a draft a human
  approves before anything lands in Jira?
- Ticket ownership when a follow-up spans both reps (revenue + relationship) —
  one ticket with two owners, or split?
- Where do filed tickets get reconciled — back into the scorecard's health
  signal, or a standalone follow-up ledger?

## Improvement Log

- **2026-06-13** — Created when `/call-notes-to-jira` had no owning rock: the
  existing rocks own measurement (attribution, scorecard), program mechanics,
  comp, and planning, but nothing owned field *execution* — turning partner
  conversations into tracked action. This rock is that home, and
  `/next-best-action` moves here from the showcase backlog.
