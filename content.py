"""Career facts — the single source feeding every surface.

Three renderers read this module:

    resume/build_resumes.py   the four one-page resume PDFs (2 lenses x 2 layouts)
    build_site.py             the public site (docs/index.html)
    (site_qa.py does NOT — its FACTS corpus is authored per-question and stays
     separately curated; the /new-entry skill appends to both deliberately)

Everything here is PLAIN TEXT. Renderers escape at render time — never store
`&amp;` or any other entity in this file. Fields that describe the same job
differently per surface (resume bullets vs. the site timeline blurb) are
parallel on purpose: they are different tellings, not derivable from one
another.

The two lenses are the two job-search framings of the same career:
    "ai"   AI Deployment      (Applied AI / AI Ops / AI Strategy & Enablement)
    "ops"  Business Operations (BizOps / Chief of Staff / Partner & Revenue Ops)

New entries land here via the /new-entry skill (interview -> options -> approval
gate), never by ad-hoc edits. No invented or internal-only figures — public-safe
framings only (multiples, ranges, "first/only" markers).
"""

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

NAME = "Dylan Ram"
EMAIL = "dylanmr96@gmail.com"
PHONE = "916-690-5681"
LINKEDIN = "linkedin.com/in/dylanram"
GITHUB_USER = "dylan3796"
REPO_SLUG = "dylan3796/dylan3796.github.io"
EDUCATION_SCHOOL = "University of California, Santa Barbara"
EDUCATION_DEGREE = "B.A. Economics & Accounting · Dean's Honors"

# ---------------------------------------------------------------------------
# Per-lens positioning
# ---------------------------------------------------------------------------

LENSES = {
    "ai": {
        "resume_stem": "dylan-ram-ai-deployment",
        "tagline": "AI Deployment · Agent Systems · Strategy & Enablement",
        "summary": (
            "Deploys AI into the workflows a go-to-market org runs on — reporting, "
            "forecasting, crediting — and sets up how the org adopts it: data, KPIs, "
            "self-serve enablement. An operator who builds the systems himself and draws "
            "the line where deterministic, tested code must own the outcome. "
            "As Databricks' first Partner Strategy & Ops hire, shipped the team's first LLM "
            "agents to production — reporting agents, partner-recommendation agents for "
            "reps' deals, natural-language partner-fit Q&A — and independently built a full "
            "agent operating system in Claude Code, with a golden-tested engine that keeps "
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
        "site_copy": (
            "The AI-native operator. I deploy LLM agents into the workflows a GTM org "
            "runs on — reporting, forecasting, crediting — and set up how it adopts them: "
            "foundational data, KPI alignment, self-serve enablement, with tested code "
            "owning anything that touches money. All of it is public, down to the eval "
            "suite."
        ),
        "site_targets": "Applied AI · AI Operations · AI Strategy & Enablement",
        "site_label": "AI Deployment résumé",
    },
    "ops": {
        "resume_stem": "dylan-ram-business-operations",
        "tagline": "GTM Strategy & Operations · Annual Planning · Executive Partnership",
        "summary": (
            "The strategy-and-operations spine of a GTM org: a zero-to-one builder and "
            "one-to-100 scaler. As Databricks' first Partner Strategy & Ops hire, stood up "
            "the forecast, attribution, and first new-logo incentive programs from scratch, "
            "and ran annual planning across Sales, Finance, and Partner leadership: quotas, "
            "headcount, and coverage, top-down and bottoms-up. Runs the strategic "
            "initiatives that shape the partner book — which regional SIs to invest in, how "
            "partners are tiered — and writes the investment cases that fund them, "
            "presented at the most senior levels. "
            "Seven years of working relationships with GTM executives at Databricks, "
            "Salesforce, and CBRE — the access that gets the data in the room at all."
        ),
        "skills": [
            ("Operations & strategy", "Operating cadence, annual & quota planning, OKRs, "
             "territory design, incentive/comp program design, revenue forecasting, "
             "executive & board reporting"),
            ("Data & AI", "SQL, Python (pandas), PySpark, Tableau, Salesforce, revenue "
             "attribution, deployed AI agents, AI enablement (Claude Code)"),
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
        "site_copy": (
            "The operating spine of a GTM org — zero to one, then one to 100. I run the "
            "forecast, attribution, incentive, and quota systems a partner business "
            "depends on, and align them across a two-sided marketplace."
        ),
        "site_targets": "Business Operations · Chief of Staff · Partner & Revenue Ops",
        "site_label": "Business Operations résumé",
    },
}

# ---------------------------------------------------------------------------
# Jobs — one record per job; per-lens resume bullets, plus the site telling
# ---------------------------------------------------------------------------

JOBS = [
    {
        "company": "Databricks",
        "role": "Partner Strategy & Ops Manager",
        "resume_note": "promoted Feb 2023 · first Partner S&O hire",
        "dates": "Aug 2021 – Present",
        "site_when": "2021 — now",
        "site_note": "first Partner S&O hire · promoted 2023",
        "site_desc": (
            "Built the data-and-AI foundation and the forecast, attribution, and incentive "
            "systems the partner business runs on; deployed the team's first LLM agents; "
            "leads quota-setting across Sales, Finance, and Partner leadership."
        ),
        "bullets": {
            "ai": [
                "Deployed the partner team's first LLM agents to production: reporting "
                "agents (Newsletter, FAQ), partner-recommendation agents for reps' deals, "
                "and natural-language partner-fit Q&A.",
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
            "ops": [
                "Built the partner team's revenue forecasting process from a blank "
                "page; its methodology and cadence remain the spine of the team's "
                "forecast years later.",
                "Designed the canonical partner attribution model — the single source of "
                "truth for how sourced, influenced, and attributed revenue is credited "
                "across both sides of the marketplace.",
                "Launched the partner org's incentive program tied to new-logo "
                "acquisition — crediting and payout logic designed end to end, still "
                "in force today.",
                "Diagnosed why partner leads were stalling, wrote the org's lead rules "
                "of engagement, and cut routing time from weeks to days.",
                "Led annual planning across Sales, Finance, and Partner leadership: "
                "quota-setting, headcount, and coverage design, top-down and bottoms-up.",
                "Wrote the investment cases behind new programs and presented them to "
                "senior GTM leadership.",
                "Shaped the partner program strategy — the Partner Value Score and tiering "
                "framework — earning global alignment and executive adoption.",
            ],
        },
    },
    {
        "company": "Salesforce",
        "role": "SMB Sales Strategy & Operations Analyst",
        "resume_note": "",
        "dates": "Jul 2019 – Aug 2021",
        "site_when": "2019 — 2021",
        "site_note": "",
        "site_desc": (
            "Built the territory-carving model behind the annual GTM plan, automated QBR "
            "and forecast-accuracy tooling, and was the direct analytics partner to a "
            "$250M AMER SMB business."
        ),
        "bullets": {
            "ai": [
                "Built the territory-carving Python script that encoded the org's guiding "
                "principles, personnel, and accounts — the engine behind the annual GTM plan.",
                "Automated QBR decks, forecast-accuracy tracking, and territory data pulls "
                "with Python, APIs, and G Suite.",
                "Led the business unit's Tableau migration and established data governance "
                "for the $250M AMER SMB Central business.",
            ],
            "ops": [
                "Direct business partner to the $250M AMER SMB Central business, advising "
                "AVPs, VPs, and RMs across the org.",
                "Built the territory-carving model (Python) that encoded the org's guiding "
                "principles — the basis of the annual GTM plan.",
                "Crafted the FY22 GTM guiding-principles analyses: customer continuity, "
                "account proximity, industry mix, top accounts, AE tenure.",
            ],
        },
    },
    {
        "company": "CBRE",
        "role": "Business Data Analyst",
        "resume_note": "",
        "dates": "Sep 2018 – Jul 2019",
        "site_when": "2018 — 2019",
        "site_note": "",
        "site_desc": (
            "Owned the product-analytics stack end to end — data warehouse, Python data "
            "collection, and client-facing Tableau dashboards."
        ),
        "bullets": {
            "ai": [
                "Built Python web-scraping tools and managed the product data warehouse; "
                "shipped client-facing Tableau dashboards and streamlined the analytics "
                "pipeline end to end.",
            ],
            "ops": [
                "Owned the product-analytics stack end to end — data warehouse, Python "
                "data collection, and client-facing Tableau dashboards.",
                "Streamlined the product-analytics process: defined key metrics, the "
                "dataset, and the flow to visualization.",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Signature work — the site's "Signature work" cards
# ---------------------------------------------------------------------------

PROGRAMS = [
    ("The forecast",
     "Built from a blank page: methodology and cadence designed end to end, and still "
     "the operating rhythm the team runs today."),
    ("The attribution model",
     "The canonical, single source of truth for how sourced, influenced, and attributed "
     "revenue is credited across the marketplace — still the standard today."),
    ("The new-logo incentive",
     "Launched the partner org's incentive program tied to new-logo acquisition — "
     "crediting and payout logic built from scratch, still in force."),
    ("The rules of engagement",
     "Traced stalled partner leads to a missing layer of rules of engagement and wrote "
     "them — leads that sat for weeks route in days, and the rules still stand."),
]

# Signature work through the AI lens — same record, the building side of it.
PROGRAMS_AI = [
    ("The production agents",
     "Newsletter and FAQ agents shipped to production — answering partner-metric "
     "questions and pushing updates automatically, still running today."),
    ("The recommendation layer",
     "Agents that suggest the right partner for a rep's deal, and natural-language "
     "Q&A over which partners fit a use case, deal, or account."),
    ("The governed data layer",
     "A medallion architecture in Spark and SQL with one metric dictionary — the "
     "foundation every agent answers from."),
    ("The crediting engine",
     "The AI/deterministic boundary made real: a model authors plain-English rules, "
     "a golden-tested engine computes the money, an eval suite pins the math."),
]
