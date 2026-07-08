# Resume Strategy — one fact base, three lenses, two designs

The play: **maintain one fact base**, render it through **three lenses**
(builder / AI-native operator / operating leader) in **two visual designs**.
Every bullet traces back to the same source material (the current resume, the
real Databricks work Dylan described, and what's verifiably in this repo), so
nothing drifts into embellishment — the lenses differ only in what leads and
which vocabulary they speak; the designs differ only in layout.

Content and layout both live in `build_resumes.py`. Regenerate:

```bash
python3 resume/assets/fetch_fonts.py     # once — bundles Inter + Lora as base64
python3 resume/build_resumes.py          # writes resume/output/<stem>--<design>.html
# then print each to PDF:
chromium --headless --no-sandbox --print-to-pdf-no-header \
  --print-to-pdf=resume/output/<name>.pdf file://$PWD/resume/output/<name>.html
```

## The three lenses and the roles they chase

The three cover the five archetypes Dylan is targeting without overlap: a
**builder** pole, an **AI-native operator** pole, and an **operating-leader**
pole.

| Lens | Stem | Primary targets | What leads |
|---|---|---|---|
| **Forward Deployed / Applied AI** | `dylan-ram-ai-forward-deployed` | Applied AI, AI Solutions Engineer, AI Operations, adjacent-FDE | The self-built Claude Code platform as centerpiece — architecture, the deterministic tested engine, and **evals** ("how do you know it's working"), backed by shipped AI at Databricks |
| **AI Strategy & Deployment** | `dylan-ram-ai-strategy` | AI Strategy, AI Enablement, AI Operations (non-eng), Head of Automation, "BizOps 2.0" at AI companies | Setting up how an org deploys AI: foundational data layer, KPI alignment, self-serve enablement, the operating-system build as a *reference pattern* |
| **Business Operations / Strategy** | `dylan-ram-business-operations` | **Business Operations Lead (primary)**, Chief of Staff, Partner S&O | The signature programs built from scratch (forecast, attribution, first new-logo incentive), the two-sided-marketplace stakeholder story, "zero to one / one to 100" — AI as the modern edge |

**Why FDE and AI-Strategy are separate resumes (not one):** the market draws a
hard line. FDE/Applied-AI screens for *ship production code*; AI-Strategy /
Enablement screens for *built-and-deployed AI in real workflows, drove
adoption* — a real but lower coding bar. Same person, two bars, two resumes.

**Decision rule when a JD blends categories:** read the first three
responsibilities. "Write production Python / ship integrations" → Forward
Deployed. "Drive AI adoption / enablement / prototype workflows" → AI Strategy.
"Operating cadence / planning / cross-functional / own the business" →
Business Operations. When two fit, send the one whose keyword bank the JD
echoes more.

## The two designs

Both are built from the same content; pick per how the resume will be read.

| Design | File suffix | Look | Use when |
|---|---|---|---|
| **Editorial** | `--editorial` | Single column, Lora serif nameplate, terracotta accents. ATS-safe. | Applying through a job portal / ATS, or when you don't know how it'll be parsed. The safe default. |
| **Modern** | `--modern` | Two-column with a skills rail on a warm panel, uppercase display name. More designed. | Sending straight to a hiring manager, a referral, or attaching alongside the portfolio. |

**The ATS trade-off, stated plainly:** single-column parses cleanly everywhere;
two-column *can* confuse older ATS parsers (they sometimes read across the
columns). The text is real and selectable in both, so most modern parsers are
fine — but if a posting screams "big-company ATS portal," send Editorial.
Typography (Inter + Lora) is bundled as base64 in `assets/fonts.css`, so the
PDFs render identically anywhere with no network.

## What the 2026 market research changed

- **BizOps has become "BizOps 2.0."** JDs now expect an operator who can "open
  Claude, open Zapier, open the CRM, and just build" — AI fluency is "the job."
  Dylan's self-built agent system is exactly this signal, so the Business
  Operations resume keeps AI prominent, not buried.
- **Chief of Staff JDs now include "own the AI agenda."** Only ~7% of senior
  operators read as truly "AI-native" — Dylan clears that bar, and it's his
  sharpest differentiator for CoS/BizOps.
- **Partner S&O is a near-verbatim match** to his current title; the level-up
  keyword is *Senior Manager / Head*, and the phrase to lead with is "architect
  strategy while operationalizing it and diving deep into the details."
- **True lab FDE (Anthropic/OpenAI/Palantir) is a reach** — those want "ship
  production applications in Python/TypeScript, 5+ yrs engineering." The Forward
  Deployed resume aims at *Applied AI / AI Solutions / AI Operations* adjacents,
  leaning on the repo + the evals story as proof. Do not claim "software
  engineer," "production integrations," or "distributed systems."

## Keyword banks (mirror the JD's language in summary + skills)

- **AI / agents:** deployed AI agents, agentic workflows, LLM deployment,
  prompt engineering, agent development, evaluation frameworks / evals, RAG,
  MCP (Model Context Protocol), AI enablement, AI fluency, self-serve analytics,
  "AI-native," build/prototype AI-enabled workflows, playbooks & standards.
- **Strategy / ops:** operating cadence, strategic planning, OKRs,
  cross-functional, GTM strategy & operations, co-sell, channel/partner
  management, business acumen, influence without authority, zero-to-one,
  one-to-100 scaling, executive/board reporting, incentive/comp design,
  quota-setting, forecasting, two-sided marketplace / multi-stakeholder.
- **Data:** SQL, Python, Tableau, Salesforce reporting, dashboards, revenue
  attribution, medallion architecture / Spark, KPI definition & tracking.

## On quantification — a deliberate choice

Dylan's call, and a defensible one: **no dollar/stakeholder counts on the
page.** The bullets lead with *what the work was and its quality* ("built the
team's first forecasting process," "designed the canonical attribution model,"
"zero to one … one to 100"); scale is an interview conversation, where it's
credible rather than a number a screener discounts as inflated. If a specific
role rewards a hard metric and Dylan has a defensible one, add it inline for
that application only.

## Honesty guardrails (do not cross)

- Every Experience bullet is a rewording of the current resume or of a fact
  Dylan stated directly — no new claims, no invented numbers.
- The repo's scorecard figures ($6.5M sourced, 12 partners, etc.) are
  **synthetic demo data**. They never appear on any resume.
- The Claude Code build is always labeled a public / independent project.
- The Forward Deployed resume stays inside "operator-engineer who deploys" and
  "fluent in Python/SQL" — never "software engineer."

## Known gaps and how the variants compensate

- **No formal engineering title** → the FDE lens leans on the *public repo*
  (link is on the resume) and the evals answer as the "can you really build?"
  proof; it targets Applied-AI adjacents, not true lab FDE.
- **One LinkedIn for three resumes** → update LinkedIn to the AI-native
  operator blend (Business Operations lens with AI forward), since all variants
  link to it.
- **Portfolio URL** → the Replit site becomes the broad career showcase (next
  deliverable); when it's live, swap the GitHub link for it on the AI variants
  and keep the repo public as the code-proof.

## Per-application checklist

1. Pick the lens by the decision rule; pick the design by how it'll be read.
2. Echo the JD's top three responsibility phrases in the summary (only where
   true).
3. Reorder the Databricks bullets so the first two match what the role screens
   for.
4. Export and submit as `Dylan-Ram-Resume.pdf` — recruiters see filenames.
5. Confirm it's still one page.
