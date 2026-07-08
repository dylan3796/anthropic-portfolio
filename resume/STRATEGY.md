# Resume Strategy — one fact base, three lenses

The play: **don't maintain three resumes, maintain one fact base** with three
orderings. Every bullet across all variants traces back to the same source
material (the current resume + the work in this repo), so nothing can drift
into embellishment — the variants differ only in what leads, what's grouped,
and which vocabulary the summary and skills sections speak.

Content lives in `build_resumes.py`. Edit the dicts, rerun, reprint:

```bash
python3 resume/build_resumes.py
chromium --headless --no-sandbox --print-to-pdf-no-header \
  --print-to-pdf=resume/output/<name>.pdf file://$PWD/resume/output/<name>.html
```

## The three variants

| Variant | File | Target roles | What leads |
|---|---|---|---|
| **AI Operations** | `dylan-ram-ai-operations` | AI Operations Manager/Lead, Deployed/Forward-Deployed Engineer (business-facing), AI Enablement, Applied AI / GTM AI, solutions roles at AI-native companies | The deployed agents at Databricks, then the Claude Code operating-system build with the "AI for judgment, tested code for money" boundary |
| **Strategy & Ops** | `dylan-ram-strategy-ops` | Business Operations, Strategy & Operations, GTM Strategy, Revenue/Partner Operations, ecosystem ops | First-S&O-hire narrative: quota-setting, tiering framework, executive alignment, $250M business partnership — AI as the capacity multiplier, not the headline |
| **Data & Analytics** | `dylan-ram-data-analytics` | GTM/Revenue Analytics, Senior Analytics/BI, Data & Insights, analytics-engineering-adjacent | Attribution systems, company-wide standardized datasets, single-source-of-truth dashboards, governance — with LLM agents as the distribution layer |

**Decision rule when a JD blends categories:** read the first three
responsibilities. Pick the variant whose top two Databricks bullets match
them. If a role is explicitly "AI + ops" (increasingly common), start from
the AI variant and promote the quota/planning bullet to position three.

## Keyword banks (mirror the JD's language in summary + skills)

- **AI ops:** deployed AI, agents, LLM workflows, evals, Claude Code, agent
  operating system, human-in-the-loop, AI enablement, applied AI, guardrails
- **Strategy & ops:** annual planning, quota setting, territory design,
  executive alignment, cross-functional, partner ecosystem, GTM strategy,
  operating cadence, QBR
- **Data:** attribution, single source of truth, data governance, metric
  definitions, standardized datasets, Spark/SQL pipelines, executive
  dashboards, self-serve analytics

## What changed from the current resume, and why

1. **Single-column format.** The old two-column sidebar layout is what ATS
   parsers mangle most — skills and dates end up attached to the wrong jobs.
   The new template is deliberately parse-safe: standard section headings, no
   layout tables, no graphics.
2. **A summary + tagline per variant.** The old resume had no positioning
   statement; a screener had to infer the story. Now the first four lines do
   the targeting.
3. **The portfolio became a "Selected Project" section.** The Claude Code
   build is the strongest AI evidence available, but it is *not* Databricks
   work — so it's labeled a public build with the repo link, never merged
   into employment history.
4. **Cut "stackoverflow searches," Activities, and most Interests.** Charming
   at analyst level, costly at manager level. The space went to the project
   section.
5. **Same facts, stronger frames.** e.g. "Deployed AI-driven reporting
   agents…" now closes with what it means ("…into how partner metrics are
   distributed across the org") — reworded, never inflated.

## Honesty guardrails (do not cross)

- Every Experience bullet is a rewording of the current resume — no new
  claims, no new numbers.
- The repo's scorecard figures ($6.5M sourced, 12 partners, etc.) are
  **synthetic demo data**. They never appear on any resume.
- The Claude Code build is always labeled as a public/independent project.
- Only add real quantification (agent user counts, hours saved, quota size
  covered) if it's defensible in an interview and not confidential.

## Known gaps, and how the variants compensate

- **No formal engineering title** → the AI variant leans on *working,
  verifiable systems*: the repo link is on the resume, and `crediting/engine.py`
  + `tests/` are the code-review answer to "can you actually build?"
- **Thin quantification** ("10+", "$250M") → the highest-ROI edit available
  is adding 2–3 real, defensible numbers to the Databricks bullets.
- **One LinkedIn for three resumes** → update LinkedIn to the A/B blend
  (AI-forward strategy & ops) since every variant links to it.
- **Portfolio URL** → if the Streamlit app gets a public deployment, swap the
  GitHub link for it on the AI variant; keep the repo public either way.

## Per-application checklist

1. Pick the variant by the decision rule above.
2. Echo the JD's top three responsibility phrases in the summary (only where
   true).
3. Reorder Databricks bullets so the first two match what the role screens
   for.
4. Export and submit as `Dylan-Ram-Resume.pdf` — recruiters see filenames;
   don't leak the variant name.
5. Confirm it's still one page (`build_resumes.py` + print preview).
