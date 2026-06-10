"""
The AI-First Partner Org — a visual walkthrough.
The page describes an agentic AI operating system; the repo it lives in IS that system.
"""

import re
from datetime import datetime
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.sample_data import ATTRIBUTION_MODELS

REPO_ROOT = Path(__file__).parent
REPO_URL = "https://github.com/dylan3796/anthropic-portfolio"
ACCENT = "#D97757"

st.set_page_config(
    page_title="Dylan Ram | The AI-First Partner Org",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #FAFAF9; }

    .main .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1 { color: #1a1a1a; font-weight: 600; letter-spacing: -0.02em; }
    h2 { color: #2d2d2d; font-weight: 500; margin-top: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e5e5e5; }
    h3 { color: #3d3d3d; font-weight: 500; }
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

    .metric-highlight { text-align: center; padding: 0.8rem; }
    .metric-number { font-size: 2.4rem; font-weight: 600; color: #D97757; line-height: 1.1; }
    .metric-label { color: #666; font-size: 0.88rem; margin-top: 0.3rem; }

    .stTabs [data-baseweb="tab"] {
        font-size: 1.05rem;
        font-weight: 500;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .streamlit-expanderHeader { background-color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DATA HELPERS — everything below reads the repo's real files at runtime
# =============================================================================

def _parse_frontmatter(path):
    """Pull simple `key: value` frontmatter fields from a markdown file."""
    fields = {}
    try:
        text = path.read_text()
    except OSError:
        return fields
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    block = match.group(1) if match else text
    for key in ("name", "description", "status", "horizon", "owned-skills", "allowed-tools"):
        found = re.search(rf"^{key}:\s*(.+)$", block, re.MULTILINE)
        if found:
            fields[key] = found.group(1).strip()
    return fields


def load_claude_setup():
    """Parse this repo's actual .claude/ skills and big-rock plans at runtime."""
    skills, rocks, skill_owner = [], [], {}
    for rock_path in sorted((REPO_ROOT / "plans" / "big-rocks").glob("*.md")):
        if rock_path.name == "00-INDEX.md":
            continue
        fm = _parse_frontmatter(rock_path)
        owned = fm.get("owned-skills", "")
        rocks.append({
            "Big Rock": rock_path.stem,
            "Status": fm.get("status", "?"),
            "Horizon": fm.get("horizon", "?"),
            "Owned Skills": owned,
        })
        for skill_name in owned.split(","):
            skill_name = skill_name.strip()
            if skill_name and skill_name != "none yet":
                skill_owner[skill_name] = rock_path.stem
    for skill_path in sorted((REPO_ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        fm = _parse_frontmatter(skill_path)
        name = fm.get("name", skill_path.parent.name)
        skills.append({
            "Skill": f"/{name}",
            "Owning Big Rock": skill_owner.get(name, "meta — the setup itself"),
            "Allowed Tools": fm.get("allowed-tools", ""),
            "Description": fm.get("description", ""),
        })
    return skills, rocks


def load_partner_metrics():
    try:
        return pd.read_csv(REPO_ROOT / "data" / "partner_metrics.csv")
    except OSError:
        return pd.DataFrame()


def _chart_layout(fig, height=300):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a4a4a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


metrics_df = load_partner_metrics()


# =============================================================================
# HERO
# =============================================================================

st.markdown("""
<div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
    <h1 style="font-size: 2.9rem; margin-bottom: 0.5rem; border: none;">The AI-First Partner Org</h1>
    <p style="font-size: 1.15rem; color: #666; margin-bottom: 0.4rem;">
        How I run partnerships as an operating system — agentic AI under the hood, GTM on the surface.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        Dylan Ram &nbsp;·&nbsp; GTM Strategy & Ops &nbsp;·&nbsp;
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

if not metrics_df.empty:
    live_partners = len(metrics_df)
    live_revenue = f"${metrics_df['attributed_revenue_fy26'].sum() / 1e6:.1f}M"
else:
    live_partners, live_revenue = "—", "—"

hero_cols = st.columns(4)
HERO_STATS = [
    ("3 days → 20 min", "QBR prep, before → after"),
    ("0", "analyst queue for recurring asks"),
    (live_revenue, "partner book, parsed live from the gold layer"),
    (f"{live_partners} / 4", "partners tracked / skills shipped"),
]
for col, (stat, label) in zip(hero_cols, HERO_STATS):
    with col:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="metric-number">{stat}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.caption("Impact figures illustrative; partner data synthetic. The operating system is real — this page parses its own repo at runtime.")

tab_goals, tab_setup, tab_playbook, tab_enable = st.tabs(["  Goals  ", "  Setup  ", "  The Playbook  ", "  Enablement  "])


# =============================================================================
# TAB 1 — GOALS
# =============================================================================

with tab_goals:
    st.markdown("""
    <div class="narrative-quote">
    Three goals. Governed self-serve analytics — anyone gets a trusted answer without an analyst.
    GTM motions that run themselves — QBRs, scorecards, attribution as one-command skills.
    And a setup that compounds — the system rewrites itself as the business changes.
    </div>
    """, unsafe_allow_html=True)

    goal_cols = st.columns(3)
    GOALS = [
        ("Self-serve analytics", "Every metric has one definition. Every session boots knowing the business. Nobody waits in a queue to learn their own partner's health."),
        ("AI embedded in the motion", "Attribution, scorecards, QBRs, and planning aren't dashboards someone checks — they're skills the team invokes mid-workflow."),
        ("A system that compounds", "Most AI rollouts decay after the demo. This one runs retros on itself and ships its own improvements — it gets better every month."),
    ]
    for col, (goal_title, goal_desc) in zip(goal_cols, GOALS):
        with col:
            st.markdown(f"""
            <div class="experience-card" style="min-height: 175px;">
                <strong style="color: #D97757;">{goal_title}</strong>
                <p style="font-size: 0.88rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{goal_desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### What that buys back")

    DELIVERABLES = ["Quota scenario", "Attribution analysis", "Scorecard refresh", "QBR brief"]
    HOURS_BEFORE = [16, 8, 6, 12]
    HOURS_AFTER = [1.5, 0.5, 0.2, 0.3]

    fig_hours = go.Figure()
    fig_hours.add_trace(go.Bar(
        y=DELIVERABLES, x=HOURS_BEFORE, name="Manual (before)",
        orientation="h", marker_color="#d9d4cf",
        text=[f"{h}h" for h in HOURS_BEFORE], textposition="outside",
    ))
    fig_hours.add_trace(go.Bar(
        y=DELIVERABLES, x=HOURS_AFTER, name="With the OS (skill run + review)",
        orientation="h", marker_color=ACCENT,
        text=[f"{h}h" for h in HOURS_AFTER], textposition="outside",
    ))
    fig_hours.update_layout(barmode="group", xaxis_title="hours per deliverable")
    st.plotly_chart(_chart_layout(fig_hours, height=320), use_container_width=True)
    st.caption("Illustrative, based on typical partner-ops cycle times. The point isn't the hours — it's that the senior team stops being the bottleneck for its own data.")


# =============================================================================
# TAB 2 — SETUP
# =============================================================================

with tab_setup:
    st.markdown("""
    <div class="narrative-quote">
    Read it bottom-up: data you can trust, context that's always loaded, plans tied to the epics
    the team already runs, skills that do the work, and retros that rewrite the system itself.
    </div>
    """, unsafe_allow_html=True)

    # --- Architecture diagram (plotly shapes) ---
    LAYERS = [
        ("DATA", "gold tables +<br>metric dictionary"),
        ("MEMORY", "context every<br>session boots with"),
        ("PLANS", "big rocks ↔<br>Jira epics"),
        ("SKILLS", "the playbook,<br>invocable"),
        ("RETROS", "the OS<br>edits itself"),
    ]
    BOX_W, GAP = 1.6, 0.45
    fig_arch = go.Figure()
    for i, (layer_title, layer_sub) in enumerate(LAYERS):
        x0 = i * (BOX_W + GAP)
        fig_arch.add_shape(
            type="rect", x0=x0, y0=0, x1=x0 + BOX_W, y1=1,
            line=dict(color="#e5e5e5", width=1), fillcolor="white",
        )
        fig_arch.add_shape(
            type="rect", x0=x0, y0=0.97, x1=x0 + BOX_W, y1=1,
            line=dict(color=ACCENT, width=1), fillcolor=ACCENT,
        )
        fig_arch.add_annotation(x=x0 + BOX_W / 2, y=0.66, text=f"<b>{layer_title}</b>",
                                showarrow=False, font=dict(color=ACCENT, size=16))
        fig_arch.add_annotation(x=x0 + BOX_W / 2, y=0.3, text=layer_sub,
                                showarrow=False, font=dict(color="#4a4a4a", size=11))
        if i < len(LAYERS) - 1:
            fig_arch.add_annotation(x=x0 + BOX_W + GAP / 2, y=0.5, text="→",
                                    showarrow=False, font=dict(color=ACCENT, size=24))
    last_mid = 4 * (BOX_W + GAP) + BOX_W / 2
    fig_arch.add_shape(
        type="path",
        path=f"M {last_mid},1.08 C {last_mid - 2.5},1.95 2.8,1.95 {BOX_W / 2 + 0.25},1.18",
        line=dict(color=ACCENT, width=2, dash="dot"),
    )
    fig_arch.add_annotation(x=BOX_W / 2, y=1.1, ax=BOX_W / 2 + 0.55, ay=1.4,
                            axref="x", ayref="y", showarrow=True,
                            arrowhead=2, arrowsize=1.3, arrowcolor=ACCENT, text="")
    fig_arch.add_annotation(x=(last_mid + BOX_W / 2) / 2, y=1.78,
                            text="<i>/improve-setup — approved edits flow back into every layer</i>",
                            showarrow=False, font=dict(color="#999", size=12))
    fig_arch.update_xaxes(visible=False, range=[-0.2, last_mid + BOX_W / 2 + 0.2])
    fig_arch.update_yaxes(visible=False, range=[-0.1, 2.05])
    st.plotly_chart(_chart_layout(fig_arch, height=290), use_container_width=True,
                    config={"displayModeBar": False, "staticPlot": True})

    # --- Data layer: medallion + live gold scatter ---
    med_col, gold_col = st.columns([2, 3])

    with med_col:
        st.markdown("#### It starts with data")
        fig_med = go.Figure(go.Funnel(
            y=["Bronze · raw CRM & PRM exports", "Silver · cleaned, conformed", "Gold · partner_metrics", "Dictionary · one definition per metric"],
            x=[100, 65, 35, 18],
            marker=dict(color=["#b08d57", "#b9b9b9", "#d4af37", ACCENT]),
            textinfo="none",
            connector=dict(line=dict(color="#e5e5e5")),
        ))
        fig_med.update_layout(showlegend=False)
        st.plotly_chart(_chart_layout(fig_med, height=270), use_container_width=True,
                        config={"displayModeBar": False, "staticPlot": True})
        st.caption("Medallion architecture: agents only ever read gold + the dictionary. No model is asked to guess what a metric means.")

    with gold_col:
        st.markdown("#### The gold layer, live")
        if not metrics_df.empty:
            fig_gold = px.scatter(
                metrics_df,
                x="sourced_pipeline", y="attributed_revenue_fy26",
                size="certified_engineers", color="health_flag",
                hover_name="partner_name",
                color_discrete_map={"green": "#6aa84f", "yellow": "#e6b84a", "red": "#cc4125"},
                labels={"sourced_pipeline": "sourced pipeline", "attributed_revenue_fy26": "FY26 attributed revenue", "health_flag": "health"},
            )
            fig_gold.update_xaxes(tickformat="$.2s")
            fig_gold.update_yaxes(tickformat="$.2s")
            st.plotly_chart(_chart_layout(fig_gold, height=300), use_container_width=True)
            st.caption("Rendered from data/partner_metrics.csv at runtime — the same file the skills read. Bubble size = certified engineers.")
        else:
            st.info("Gold layer not present in this deployment.")

    # --- Plans: roadmap ---
    st.markdown("#### Plans are the roadmap — one big rock per Jira epic")
    roadmap = pd.DataFrame([
        dict(Rock="Partner Attribution", Start="2026-02-01", Finish="2026-07-31", Status="active"),
        dict(Rock="Partner Scorecard", Start="2026-03-01", Finish="2026-08-31", Status="active"),
        dict(Rock="Partner Planning", Start="2026-08-01", Finish="2027-01-31", Status="planned"),
    ])
    fig_road = px.timeline(
        roadmap, x_start="Start", x_end="Finish", y="Rock", color="Status",
        color_discrete_map={"active": ACCENT, "planned": "#d9c2b8"},
    )
    fig_road.update_yaxes(autorange="reversed", title="")
    fig_road.add_vline(x=datetime(2026, 6, 10), line_dash="dot", line_color="#999")
    fig_road.add_annotation(x=datetime(2026, 6, 10), y=-0.7, text="today", showarrow=False, font=dict(color="#999", size=11))
    st.plotly_chart(_chart_layout(fig_road, height=230), use_container_width=True,
                    config={"displayModeBar": False})
    st.caption("Each bar is a living plan doc: milestones, open questions, owned skills, and an improvement log. Status syncs with the epic — not a second process.")

    # --- Skills: live demo ---
    st.markdown("#### A skill in action: `/attribution-compare`")
    st.markdown("How should $150,000 of partner-influenced revenue be credited? Pick a model — this is the live output of the skill the attribution plan owns.")

    selected_model = st.selectbox("Attribution model", list(ATTRIBUTION_MODELS.keys()), index=2)
    model_data = ATTRIBUTION_MODELS[selected_model]
    st.info(model_data["description"])

    results_df = pd.DataFrame([{"Partner": k, "Attribution": v} for k, v in model_data["results"].items()])
    fig_attr = go.Figure(go.Bar(
        x=results_df["Attribution"], y=results_df["Partner"], orientation="h",
        marker=dict(color=results_df["Attribution"],
                    colorscale=[[0, "#fde8e0"], [0.5, "#e89b7b"], [1, ACCENT]], showscale=False),
        text=results_df["Attribution"].apply(lambda x: f"${x:,.0f}"), textposition="outside",
    ))
    fig_attr.update_layout(xaxis=dict(range=[0, max(results_df["Attribution"]) * 1.2], title="attributed revenue"))
    st.plotly_chart(_chart_layout(fig_attr, height=240), use_container_width=True)
    st.caption("Model weights live in the attribution plan — one source of truth. The skill computes; it doesn't decide.")

    with st.expander("**Proof: the live registry** — parsed from this repo's actual files, not hardcoded"):
        setup_skills, setup_rocks = load_claude_setup()
        if setup_skills or setup_rocks:
            reg_col1, reg_col2 = st.columns([1, 1])
            with reg_col1:
                st.dataframe(pd.DataFrame(setup_rocks), hide_index=True, use_container_width=True)
            with reg_col2:
                st.dataframe(pd.DataFrame(setup_skills), hide_index=True, use_container_width=True)
        else:
            st.info(f"Setup files not present in this deployment — browse them on [GitHub]({REPO_URL}).")
        st.markdown(f"Inspect the implementation: [CLAUDE.md]({REPO_URL}/blob/main/CLAUDE.md) · [settings.json]({REPO_URL}/blob/main/.claude/settings.json) · [architecture deep-dive]({REPO_URL}/blob/main/docs/claude-code-architecture.md)")


# =============================================================================
# TAB 3 — THE PLAYBOOK (a partner program, fully built out)
# =============================================================================

with tab_playbook:
    st.markdown("""
    <div class="narrative-quote">
    Here's how I'd build it out for a Databricks-scale partner program. Every motion becomes a
    rock. Every recurring deliverable becomes a skill. Every signal becomes a trigger. This repo
    ships the first two rocks live — the rest is the same pattern, repeated.
    </div>
    """, unsafe_allow_html=True)

    # --- Rock & skill catalog as a treemap ---
    st.markdown("#### The full catalog: six rocks, fourteen skills")

    CATALOG = {
        "Attribution": ["/attribution-compare", "/credit-dispute"],
        "Scorecard & QBRs": ["/partner-qbr", "/scorecard-refresh", "/health-digest"],
        "Planning": ["/quota-scenario", "/territory-overlap"],
        "Co-sell & Marketplace": ["/co-sell-brief", "/marketplace-audit"],
        "Enablement & Certs": ["/cert-gap", "/enablement-plan"],
        "Exec Reporting": ["/partner-newsletter", "/board-snapshot", "/win-story"],
    }
    tm_names, tm_parents = [], []
    for rock, rock_skills in CATALOG.items():
        tm_names.append(rock)
        tm_parents.append("Partner Program OS")
        for s in rock_skills:
            tm_names.append(s)
            tm_parents.append(rock)
    tm_names.append("Partner Program OS")
    tm_parents.append("")

    fig_catalog = px.treemap(
        names=tm_names, parents=tm_parents,
        color_discrete_sequence=["#D97757", "#c4624a", "#e89b7b", "#b08d57", "#d4af37", "#a9745d"],
    )
    fig_catalog.update_traces(
        root_color="#FAFAF9",
        marker=dict(cornerradius=4),
        textfont=dict(size=15),
    )
    st.plotly_chart(_chart_layout(fig_catalog, height=380), use_container_width=True,
                    config={"displayModeBar": False})
    st.caption("Attribution and Scorecard ship live in this repo. The other four rocks follow the identical pattern: a plan doc against the Jira epic, skills proposed in the plan before they're built.")

    # --- The skills, what they do ---
    skill_detail = pd.DataFrame([
        {"Skill": "/attribution-compare", "Rock": "Attribution", "What it does": "Runs any deal through six credit models, recommends one, flags >2x swings"},
        {"Skill": "/credit-dispute", "Rock": "Attribution", "What it does": "Pulls the touchpoint ledger for a disputed deal and drafts the resolution memo"},
        {"Skill": "/partner-qbr", "Rock": "Scorecard & QBRs", "What it does": "Benchmark-backed QBR brief for any partner in seconds — snapshot, risks, asks"},
        {"Skill": "/scorecard-refresh", "Rock": "Scorecard & QBRs", "What it does": "Recomputes tiers and health flags from dictionary thresholds; writes only on approval"},
        {"Skill": "/health-digest", "Rock": "Scorecard & QBRs", "What it does": "Monday-morning digest: flag changes, QBRs overdue, partners trending down"},
        {"Skill": "/quota-scenario", "Rock": "Planning", "What it does": "FY quota drafts under bear / base / bull growth cases, from trailing attribution"},
        {"Skill": "/territory-overlap", "Rock": "Planning", "What it does": "Flags partners competing for the same accounts before it becomes a channel conflict"},
        {"Skill": "/co-sell-brief", "Rock": "Co-sell & Marketplace", "What it does": "One-pager before any joint account call: history, attribution, open pipeline, talk track"},
        {"Skill": "/marketplace-audit", "Rock": "Co-sell & Marketplace", "What it does": "Sweeps partner listings for stale pricing, broken links, expired certifications"},
        {"Skill": "/cert-gap", "Rock": "Enablement & Certs", "What it does": "Which partners fall below cert thresholds next quarter — and what it costs their tier"},
        {"Skill": "/enablement-plan", "Rock": "Enablement & Certs", "What it does": "Per-partner ramp plan tied to the capacity model, not a generic curriculum"},
        {"Skill": "/partner-newsletter", "Rock": "Exec Reporting", "What it does": "Drafts the monthly partner newsletter from the gold layer — numbers always match the scorecard"},
        {"Skill": "/board-snapshot", "Rock": "Exec Reporting", "What it does": "Board-ready partner slide: sourced %, top movers, risks — same definitions, every time"},
        {"Skill": "/win-story", "Rock": "Exec Reporting", "What it does": "Turns a closed-won deal into a co-marketing-ready win story with verified figures"},
    ])
    with st.expander("**Every skill, one line each**"):
        st.dataframe(skill_detail, hide_index=True, use_container_width=True)

    # --- Triggers: the nervous system ---
    st.markdown("#### The triggers: what makes it self-improving")
    st.markdown("Skills are the muscles; triggers are the nervous system. Each one turns a business signal into either immediate context or retro evidence.")

    triggers = pd.DataFrame([
        {"Trigger": "Session starts", "Fires": "Hook injects rock statuses + scorecard headlines", "So that": "No session ever starts cold", "Status": "live in this repo"},
        {"Trigger": "Session ends", "Fires": "Hook appends one line to the session log", "So that": "The retro has evidence, not anecdotes", "Status": "live in this repo"},
        {"Trigger": "Gold table written", "Fires": "Health rules re-run; deltas posted to the scorecard plan", "So that": "A partner going red is noticed the day it happens", "Status": "org scale"},
        {"Trigger": "QBR overdue >120 days", "Fires": "/health-digest escalates; QBR milestone opens on the plan", "So that": "Coverage gaps surface before the partner churns", "Status": "org scale"},
        {"Trigger": "Quarter close", "Fires": "Scorecard snapshots; /quota-scenario pre-runs the planning cases", "So that": "Planning starts from data, not negotiation", "Status": "org scale"},
        {"Trigger": "Monthly retro", "Fires": "/improve-setup reads logs + plans, proposes diff-style edits", "So that": "The system rewrites itself as the business changes", "Status": "live in this repo"},
    ])
    st.dataframe(triggers, hide_index=True, use_container_width=True)

    # --- A quarter in the life ---
    st.markdown("#### A quarter in the life")

    STORY = [
        ("Week 1", "Monday's session opens with the hook already flagging it: Lakeshore Consulting is red — NPS 44, no QBR in 188 days. <code>/partner-qbr Lakeshore</code> drafts the brief before the coffee's done. QBR is on the calendar by Thursday."),
        ("Week 3", "An AE asks for joint-call prep on Northwind. Then again for Vector. Two near-identical asks, two sessions — nobody notices. The session log does."),
        ("Week 6", "First monthly retro. <code>/improve-setup</code> reads the log and calls it: 'co-sell prep requested 4x with no owning skill.' It proposes a new co-sell rock with <code>/co-sell-brief</code> as its first skill. Approved Tuesday, shipped Wednesday, demoed in Thursday's stand-up."),
        ("Week 9", "Quarter close fires: scorecard snapshots for QoQ deltas, and <code>/quota-scenario</code> pre-runs bear, base, and bull cases for the FY28 planning offsite. The debate is about strategy, not whose spreadsheet is right."),
        ("Week 12", "Retro #2 notices the partner newsletter still gets built by hand every month — proposes <code>/partner-newsletter</code> under exec reporting. The improvement logs now read like a changelog of the org getting faster."),
    ]
    for story_week, story_text in STORY:
        st.markdown(f"""
        <div class="experience-card" style="padding: 1rem 1.3rem; margin-bottom: 0.6rem;">
            <strong style="color: #D97757;">{story_week}</strong>
            <span style="font-size: 0.9rem; color: #4a4a4a;"> — {story_text}</span>
        </div>
        """, unsafe_allow_html=True)

    st.caption("Synthetic story, real mechanics: every beat above maps to a hook, a skill, or a retro that exists (or is templated) in this repo.")


# =============================================================================
# TAB 4 — ENABLEMENT
# =============================================================================

with tab_enable:
    st.markdown("""
    <div class="narrative-quote">
    Tools don't get adopted because they're good — they get adopted because they save someone's
    Tuesday. So enablement starts from the team's most-hated recurring task, not from a training deck.
    </div>
    """, unsafe_allow_html=True)

    ROLLOUT = [
        ("Day 1 · Bootstrap", "Stand up the repo: memory file, scoped permissions, hooks. The first session already knows the partner book."),
        ("Day 30 · First rock", "One initiative the team already cares about, planned against its existing Jira epic. A pilot pod of two, not a mandate."),
        ("Day 60 · Skills from real asks", "The three most-repeated requests become skills. Each one gets demoed in stand-up the week it ships — adoption follows saved time."),
        ("Day 90 · Compounding", "Monthly retro: the AI reads its own session logs and proposes upgrades. Self-serve becomes the default, not the exception."),
    ]
    rollout_cols = st.columns(4)
    for col, (phase_title, phase_desc) in zip(rollout_cols, ROLLOUT):
        with col:
            st.markdown(f"""
            <div class="experience-card" style="min-height: 195px;">
                <strong style="color: #D97757;">{phase_title}</strong>
                <p style="font-size: 0.85rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{phase_desc}</p>
            </div>
            """, unsafe_allow_html=True)

    curve_col, hours_col = st.columns([3, 2])

    with curve_col:
        st.markdown("#### Adoption follows demos, not mandates")
        weeks = list(range(1, 13))
        active_pct = [8, 14, 24, 31, 42, 58, 64, 70, 77, 83, 86, 88]
        fig_adopt = go.Figure(go.Scatter(
            x=weeks, y=active_pct, mode="lines+markers",
            line=dict(color=ACCENT, width=3), fill="tozeroy",
            fillcolor="rgba(217,119,87,0.12)",
        ))
        for wk, label in [(1, "pilot pod"), (3, "first stand-up demo"), (6, "retro #1 ships 2 skills"), (10, "self-serve is default")]:
            fig_adopt.add_annotation(x=wk, y=active_pct[wk - 1] + 9, text=label,
                                     showarrow=False, font=dict(size=11, color="#777"))
        fig_adopt.update_layout(xaxis_title="week", yaxis=dict(ticksuffix="%", range=[0, 105], title="team using skills weekly"))
        st.plotly_chart(_chart_layout(fig_adopt, height=300), use_container_width=True,
                        config={"displayModeBar": False})
        st.caption("Illustrative rollout curve. The inflection points are always the same: a demo that saves someone real time, and the first retro that visibly improves the system.")

    with hours_col:
        st.markdown("#### Hours returned per month")
        fig_saved = go.Figure(go.Bar(
            x=[22, 12, 9],
            y=["/partner-qbr", "/attribution-compare", "/scorecard-refresh"],
            orientation="h", marker_color=ACCENT,
            text=["22h", "12h", "9h"], textposition="outside",
        ))
        fig_saved.update_layout(xaxis=dict(range=[0, 26], title="hours / month, team-wide"))
        st.plotly_chart(_chart_layout(fig_saved, height=300), use_container_width=True,
                        config={"displayModeBar": False, "staticPlot": True})
        st.caption("Illustrative. /improve-setup doesn't save hours directly — it compounds the other three.")

    with st.expander("**How the recursion works** — the part most rollouts skip"):
        st.markdown(f"""
        1. **Evidence** — a Stop hook logs every session to `retros/session-log.md`.
        2. **Review** — the `/improve-setup` meta-skill reads the log, git history, and every plan,
           hunting for friction: repeated instructions, corrected skill output, stale milestones,
           recurring tasks with no owning skill.
        3. **Proposals** — it writes a dated retro with concrete, diff-style edits to the memory,
           skills, and plans. Nothing applies without approval.
        4. **Compounding** — approved edits land, each logged in the owning plan's Improvement Log.

        A completed iteration:
        [retros/2026-06-05-retro.md]({REPO_URL}/blob/main/retros/2026-06-05-retro.md) —
        three observations, two edits applied, one deferred into a new big rock.
        """)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 0.5rem 0; color: #666;">
    This page is its own reference implementation — every file it describes is in
    <a href="{REPO_URL}">the repo</a>.
</div>
<div style="text-align: center; padding: 0.8rem 0; color: #999; font-size: 0.85rem;">
    Dylan Ram · Built with Claude Code · 2026
</div>
""", unsafe_allow_html=True)
