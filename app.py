"""
AI engineering for a GTM partner ops team — a visual walkthrough.
The page describes the Claude Code operating system the team runs on;
the repo it lives in IS that system.
"""

import streamlit as st

st.set_page_config(
    page_title="Dylan Ram | AI Engineering for Partner Ops",
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
        border-radius: 0 8px 8px 0;
        font-style: italic;
        color: #4a4a4a;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    .experience-card {
        background: white;
        padding: 1.3rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* --- The context squares --- */
    .layer-row { display: flex; align-items: stretch; gap: 0.5rem; margin: 1.2rem 0 0.3rem 0; }
    .layer-card {
        background: white;
        border-radius: 8px;
        border-top: 3px solid #D97757;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 1rem 1.1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .layer-name { color: #D97757; font-weight: 600; letter-spacing: 0.05em; font-size: 1.02rem; margin-bottom: 0.45rem; }
    .layer-desc { color: #4a4a4a; font-size: 0.92rem; line-height: 1.5; flex: 1; }
    .layer-path { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.78rem; color: #999; margin-top: 0.9rem; }
    .layer-arrow { align-self: center; color: #D97757; font-size: 1.4rem; padding: 0 0.1rem; }
    .layer-loop { text-align: center; color: #777; font-size: 0.92rem; margin-top: 0.7rem; }

    /* --- Skill usage cards --- */
    .skill-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.7rem;
        display: flex;
        gap: 1.4rem;
        align-items: flex-start;
    }
    .skill-cmd-col { min-width: 200px; }
    .skill-cmd {
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        color: #D97757;
        font-weight: 600;
        font-size: 0.95rem;
        white-space: nowrap;
    }
    .skill-tag {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        border-radius: 4px;
        padding: 0.05rem 0.45rem;
        margin-top: 0.5rem;
    }
    .skill-tag.live { background: rgba(217,119,87,0.12); color: #c4624a; border: 1px solid rgba(217,119,87,0.4); }
    .skill-tag.org { background: #f0efed; color: #888; border: 1px solid #ddd; }
    .skill-when { font-weight: 600; color: #1a1a1a; font-size: 0.95rem; margin-bottom: 0.35rem; }
    .skill-how { font-size: 0.9rem; color: #4a4a4a; line-height: 1.55; }

    /* --- Folder tree --- */
    .tree-card {
        background: #1f1e1d;
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 0.82rem;
        line-height: 1.75;
        overflow-x: auto;
    }
    .tree-row { display: flex; align-items: baseline; white-space: nowrap; }
    .tree-path { color: #d9d4cf; white-space: pre; }
    .tree-path.dir { color: #D97757; font-weight: 600; }
    .tree-note { color: #8a8580; font-size: 0.76rem; margin-left: 1.2rem; font-family: inherit; }
    .layer-pill {
        display: inline-block;
        background: rgba(217,119,87,0.18);
        color: #e89b7b;
        border: 1px solid rgba(217,119,87,0.45);
        border-radius: 4px;
        font-size: 0.66rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 0 0.4rem;
        margin-left: 0.7rem;
        vertical-align: middle;
    }

    /* --- Glossary --- */
    .gloss-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin: 1rem 0 0.5rem 0; }
    .gloss-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 0.95rem 1.15rem;
    }
    .gloss-term { color: #1a1a1a; font-weight: 600; font-size: 0.98rem; }
    .gloss-term .abbr { color: #D97757; }
    .gloss-def { color: #4a4a4a; font-size: 0.88rem; line-height: 1.5; margin-top: 0.35rem; }

    .metric-wrap { overflow-x: auto; }
    .metric-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin: 0.6rem 0;
    }
    .metric-table th {
        text-align: left;
        font-size: 0.7rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #999;
        font-weight: 600;
        padding: 0.7rem 1.1rem;
        border-bottom: 1px solid #eee;
    }
    .metric-table td {
        padding: 0.7rem 1.1rem;
        border-bottom: 1px solid #f2f1ef;
        vertical-align: top;
        font-size: 0.88rem;
        color: #4a4a4a;
        line-height: 1.5;
    }
    .metric-table tr:last-child td { border-bottom: none; }
    .metric-table td.metric-name { color: #c4624a; font-weight: 600; white-space: nowrap; }

    /* --- "Start by saying what you want" --- */
    .ask-prompt {
        background: #1f1e1d;
        border-radius: 8px;
        padding: 1rem 1.3rem;
        margin: 1rem 0 1.2rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 0.95rem;
        color: #f0ece8;
        line-height: 1.5;
    }
    .ask-prompt .ask-label { color: #8a8580; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; display: block; margin-bottom: 0.4rem; }
    .ask-prompt .ask-caret { color: #D97757; font-weight: 700; margin-right: 0.5rem; }
    .ask-step {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 1.05rem 1.3rem;
        margin-bottom: 0.7rem;
        display: flex;
        gap: 1.1rem;
        align-items: flex-start;
    }
    .ask-tag {
        flex: 0 0 auto;
        min-width: 7.5rem;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #c4624a;
        padding-top: 0.15rem;
    }
    .ask-step-body { font-size: 0.9rem; color: #4a4a4a; line-height: 1.55; }

    /* --- Responsive: stack the wide rows so it reads top-to-bottom on phones --- */
    @media (max-width: 820px) {
        .layer-row { flex-direction: column; gap: 0.6rem; }
        .layer-arrow { transform: rotate(90deg); padding: 0.1rem 0; align-self: center; }
        .layer-desc { flex: none; }
        .gloss-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
        h1 { font-size: 2rem !important; }
        .main .block-container { padding-top: 1rem; padding-left: 1rem; padding-right: 1rem; }
        .narrative-quote { padding: 1rem 1.1rem; }
        .skill-card { flex-direction: column; gap: 0.5rem; padding: 1rem 1.1rem; }
        .skill-cmd-col { min-width: 0; }
        .tree-card { font-size: 0.72rem; padding: 1rem 1.1rem; }
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
<div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
    <h1 style="font-size: 2.7rem; margin-bottom: 0.5rem; border: none;">AI Engineering for a Partner Ops Team</h1>
    <p style="font-size: 1.15rem; color: #666; margin-bottom: 0.4rem;">
        A working example of running Claude Code as an operating system for a partner
        ops team — the context it boots with, the structure it lives in, and the
        moments a skill does the work.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        Dylan Ram &nbsp;·&nbsp; Partnerships GTM &nbsp;·&nbsp;
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# ONE QUESTION, THREE PARTS OF THE BUSINESS
# =============================================================================

st.markdown("### One question, three parts of the business")
st.markdown(
    "A concrete example of what the system is for. Someone on the team asks one specific "
    "question, and it reaches into whichever parts of the business hold the answer — without "
    "anyone deciding in advance where to look."
)

st.markdown("""
<div class="ask-prompt">
    <span class="ask-label">Someone asks</span>
    <span class="ask-caret">&gt;</span>Should we add a PSM in the West this half?
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div style="font-size:0.9rem; color:#4a4a4a; margin:0 0 0.5rem 0;">'
    'It qualifies the answer against three parts of the business at once:</div>',
    unsafe_allow_html=True,
)

ASK_ROUTES = [
    ("Metrics",
     "West sourced and attributed pipeline, and how much sits uncovered — is there enough "
     "partner revenue in motion to carry another head?"),
    ("Program",
     "Which partners and priority motions concentrate in the West, and where today's "
     "coverage is thinnest."),
    ("Compensation",
     "How the region's reps are credited now, and how a new territory split would redraw "
     "who owns what."),
]
route_cards = "".join(
    f'<div class="ask-step"><div class="ask-tag">{tag}</div>'
    f'<div class="ask-step-body">{body}</div></div>'
    for tag, body in ASK_ROUTES
)
st.markdown(route_cards, unsafe_allow_html=True)
st.caption("No one routed it to those three systems by hand — the question was specific enough to reach them on its own.")


# =============================================================================
# THE CONTEXT LAYERS
# =============================================================================

st.markdown("### The five layers of context")
st.markdown(
    "Everything a session knows comes from one of these five layers — from the governed "
    "data at the foundation to the self-editing loop that keeps the rest current."
)

LAYERS = [
    ("DATA", "The gold table and the metric dictionary. Every metric is defined once, here — skills read definitions, they never guess them.", "data/"),
    ("MEMORY", "What every session boots knowing: conventions, the fiscal calendar, the operating model. Injected by a SessionStart hook.", "CLAUDE.md"),
    ("PLANS", "One living plan per strategic initiative, tied to the epics the team already runs. Skills are proposed in a plan before they get built.", "plans/big-rocks/"),
    ("SKILLS", "The recurring work, made invocable. Each skill is owned by exactly one plan and scoped to the tools that plan allows.", ".claude/skills/"),
    ("RETROS", "A session log plus dated retros — the evidence stream the improvement loop reads instead of anecdotes.", "retros/"),
]

layer_cells = []
for i, (layer_name, layer_desc, layer_path) in enumerate(LAYERS):
    layer_cells.append(f"""
    <div class="layer-card">
        <div class="layer-name">{layer_name}</div>
        <div class="layer-desc">{layer_desc}</div>
        <div class="layer-path">{layer_path}</div>
    </div>""")
    if i < len(LAYERS) - 1:
        layer_cells.append('<div class="layer-arrow">→</div>')

st.markdown(f"""
<div class="layer-row">{"".join(layer_cells)}</div>
<div class="layer-loop">↻ &nbsp;<code>/improve-setup</code> closes the loop — a retro reads the session
log and proposes edits back into every layer above. The system rewrites itself.</div>
""", unsafe_allow_html=True)


# =============================================================================
# THE STRUCTURE ON DISK
# =============================================================================

st.markdown("### Those same five layers, as real files")

FOLDER_TREE = [
    ("partner-ops/", None, None),
    ("├── CLAUDE.md", "operating model + domain glossary (who a PSM/PAM is)", "MEMORY"),
    ("├── app.py", "this walkthrough page", None),
    ("├── data/", None, "DATA"),
    ("│   ├── partner_metrics.csv", "the gold table: revenue splits, deal regs, PVS, health", None),
    ("│   ├── coverage_assignments.csv", "the plain-English coverage sheet (the “Google Sheet”)", None),
    ("│   ├── crediting_rules.json", "codified crediting rules — output of /commissions-credit", None),
    ("│   ├── commission_deals.csv", "closed deals actuals run against", None),
    ("│   └── DATA_DICTIONARY.md", "one definition per metric + every schema above", None),
    ("├── crediting/", "deterministic, tested money path — no LLM credits a deal", "DATA"),
    ("│   └── engine.py", "applies rules → who is credited, which line, which month", None),
    ("├── tests/", "golden tests / evals that pin the crediting math", None),
    ("│   └── test_crediting.py", "handoffs, mid-quarter hires, splits, coverage gaps", None),
    ("├── plans/", None, None),
    ("│   └── big-rocks/", "one living plan per strategic initiative ↔ Jira epic", "PLANS"),
    ("│       ├── 00-INDEX.md", "lifecycle rules + the plan template", None),
    ("│       ├── partner-compensation.md", "owns /commissions-credit + the crediting engine", None),
    ("│       ├── partner-attribution.md", "canonical attribution model weights", None),
    ("│       ├── partner-scorecard.md", "owns /partner-qbr", None),
    ("│       ├── partner-program.md", "owns tiers, benefits, priority motions", None),
    ("│       ├── partner-engagement.md", "owns /call-notes-to-jira", None),
    ("│       └── partner-planning.md", "planned — /quota-scenario proposed", None),
    ("├── .claude/", None, None),
    ("│   ├── settings.json", "scoped permissions — skills write only what their rock allows", None),
    ("│   ├── hooks/", None, None),
    ("│   │   ├── session_context.sh", "SessionStart: every session boots knowing the book", None),
    ("│   │   └── log_session.sh", "Stop: one line of evidence per session", None),
    ("│   ├── agents/", None, None),
    ("│   │   └── big-rock-planner.md", "subagent that drafts new rock plans", None),
    ("│   └── skills/", "one folder per skill, each owned by exactly one rock", "SKILLS"),
    ("│       ├── commissions-credit/", "headline: plain-English coverage → crediting rules", None),
    ("│       ├── call-notes-to-jira/", "call notes → tracked Jira tickets", None),
    ("│       ├── partner-qbr/", None, None),
    ("│       └── improve-setup/", "the meta-skill — the loop that edits everything above", None),
    ("├── notebooks/scorecard_refresh.ipynb", "analysis artifact: tier/health recompute", None),
    ("├── retros/", "the evidence stream the improvement loop reads", "RETROS"),
    ("│   ├── session-log.md", None, None),
    ("│   └── 2026-06-05-retro.md", "a completed improvement iteration", None),
    ("└── docs/claude-code-architecture.md", "the deep-dive on this whole setup", None),
]
tree_rows = []
for tree_path, tree_note, tree_layer in FOLDER_TREE:
    path_class = "tree-path dir" if tree_path.rstrip().endswith("/") else "tree-path"
    pill = f'<span class="layer-pill">{tree_layer}</span>' if tree_layer else ""
    note = f'<span class="tree-note">{tree_note}</span>' if tree_note else ""
    tree_rows.append(f'<div class="tree-row"><span class="{path_class}">{tree_path}</span>{pill}{note}</div>')
st.markdown(f'<div class="tree-card">{"".join(tree_rows)}</div>', unsafe_allow_html=True)


# =============================================================================
# THE SHARED VOCABULARY (GLOSSARY)
# =============================================================================

st.markdown("### One dictionary the whole instance reads from")
st.markdown(
    "The DATA layer isn't just numbers — it's the shared language. The roles, the way "
    "the book is sliced, and every metric are each defined exactly once, so a skill never "
    "guesses what “attributed revenue” means and no two briefs disagree."
)

ROLES = [
    ("PSM", "Partner Sales Manager",
     "Quota-carrying co-sell seller. Owns partner-sourced pipeline and revenue for their "
     "territory — credited on the <em>revenue</em> line."),
    ("PAM", "Partner Account Manager",
     "Owns the partner <em>relationship</em>: enablement, certifications, QBRs, health — "
     "credited on the <em>coverage</em> line, not on sourced revenue."),
]
role_cards = "".join(
    f'<div class="gloss-card"><div class="gloss-term"><span class="abbr">{abbr}</span> — {full}</div>'
    f'<div class="gloss-def">{desc}</div></div>'
    for abbr, full, desc in ROLES
)
st.markdown(f'<div class="gloss-grid">{role_cards}</div>', unsafe_allow_html=True)

METRICS = [
    ("Sourced revenue", "FY26 closed-won on deals the partner originated (first touch). Credited at 100%."),
    ("Influenced revenue", "FY26 closed-won the partner touched but didn't source. Earns partial, role-weighted credit."),
    ("Attributed revenue", "Sourced at 100% plus the partner's role-weighted share of influenced — the headline number tiers and comp run on."),
    ("Sourced pipeline", "Open pipeline where the partner is the originating source."),
    ("Deal regs (approved)", "Registrations that passed conflict review: a 90-day protection window plus the tier's deal-reg margin."),
    ("Partner Value Score", "0–100 composite of revenue, deal-reg discipline, technical capacity, and satisfaction. No single dimension can buy a tier."),
    ("Tier", "Strategic / Premier / Select, derived from the Partner Value Score — sets benefits and coverage."),
]
metric_rows = "".join(
    f'<tr><td class="metric-name">{name}</td><td>{desc}</td></tr>' for name, desc in METRICS
)
st.markdown(
    f'<div class="metric-wrap"><table class="metric-table">'
    f'<thead><tr><th>Metric</th><th>What it means</th></tr></thead>'
    f'<tbody>{metric_rows}</tbody></table></div>',
    unsafe_allow_html=True,
)
st.caption("Full schema, formulas, and ownership live in data/DATA_DICTIONARY.md — a definition changes there first, then propagates everywhere.")


# =============================================================================
# WHY IT'S BUILT THIS WAY
# =============================================================================

st.markdown("### Why it's built this way")
st.markdown(
    "Three decisions do the heavy lifting — each trades a little up-front structure for "
    "compounding leverage."
)

WHY = [
    ("Define once, reuse everywhere",
     "One dictionary, one set of rules. Skills read definitions instead of re-deriving "
     "them — so the math is consistent and auditable, and a change lands in one place "
     "and updates every output."),
    ("Keep the model out of the money",
     "The model authors rules in plain English; deterministic, tested code applies them. "
     "The judgment that matters is knowing which work is a call for the model and which is "
     "math to encode once and test — the speed of language with the trust of a "
     "spreadsheet that can't silently miscount."),
    ("A system that improves itself",
     "Every session leaves evidence, and a retro loop turns that evidence into edits to "
     "the setup. The instance gets sharper with use instead of drifting out of date."),
]
why_cols = st.columns(3)
for col, (why_title, why_desc) in zip(why_cols, WHY):
    with col:
        st.markdown(f"""
        <div class="experience-card" style="min-height: 190px;">
            <strong style="color: #D97757;">{why_title}</strong>
            <p style="font-size: 0.88rem; color: #4a4a4a; margin: 0.5rem 0 0 0; line-height: 1.55;">{why_desc}</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# WHEN A SKILL DOES THE WORK
# =============================================================================

st.markdown("### When a skill does the work")
st.markdown(
    "Each skill exists because a recurring ask kept eating someone's week. Here's the "
    "moment each one is for."
)

SKILL_MOMENTS = [
    ("/commissions-credit", "live in this repo",
     "A rep joins mid-quarter, or a territory changes hands",
     "The headline system. A manager edits the coverage sheet in plain English — "
     "“Maria takes over the SMB book from Sam on March 15.” The skill codifies that into "
     "effective-dated crediting rules, resolving the handoff so there's no gap and no "
     "double-coverage. The money math itself is deterministic, tested code — no model "
     "credits a deal — so when finance runs actuals the right person lands on the right "
     "line for the right months, and any uncredited deal is surfaced, never zeroed."),
    ("/next-best-action", "org scale",
     "A PSM or PAM starts the week asking “where do I spend my time?”",
     "Reads the seller's book and ranks the next moves: deals blocked on a missing "
     "certification or a stalled registration, partner relationships that map into open "
     "pipeline, accounts where a partner already has a foothold. PSMs and PAMs don't want "
     "another dashboard — they want the next action with a reason attached."),
    ("/partner-qbr", "live in this repo",
     "QBR season — the org-wide review, a regional cut, or a partner asking for one",
     "QBRs here aren't a per-partner cadence with an “overdue” clock. They run for the "
     "whole org, sometimes cut by region, occasionally for a single partner who requests "
     "one. The skill pulls the data cut for whatever slice the review covers, using the "
     "dictionary's definitions so every brief reads the same."),
    ("/call-notes-to-jira", "live in this repo",
     "A partner call wraps and the follow-ups are buried in someone's notes",
     "Turns raw call notes into tracked Jira tickets — a stalled deal-reg to chase, a "
     "missing certification to schedule, an exec intro to tee up — each tagged to the "
     "partner and the owning rep, so nothing from the conversation dies in a doc."),
    ("/improve-setup", "live in this repo",
     "The same ask shows up three sessions in a row",
     "The meta-skill. It reads the session log and git history, spots recurring work with "
     "no owning skill, and proposes the next one as a diff to the plans — that's how "
     "skills like /next-best-action earn their way into the catalog."),
]

for skill_cmd, skill_tag, skill_when, skill_how in SKILL_MOMENTS:
    tag_class = "live" if skill_tag.startswith("live") else "org"
    st.markdown(f"""
    <div class="skill-card">
        <div class="skill-cmd-col">
            <div class="skill-cmd">{skill_cmd}</div>
            <span class="skill-tag {tag_class}">{skill_tag}</span>
        </div>
        <div>
            <div class="skill-when">{skill_when}</div>
            <div class="skill-how">{skill_how}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("Four of the five ship in this repo's .claude/skills/ — open any SKILL.md to see the inputs, steps, and guardrails. /commissions-credit is the one to read first: the AI authors the rules, crediting/engine.py does the money math, and tests/ pins it. /next-best-action sketches the same pattern at org scale.")


# =============================================================================
# ENABLEMENT — THE OPS TEAM WENT FIRST
# =============================================================================

st.markdown("### Enablement: our own strategy and ops team went first")
st.markdown("""
<div class="narrative-quote">
The adoption unlock wasn't a training deck — it was the strategy and ops team
self-serving. When the people who used to field the data requests started pulling
their own cuts, the request queue shrank and the GTM teams followed.
</div>
""", unsafe_allow_html=True)

enable_cols = st.columns(2)
ENABLEMENT = [
    ("From ticket to command",
     "QBR data pulls used to be a request to analytics and a few days' wait. Now an ops "
     "lead scopes /partner-qbr to their own area of the business — a region, a segment, "
     "a motion — and pulls the cut themselves, in the dictionary's definitions, in one "
     "command."),
    ("From operators to authors",
     "Once the team was self-serving, they stopped asking for tools and started proposing "
     "them — new skills sketched directly in the plans, refined by the retro loop. The "
     "system grew from inside the team that runs it, which is the only way these things "
     "stick."),
]
for col, (enable_title, enable_desc) in zip(enable_cols, ENABLEMENT):
    with col:
        st.markdown(f"""
        <div class="experience-card" style="min-height: 190px;">
            <strong style="color: #D97757;">{enable_title}</strong>
            <p style="font-size: 0.88rem; color: #4a4a4a; margin: 0.5rem 0 0 0; line-height: 1.55;">{enable_desc}</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 0.8rem 0; color: #999; font-size: 0.85rem;">
    Dylan Ram · Built with Claude Code · 2026
</div>
""", unsafe_allow_html=True)
