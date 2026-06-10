---
name: improve-setup
description: The recursive improvement loop. Reviews the session log, git history, and big-rock plans for friction signals, then proposes concrete edits to CLAUDE.md, the skills, and the plans themselves. Run after sessions with meaningful work or meaningful friction.
allowed-tools: Read, Grep, Glob, Bash(git log:*), Edit, Write
---

# Improve Setup (meta-skill)

This skill closes the loop that makes the whole setup compound: hooks generate
evidence → this skill reviews the evidence → it proposes edits to the setup
itself → accepted edits are logged where they belong. The subject of the
review is not the portfolio app — it is `CLAUDE.md`, the skills, the hooks,
and the big-rock plans.

## Evidence to gather

1. `retros/session-log.md` (written by the Stop hook).
2. `git log --oneline -15` — what actually shipped recently.
3. Every plan in `plans/big-rocks/*.md` — statuses, unchecked milestones,
   open questions, last Improvement Log dates.
4. The current `CLAUDE.md` and each `SKILL.md`.

## Friction signals to look for

| Signal | Proposed fix target |
|---|---|
| An instruction the user repeated across sessions | new convention in `CLAUDE.md` |
| A skill that was invoked and then manually corrected | edit to that `SKILL.md` |
| A milestone untouched for >30 days on an `active` rock | plan update or descope |
| A recurring task with no owning skill | new skill, proposed in the owning rock's plan |
| Work that mapped to no big rock | new rock, drafted via the `big-rock-planner` agent |
| Definitions duplicated across files | consolidate to the single source of truth |

## Output

1. Write `retros/YYYY-MM-DD-retro.md` (today's date) containing:
   - **Observations** — each tied to specific evidence (session-log lines,
     commits, stale milestones).
   - **Proposed edits** — concrete, diff-style snippets against the exact
     files (`CLAUDE.md`, a `SKILL.md`, a plan doc). No vague "consider
     improving X".
2. Present the proposals and **ask which to apply**. Apply only approved ones.
3. For each applied edit, append a dated entry to the **Improvement Log** of
   the big rock it belongs to (or note it in `CLAUDE.md`'s history if it is
   setup-wide).
4. Trim `retros/session-log.md` to its header plus entries newer than the
   retro you just wrote, so the next run starts from fresh evidence.

## Don'ts

- Don't edit anything before approval — this skill's value is judgment, and
  unreviewed self-modification erodes trust in the whole loop.
- Don't propose more than ~5 edits per run; rank by friction removed.

## Worked example

See `retros/2026-06-05-retro.md` for a completed iteration of this loop:
two observations, three proposed edits, two applied (a `CLAUDE.md` convention
and a weight-table consolidation), one deferred as a proposed skill in the
partner-planning rock.
