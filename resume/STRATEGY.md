# Resume Strategy — one fact base, two lenses, two designs

The play: **maintain one fact base**, render it through **two lenses** and
**two visual designs**. Every bullet traces back to the same source material
(the current resume, the real Databricks work Dylan described, and what's
verifiably in this repo), so nothing drifts into embellishment — the lenses
differ only in what leads and which vocabulary they speak; the designs differ
only in layout.

Content and layout both live in `build_resumes.py`. Regenerate:

```bash
python3 resume/assets/fetch_fonts.py     # once — bundles Inter + Lora as base64
python3 resume/build_resumes.py          # writes resume/output/<stem>--<design>.html
# then print each to PDF:
chromium --headless --no-sandbox --print-to-pdf-no-header \
  --print-to-pdf=resume/output/<name>.pdf file://$PWD/resume/output/<name>.html
```

## Why two, not three

An earlier cut had three lenses — Forward Deployed (builder), AI Strategy
(operator), and Business Operations. But FDE and AI-Strategy shared ~70% of
their content: the same Claude Code project, the same "shipped the first LLM
agents / medallion / KPI alignment / attribution" Databricks bullets, and the
same summary spine. The *target roles* differ (FDE screens for "ship code";
AI-Strategy for "drove adoption"), but Dylan's *evidence base is identical* for
both, so two files just meant maintenance overhead with no real
differentiation. They're now merged into one **AI Deployment** resume that
carries both the builder proof and the strategy/enablement angle.

## The two lenses and the roles they chase

| Lens | Stem | Primary targets | What leads |
|---|---|---|---|
| **AI Deployment** | `dylan-ram-ai-deployment` | Applied AI / AI Solutions Engineer, AI Operations, FDE-adjacent · **and** AI Strategy / Enablement, Head of AI/Automation, "BizOps 2.0" at AI companies | The shipped AI at Databricks + the self-built Claude Code platform (architecture, the tested engine, **evals**, and the enablement pattern) |
| **Business Operations** | `dylan-ram-business-operations` | **Business Operations Lead (primary)**, Chief of Staff, Partner / Revenue / GTM Ops | The signature programs built from scratch (forecast, attribution, first new-logo incentive), the two-sided-marketplace stakeholder story, zero-to-one / one-to-100 — AI as the modern edge |

### The AI Deployment resume flexes two ways

Because it merges the builder and the operator, tune it per JD — a reorder, not
a rewrite:

- **Technical-forward** (Applied AI / AI Solutions / FDE-adjacent): keep Skills
  led by *AI & agents*; keep the project's architecture → boundary → **evals**
  bullets up top. Lead the summary on "operator-engineer… tested code owns the
  outcome… how do you know it's working."
- **Strategy-forward** (AI Strategy / Enablement / Head of AI): move the
  self-serve + enablement bullets up; lead the summary on "sets up how an org
  adopts AI… self-serve enablement." The enablement project bullet does the
  heavy lifting.

### Decision rule

Read the JD's first three responsibilities. "Build / ship / deploy AI, agents,
evals, prototype workflows" → **AI Deployment**. "Operating cadence, planning,
OKRs, cross-functional, own the business, stakeholder alignment" → **Business
Operations**. When unsure, **Business Operations is the default** — it's the
broad operator resume; reach for AI Deployment only when the role is clearly
about AI itself.

### Scenarios — which resume when

| You're looking at… | Send | Design |
|---|---|---|
| "Business Operations Lead / Manager," "Strategy & Ops" | Business Operations | Modern (direct) / Editorial (portal) |
| "Chief of Staff to the CRO/COO/CEO" | Business Operations | Editorial |
| "Partner / Channel Strategy & Ops (Sr Manager, Head)" | Business Operations | either |
| "Revenue / GTM Operations" | Business Operations | either |
| Networking / warm intro / "just send me your resume" | Business Operations | Modern |
| "AI Strategy / AI Enablement Lead," "Head of AI/Automation" | AI Deployment *(strategy-forward)* | Modern |
| "AI Program Manager," BizOps at an AI company | AI Deployment *(strategy-forward)* | Modern |
| "Applied AI / AI Solutions Engineer," "AI Operations" | AI Deployment *(technical-forward)* | Modern |
| "Forward Deployed Engineer" (non-lab / adjacent) | AI Deployment *(technical-forward)* | Modern |

## The two designs

Same content; pick per how the resume will be read.

| Design | File suffix | Look | Use when |
|---|---|---|---|
| **Editorial** | `--editorial` | Single column, Lora serif nameplate, terracotta accents. ATS-safe. | Applying through a job portal / ATS, or when you don't know how it'll be parsed. The safe default. |
| **Modern** | `--modern` | Two-column with a skills rail on a warm panel, uppercase display name. More designed. | Sending straight to a hiring manager, a referral, or alongside the portfolio. |

**The ATS trade-off:** single-column parses cleanly everywhere; two-column
*can* confuse older ATS parsers. Text is real and selectable in both, so most
modern parsers are fine — but if a posting screams "big-company ATS portal,"
send Editorial. Typography (Inter + Lora) is bundled as base64 in
`assets/fonts.css`, so the PDFs render identically anywhere with no network.

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

## What the 2026 market research said

- **BizOps has become "BizOps 2.0"** — JDs expect an operator who can "open
  Claude and just build." Dylan's agent system is exactly that signal, so the
  Business Operations resume keeps AI prominent, not buried.
- **Chief of Staff JDs now include "own the AI agenda."** Only ~7% of senior
  operators read as truly "AI-native"; Dylan clears that bar — his sharpest
  differentiator for CoS/BizOps.
- **Partner S&O is a near-verbatim match** to his current title; the level-up
  keyword is *Senior Manager / Head*.
- **True lab FDE (Anthropic/OpenAI/Palantir) is a reach** — those want "ship
  production applications, 5+ yrs engineering." AI Deployment (technical-
  forward) aims at *Applied AI / AI Solutions / AI Operations* adjacents,
  leaning on the repo + evals as proof. Never claim "software engineer,"
  "production integrations," or "distributed systems."

## On quantification — a deliberate choice

Dylan's call: **no dollar/stakeholder counts on the page.** Bullets lead with
*what the work was and its quality* ("built the team's first forecasting
process," "designed the canonical attribution model," "zero to one … one to
100"); scale is an interview conversation, where it's credible rather than a
number a screener discounts. Add a hard metric inline only for a specific role
that rewards one, and only if it's defensible.

## Honesty guardrails (do not cross)

- Every Experience bullet is a rewording of the current resume or of a fact
  Dylan stated directly — no new claims, no invented numbers.
- The repo's scorecard figures ($6.5M sourced, 12 partners, etc.) are
  **synthetic demo data**. They never appear on any resume.
- The Claude Code build is always labeled a public / independent project.
- AI Deployment stays inside "operator-engineer who deploys" and "fluent in
  Python/SQL" — never "software engineer."

## Per-application checklist

1. Pick the lens by the decision rule; for AI Deployment, pick technical- or
   strategy-forward and reorder.
2. Pick the design by how it'll be read.
3. Echo the JD's top three responsibility phrases in the summary (only where
   true).
4. Reorder the Databricks bullets so the first two match what the role screens
   for.
5. Export and submit as `Dylan-Ram-Resume.pdf` — recruiters see filenames.
6. Confirm it's still one page.
