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

- [x] Site + lens toggle + resume downloads — 2026-08
- [x] Grounded chat + provider-agnostic Worker — 2026-08
- [x] content.py single source + one-page PDF guard + CI — 2026-08
- [x] Requirement-mapping prompt (maximalist: LISTED/TRANSFERS/RAMP/NOT LISTED) — 2026-08
- [x] JD fit check (dark until Worker deploy) — 2026-08
- [x] Lens URLs, OG card, llms.txt, JSON-LD, robots/sitemap — 2026-08
- [x] Cold-email playbook (outreach/PLAYBOOK.md) — 2026-08
- [ ] /new-entry exercised on a real project
- [ ] Worker deployed + spend cap + CHAT_ENDPOINT (owner)
- [ ] dylanram.com live (owner; DOMAIN-SETUP.md)
- [ ] ANALYTICS_ID set before first email batch (owner)

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
