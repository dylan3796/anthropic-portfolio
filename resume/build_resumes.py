#!/usr/bin/env python3
"""Render Dylan Ram's targeted resume variants to print-ready HTML.

One fact base, three lenses. All content lives in VARIANTS below —
edit the dicts, rerun, reprint. Every claim traces to the source
resume or to work that exists in this repo; see resume/STRATEGY.md
for the honesty guardrails, the variant-to-archetype mapping, and the
quantification punch-list.

    python3 resume/build_resumes.py            # writes resume/output/*.html
    # then print to PDF (chromium shown; any browser's Print works):
    #   chromium --headless --no-sandbox --print-to-pdf-no-header \
    #     --print-to-pdf=out.pdf file:///.../resume/output/<file>.html

Tokens wrapped in <span class="todo">⟪ … ⟫</span> are review placeholders —
Dylan's real numbers go there. They render in accent italic so they're
impossible to miss, and MUST be filled or deleted before a resume is sent.
"""

from pathlib import Path

OUT_DIR = Path(__file__).parent / "output"

NAME = "DYLAN RAM"
CONTACT = [
    "916-690-5681",
    "dylanmr96@gmail.com",
    "linkedin.com/in/dylanram",
    "github.com/dylan3796/anthropic-portfolio",
]

EDUCATION = (
    "<strong>University of California, Santa Barbara</strong> — "
    "B.A. Economics &amp; Accounting · Dean's Honors"
)


def todo(hint: str) -> str:
    """A visible fill-me placeholder for a metric Dylan will supply."""
    return f'<span class="todo">⟪{hint}⟫</span>'


# ---------------------------------------------------------------------------
# The three variants. Same jobs, same facts — different lead, order, and
# vocabulary, calibrated to the keyword banks in STRATEGY.md. Bullets are
# reworded per lens but never inflated.
# ---------------------------------------------------------------------------

VARIANTS = {
    # =====================================================================
    # 1 · FORWARD DEPLOYED / APPLIED AI  — the builder pole
    #     Targets: Applied AI, AI Solutions Engineer, AI Operations,
    #     adjacent-FDE. Project is the centerpiece; evals are the hook.
    # =====================================================================
    "dylan-ram-ai-forward-deployed": {
        "tagline": "Forward Deployed &amp; Applied AI · Agent Systems · Evals &amp; Deployment",
        "summary": (
            "Operator-engineer who deploys LLM and agent systems into real business "
            "workflows — and draws the hard line on where deterministic, tested code must "
            "own the outcome. At Databricks, shipped the partner team's first LLM agents to "
            "production. Independently designed a full agent operating system in Claude Code — "
            "skills, hooks, subagents, MCP, and a golden-tested engine that keeps the model "
            "out of the money path. Fluent in Python and SQL, comfortable owning a deployment "
            "end to end and answering the question that matters: how do you know it's working."
        ),
        "skills": [
            ("Agents &amp; LLMs", "Claude Code (skills, hooks, subagents, MCP, scoped "
             "permissions), agent &amp; LLM workflow design, prompt engineering, evals &amp; "
             "golden-test patterns"),
            ("Languages &amp; data", "Python (pandas, NumPy), SQL, PySpark, Salesforce "
             "APIs, Tableau, Git/GitHub"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Deployed the partner team's first LLM reporting agents (Newsletter Agent, "
                    "FAQ Agent) into production — automated Q&amp;A, insights, and "
                    "notifications, embedding agentic workflows into how partner metrics reach "
                    f"the org, now serving {todo('N stakeholders / queries per week')}.",
                    "Building the team's foundational data-and-AI layer: a medallion "
                    "(bronze/silver/gold) architecture in Spark/SQL and self-serve interfaces "
                    "so stakeholders query answers directly instead of filing requests.",
                    "Aligning KPIs across internal, external, and partner stakeholders as the "
                    "measurement backbone the AI layer reports against.",
                    "Designed the partner attribution model and built the attribution systems "
                    "in Salesforce, SQL, and Spark — sourced, influenced, and attributed "
                    "revenue across a two-sided marketplace; the governed data the agents run on.",
                    "Stood up the team's first revenue forecasting process where none existed — "
                    f"{todo('what it forecasts + scale')}.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Built the territory-carving Python script that encoded the org's guiding "
                    "principles, personnel, and accounts — the engine behind the annual GTM plan.",
                    "Automated QBR decks, forecast-accuracy tracking, and territory data pulls "
                    "with Python, APIs, and G Suite.",
                    "Led the business unit's Tableau migration and established data governance "
                    "for the $250M AMER SMB Central business.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Built Python web-scraping tools and managed the product data warehouse; "
                    "shipped client-facing Tableau dashboards and streamlined the analytics "
                    "pipeline end to end.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — a self-built agent platform "
                         "(public repo, 2026)",
        "project_bullets": [
            "Architected a five-layer agent system: persistent memory, SessionStart hooks "
            "that boot each session with live data, long-horizon plans, invocable skills, and "
            "a retro loop that proposes edits to its own setup.",
            "Drew the AI/deterministic boundary for commissions crediting: an agent turns "
            "managers' plain-English coverage into effective-dated rules; a golden-tested "
            "Python engine (crediting/engine.py) applies them to deals — no LLM ever computes "
            "a credited dollar.",
            "Wrote the eval suite that proves it: golden tests over mid-quarter hires, "
            "territory handoffs at the boundary, split credit, and coverage gaps — an "
            "uncredited deal is surfaced, never silently zeroed.",
            "Shipped scoped skills, a plan-drafting subagent, least-privilege permissions, and "
            "MCP integrations; documented the architecture in a Streamlit walkthrough.",
        ],
    },

    # =====================================================================
    # 2 · AI STRATEGY & DEPLOYMENT  — the AI-native operator pole
    #     Targets: AI Strategy, AI Enablement, AI Operations (non-eng),
    #     Head of Automation, BizOps-2.0 at AI companies.
    # =====================================================================
    "dylan-ram-ai-strategy": {
        "tagline": "AI Strategy &amp; Deployment · Enablement · Agentic Operating Systems",
        "summary": (
            "Sets up how an organization actually deploys AI — from the foundational data "
            "layer to KPI alignment to the self-serve enablement that gets non-technical "
            "teams building. At Databricks, spearheading the partner team's AI strategy on "
            "top of a data foundation built from scratch, and shipped its first LLM agents to "
            "production. Independently designed a full agent operating system in Claude Code — "
            "skills, hooks, subagents, MCP, and a tested boundary between AI judgment and "
            "deterministic execution: built-and-deployed AI work, not slideware."
        ),
        "skills": [
            ("AI deployment &amp; enablement", "Agent operating systems (Claude Code, "
             "CLAUDE.md, MCP), LLM workflow design, prompt engineering, evals, self-serve "
             "enablement, playbooks &amp; standards"),
            ("Data &amp; ops", "SQL, Python (pandas), PySpark, Tableau, Salesforce, medallion "
             "architecture, KPI definition, executive reporting"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Spearheading the partner team's AI strategy — building the foundational "
                    "data-and-AI layer (a medallion architecture) and aligning KPIs across "
                    "internal, external, and partner stakeholders as the backbone every AI "
                    "output measures against.",
                    "Building self-serve analytics spaces so the team and its stakeholders "
                    "answer their own questions — turning a standing request queue into direct "
                    "access.",
                    "Deployed the team's first LLM agents (Newsletter, FAQ) into production for "
                    f"automated Q&amp;A, insights, and notifications, reaching {todo('N stakeholders')}.",
                    "Designed the partner attribution model and the first revenue forecasting "
                    "process — the governed data the AI layer depends on.",
                    "Shaped the Partner Value Score and tiering framework adopted globally.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Automated reporting and forecasting tooling with Python, APIs, and G Suite "
                    "— QBR decks, forecast accuracy, and territory data.",
                    "Developed the territory-carving Python model behind the annual GTM plan; "
                    "led the unit's Tableau migration with data governance.",
                    "Direct analytics partner to the $250M AMER SMB Central business.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Managed the product data warehouse and built Python data-collection tools.",
                    "Built client-facing Tableau dashboards; streamlined the product-analytics "
                    "process end to end.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — a reference build for "
                         "deploying AI in a function (public repo, 2026)",
        "project_bullets": [
            "Designed a five-layer operating model for running AI in a team: governed data "
            "and a single metric dictionary, memory, long-horizon plans, invocable skills, and "
            "a self-improvement loop — define once, reuse everywhere.",
            "Set the boundary that makes AI trustworthy in production: the model authors rules "
            "in plain English; deterministic, tested code executes anything that touches money "
            "— the speed of language with the trust of a spreadsheet that can't miscount.",
            "Built the enablement pattern: the ops team self-served first, then began "
            "authoring their own skills — reusable playbooks and standards, the adoption "
            "unlock these roles are hired to drive.",
        ],
    },

    # =====================================================================
    # 3 · BUSINESS OPERATIONS / STRATEGY  — the operating-leader pole
    #     Primary: Business Operations Lead. Also serves Chief of Staff
    #     and Partner S&O. Signature programs lead; AI is the modern edge.
    # =====================================================================
    "dylan-ram-business-operations": {
        "tagline": "Business Operations · Strategy &amp; Planning · GTM Systems",
        "summary": (
            "The operating spine of a GTM org. As Databricks' first Partner Strategy &amp; Ops "
            "hire, built the forecast, attribution, and first new-logo incentive programs from "
            "scratch, ran annual quota-setting across Sales, Finance, and Partner leadership, "
            "and now sets the AI strategy that makes the team faster. Architects the high-level "
            "plan, operationalizes it, and dives into the detail — seven years partnering "
            "directly with GTM executives at Databricks, Salesforce, and CBRE."
        ),
        "skills": [
            ("Operations &amp; strategy", "Operating cadence, annual &amp; quota planning, "
             "OKRs, territory design, incentive/comp program design, revenue forecasting, "
             "executive &amp; board reporting"),
            ("Data &amp; AI", "SQL, Python (pandas), PySpark, Tableau, Salesforce, revenue "
             "attribution, deployed AI agents, AI enablement (Claude Code)"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Built the partner team's first revenue forecasting process where none "
                    f"existed — {todo('what it forecasts + scale, e.g. $XXXM quarterly partner-sourced')}.",
                    "Designed the canonical partner attribution model — "
                    f"{todo('adoption, e.g. company-wide source of truth across N teams')} — "
                    "defining sourced, influenced, and attributed revenue across a two-sided "
                    "marketplace.",
                    "Launched the first partner incentive program tied to new-logo acquisition — "
                    f"{todo('what it rewards + impact, e.g. drove N net-new logos')}.",
                    "Led annual quota-setting across Sales, Finance, and Partner leadership "
                    "through top-down and bottoms-up planning.",
                    "Shaped the Partner Value Score and tiering framework, earning global "
                    "alignment and executive adoption.",
                    "Now spearheading KPI alignment across internal, external, and partner "
                    "stakeholders and building self-serve, AI-driven analytics — the operating "
                    "cadence's modern layer.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Direct business partner to the $250M AMER SMB Central business, advising "
                    "AVPs, VPs, and RMs across the org.",
                    "Built the territory-carving model (Python) that encoded the org's guiding "
                    "principles — the basis of the annual GTM plan.",
                    "Crafted the FY22 GTM guiding-principles analyses: customer continuity, "
                    "account proximity, industry mix, top accounts, AE tenure.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Owned the product-analytics stack end to end — data warehouse, Python "
                    "data collection, and client-facing Tableau dashboards.",
                    "Streamlined the product-analytics process: defined key metrics, the "
                    "dataset, and the flow to visualization.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — running an AI-native operating "
                         "cadence (public repo, 2026)",
        "project_bullets": [
            "Built a working operating system for a function: big rocks as the planning "
            "pillars, skills as the repeatable plays, a metric dictionary as governance, and a "
            "retro loop that runs the QBR on the tooling itself.",
            "Headline workflow — commissions crediting: an agent codifies managers' "
            "plain-English coverage changes into effective-dated rules, and tested code, never "
            "a model, computes the money.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Template — single column, standard headings, letter-size, one page.
# Deliberately ATS-safe: no sidebars, no tables for layout, no graphics.
# ---------------------------------------------------------------------------

CSS = """
    @page { size: letter; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { background: white; }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1a1a1a; font-size: 9.3pt; line-height: 1.33;
        -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }
    .page { width: 8.5in; padding: 0.4in 0.62in; margin: 0 auto; }
    .name { font-size: 21pt; font-weight: 700; letter-spacing: 0.14em; }
    .tagline { font-size: 10pt; color: #b5543b; font-weight: 600; margin-top: 2pt; }
    .contact { font-size: 8.6pt; color: #555; margin-top: 4pt; }
    .contact span + span::before { content: "  ·  "; color: #bbb; }
    h2 {
        font-size: 8.6pt; font-weight: 700; letter-spacing: 0.13em;
        text-transform: uppercase; color: #b5543b;
        border-bottom: 1px solid #e3ddd8; padding-bottom: 2pt;
        margin: 9pt 0 4.5pt 0;
    }
    .summary { color: #333; }
    .skill-line { margin-bottom: 2.5pt; }
    .skill-line strong { color: #1a1a1a; }
    .job { margin-bottom: 7pt; }
    .job-head { display: flex; justify-content: space-between; align-items: baseline; }
    .job-role { font-weight: 700; font-size: 9.8pt; }
    .job-co { color: #b5543b; font-weight: 600; }
    .job-note { color: #777; font-style: italic; font-weight: 400; font-size: 8.8pt; }
    .job-dates { color: #555; font-size: 8.8pt; white-space: nowrap; }
    ul { margin: 2.5pt 0 0 0; padding-left: 13pt; }
    li { margin-bottom: 1.5pt; color: #333; }
    .proj-title { font-weight: 700; font-size: 9.6pt; }
    .proj-title .proj-link { color: #777; font-weight: 400; font-size: 8.6pt; }
    .edu { color: #333; }
    .todo {
        color: #b5543b; font-style: italic; font-weight: 600;
        border-bottom: 1px dotted #d9a08c;
    }
"""


def render(variant: dict) -> str:
    contact = "".join(f"<span>{c}</span>" for c in CONTACT)
    skills = "".join(
        f'<div class="skill-line"><strong>{label}:</strong> {body}</div>'
        for label, body in variant["skills"]
    )
    jobs = []
    for job in variant["jobs"]:
        note = f' <span class="job-note">({job["note"]})</span>' if job["note"] else ""
        bullets = "".join(f"<li>{b}</li>" for b in job["bullets"])
        jobs.append(
            f'<div class="job"><div class="job-head">'
            f'<div class="job-role">{job["role"]} — '
            f'<span class="job-co">{job["company"]}</span>{note}</div>'
            f'<div class="job-dates">{job["dates"]}</div></div>'
            f"<ul>{bullets}</ul></div>"
        )
    proj_bullets = "".join(f"<li>{b}</li>" for b in variant["project_bullets"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{NAME} — Resume</title>
<style>{CSS}</style></head><body><div class="page">
<div class="name">{NAME}</div>
<div class="tagline">{variant["tagline"]}</div>
<div class="contact">{contact}</div>
<h2>Summary</h2>
<div class="summary">{variant["summary"]}</div>
<h2>Skills</h2>
{skills}
<h2>Experience</h2>
{"".join(jobs)}
<h2>Selected Project</h2>
<div class="job">
<div class="proj-title">{variant["project_title"]}
 <span class="proj-link">— github.com/dylan3796/anthropic-portfolio</span></div>
<ul>{proj_bullets}</ul>
</div>
<h2>Education</h2>
<div class="edu">{EDUCATION}</div>
</div></body></html>"""


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    for stem, variant in VARIANTS.items():
        path = OUT_DIR / f"{stem}.html"
        path.write_text(render(variant))
        print(f"wrote {path}")
