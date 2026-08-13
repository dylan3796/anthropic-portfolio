# Big Rocks Index

Long-horizon strategic initiatives. Each rock has one living plan document,
owns its skills, and carries an Improvement Log written by the `/improve-setup`
loop. The SessionStart hook surfaces this table's status into every session.

| Big Rock | Status | Horizon | Owned Skills | Last Touched |
|---|---|---|---|---|
| [Partner Compensation](partner-compensation.md) | active | FY27 H1 | `/commissions-credit` | 2026-06-13 |
| [Partner Attribution](partner-attribution.md) | active | FY27 H1 | none (`/attribution-compare` retired) | 2026-06-13 |
| [Partner Scorecard](partner-scorecard.md) | active | FY27 H1 | `/partner-qbr` | 2026-06-13 |
| [Partner Program](partner-program.md) | active | FY27 H2 | none yet (`/tier-review`, `/benefits-audit` proposed) | 2026-06-10 |
| [Partner Engagement](partner-engagement.md) | active | FY27 H2 | `/call-notes-to-jira` (`/next-best-action` proposed) | 2026-06-13 |
| [Partner Planning](partner-planning.md) | planned | FY27 H2 | none yet (`/quota-scenario` proposed) | 2026-06-05 |
| [Career Site](career-site.md) | proposed | FY27 H1 | `/new-entry` | 2026-08-13 |

## Lifecycle

`proposed → planned → active → maintaining → done`

A rock moves to `active` when its first milestone is in flight, and to
`maintaining` when the remaining work is operational (skills exist, plan is
mostly checkboxes). New rocks are drafted with the `big-rock-planner` agent
using the template below.

## Plan template

Every rock doc starts with this header and follows this section order:

```markdown
---
status: proposed | planned | active | maintaining | done
owner: <name>
horizon: <fiscal period>
owned-skills: <comma-separated skill names, or "none yet">
---

## Objective
## Milestones
## Owned Skills
## Open Questions
## Improvement Log
```
