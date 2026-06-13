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

    /* --- Responsive: stack the wide rows so it reads top-to-bottom on phones --- */
    @media (max-width: 820px) {
        .layer-row { flex-direction: column; gap: 0.6rem; }
        .layer-arrow { transform: rotate(90deg); padding: 0.1rem 0; align-self: center; }
        .layer-desc { flex: none; }
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
        Not dashboards — an operating system: the context Claude boots with,
        the structure it lives in, and the moments a skill does the work.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        Dylan Ram &nbsp;·&nbsp; Partnerships GTM &nbsp;·&nbsp;
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#fdf6f2; border:1px solid rgba(217,119,87,0.35); border-radius:8px;
            padding:0.85rem 1.1rem; margin:0.5rem 0 1.2rem 0; color:#7a5c4f;
            font-size:0.86rem; line-height:1.5; text-align:center;">
    <strong style="color:#c4624a;">Concept mockup.</strong> This is a personal portfolio
    concept by Dylan Ram, built to illustrate an idea. It is not an Anthropic product and is
    not affiliated with, endorsed by, or representative of Anthropic. All data is synthetic,
    and "Claude" / "Claude Code" are referenced illustratively.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="narrative-quote">
This page is its own reference implementation. Every layer, file, and skill described
below exists in the repo this page is served from — the point isn't the numbers a
partner org produces, it's the engineering that lets a GTM ops team produce them
with AI doing the recurring work.
</div>
""", unsafe_allow_html=True)


# =============================================================================
# THE CONTEXT LAYERS
# =============================================================================

st.markdown("### The five layers of context")
st.markdown(
    "Everything a session knows comes from one of these layers. Read left to right: "
    "governed data at the bottom of the stack, a self-editing loop at the top."
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

st.markdown("### The same five layers, on disk")
st.markdown(
    "This is the actual folder structure of the instance — not a mockup of one. "
    "Every layer above is a path you can open."
)

FOLDER_TREE = [
    ("partner-ops/", None, None),
    ("├── CLAUDE.md", "operating model + domain glossary (who a PSM/PAM is)", "MEMORY"),
    ("├── app.py", "this walkthrough page", None),
    ("├── data/", None, "DATA"),
    ("│   ├── partner_metrics.csv", "the gold table: revenue splits, deal regs, PVS, health", None),
    ("│   ├── coverage_assignments.csv", "the plain-English coverage sheet (the “Google Sheet”)", None),
    ("│   ├── crediting_rules.json", "codified crediting rules — output of /commissions-credit", None),
    ("│   ├── commission_deals.csv", "closed deals actuals run against", None),
    ("│   ├── DATA_DICTIONARY.md", "one definition per metric + every schema above", None),
    ("│   └── sample_data.py", "the attribution deal fixture", None),
    ("├── crediting/", "deterministic, tested money path — no LLM credits a deal", "DATA"),
    ("│   └── engine.py", "applies rules → who is credited, which line, which month", None),
    ("├── tests/", "golden tests / evals that pin the crediting math", None),
    ("│   └── test_crediting.py", "handoffs, mid-quarter hires, splits, coverage gaps", None),
    ("├── plans/", None, None),
    ("│   └── big-rocks/", "one living plan per strategic initiative ↔ Jira epic", "PLANS"),
    ("│       ├── 00-INDEX.md", "lifecycle rules + the plan template", None),
    ("│       ├── partner-compensation.md", "owns /commissions-credit + the crediting engine", None),
    ("│       ├── partner-attribution.md", "owns /attribution-compare + canonical model weights", None),
    ("│       ├── partner-scorecard.md", "owns /partner-qbr", None),
    ("│       ├── partner-program.md", "owns tiers, benefits, priority motions", None),
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
    ("│       ├── attribution-compare/", None, None),
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
st.caption("Identical shape at org scale: swap the CSV for Unity Catalog gold tables and point the team's shared instance at the same repo — the memory, plans, skills, and retro loop don't change.")


# =============================================================================
# WHEN A SKILL DOES THE WORK
# =============================================================================

st.markdown("### When you reach for a skill")
st.markdown(
    "Skills aren't features — each one exists because a recurring ask kept eating "
    "someone's week. These are the moments you actually use one."
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
    ("/attribution-compare", "live in this repo",
     "Two partners claim credit on the same deal",
     "Runs the deal through the credit models defined in the attribution plan and shows "
     "how the split swings by model. The weights live in the plan, not the prompt — so "
     "the argument is about which model, never about the math."),
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

st.caption("Four of the five ship in this repo's .claude/skills/ — open any SKILL.md to see the inputs, steps, and guardrails. /commissions-credit is the one to read first: the AI authors the rules, crediting/engine.py does the money math, and tests/ pins it. /next-best-action follows the identical pattern at org scale.")


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
        <div class="experience-card" style="min-height: 170px;">
            <strong style="color: #D97757;">{enable_title}</strong>
            <p style="font-size: 0.9rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{enable_desc}</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 0.8rem 0; color: #999; font-size: 0.85rem;">
    Dylan Ram · Built with Claude Code · 2026<br>
    <span style="font-size: 0.78rem;">
        Personal concept mockup — not an Anthropic product, and not affiliated with or
        endorsed by Anthropic. Synthetic data throughout.
    </span>
</div>
""", unsafe_allow_html=True)
