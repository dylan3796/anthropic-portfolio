#!/usr/bin/env python3
"""Render Dylan Ram's targeted resume variants to print-ready HTML.

One fact base, three lenses. All content lives in VARIANTS below —
edit the dicts, rerun, reprint. Every claim traces to the source
resume or to work that exists in this repo; see resume/STRATEGY.md
for the honesty guardrails and the variant-to-job mapping.

    python3 resume/build_resumes.py            # writes resume/output/*.html
    # then print to PDF (chromium shown; any browser's Print works):
    #   chromium --headless --no-sandbox --print-to-pdf-no-header \
    #     --print-to-pdf=out.pdf file:///.../resume/output/<file>.html
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

# ---------------------------------------------------------------------------
# The three variants. Same jobs, same facts — different lead, order, and
# vocabulary. Bullets are reworded for the lens but never inflated.
# ---------------------------------------------------------------------------

VARIANTS = {
    "dylan-ram-ai-operations": {
        "tagline": "AI Operations · GTM Systems · Agent Deployment",
        "summary": (
            "Operations leader who deploys AI inside real business workflows — and knows "
            "where it doesn't belong. As Databricks' first Partner Strategy &amp; Ops hire, "
            "built the partner data foundation, then put LLM reporting agents into "
            "production on top of it. Independently designed and shipped a full agent "
            "operating system (Claude Code) for a partner-ops function: session-boot "
            "context hooks, invocable skills, and a golden-tested boundary that keeps "
            "models out of the money path."
        ),
        "skills": [
            ("AI systems", "Claude Code (skills, hooks, subagents, scoped permissions), "
             "LLM workflow design, agent evals &amp; golden-test patterns"),
            ("Data", "Python (pandas, NumPy), PySpark, SQL, Salesforce &amp; Einstein "
             "Analytics, Tableau, Excel/GSheets"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Deployed AI reporting agents (Newsletter Agent, FAQ Agent) for automated "
                    "Q&amp;A, insights, and notifications — integrating LLM workflows into how "
                    "partner metrics are distributed across the org.",
                    "Built the standardized partner datasets those agents run on — adopted "
                    "company-wide and powering 10+ executive and team dashboards.",
                    "Scaled partner attribution systems in Salesforce, SQL, and Spark to track "
                    "bookings, consumption, and pipeline across a two-sided marketplace.",
                    "Designed the Partner Executive and Partner Scorecard dashboards — the "
                    "single source of truth for Partner Sales and ecosystem health.",
                    "Shaped the Partner Value Score and partner tiering framework, earning "
                    "global alignment and executive adoption.",
                    "Led the annual quota-setting process, aligning Sales, Finance, and Partner "
                    "leadership through top-down and bottoms-up planning.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Automated reporting and forecasting tooling with Python, APIs, and G Suite "
                    "— QBR decks, forecast-accuracy tracking, and account/territory data pulls.",
                    "Developed the territory-carving Python script that encoded the org's sales "
                    "guiding principles, personnel, and accounts — the basis of the GTM plan.",
                    "Led the business unit's Tableau migration through enablement and data "
                    "governance; direct analytics partner to the $250M AMER SMB Central business.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Managed the product data warehouse; built Python web-scraping tools and "
                    "client-facing Tableau dashboards.",
                    "Spearheaded streamlining of the product analytics process — defining key "
                    "metrics, the dataset, and the flow to visualization.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — agentic infrastructure "
                         "for partner ops (public build, 2026)",
        "project_bullets": [
            "Designed a five-layer agent operating system: persistent memory, SessionStart "
            "hooks that boot every session with live plan and scorecard context, long-horizon "
            "plans, invocable skills, and a retro loop that proposes edits to its own setup.",
            "Drew the AI/deterministic boundary for commissions crediting: an agent codifies "
            "managers' plain-English coverage changes into effective-dated rules; a "
            "golden-tested Python engine applies them to deals — no LLM ever computes a "
            "credited dollar.",
            "Shipped scoped domain skills (/commissions-credit, /partner-qbr, "
            "/call-notes-to-jira), a plan-drafting subagent, least-privilege permissions, and "
            "a Streamlit walkthrough of the architecture.",
        ],
    },

    "dylan-ram-strategy-ops": {
        "tagline": "Strategy & Operations · GTM Planning · Partner Ecosystems",
        "summary": (
            "Strategy &amp; operations leader with seven years as a direct business partner "
            "to GTM executives at Databricks, Salesforce, and CBRE. First Partner Strategy "
            "&amp; Ops hire at Databricks: ran annual planning and quota-setting across "
            "Sales, Finance, and Partner leadership, shaped the tiering framework the global "
            "partner program runs on, and built the data foundation under all of it — then "
            "multiplied the team's capacity with AI reporting agents."
        ),
        "skills": [
            ("Planning & ops", "Annual planning, quota setting, territory design, partner "
             "programs &amp; tiering, executive reporting, QBRs"),
            ("Technical", "SQL, Python (pandas), PySpark, Salesforce, Tableau, "
             "Claude Code / LLM workflows"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Led the annual quota-setting process, aligning Sales, Finance, and Partner "
                    "leadership through top-down and bottoms-up planning.",
                    "Shaped the Partner Value Score and partner tiering framework, earning "
                    "global alignment and executive adoption.",
                    "Designed the Partner Executive and Partner Scorecard dashboards — the "
                    "single source of truth executives use to run Partner Sales and ecosystem "
                    "health.",
                    "Built standardized partner datasets adopted company-wide (powering 10+ "
                    "executive and team dashboards) and scaled the attribution systems tracking "
                    "bookings, consumption, and pipeline across a two-sided marketplace.",
                    "Deployed AI reporting agents (Newsletter Agent, FAQ Agent) for automated "
                    "Q&amp;A, insights, and notifications, integrating LLM workflows into "
                    "metric distribution.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Acted as direct business partner to the $250M AMER SMB Central business, "
                    "providing guidance to AVPs, VPs, and RMs across the org.",
                    "Crafted the FY22 GTM guiding-principles analyses — customer continuity, "
                    "account proximity, industry mix, top accounts, top cities, AE tenure.",
                    "Developed the territory-carving Python script that encoded sales guiding "
                    "principles, personnel, and accounts — the basis of the GTM plan.",
                    "Automated QBR decks, forecast-accuracy tracking, and territory reporting "
                    "with Python and APIs; led the unit's Tableau migration with enablement and "
                    "data governance.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Owned the product analytics stack end to end — data warehouse management, "
                    "Python data collection, and client-facing Tableau dashboards.",
                    "Spearheaded streamlining of the product analytics process — defining key "
                    "metrics, the dataset, and the flow to visualization.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — public reference build "
                         "for a partner-ops team (2026)",
        "project_bullets": [
            "Built a working demonstration of running Claude Code as a team operating "
            "system: persistent memory, live-data session hooks, long-horizon plans tied to "
            "strategic initiatives, invocable skills, and a self-improvement loop.",
            "Headline workflow: commissions crediting where an agent codifies managers' "
            "plain-English coverage changes into effective-dated rules — and tested code, "
            "never a model, computes the money.",
        ],
    },

    "dylan-ram-data-analytics": {
        "tagline": "GTM Data & Analytics · Revenue Analytics · AI-Augmented Reporting",
        "summary": (
            "Analytics leader who builds the data layer GTM organizations run on — "
            "attribution systems, governed company-wide datasets, and the executive "
            "reporting on top — then automates distribution with LLM agents. Seven years "
            "across Databricks, Salesforce, and CBRE spanning Spark and SQL pipelines, "
            "Tableau at scale, Salesforce analytics, and deployed AI reporting."
        ),
        "skills": [
            ("Analytics", "SQL (window functions, subqueries), Python (pandas, NumPy), "
             "PySpark, Tableau (LODs, Set Actions, Prep), Salesforce &amp; Einstein "
             "Analytics, Excel/GSheets"),
            ("Governance & AI", "Metric dictionaries, standardized datasets, golden tests, "
             "LLM workflow integration, Claude Code"),
        ],
        "jobs": [
            {
                "company": "Databricks",
                "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire",
                "dates": "Aug 2021 – Present",
                "bullets": [
                    "Scaled partner attribution systems in Salesforce, SQL, and Spark to track "
                    "bookings, consumption, and pipeline across a two-sided marketplace.",
                    "Built standardized partner datasets adopted company-wide, powering 10+ "
                    "executive and team dashboards.",
                    "Designed the Partner Executive and Partner Scorecard dashboards — the "
                    "single source of truth for Partner Sales and ecosystem health.",
                    "Shaped the Partner Value Score — the composite metric behind the global "
                    "partner tiering framework — earning executive adoption worldwide.",
                    "Deployed AI reporting agents (Newsletter Agent, FAQ Agent) for automated "
                    "Q&amp;A, insights, and notifications — integrating LLM workflows into "
                    "metric distribution.",
                    "Led the annual quota-setting process, aligning Sales, Finance, and Partner "
                    "leadership through top-down and bottoms-up planning.",
                ],
            },
            {
                "company": "Salesforce",
                "role": "SMB Sales Strategy & Operations Analyst",
                "note": "",
                "dates": "Jul 2019 – Aug 2021",
                "bullets": [
                    "Automated reporting and forecasting tools using Python, APIs, and G Suite "
                    "— QBR decks, forecast accuracy, account/territory-specific data.",
                    "Led the business unit's Tableau migration through enablement and "
                    "establishing data governance; maintained and improved its dashboard estate.",
                    "Developed a territory-carving Python script incorporating sales guiding "
                    "principles, personnel, and accounts — the basis of the GTM plan.",
                    "Crafted FY22 GTM analyses for the $250M AMER SMB Central business: "
                    "customer continuity, account proximity, industry mix, top accounts, AE "
                    "tenure.",
                ],
            },
            {
                "company": "CBRE",
                "role": "Business Data Analyst",
                "note": "",
                "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Managed the product data warehouse with quarterly SQL updates; built "
                    "Python web-scraping tools for component data collection.",
                    "Partnered with clients on durable Tableau dashboards; spearheaded "
                    "streamlining of product analytics — key metric definitions, dataset "
                    "design, and the flow to visualization.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — public reference build "
                         "for a partner-ops team (2026)",
        "project_bullets": [
            "Built a governed analytics core for an agentic setup: one metric dictionary as "
            "single source of truth, session hooks injecting live scorecard data, and agent "
            "skills that read definitions instead of re-deriving them.",
            "Wrote a deterministic commissions-crediting engine with golden tests "
            "(mid-quarter hires, territory handoffs, split credit, coverage gaps); the LLM "
            "only authors rules — tested code computes every credited dollar.",
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
