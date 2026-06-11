---
status: active
owner: Dylan Ram
horizon: FY27 H2
owned-skills: none yet
---

# Big Rock: AI Solutions Strategy

## Objective

Own the portfolio's strategic point of view on the emerging AI-services /
forward-deployed-engineer (FDE) market, anchored on an analysis of Ramp AI
Solutions — Ramp's services arm that embeds FDEs to make finance orgs
"agent-friendly" (data connectivity, context layer, evals and feedback
loops, production infrastructure). The portfolio's counter-position must be
explicit: what FDE firms sell as an embedded service, this repo demonstrates
as a self-serve operating model, and the orgs that adopt that model
internally are the ones that won't need to rent FDEs. This rock also owns
the cross-repo narrative that ties Dylan's three repos into one thesis, so
the portfolio reads as a single argument rather than three demos.

This rock is the **source of truth for the strategic thesis** in this repo.
App sections and any future skills reference the thesis below rather than
restating it.

## Thesis (canonical)

- **Service vs. operating model.** FDE firms embed people to install agent
  readiness; this repo demonstrates the same outcomes (context layer, plans,
  skills, recursive improvement) as a self-serve operating model an org runs
  itself.
- **Compound vs. depreciate.** Differentiation should sit on assets that
  compound — captured context, domain judgment, data — not on plumbing that
  depreciates: hosting, connectors, telemetry.
- **One thesis, three repos.** Covant (`partner-attribution-ai`) captures
  the context of a company's partner business and generalizes it into a
  structure agentic workflows can run on, so partner teams deliver
  best-in-class partner experience. Compass provides agent fleet
  observability — the evals/feedback-loops layer. This portfolio is the
  operating model and context layer that the other two plug into.

## Milestones

- [x] Complete Ramp AI Solutions analysis and document the canonical thesis
  in this plan (2026-06-11)
- [x] Ship the "Service vs. operating model" section in `app.py`, citing the
  thesis above (2026-06-11)
- [x] Ship the cross-repo narrative section in `app.py` connecting Covant,
  Compass, and this portfolio as one thesis (2026-06-11)
- [ ] Resolve the name-vs-category question (cite Ramp directly or describe
  the FDE category) and make the shipped sections consistent with the call —
  shipped sections currently describe the category, provisionally
- [ ] Complete the first quarterly refresh of the market view — labs'
  deployment programs, vertical SaaS services arms — and log what changed
  (due FY27 Q3, by 2026-10-31)
- [ ] Decide whether quarterly refreshes justify building `/strategy-refresh`
  or stay a manual checklist in this plan

## Owned Skills

None yet. Proposed:

- `/strategy-refresh` — re-checks the FDE market (labs' deployment programs,
  vertical SaaS services arms, Ramp AI Solutions itself) against the thesis
  above and proposes updates to the `app.py` sections this rock owns. Build
  only if the first manual quarterly refresh proves the loop is worth
  automating.

## Open Questions

- Should the thesis section cite Ramp AI Solutions by name (concrete, but
  dates as Ramp's offering evolves) or describe the FDE-services category
  (durable, but less vivid)? Shipped sections describe the category for now.
- Do Covant and Compass deep-links belong in the portfolio app, or does
  linking out dilute the single-page walkthrough? Links shipped for now —
  a portfolio that hides its own products argues against itself.
- Is quarterly the right refresh cadence for the market view, or should
  refreshes be event-driven (e.g., a major lab launches a deployment
  program)?

## Improvement Log

- **2026-06-11** — Rock created via `big-rock-planner` with the Ramp AI
  Solutions analysis as its founding milestone; thesis placed in the plan
  (not the app) so `app.py` sections reference one canonical definition.
  Both app sections shipped the same day; provisional calls (category over
  name, deep-links included) recorded in Open Questions for the first
  refresh to revisit.
