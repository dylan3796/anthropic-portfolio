---
name: new-entry
description: Add a new project or accomplishment to the resume system — interview Dylan to position it, draft options per surface, then write it into content.py and site_qa.py with rebuilds and evals green. Use whenever Dylan has new work worth putting on the record, or wants an existing entry repositioned.
allowed-tools: Read, Grep, Bash(python3:*), Write, Edit
---

# New Entry — interview, draft, gate, ship

Owned by big rock: [`plans/big-rocks/career-site.md`](../../../plans/big-rocks/career-site.md)

One content source, three surfaces: `content.py` feeds the resume PDFs and the
site; `site_qa.py` FACTS feeds the AI stand-in and the offline retrieval. The
interview and drafting are the AI half of this skill; the builders and eval
suites are the deterministic half that decides whether the result ships. Keep
that boundary — never hand-tune generated files to make something fit.

## Inputs

- Dylan's raw dump of the new work (any form — a paragraph, bullets, a link).
- `content.py` — jobs, per-lens bullets, positioning. The lenses are `ai` and `ops`.
- `site_qa.py` — FACTS (`id`/`q`/`k`/`a`/`src`), DECLINE, STARTERS.
- `tests/qa_harness.js` — the CASES list every FACT must be pinned in.
- `resume/STRATEGY.md` — positioning rules; no fabricated metrics, ever.

## Steps

1. Interview in conversational rounds of 2–4 questions — not a form. Cover:
   scale and stakeholders; what changed (before/after); **what's public-safe**
   — Dylan doesn't publish internal absolutes, so ask for safe framings
   (multiples, ranges, "first/only" markers); which lens(es) it serves; and
   whether it shifts the top-line summary or tagline. Stop asking when the
   answers stop changing what you'd write.
2. Draft 2–3 options per surface it touches: per-lens resume bullet(s); site
   entry (a `PROGRAMS` card and/or the job's `site_desc`, plus an optional
   proof link); 1–3 FACTS entries with retrieval keywords in `k`; a STARTERS
   chip only if a recruiter would plausibly open with it. Flag any summary or
   tagline delta the entry implies — repositioning is part of the job.
3. **Show all options and proposed positioning changes, and wait for Dylan's
   picks before writing anything.**
4. Edit `content.py` and `site_qa.py` only — never `docs/` or
   `worker/corpus.js` (generated). For every FACT added, append a matching
   case to `CASES` in `tests/qa_harness.js`.
5. Rebuild and verify:

   ```bash
   python3 resume/build_resumes.py
   python3 build_site.py
   python3 tests/test_site_qa.py
   python3 tests/test_resume_pdfs.py
   ```

   If resume text changed, regenerate the PDFs (Chromium command in the
   `build_resumes.py` docstring); if Chromium is unavailable, say so plainly
   and leave PDF regeneration as a flagged follow-up — never ship silently
   stale PDFs.
6. If an *old* retrieval case regresses, fix it by tuning the new FACT's `k`
   keywords — never by weakening the old case. If a PDF overflows one page,
   the remedy is editorial: propose what to cut, and let Dylan choose.
7. Show the full diff; commit only on approval.

## Don'ts

- Don't invent or publish an internal figure — a confident wrong number about
  Dylan's career is the one unrecoverable failure. Public-safe framings only.
- Don't add a FACT without an eval case — unpinned facts are how BM25 keyword
  collisions silently steal an old fact's queries as the corpus grows.
- Don't shrink fonts or squeeze margins to make a page fit — one page per PDF
  is a hard constraint, and the remedy is cutting content, decided by Dylan.
