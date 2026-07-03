"""
Dylan Ram — AI product portfolio.
Three projects, one throughline: making revenue relationships legible and every
dollar explainable. Covant (the channel), Causa (the AI-agent economy), and the
partner semantic layer this app itself runs on.
"""

import streamlit as st

st.set_page_config(
    page_title="Dylan Ram | AI Product Portfolio",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #FAFAF9; }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1 { color: #1a1a1a; font-weight: 600; letter-spacing: -0.02em; }
    h3 { color: #3d3d3d; font-weight: 500; margin-top: 2.2rem; }
    hr { border: none; border-top: 1px solid #e5e5e5; margin: 2.5rem 0; }

    a { color: #D97757; text-decoration: none; }
    a:hover { color: #c4624a; text-decoration: underline; }

    .narrative-quote {
        background-color: white;
        border-left: 3px solid #D97757;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0 1.5rem 0;
        font-style: italic;
        color: #4a4a4a;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    .experience-card {
        background: white;
        padding: 1.3rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* --- Eyebrow / hero --- */
    .eyebrow {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.72rem;
        font-weight: 700;
        color: #D97757;
        margin-bottom: 0.6rem;
    }

    /* --- Project case-study cards --- */
    .project-card {
        background: white;
        border-radius: 10px;
        border-top: 3px solid #D97757;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 1.6rem 1.8rem 1.7rem 1.8rem;
        margin-bottom: 1.3rem;
    }
    .project-head {
        display: flex;
        align-items: baseline;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 0.15rem;
    }
    .project-name { font-size: 1.55rem; font-weight: 700; color: #1a1a1a; letter-spacing: -0.01em; }
    .project-kind { font-size: 0.9rem; color: #999; font-weight: 500; }
    .status-pill {
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border-radius: 5px;
        padding: 0.12rem 0.5rem;
        vertical-align: middle;
    }
    .status-pill.live { background: rgba(217,119,87,0.12); color: #c4624a; border: 1px solid rgba(217,119,87,0.45); }
    .status-pill.demo { background: #eef4f4; color: #5a8a8a; border: 1px solid #cfe0e0; }
    .status-pill.oss  { background: #f0efed; color: #888; border: 1px solid #ddd; }

    .project-tagline {
        font-size: 1.05rem;
        color: #3d3d3d;
        font-weight: 500;
        line-height: 1.5;
        margin: 0.5rem 0 0.4rem 0;
    }
    .project-link { font-size: 0.9rem; margin-bottom: 1.1rem; }
    .project-link .dot { color: #ccc; margin: 0 0.5rem; }

    .proj-label {
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-size: 0.68rem;
        font-weight: 700;
        color: #b0b0b0;
        margin: 1.1rem 0 0.45rem 0;
    }
    .proj-body { font-size: 0.93rem; color: #4a4a4a; line-height: 1.6; }
    .proj-list { margin: 0.2rem 0 0 0; padding: 0; list-style: none; }
    .proj-list li {
        font-size: 0.92rem;
        color: #4a4a4a;
        line-height: 1.55;
        padding: 0.16rem 0 0.16rem 1.1rem;
        position: relative;
    }
    .proj-list li:before {
        content: "";
        position: absolute;
        left: 0; top: 0.72rem;
        width: 5px; height: 5px;
        border-radius: 50%;
        background: #D97757;
    }
    .proj-list li b { color: #1a1a1a; font-weight: 600; }

    .stack-row { margin-top: 1rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
    .stack-chip {
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 0.74rem;
        color: #6a6a6a;
        background: #f4f2f0;
        border: 1px solid #e6e3e0;
        border-radius: 5px;
        padding: 0.16rem 0.55rem;
    }
    .scale-line {
        margin-top: 1rem;
        font-size: 0.82rem;
        color: #999;
        border-top: 1px solid #f0efed;
        padding-top: 0.8rem;
    }
    .scale-line b { color: #c4624a; font-weight: 600; }

    /* --- The context squares (walkthrough expander) --- */
    .layer-row { display: flex; align-items: stretch; gap: 0.5rem; margin: 1.2rem 0 0.3rem 0; }
    .layer-card {
        background: #faf9f8;
        border-radius: 8px;
        border-top: 3px solid #D97757;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        padding: 1rem 1.1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .layer-name { color: #D97757; font-weight: 600; letter-spacing: 0.05em; font-size: 0.98rem; margin-bottom: 0.45rem; }
    .layer-desc { color: #4a4a4a; font-size: 0.88rem; line-height: 1.5; flex: 1; }
    .layer-path { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.76rem; color: #999; margin-top: 0.9rem; }
    .layer-arrow { align-self: center; color: #D97757; font-size: 1.4rem; padding: 0 0.1rem; }
    .layer-loop { text-align: center; color: #777; font-size: 0.9rem; margin-top: 0.7rem; }

    .skill-card {
        background: #faf9f8;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.7rem;
        display: flex;
        gap: 1.4rem;
        align-items: flex-start;
    }
    .skill-cmd-col { min-width: 190px; }
    .skill-cmd {
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        color: #D97757;
        font-weight: 600;
        font-size: 0.92rem;
        white-space: nowrap;
    }
    .skill-when { font-weight: 600; color: #1a1a1a; font-size: 0.92rem; margin-bottom: 0.35rem; }
    .skill-how { font-size: 0.88rem; color: #4a4a4a; line-height: 1.55; }

    @media (max-width: 820px) {
        .layer-row { flex-direction: column; gap: 0.6rem; }
        .layer-arrow { transform: rotate(90deg); padding: 0.1rem 0; align-self: center; }
        .layer-desc { flex: none; }
    }
    @media (max-width: 640px) {
        h1 { font-size: 2rem !important; }
        .main .block-container { padding-top: 1rem; padding-left: 1rem; padding-right: 1rem; }
        .project-card { padding: 1.3rem 1.2rem; }
        .project-name { font-size: 1.35rem; }
        .skill-card { flex-direction: column; gap: 0.5rem; }
        .skill-cmd-col { min-width: 0; }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HERO
# =============================================================================

st.markdown("""
<div style="text-align: center; padding: 1.2rem 0 0.4rem 0;">
    <div class="eyebrow">AI Product Portfolio</div>
    <h1 style="font-size: 2.9rem; margin-bottom: 0.6rem; border: none;">Dylan Ram</h1>
    <p style="font-size: 1.18rem; color: #555; max-width: 760px; margin: 0 auto 0.7rem auto; line-height: 1.55;">
        I build AI products that make revenue relationships legible — every partner touch
        tracked, every commission explained, every agent outcome settled. Partnerships &amp;
        GTM operator turned builder; I ship the whole thing, from doctrine to deploy.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a> &nbsp;·&nbsp;
        <a href="https://covant.ai">covant.ai</a>
    </p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# THE THROUGHLINE
# =============================================================================

st.markdown("### The throughline")
st.markdown("""
<div class="narrative-quote">
The same problem shows up in three places: a relationship that matters — a channel
partner, an AI agent, a GTM operating model — lives in spreadsheets, Slack threads,
and self-reported dashboards, and no one can prove who actually drove what. Each of
these projects makes one of those relationships legible and every dollar explainable.
Attribution you can't explain is attribution no one trusts — so explainability is the
wedge in all three.
</div>
""", unsafe_allow_html=True)


# =============================================================================
# CASE STUDIES
# =============================================================================

def render_project(p):
    # Streamlit renders each st.markdown call in isolation and auto-closes stray
    # tags, so a card that spans multiple calls breaks. Compose the whole card as
    # one HTML string and emit it in a single call.
    pill = f'<span class="status-pill {p["status_class"]}">{p["status"]}</span>'
    link = f'<div class="project-link">{p["link"]}</div>' if p.get("link") else ""
    built = "".join(f"<li>{b}</li>" for b in p["built"])
    ai = "".join(f"<li>{b}</li>" for b in p["ai"])
    chips = "".join(f'<span class="stack-chip">{c}</span>' for c in p["stack"])

    st.markdown(
        f'<div class="project-card">'
        f'<div class="project-head">'
        f'<span class="project-name">{p["name"]}</span>{pill}'
        f'<span class="project-kind">{p["kind"]}</span></div>'
        f'<div class="project-tagline">{p["tagline"]}</div>'
        f'{link}'
        f'<div class="proj-label">The problem</div>'
        f'<div class="proj-body">{p["problem"]}</div>'
        f'<div class="proj-label">What I built</div>'
        f'<ul class="proj-list">{built}</ul>'
        f'<div class="proj-label">The AI &amp; technical work</div>'
        f'<ul class="proj-list">{ai}</ul>'
        f'<div class="stack-row">{chips}</div>'
        f'<div class="scale-line">{p["scale"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


st.markdown("### Selected work")

# --- 1. COVANT -------------------------------------------------------------
render_project({
    "name": "Covant",
    "kind": "The Channel Graph",
    "status": "Live",
    "status_class": "live",
    "tagline": "Your CRM runs the deals. Covant is the partner hub alongside it — a living "
               "model of how a B2B channel actually operates, with every commission calculated "
               "and explained.",
    "link": '<a href="https://covant.ai">covant.ai</a>'
            '<span class="dot">·</span>full-stack founder build',
    "problem": "The partner motion lives in spreadsheets, Slack threads, and CRM reports — "
               "partner-sourced pipeline stalls because no one system owns it, and every "
               "commission is disputable because attribution is a black box. Partners stop "
               "trusting the numbers, so they stop sending deals.",
    "built": [
        "A full product: marketing site, an operator <b>dashboard of 40+ views</b> "
        "(partners, deals, pipeline, payouts, health, forecasting, MDF, certifications, "
        "leaderboards), and a branded <b>partner portal of 20+ pages</b> partners self-serve from.",
        "An <b>attribution engine</b> — first-touch, last-touch, time-decay, equal-split, "
        "role-based, and custom-weight models — that ships every credit decision with a full "
        "audit trail, so a commission is never a number without a why.",
        "A <b>priority-based commission rules engine</b>, deal-registration + approval "
        "workflow, payouts pipeline (pending → approved → paid), and reconciliation reporting.",
        "Salesforce &amp; HubSpot connectors so registrations flow in and closed-deal data "
        "flows back — the graph stays current without re-implementing when the program changes.",
    ],
    "ai": [
        "<b>Natural-language commission rules</b> — a manager types “Gold partners get 20%, "
        "deals over $100k get an extra 5%” and Claude parses it into structured, "
        "priority-ordered rules (Anthropic SDK, Claude Haiku).",
        "<b>Ask Covant</b> — an embedded AI analyst grounded in the org's real partner data, "
        "with a fast primary model (Groq / Llama 3.3 70B), a Claude fallback, and a "
        "deterministic regex engine underneath so it never fabricates a number.",
        "<b>Recursive attribution learning</b> (designed) — every human judge override becomes "
        "a labeled signal the recommender consults next time, learning each customer's own "
        "credit taxonomy while the payout math stays bounded to a defensible set of models. "
        "The loop gets smarter; the guardrails never come off.",
    ],
    "stack": ["Next.js (App Router)", "React", "Convex", "Clerk", "Vercel",
              "Anthropic SDK", "Groq", "Salesforce / HubSpot APIs"],
    "scale": "<b>~60 Convex backend modules</b> · 40+ dashboard views · 20+ portal pages · "
             "live at covant.ai · designed, built, and deployed end to end.",
})

# --- 2. CAUSA --------------------------------------------------------------
render_project({
    "name": "Causa",
    "kind": "Verification for the AI-agent economy",
    "status": "Concept + demo",
    "status_class": "demo",
    "tagline": "The vendor shouldn't grade its own homework. Causa is the independent layer "
               "that verifies what AI agents actually delivered — it doesn't report outcomes, "
               "it settles them.",
    "link": "founding doctrine · interactive product demo",
    "problem": "Software is shifting to paying for results — per resolved ticket, per "
               "provisioned account, per booked meeting — and the party reporting the result "
               "is the party getting paid. Companies can't verify what an agent accomplished, "
               "so they can't dispute an invoice, compare two vendors, or decide whether to "
               "build more. Doubt freezes agent budgets.",
    "built": [
        "The <b>founding product doctrine</b> — the thesis, the wedge, the moat, and the "
        "scope discipline — written so a CFO and a CTO read the same document at different "
        "altitudes.",
        "A <b>live landing page and an interactive 4-screen demo</b>: define the outcome "
        "contract → connect the data → read the settlement statement → act on the verdict.",
        "The <b>settlement model</b> itself — Claimed → Verified → Attributable, five verdicts "
        "(Reprice, Reroute, Renegotiate, Retire, Expand), each with the dollar impact and the "
        "follow-through drafted, and an A–D evidence grade so buyers know how much to trust each call.",
        "<b>Build-time data-integrity assertions</b>: every number on every screen traces to one "
        "ledger, and the build fails if the ledger doesn't reconcile — the product can't ship a "
        "figure that doesn't add up.",
    ],
    "ai": [
        "An <b>architecture doctrine</b> that consumes commodity plumbing (observability traces, "
        "systems of record) and owns the hard part: the actor model, the run→entity→outcome "
        "contribution graph, and the verdict engine.",
        "A <b>sealed, deterministic causal core</b> — LLMs are confined to ingestion, "
        "interpretation, and narrative; verdicts come from replayable logic, because a verdict "
        "you can't replay is a verdict you can't defend in a billing dispute.",
        "<b>Model recorded as an attribute of every run</b>, making “cost per real result, by "
        "model” a native primitive — the product gets more valuable as the model landscape "
        "fragments, not less.",
    ],
    "stack": ["Next.js (App Router)", "TypeScript", "Tailwind", "Framer Motion",
              "Vercel", "build-time data assertions"],
    "scale": "Product concept taken from blank page to <b>articulated doctrine + working "
             "interactive demo</b> — the category (an independent referee for machine labor) and "
             "its first artifact, built together.",
})

# --- 3. PARTNER SEMANTIC LAYER ---------------------------------------------
render_project({
    "name": "Partner Semantic Layer",
    "kind": "Claude Code as an operating system",
    "status": "Open source",
    "status_class": "oss",
    "tagline": "The operating model underneath the channel work: run an agent as an operating "
               "system for a partner-ops team, on one governed semantic layer where every metric "
               "is defined exactly once.",
    "link": "this app is the artifact — the repo it lives in <em>is</em> the system",
    "problem": "GTM and partner metrics disagree across teams because everyone re-derives them; "
               "the same recurring asks eat someone's week; and putting an LLM in the money path "
               "risks it silently miscounting. Speed and trust look like a tradeoff.",
    "built": [
        "A single <b>data dictionary as the semantic layer</b> — sourced, influenced, and "
        "attributed revenue, tiers, health, the fiscal calendar — defined once and read "
        "everywhere, so no two briefs disagree and no skill guesses a definition.",
        "A <b>deterministic, unit-tested crediting engine</b>: the model authors plain-English "
        "coverage rules, and tested code does the money math — mid-quarter hires, handoffs, and "
        "splits credit the right person on the right line for the right months.",
        "<b>Skills owned by strategic plans</b> — <code>/commissions-credit</code>, "
        "<code>/partner-qbr</code>, <code>/call-notes-to-jira</code> — each scoped to exactly the "
        "tools its plan allows, plus a SessionStart hook so every session boots knowing the book.",
        "A <b>recursive self-improvement loop</b> (<code>/improve-setup</code>) that reads the "
        "session log and proposes edits back into the memory, the skills, and the plans — the "
        "setup compounds with use instead of drifting stale.",
    ],
    "ai": [
        "The core principle carried into Covant and Causa: <b>keep the model out of the money</b>. "
        "The LLM authors rules in language; deterministic, tested code applies them — the speed of "
        "language with the trust of a spreadsheet that can't silently miscount.",
        "<b>Define once, reuse everywhere</b> — one dictionary, one set of rules, so a change lands "
        "in a single place and every downstream output updates, auditable to the definition.",
        "A working demonstration of <b>agent memory, plans, skills, and hooks</b> composing into an "
        "operating system a non-engineering team can extend themselves.",
    ],
    "stack": ["Python", "Streamlit", "pandas", "Claude Code (skills · hooks · subagents · MCP)"],
    "scale": "Open source · the walkthrough below is generated from the live repo — "
             "definitions, crediting tests, and skills all run.",
})

# --- Expander: the full architecture walkthrough ---------------------------
with st.expander("Open the full architecture walkthrough of the partner semantic layer"):
    st.markdown(
        "Everything a session knows comes from one of five layers — from the governed data at "
        "the foundation to the self-editing loop that keeps the rest current."
    )

    LAYERS = [
        ("DATA", "The gold table and the metric dictionary. Every metric is defined once, here — skills read definitions, they never guess them.", "data/"),
        ("MEMORY", "What every session boots knowing: conventions, the fiscal calendar, the operating model. Injected by a SessionStart hook.", "CLAUDE.md"),
        ("PLANS", "One living plan per strategic initiative. Skills are proposed in a plan before they get built.", "plans/big-rocks/"),
        ("SKILLS", "The recurring work, made invocable. Each skill is owned by exactly one plan and scoped to the tools that plan allows.", ".claude/skills/"),
        ("RETROS", "A session log plus dated retros — the evidence stream the improvement loop reads instead of anecdotes.", "retros/"),
    ]
    layer_cells = []
    for i, (nm, desc, path) in enumerate(LAYERS):
        layer_cells.append(
            f'<div class="layer-card"><div class="layer-name">{nm}</div>'
            f'<div class="layer-desc">{desc}</div>'
            f'<div class="layer-path">{path}</div></div>'
        )
        if i < len(LAYERS) - 1:
            layer_cells.append('<div class="layer-arrow">→</div>')
    st.markdown(
        f'<div class="layer-row">{"".join(layer_cells)}</div>'
        f'<div class="layer-loop">↻ &nbsp;<code>/improve-setup</code> closes the loop — a retro '
        f'reads the session log and proposes edits back into every layer above. The system '
        f'rewrites itself.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div class='proj-label' style='margin-top:1.4rem;'>When a skill does the work</div>", unsafe_allow_html=True)
    SKILL_MOMENTS = [
        ("/commissions-credit",
         "A rep joins mid-quarter, or a territory changes hands",
         "A manager edits the coverage sheet in plain English. The skill codifies it into "
         "effective-dated crediting rules — no gap, no double-coverage — and the money math is "
         "deterministic, tested code, so finance's actuals land the right person on the right "
         "line for the right months."),
        ("/partner-qbr",
         "QBR season — the whole org, a regional cut, or a single partner",
         "Pulls the data cut for whatever slice the review covers, using the dictionary's "
         "definitions so every brief reads the same."),
        ("/call-notes-to-jira",
         "A partner call wraps and the follow-ups are buried in notes",
         "Turns raw call notes into tracked Jira tickets — a stalled deal-reg, a missing "
         "certification, an exec intro — each tagged to the partner and the owning rep."),
        ("/improve-setup",
         "The same ask shows up three sessions in a row",
         "The meta-skill. Reads the session log and git history, spots recurring work with no "
         "owning skill, and proposes the next one as a diff to the plans."),
    ]
    for cmd, when, how in SKILL_MOMENTS:
        st.markdown(
            f'<div class="skill-card"><div class="skill-cmd-col"><div class="skill-cmd">{cmd}</div></div>'
            f'<div><div class="skill-when">{when}</div><div class="skill-how">{how}</div></div></div>',
            unsafe_allow_html=True,
        )


# =============================================================================
# HOW I WORK
# =============================================================================

st.markdown("### How I work")
work_cols = st.columns(3)
HOW = [
    ("Doctrine before pixels",
     "Each project starts with a written thesis — what it is, why it wins, what it refuses to "
     "be. The build is an expression of the doctrine, so decisions stay coherent as scope grows."),
    ("Keep the model out of the money",
     "LLMs author, interpret, and narrate; deterministic, tested code decides anything a dollar "
     "or a dispute rides on. The judgment is knowing which is which — and it's the same call in "
     "all three projects."),
    ("Explainable or it doesn't ship",
     "Every credit, verdict, and metric traces to a why a human can read. Trust is the actual "
     "product; the dashboard is just where it shows up."),
]
for col, (title, desc) in zip(work_cols, HOW):
    with col:
        st.markdown(
            f'<div class="experience-card" style="min-height: 210px;">'
            f'<strong style="color: #D97757;">{title}</strong>'
            f'<p style="font-size: 0.88rem; color: #4a4a4a; margin: 0.5rem 0 0 0; line-height: 1.55;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 0.8rem 0; color: #999; font-size: 0.85rem;">
    Dylan Ram &nbsp;·&nbsp;
    <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/dylanram">LinkedIn</a> &nbsp;·&nbsp;
    Built with Claude Code · 2026
</div>
""", unsafe_allow_html=True)
