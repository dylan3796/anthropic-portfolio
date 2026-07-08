# Resume Strategy — one fact base, three lenses

The play: **don't maintain three resumes, maintain one fact base** with three
orderings. Every bullet across all variants traces back to the same source
material (the current resume + the real Databricks work + what's verifiably in
this repo), so nothing drifts into embellishment — the variants differ only in
what leads, what's grouped, and which vocabulary the summary and skills speak.

Content lives in `build_resumes.py`. Edit the dicts, rerun, reprint:

```bash
python3 resume/build_resumes.py
chromium --headless --no-sandbox --print-to-pdf-no-header \
  --print-to-pdf=resume/output/<name>.pdf file://$PWD/resume/output/<name>.html
```

## The three variants and the roles they chase

The three cover the five archetypes Dylan is targeting without overlap: a
**builder** pole, an **AI-native operator** pole, and an **operating-leader**
pole.

| Variant | File | Primary targets | What leads |
|---|---|---|---|
| **Forward Deployed / Applied AI** | `dylan-ram-ai-forward-deployed` | Applied AI, AI Solutions Engineer, AI Operations, adjacent-FDE | The self-built Claude Code platform as centerpiece — architecture, the deterministic tested engine, and **evals** ("how do you know it's working"), backed by shipped AI at Databricks |
| **AI Strategy & Deployment** | `dylan-ram-ai-strategy` | AI Strategy, AI Enablement, AI Operations (non-eng), Head of Automation, "BizOps 2.0" at AI companies | Setting up how an org deploys AI: foundational data layer, KPI alignment, self-serve enablement, the operating-system build as a *reference pattern* |
| **Business Operations / Strategy** | `dylan-ram-business-operations` | **Business Operations Lead (primary)**, Chief of Staff, Partner S&O | The signature programs built from scratch (forecast, attribution, first new-logo incentive), quota-setting, operating cadence — AI as the modern edge |

**Why FDE and AI-Strategy are separate resumes (not one):** the market draws a
hard line between them. FDE/Applied-AI screens for *ship production code*;
AI-Strategy/Enablement screens for *built-and-deployed AI in real workflows,
drove adoption* — a real but lower coding bar. Same person, two different bars,
so two resumes.

**Decision rule when a JD blends categories:** read the first three
responsibilities. If they say "write production Python / ship integrations" →
Forward Deployed. If "drive AI adoption / enablement / prototype workflows" →
AI Strategy. If "operating cadence / planning / cross-functional / own the
business" → Business Operations. When two fit, send the one whose *keyword bank*
(below) the JD echoes more.

## What the 2026 market research changed

Full findings summarized here; they drove the wording above.

- **BizOps has become "BizOps 2.0."** JDs now expect an operator who can "open
  Claude, open Zapier, open the CRM, and just build" — AI fluency is "the job,
  not a nice-to-have." Dylan's self-built agent system is exactly this signal,
  so the Business Operations resume keeps AI prominent, not buried.
- **Chief of Staff JDs now include "own the AI agenda."** Databricks' own CoS
  posting asks the holder to "identify and implement AI-powered tools to improve
  operating efficiency." Only ~7% of senior operators read as truly "AI-native"
  — Dylan clears that bar, and it's his sharpest differentiator for CoS/BizOps.
- **Partner S&O is a near-verbatim match** to his current title; the level-up
  keyword is *Senior Manager / Head*, and the phrase to lead with is "architect
  strategy while operationalizing it and diving deep into the details."
- **True lab FDE (Anthropic/OpenAI/Palantir) is a reach** — those want "3–5+
  yrs engineering, ship production applications in Python/TypeScript." The
  Forward Deployed resume therefore aims at *Applied AI / AI Solutions / AI
  Operations* adjacents, and leans on the repo + the evals story as proof. Do
  not claim "software engineer," "production integrations," or "distributed
  systems" — the research flags these as easily disproven overreach.

## Keyword banks (mirror the JD's language in summary + skills)

- **AI / agents:** deployed AI agents, agentic workflows, LLM deployment,
  prompt engineering, agent development, evaluation frameworks / evals, RAG,
  MCP (Model Context Protocol), AI enablement, AI fluency, self-serve analytics,
  "AI-native," build/prototype AI-enabled workflows, orchestration, playbooks
  & standards.
- **Strategy / ops:** operating cadence / operating rhythm, strategic planning,
  OKRs, cross-functional, GTM strategy & operations, co-sell, channel/partner
  management, business acumen, influence without authority, scalable processes,
  executive/board reporting, incentive/comp program design, quota-setting,
  forecasting.
- **Data:** SQL, Python, Tableau / CRM Analytics, Salesforce reporting,
  dashboards, financial models, revenue attribution, medallion architecture /
  Spark, data storytelling, KPI definition & tracking.

## Quantification punch-list (the ⟪…⟫ placeholders)

The single highest-ROI upgrade. Each placeholder in the resumes maps to a
number that turns a good bullet into a strong one. Even rough, defensible
figures work — anything you'd stand behind in an interview.

| Program | The number that would land it |
|---|---|
| **Forecast process** | What it forecasts (partner-sourced bookings? consumption?) + scale ($ forecasted per Q, or accuracy % / accuracy improvement) + who relies on it |
| **Attribution model** | How widely adopted (company-wide? # teams/dashboards) + $ revenue or pipeline it attributes |
| **New-logo incentive program** | What it rewards + who's enrolled (# PSMs/partners) + impact (# net-new logos, participation, $ influenced) |
| **AI agents (Newsletter/FAQ)** | Reach — # stakeholders served, queries/week, or hours saved |
| **Medallion / self-serve** | # sources or tables, # consumers of the gold layer, request-queue reduction |

## Honesty guardrails (do not cross)

- Every Experience bullet is a rewording of the current resume or of a fact
  Dylan stated directly — no new claims, no invented numbers.
- The repo's scorecard figures ($6.5M sourced, 12 partners, etc.) are
  **synthetic demo data**. They never appear on any resume.
- The Claude Code build is always labeled a public / independent project.
- The Forward Deployed resume stays inside "operator-engineer who deploys" and
  "fluent in Python/SQL" — never "software engineer."

## Known gaps and how the variants compensate

- **No formal engineering title** → the FDE variant leans on the *public repo*
  (link is on the resume) and the evals answer as the "can you really build?"
  proof; it targets Applied-AI adjacents, not true lab FDE.
- **Thin quantification** → the punch-list above is the fix; it's the biggest
  lever available.
- **One LinkedIn for three resumes** → update LinkedIn to the AI-native
  operator blend (the Business Operations lens with AI forward), since all three
  variants link to it.
- **Portfolio URL** → the Replit site should become the broad career showcase
  (next deliverable); when it's live, swap the GitHub link for it on the AI
  variants and keep the repo public as the code-proof.

## Per-application checklist

1. Pick the variant by the decision rule above.
2. Fill or delete every ⟪…⟫ placeholder — none ship.
3. Echo the JD's top three responsibility phrases in the summary (only where
   true).
4. Reorder the Databricks bullets so the first two match what the role screens
   for.
5. Export and submit as `Dylan-Ram-Resume.pdf` — recruiters see filenames;
   don't leak the variant name.
6. Confirm it's still one page.
