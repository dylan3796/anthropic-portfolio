---
status: proposed
owner: Dylan Ram
horizon: FY27 H1
owned-skills: new-entry
---

# Big Rock: Career Site & Resume System

## Objective

Run the career itself as a governed system — the repo's own thesis applied to
its owner. One content source (`content.py`) feeds three surfaces: the resume
PDFs, the public site on a personal domain, and the AI stand-in's grounded
corpus. New work enters through an interview (`/new-entry`), never ad-hoc
edits, so every claim stays consistent, public-safe, and eval-pinned across
all three surfaces. The stand-in answers a recruiter's screen without
hallucinating: facts come from the corpus, and requirement questions get an
explicit mapping to listed experience — fit and gap both.

## Milestones

- [x] One-link portfolio site with lens toggle and resume downloads — 2026-08
- [x] Grounded answer engine + live chat behind a provider-agnostic Worker — 2026-08
- [x] Content consolidation: `content.py` single source, escape-at-render,
      one-page PDF guard, CI — 2026-08
- [ ] `/new-entry` shipped and exercised on a real new project (the acceptance
      test is a full interview → drafts → approval → green suites run)
- [ ] Requirement-mapping ("level 1") prompt upgrade with live evals
- [ ] dylanram.com live: CNAME, HTTPS enforced, chat allowed from the new origin
- [x] JD fit-check mode built with its own Worker guards — ships dark until
      the Worker is deployed — 2026-08
- [x] Lens URLs, OG card, `docs/llms.txt` — 2026-08
- [ ] Worker deployed with a spend cap; `CHAT_ENDPOINT` set (owner task)

## Owned Skills

- `/new-entry` — reads a raw project dump, interviews Dylan to position it
  (scale, stakeholders, public-safe framings, which lens), drafts 2–3 options
  per surface, then writes `content.py` + `site_qa.py` behind an approval
  gate, with rebuilds and both eval suites green before any commit.

## Open Questions

- When does a new entry justify a third lens rather than reshaping the two?
- The retrieval corpus is BM25-lite over keywords; past roughly 60 FACTS,
  collisions get likelier. What triggers a re-tuning pass — a count, or the
  first eval regression?
- One page per PDF means entries eventually compete. Who decides what falls
  off, and does anything get an "archive" surface (site-only, not resume)?

## Improvement Log

- **2026-08-13** — Created. First three milestones landed the same week the
  rock was drafted; promoted status is the owner's call.
