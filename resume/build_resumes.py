#!/usr/bin/env python3
"""Render Dylan Ram's targeted resumes to print-ready HTML in two designs.

One fact base, two lenses, two layouts. Content lives in VARIANTS; the look
lives in the two CSS blocks + render fns. Every claim traces to the source
resume or to work in this repo — see resume/STRATEGY.md.

    python3 resume/assets/fetch_fonts.py     # once — bundles the fonts
    python3 resume/build_resumes.py          # writes resume/output/*.html

    # print to PDF (chromium shown; any browser's Print works):
    #   chromium --headless --no-sandbox --print-to-pdf-no-header \
    #     --print-to-pdf=out.pdf file:///.../resume/output/<file>.html

The two lenses
--------------
- ai-deployment      : the AI person — builds/ships AI AND sets the strategy
                       for deploying it. Flexes technical-forward (lead with
                       the engine + evals) or strategy-forward (lead with
                       self-serve + enablement) by reordering bullets.
- business-operations: the operating leader — signature programs, planning,
                       the two-sided-marketplace stakeholder story, zero-to-one
                       / one-to-100, with AI as the modern edge.

Design notes
------------
- Typography: Lora (editorial serif) for display, Inter for everything else,
  bundled as base64 in assets/fonts.css so PDFs are fully self-contained.
- Palette: warm near-black ink, terracotta accent — the same family as the
  portfolio, so the resume and the site read as one system.
- Two layouts: editorial (single column, ATS-safe) and modern (two-column
  with a skills rail; more designed, slight ATS risk — see STRATEGY.md).
- No fabricated metrics. Bullets lead with what the work was and its quality.
"""

from pathlib import Path

HERE = Path(__file__).parent
OUT_DIR = HERE / "output"
FONTS = (HERE / "assets" / "fonts.css").read_text()

NAME = "Dylan Ram"
CONTACT = [
    "dylanmr96@gmail.com",
    "916-690-5681",
    "linkedin.com/in/dylanram",
    "github.com/dylan3796/anthropic-portfolio",
]
EDUCATION_SCHOOL = "University of California, Santa Barbara"
EDUCATION_DEGREE = "B.A. Economics &amp; Accounting · Dean's Honors"

# ---------------------------------------------------------------------------
# The two variants. Same jobs, same facts — different lead, order, and
# vocabulary. Substance over scale; no invented numbers.
# ---------------------------------------------------------------------------

VARIANTS = {
    # 1 · AI DEPLOYMENT — merges the builder (Applied AI / FDE-adjacent) and
    #     the AI-native operator (AI Strategy / Enablement). Reorder to lean
    #     technical (skills+project first) or strategic (self-serve+enablement).
    "dylan-ram-ai-deployment": {
        "tagline": "AI Deployment · Agent Systems · Strategy & Enablement",
        "summary": (
            "Deploys AI into the workflows a go-to-market org runs on — reporting, "
            "forecasting, crediting — and sets up how the org adopts it: foundational data, "
            "KPI alignment, and self-serve enablement. An operator who builds the systems "
            "himself and draws the line where deterministic, tested code must own the outcome. "
            "As Databricks' first Partner Strategy & Ops hire, shipped the team's first LLM "
            "agents to production and independently built a full agent operating system in "
            "Claude Code — skills, hooks, subagents, MCP, and a golden-tested engine that keeps "
            "the model out of the money path. Fluent in Python and SQL, and builds with the "
            "evals that answer the only question that matters: how do you know it's working."
        ),
        "skills": [
            ("AI & agents", "Claude Code (skills, hooks, subagents, MCP, scoped permissions), "
             "agent & LLM workflow design, prompt engineering, evals & golden-test patterns, "
             "self-serve enablement, playbooks & standards"),
            ("Data & engineering", "Python (pandas, NumPy), SQL, PySpark, Tableau, Salesforce, "
             "medallion architecture, KPI definition, Git/GitHub"),
        ],
        "jobs": [
            {
                "company": "Databricks", "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire", "dates": "Aug 2021 – Present",
                "bullets": [
                    "Deployed the partner team's first LLM reporting agents (Newsletter Agent, "
                    "FAQ Agent) into production — answering partner-metric questions and "
                    "pushing updates automatically, the team's first agentic reporting motion.",
                    "Set the team's AI strategy and built the foundational data-and-AI layer — "
                    "a medallion architecture in Spark/SQL with self-serve interfaces so "
                    "stakeholders answer their own questions.",
                    "Align KPIs across a two-sided marketplace — the partner team, the sales "
                    "org co-selling through partners, and the partners themselves — the "
                    "measurement backbone every AI output reports against.",
                    "Designed the partner attribution model (Salesforce/SQL/Spark) and built "
                    "the team's first revenue forecasting process from scratch — the governed "
                    "data the agents run on.",
                ],
            },
            {
                "company": "Salesforce", "role": "SMB Sales Strategy & Operations Analyst",
                "note": "", "dates": "Jul 2019 – Aug 2021",
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
                "company": "CBRE", "role": "Business Data Analyst",
                "note": "", "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Built Python web-scraping tools and managed the product data warehouse; "
                    "shipped client-facing Tableau dashboards and streamlined the analytics "
                    "pipeline end to end.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — a self-built agent platform "
                         "(public repo)",
        "project_bullets": [
            "Architected a five-layer agent operating system: persistent memory, session-boot "
            "data hooks, long-horizon plans, invocable skills, and a retro loop that proposes "
            "edits to its own setup.",
            "Drew the AI/deterministic boundary for commissions crediting: an agent turns "
            "managers' plain-English coverage into effective-dated rules; a golden-tested "
            "Python engine applies them to deals — no LLM ever computes a credited dollar.",
            "Wrote the eval suite that proves it: golden tests over mid-quarter hires, "
            "territory handoffs, split credit, and coverage gaps — an uncredited deal is "
            "surfaced, never silently zeroed.",
            "Built the enablement pattern: the ops team self-served first, then began "
            "authoring their own skills — reusable playbooks and standards, the adoption "
            "unlock these roles are hired to drive.",
        ],
    },

    # 2 · BUSINESS OPERATIONS / STRATEGY — the operating-leader pole
    "dylan-ram-business-operations": {
        "tagline": "Business Operations · Strategy & Planning · GTM Systems",
        "summary": (
            "The operating spine of a GTM org — a zero-to-one builder and one-to-100 scaler. "
            "As Databricks' first Partner Strategy & Ops hire, stood up the forecast, "
            "attribution, and first new-logo incentive programs from scratch, ran annual "
            "quota-setting across Sales, Finance, and Partner leadership, and now owns the "
            "team's AI agenda — deployed its first LLM agents to production and built, in "
            "public, a working agent operating system for a function like his. Works across a "
            "two-sided marketplace — aligning the partner team, the sales org that co-sells "
            "through partners, and the partners themselves. Seven years partnering directly "
            "with GTM executives at Databricks, Salesforce, and CBRE."
        ),
        "skills": [
            ("Operations & strategy", "Operating cadence, annual & quota planning, OKRs, "
             "territory design, incentive/comp program design, revenue forecasting, "
             "executive & board reporting"),
            ("Data & AI", "SQL, Python (pandas), PySpark, Tableau, Salesforce, revenue "
             "attribution, deployed AI agents, AI enablement (Claude Code)"),
        ],
        "jobs": [
            {
                "company": "Databricks", "role": "Partner Strategy & Ops Manager",
                "note": "promoted Feb 2023 · first Partner S&O hire", "dates": "Aug 2021 – Present",
                "bullets": [
                    "Built the partner team's first revenue forecasting process from a blank "
                    "page — the methodology and cadence, designed end to end.",
                    "Designed the canonical partner attribution model — the single source of "
                    "truth for how sourced, influenced, and attributed revenue is credited "
                    "across both sides of the marketplace.",
                    "Launched the partner org's first incentive program tied to new-logo "
                    "acquisition — designing the crediting and payout logic end to end.",
                    "Led annual quota-setting across Sales, Finance, and Partner leadership "
                    "through top-down and bottoms-up planning.",
                    "Shaped the partner program strategy — the Partner Value Score and tiering "
                    "framework — earning global alignment and executive adoption.",
                    "Run KPI alignment across the marketplace — partner team, co-sell sales "
                    "org, and partners — and build the self-serve, AI-driven analytics on top.",
                ],
            },
            {
                "company": "Salesforce", "role": "SMB Sales Strategy & Operations Analyst",
                "note": "", "dates": "Jul 2019 – Aug 2021",
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
                "company": "CBRE", "role": "Business Data Analyst",
                "note": "", "dates": "Sep 2018 – Jul 2019",
                "bullets": [
                    "Owned the product-analytics stack end to end — data warehouse, Python "
                    "data collection, and client-facing Tableau dashboards.",
                    "Streamlined the product-analytics process: defined key metrics, the "
                    "dataset, and the flow to visualization.",
                ],
            },
        ],
        "project_title": "Claude Code as an Operating System — running an AI-native operating "
                         "cadence (public repo)",
        "project_bullets": [
            "Built a working operating system for a function: big rocks as the planning "
            "pillars, skills as the repeatable plays, a metric dictionary as governance, and "
            "a retro loop that runs the QBR on the tooling itself.",
            "Headline workflow — commissions crediting: an agent codifies managers' "
            "plain-English coverage changes into effective-dated rules, and tested code, never "
            "a model, computes the money.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Shared bits
# ---------------------------------------------------------------------------

RESET = """
    @page { size: letter; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { background: #ffffff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
"""


def _skill_lines(variant, label_cls, body_cls):
    return "".join(
        f'<div class="skill-line"><span class="{label_cls}">{label}</span>'
        f'<span class="{body_cls}">{body}</span></div>'
        for label, body in variant["skills"]
    )


def _jobs(variant):
    out = []
    for job in variant["jobs"]:
        note = f' <span class="job-note">{job["note"]}</span>' if job["note"] else ""
        bullets = "".join(f"<li>{b}</li>" for b in job["bullets"])
        out.append(
            f'<div class="job"><div class="job-head">'
            f'<div class="job-role">{job["role"]} &nbsp;·&nbsp; '
            f'<span class="job-co">{job["company"]}</span>{note}</div>'
            f'<div class="job-dates">{job["dates"]}</div></div>'
            f'<ul>{bullets}</ul></div>'
        )
    return "".join(out)


def _project(variant):
    pb = "".join(f"<li>{b}</li>" for b in variant["project_bullets"])
    return (
        f'<div class="job"><div class="proj-title">{variant["project_title"]}'
        f' <span class="proj-link">— github.com/dylan3796/anthropic-portfolio</span></div>'
        f'<ul>{pb}</ul></div>'
    )


def _doc(css, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{NAME} — Resume</title><style>{FONTS}{RESET}{css}</style></head>'
            f'<body>{body}</body></html>')


# ---------------------------------------------------------------------------
# Layout A — EDITORIAL (single column, ATS-safe)
# ---------------------------------------------------------------------------

EDITORIAL_CSS = """
    body { font-family: 'Inter', system-ui, sans-serif; font-size: 9.2pt;
           line-height: 1.33; color: #33302e; }
    .page { width: 8.5in; padding: 0.4in 0.6in; }
    .name { font-family: 'Lora', Georgia, serif; font-size: 22pt; font-weight: 600;
            color: #1c1a19; line-height: 1; letter-spacing: 0.005em; }
    .tagline { font-size: 9.8pt; font-weight: 600; color: #B4552F; margin-top: 4pt;
               letter-spacing: 0.01em; }
    .contact { font-size: 8.5pt; color: #6b6560; margin-top: 4pt; }
    .contact span + span::before { content: "   ·   "; color: #cbc4bd; }
    h2 { font-size: 7.9pt; font-weight: 700; letter-spacing: 0.17em; text-transform: uppercase;
         color: #B4552F; border-bottom: 1px solid #e6e1dc; padding-bottom: 2pt;
         margin: 8.5pt 0 4pt; }
    .summary { color: #33302e; }
    .skill-line { margin-bottom: 2.5pt; }
    .skill-line .sk-label { font-weight: 700; color: #1c1a19; }
    .skill-line .sk-label::after { content: "  —  "; color: #b8b1aa; font-weight: 400; }
    .job { margin-bottom: 5pt; }
    .job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
    .job-role { font-size: 9.9pt; font-weight: 600; color: #1c1a19; }
    .job-co { color: #B4552F; font-weight: 600; }
    .job-note { font-size: 8.3pt; font-style: italic; font-weight: 400; color: #8a8580; }
    .job-dates { font-size: 8.7pt; color: #6b6560; white-space: nowrap; }
    ul { margin: 2.5pt 0 0; padding-left: 14pt; }
    li { margin-bottom: 1.7pt; color: #33302e; }
    li::marker { color: #D97757; }
    .proj-title { font-size: 9.8pt; font-weight: 600; color: #1c1a19; }
    .proj-title .proj-link { font-weight: 400; font-size: 8.3pt; color: #8a8580; }
    .edu { color: #33302e; }
    .edu strong { color: #1c1a19; }
"""


def render_editorial(variant):
    contact = "".join(f"<span>{c}</span>" for c in CONTACT)
    skills = _skill_lines(variant, "sk-label", "sk-body")
    body = f"""<div class="page">
      <div class="name">{NAME}</div>
      <div class="tagline">{variant["tagline"]}</div>
      <div class="contact">{contact}</div>
      <h2>Summary</h2><div class="summary">{variant["summary"]}</div>
      <h2>Skills</h2>{skills}
      <h2>Experience</h2>{_jobs(variant)}
      <h2>Selected Project</h2>{_project(variant)}
      <h2>Education</h2>
      <div class="edu"><strong>{EDUCATION_SCHOOL}</strong> — {EDUCATION_DEGREE}</div>
    </div>"""
    return _doc(EDITORIAL_CSS, body)


# ---------------------------------------------------------------------------
# Layout B — MODERN (two-column, skills rail)
# ---------------------------------------------------------------------------

MODERN_CSS = """
    body { font-family: 'Inter', system-ui, sans-serif; font-size: 8.9pt;
           line-height: 1.31; color: #33302e; }
    .page { width: 8.5in; }
    .header { padding: 0.38in 0.55in 0.18in; display: flex; justify-content: space-between;
              align-items: flex-end; border-bottom: 2.2px solid #1c1a19; gap: 18pt; }
    .name { font-size: 21pt; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
            color: #1c1a19; line-height: 1; }
    .tagline { font-size: 8.7pt; font-weight: 600; color: #B4552F; text-transform: uppercase;
               letter-spacing: 0.11em; margin-top: 5pt; }
    .header-contact { text-align: right; font-size: 8.3pt; color: #6b6560; line-height: 1.65;
                      white-space: nowrap; }
    .cols { display: flex; align-items: stretch; }
    .rail { width: 31%; background: #F6F3F1; padding: 0.24in 0.28in; }
    .main { width: 69%; padding: 0.24in 0.36in 0.3in 0.34in; }
    h2 { font-size: 7.5pt; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase;
         color: #B4552F; margin: 0 0 5pt; }
    .main h2 { border-bottom: 1px solid #e6e1dc; padding-bottom: 2.5pt; }
    .block + .block { margin-top: 9pt; }
    .summary { color: #33302e; }
    .rail .skill-line { margin-bottom: 6pt; }
    .rail .sk-label { display: block; font-weight: 700; color: #1c1a19; margin-bottom: 1pt; }
    .rail .sk-body { color: #4f4a46; font-size: 8.6pt; }
    .rail .rail-links { font-size: 8.5pt; color: #4f4a46; line-height: 1.7; }
    .rail .edu-school { font-weight: 700; color: #1c1a19; }
    .rail .edu-degree { color: #4f4a46; font-size: 8.6pt; margin-top: 1pt; }
    .job { margin-bottom: 5.5pt; }
    .job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10pt; }
    .job-role { font-size: 9.4pt; font-weight: 600; color: #1c1a19; }
    .job-co { color: #B4552F; font-weight: 600; }
    .job-note { display: block; font-size: 8.1pt; font-style: italic; font-weight: 400;
                color: #8a8580; margin-top: 1pt; }
    .job-dates { font-size: 8.3pt; color: #6b6560; white-space: nowrap; }
    ul { margin: 3pt 0 0; padding-left: 13pt; }
    li { margin-bottom: 1.7pt; color: #33302e; }
    li::marker { color: #D97757; }
    .proj-title { font-size: 9.4pt; font-weight: 600; color: #1c1a19; }
    .proj-title .proj-link { display: block; font-weight: 400; font-size: 8.1pt;
                             color: #8a8580; margin-top: 1pt; }
"""


def render_modern(variant):
    header_contact = "<br>".join(CONTACT[:2])
    links = "<br>".join(CONTACT[2:])
    skills = _skill_lines(variant, "sk-label", "sk-body")
    body = f"""<div class="page">
      <div class="header">
        <div><div class="name">{NAME}</div>
             <div class="tagline">{variant["tagline"]}</div></div>
        <div class="header-contact">{header_contact}</div>
      </div>
      <div class="cols">
        <div class="rail">
          <div class="block"><h2>Skills</h2>{skills}</div>
          <div class="block"><h2>Links</h2>
            <div class="rail-links">{links}</div></div>
          <div class="block"><h2>Education</h2>
            <div class="edu-school">{EDUCATION_SCHOOL}</div>
            <div class="edu-degree">{EDUCATION_DEGREE}</div></div>
        </div>
        <div class="main">
          <div class="block"><h2>Summary</h2>
            <div class="summary">{variant["summary"]}</div></div>
          <div class="block"><h2>Experience</h2>{_jobs(variant)}</div>
          <div class="block"><h2>Selected Project</h2>{_project(variant)}</div>
        </div>
      </div>
    </div>"""
    return _doc(MODERN_CSS, body)


LAYOUTS = {"editorial": render_editorial, "modern": render_modern}


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    for stem, variant in VARIANTS.items():
        for layout, fn in LAYOUTS.items():
            path = OUT_DIR / f"{stem}--{layout}.html"
            path.write_text(fn(variant))
            print(f"wrote {path.name}")
