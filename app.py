"""
The AI-First Partner Org — a visual walkthrough.
The page describes an agentic AI operating system for partnerships GTM;
the repo it lives in IS that system.
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
AS_OF = datetime(2026, 6, 10)  # snapshot date the synthetic book is built around

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

    .domain-kpi { font-size: 0.86rem; color: #4a4a4a; margin: 0.25rem 0; }
    .domain-kpi b { color: #1a1a1a; }

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
        Partner sales, partner management, and the partner program — one operating system, run on Claude.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        Dylan Ram &nbsp;·&nbsp; Partnerships GTM &nbsp;·&nbsp;
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

if not metrics_df.empty:
    live_attr = f"${metrics_df['attributed_revenue_fy26'].sum() / 1e6:.1f}M"
    live_sourced = f"${metrics_df['sourced_revenue_fy26'].sum() / 1e6:.1f}M"
    live_regs = f"{metrics_df['deal_regs_approved_fy26'].sum():,}"
    tier_counts = metrics_df["tier"].value_counts()
    live_tiers = " · ".join(str(tier_counts.get(t, 0)) for t in ["Strategic", "Premier", "Select"])
else:
    live_attr = live_sourced = live_regs = live_tiers = "—"

hero_cols = st.columns(4)
HERO_STATS = [
    (live_sourced, "FY26 partner-sourced revenue"),
    (live_attr, "FY26 attributed revenue, parsed live from the gold layer"),
    (live_regs, "deal registrations approved FY26"),
    (live_tiers, "Strategic · Premier · Select partners"),
]
for col, (stat, label) in zip(hero_cols, HERO_STATS):
    with col:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="metric-number">{stat}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.caption("Partner data synthetic; mechanics real — this page parses its own repo at runtime, the same files the skills read.")

tab_org, tab_setup, tab_playbook, tab_enable = st.tabs(["  The Partner Org  ", "  The Claude Setup  ", "  The Playbook  ", "  Enablement  "])


# =============================================================================
# TAB 1 — THE PARTNER ORG (three domains, their KPIs, and shifting priorities)
# =============================================================================

with tab_org:
    st.markdown("""
    <div class="narrative-quote">
    Partnerships GTM is three jobs that have to agree with each other. Partner sales closes
    revenue with partners and lives in deal registration. Partner management keeps the book
    healthy partner by partner. The partner program decides where every partner stands and
    what that standing is worth. Most orgs run them on three spreadsheets — here they run
    on one data layer, one set of definitions, one operating system.
    </div>
    """, unsafe_allow_html=True)

    if not metrics_df.empty:
        df = metrics_df
        total_sourced = df["sourced_revenue_fy26"].sum()
        total_influenced = df["influenced_revenue_fy26"].sum()
        total_attr = df["attributed_revenue_fy26"].sum()
        regs_sub = df["deal_regs_submitted_fy26"].sum()
        regs_app = df["deal_regs_approved_fy26"].sum()
        qbr_overdue = (AS_OF - pd.to_datetime(df["last_qbr_date"])).dt.days.gt(120).sum()
        reds = (df["health_flag"] == "red").sum()
        on_the_line = df["partner_value_score"].sub(40).abs().le(3).sum() + df["partner_value_score"].sub(70).abs().le(3).sum()

        DOMAINS = [
            ("Partner Sales",
             "Sourcing, co-sell, and the deal-registration desk. The questions are always the same: "
             "what did this partner source vs. influence, and is this reg clean?",
             [f"Sourced revenue FY26: <b>${total_sourced/1e6:.1f}M</b>",
              f"Influenced revenue FY26: <b>${total_influenced/1e6:.1f}M</b>",
              f"Deal regs: <b>{regs_app} approved</b> of {regs_sub} submitted ({regs_app/regs_sub:.0%})"],
             "/attribution-compare · /deal-reg-triage · /co-sell-brief"),
            ("Partner Management",
             "The named-account motion: QBRs, health, certifications, escalations. "
             "Every PSM conversation starts from the same scorecard, not a private spreadsheet.",
             [f"Book health: <b>{reds} red</b> of {len(df)} partners",
              f"QBRs overdue (>120 days): <b>{qbr_overdue}</b>",
              f"Median partner NPS: <b>{df['nps'].median():.0f}</b>"],
             "/partner-qbr · /scorecard-refresh · /health-digest"),
            ("Partner Program",
             "Where every partner stands and what it's worth: the Partner Value Score sets the "
             "tier, the tier sets benefits eligibility — deal-reg margin, MDF, co-sell SLA.",
             [f"Tier mix: <b>{live_tiers}</b> (Strategic · Premier · Select)",
              f"Median Partner Value Score: <b>{df['partner_value_score'].median():.0f}</b> / 100",
              f"Partners within ±3 pts of a tier line: <b>{on_the_line}</b>"],
             "/tier-review · /benefits-audit (proposed in the program plan)"),
        ]
        domain_cols = st.columns(3)
        for col, (dom_title, dom_desc, dom_kpis, dom_skills) in zip(domain_cols, DOMAINS):
            kpi_html = "".join(f'<div class="domain-kpi">{k}</div>' for k in dom_kpis)
            with col:
                st.markdown(f"""
                <div class="experience-card" style="min-height: 300px;">
                    <strong style="color: #D97757; font-size: 1.05rem;">{dom_title}</strong>
                    <p style="font-size: 0.84rem; color: #666; margin: 0.5rem 0 0.7rem 0;">{dom_desc}</p>
                    {kpi_html}
                    <p style="font-size: 0.78rem; color: #999; margin: 0.8rem 0 0 0;"><code>{dom_skills}</code></p>
                </div>
                """, unsafe_allow_html=True)
        st.caption("Every number above is computed from data/partner_metrics.csv at render time — the same gold table the skills read. Definitions in data/DATA_DICTIONARY.md.")

        sales_col, program_col = st.columns(2)

        with sales_col:
            st.markdown("#### Sourced vs. influenced, by partner")
            rev_df = df.sort_values("attributed_revenue_fy26", ascending=True)
            fig_rev = go.Figure()
            fig_rev.add_trace(go.Bar(
                y=rev_df["partner_name"], x=rev_df["sourced_revenue_fy26"],
                name="Sourced (100% credit)", orientation="h", marker_color=ACCENT,
            ))
            fig_rev.add_trace(go.Bar(
                y=rev_df["partner_name"], x=rev_df["influenced_revenue_fy26"],
                name="Influenced (partial credit via attribution)", orientation="h", marker_color="#d9c2b8",
            ))
            fig_rev.update_layout(barmode="stack", xaxis=dict(tickformat="$.2s", title="FY26 revenue"))
            st.plotly_chart(_chart_layout(fig_rev, height=380), use_container_width=True,
                            config={"displayModeBar": False})
            st.caption("The partner-sales ledger. Attributed revenue = sourced at 100% plus a Role-Weighted share of influenced — weights live in the attribution plan, not in anyone's head.")

        with program_col:
            st.markdown("#### Partner Value Score sets the tier")
            pvs_df = df.sort_values("partner_value_score", ascending=True)
            fig_pvs = go.Figure(go.Bar(
                y=pvs_df["partner_name"], x=pvs_df["partner_value_score"], orientation="h",
                marker_color=[{"Strategic": ACCENT, "Premier": "#e89b7b", "Select": "#d9d4cf"}[t] for t in pvs_df["tier"]],
                text=pvs_df["partner_value_score"], textposition="outside",
            ))
            fig_pvs.add_vline(x=40, line_dash="dot", line_color="#999",
                              annotation_text="Premier ≥ 40", annotation_font_size=11)
            fig_pvs.add_vline(x=70, line_dash="dot", line_color="#999",
                              annotation_text="Strategic ≥ 70", annotation_font_size=11)
            fig_pvs.update_layout(xaxis=dict(range=[0, 105], title="Partner Value Score (0–100)"), showlegend=False)
            st.plotly_chart(_chart_layout(fig_pvs, height=380), use_container_width=True,
                            config={"displayModeBar": False})
            st.caption("The program's spine: revenue 40 pts, deal regs 20, certified engineers 20, NPS 20 — capped so no single dimension buys a tier. Within ±3 of a line means tier review, not auto-move. Note Vector and Analytics sitting exactly on the Premier floor.")

        st.markdown("#### What a tier is worth")
        st.markdown(
            "Tiers only matter because benefits hang off them. This is the eligibility table the program owns — "
            "when partner sales asks \"what margin does this reg get?\" or a partner asks \"why fund their MDF and not ours?\", "
            "the answer comes from here, traced to the score."
        )
        benefits = pd.DataFrame([
            {"Benefit": "Deal-reg margin on approved regs", "Strategic": "20%", "Premier": "15%", "Select": "10%"},
            {"Benefit": "Market development funds (annual)", "Strategic": "$150,000", "Premier": "$50,000", "Select": "—"},
            {"Benefit": "Partner manager coverage", "Strategic": "named PSM", "Premier": "pooled PSM", "Select": "portal-led"},
            {"Benefit": "Co-sell desk SLA", "Strategic": "24 hours", "Premier": "72 hours", "Select": "best effort"},
            {"Benefit": "Certification vouchers (annual)", "Strategic": "40", "Premier": "15", "Select": "5"},
            {"Benefit": "Product roadmap briefings", "Strategic": "quarterly", "Premier": "semi-annual", "Select": "—"},
        ])
        st.dataframe(benefits, hide_index=True, use_container_width=True)

        st.markdown("#### Priorities change — the system absorbs the change")
        motion_col, motion_text_col = st.columns([3, 2])
        with motion_col:
            motion_rev = df.groupby("active_motion")[["sourced_revenue_fy26", "attributed_revenue_fy26"]].sum().reset_index()
            motion_rev = motion_rev.sort_values("attributed_revenue_fy26", ascending=False)
            fig_motion = go.Figure(go.Bar(
                x=motion_rev["active_motion"], y=motion_rev["attributed_revenue_fy26"],
                marker_color=[ACCENT, "#e89b7b", "#d9c2b8"],
                text=[f"${v/1e6:.1f}M" for v in motion_rev["attributed_revenue_fy26"]],
                textposition="outside",
            ))
            fig_motion.update_layout(yaxis=dict(tickformat="$.2s", title="FY26 attributed revenue"),
                                     xaxis_title="active priority motion", showlegend=False)
            st.plotly_chart(_chart_layout(fig_motion, height=300), use_container_width=True,
                            config={"displayModeBar": False, "staticPlot": True})
        with motion_text_col:
            st.markdown("""
            This half the push is **migrations**; next half it might be **solution development**.
            In most orgs a priority shift means new spreadsheets and a quarter of confusion.
            Here it's a defined sequence:

            1. The new motion becomes a **big rock** with a plan doc
            2. Partners get enrolled via `active_motion` in the gold layer
            3. The rock proposes the skills the motion needs
            4. The session hook starts reporting it — every session wakes up knowing the new priority

            The system is built for the priorities to change.
            """)
    else:
        st.info("Gold layer not present in this deployment — browse the data on GitHub.")


# =============================================================================
# TAB 2 — THE CLAUDE SETUP (how the cloud instance is configured)
# =============================================================================

with tab_setup:
    st.markdown("""
    <div class="narrative-quote">
    This is how the Claude Code instance is set up — read it bottom-up: a governed data layer,
    context every session boots with, plans tied to the epics the team already runs, skills that
    do the recurring work, and retros that rewrite the system itself. Everything on this page
    exists as a real file in this repo.
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
        st.markdown("#### It starts with governed data")
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
        st.caption("Medallion architecture: agents only ever read gold + the dictionary. Sourced vs. influenced vs. attributed, deal-reg rules, the Partner Value Score formula — defined once, never guessed.")

    with gold_col:
        st.markdown("#### The gold layer, live")
        if not metrics_df.empty:
            fig_gold = px.scatter(
                metrics_df,
                x="partner_value_score", y="attributed_revenue_fy26",
                size="deal_regs_approved_fy26", color="health_flag",
                hover_name="partner_name",
                color_discrete_map={"green": "#6aa84f", "yellow": "#e6b84a", "red": "#cc4125"},
                labels={"partner_value_score": "Partner Value Score",
                        "attributed_revenue_fy26": "FY26 attributed revenue",
                        "deal_regs_approved_fy26": "approved deal regs",
                        "health_flag": "health"},
            )
            fig_gold.add_vline(x=40, line_dash="dot", line_color="#ccc")
            fig_gold.add_vline(x=70, line_dash="dot", line_color="#ccc")
            fig_gold.update_yaxes(tickformat="$.2s")
            st.plotly_chart(_chart_layout(fig_gold, height=300), use_container_width=True)
            st.caption("All three domains in one frame: score (program) × revenue (sales) × health (management). Bubble size = approved deal regs. Rendered from data/partner_metrics.csv at runtime — the same file the skills read.")
        else:
            st.info("Gold layer not present in this deployment.")

    # --- Plans: roadmap ---
    st.markdown("#### Plans are the roadmap — one big rock per Jira epic")
    roadmap = pd.DataFrame([
        dict(Rock="Partner Attribution", Start="2026-02-01", Finish="2026-07-31", Status="active"),
        dict(Rock="Partner Scorecard", Start="2026-03-01", Finish="2026-08-31", Status="active"),
        dict(Rock="Partner Program", Start="2026-06-01", Finish="2026-12-31", Status="active"),
        dict(Rock="Partner Planning", Start="2026-08-01", Finish="2027-01-31", Status="planned"),
    ])
    fig_road = px.timeline(
        roadmap, x_start="Start", x_end="Finish", y="Rock", color="Status",
        color_discrete_map={"active": ACCENT, "planned": "#d9c2b8"},
    )
    fig_road.update_yaxes(autorange="reversed", title="")
    fig_road.add_vline(x=AS_OF, line_dash="dot", line_color="#999")
    fig_road.add_annotation(x=AS_OF, y=-0.7, text="today", showarrow=False, font=dict(color="#999", size=11))
    st.plotly_chart(_chart_layout(fig_road, height=250), use_container_width=True,
                    config={"displayModeBar": False})
    st.caption("Each bar is a living plan doc: milestones, open questions, owned skills, and an improvement log. The program rock is the newest — created when tiering and benefits needed an owner. Status syncs with the epic — not a second process.")

    # --- Skills: live demo ---
    st.markdown("#### A skill in action: `/attribution-compare`")
    st.markdown("The question partner sales argues about most: how should $150,000 of partner-influenced revenue be credited? Pick a model — this is the live output of the skill the attribution plan owns.")

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
# TAB 3 — THE PLAYBOOK (the three domains, fully built out)
# =============================================================================

with tab_playbook:
    st.markdown("""
    <div class="narrative-quote">
    Built out for a Databricks-scale partner organization: each of the three domains owns its
    rocks, each rock owns its skills, and every recurring deliverable in the GTM motion becomes
    one command. This repo ships the attribution, scorecard, and program rocks live — the rest
    is the same pattern, repeated.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### The full catalog: three domains, nine rocks, nineteen skills")

    CATALOG = {
        "Partner Sales": {
            "Attribution": ["/attribution-compare", "/credit-dispute"],
            "Deal Registration": ["/deal-reg-triage", "/reg-conflict-check"],
            "Co-Sell": ["/co-sell-brief", "/marketplace-audit"],
        },
        "Partner Management": {
            "Scorecard & QBRs": ["/partner-qbr", "/scorecard-refresh", "/health-digest"],
            "Enablement & Certs": ["/cert-gap", "/enablement-plan"],
            "Capacity Planning": ["/quota-scenario", "/territory-overlap"],
        },
        "Partner Program": {
            "Tiering & Benefits": ["/tier-review", "/benefits-audit"],
            "Priority Motions": ["/migration-pipeline", "/solution-launch-check"],
            "Exec Reporting": ["/board-snapshot", "/win-story"],
        },
    }
    tm_names, tm_parents = ["Partner OS"], [""]
    for domain, domain_rocks in CATALOG.items():
        tm_names.append(domain)
        tm_parents.append("Partner OS")
        for rock, rock_skills in domain_rocks.items():
            tm_names.append(rock)
            tm_parents.append(domain)
            for s in rock_skills:
                tm_names.append(s)
                tm_parents.append(rock)

    fig_catalog = px.treemap(
        names=tm_names, parents=tm_parents,
        color_discrete_sequence=["#D97757", "#b08d57", "#a9745d"],
    )
    fig_catalog.update_traces(
        root_color="#FAFAF9",
        marker=dict(cornerradius=4),
        textfont=dict(size=14),
    )
    st.plotly_chart(_chart_layout(fig_catalog, height=420), use_container_width=True,
                    config={"displayModeBar": False})
    st.caption("Attribution, Scorecard & QBRs, and Tiering & Benefits ship live in this repo. The other rocks follow the identical pattern: a plan doc against the Jira epic, skills proposed in the plan before they're built.")

    skill_detail = pd.DataFrame([
        {"Skill": "/attribution-compare", "Domain": "Partner Sales", "What it does": "Runs any deal through six credit models, recommends one, flags >2x swings"},
        {"Skill": "/credit-dispute", "Domain": "Partner Sales", "What it does": "Pulls the touchpoint ledger for a disputed deal and drafts the resolution memo"},
        {"Skill": "/deal-reg-triage", "Domain": "Partner Sales", "What it does": "Checks a new registration for conflicts: existing regs, account ownership, sourcing evidence — approve / reject / escalate with reasons"},
        {"Skill": "/reg-conflict-check", "Domain": "Partner Sales", "What it does": "When two partners register the same opportunity, reconstructs first touch from the ledger and drafts the ruling"},
        {"Skill": "/co-sell-brief", "Domain": "Partner Sales", "What it does": "One-pager before any joint account call: history, attribution, open pipeline, talk track"},
        {"Skill": "/marketplace-audit", "Domain": "Partner Sales", "What it does": "Sweeps partner listings for stale pricing, broken links, expired certifications"},
        {"Skill": "/partner-qbr", "Domain": "Partner Management", "What it does": "Benchmark-backed QBR brief for any partner in seconds — snapshot, risks, asks"},
        {"Skill": "/scorecard-refresh", "Domain": "Partner Management", "What it does": "Recomputes Partner Value Scores, tiers, and health flags from dictionary thresholds; writes only on approval"},
        {"Skill": "/health-digest", "Domain": "Partner Management", "What it does": "Monday-morning digest: flag changes, QBRs overdue, partners trending down"},
        {"Skill": "/cert-gap", "Domain": "Partner Management", "What it does": "Which partners fall below cert thresholds next quarter — and what it costs their score"},
        {"Skill": "/enablement-plan", "Domain": "Partner Management", "What it does": "Per-partner ramp plan tied to the capacity model, not a generic curriculum"},
        {"Skill": "/quota-scenario", "Domain": "Partner Management", "What it does": "FY quota drafts under bear / base / bull growth cases, from trailing attribution"},
        {"Skill": "/territory-overlap", "Domain": "Partner Management", "What it does": "Flags partners competing for the same accounts before it becomes a channel conflict"},
        {"Skill": "/tier-review", "Domain": "Partner Program", "What it does": "Half-close memo for any partner near a tier line: score components, trajectory, benefits delta if moved"},
        {"Skill": "/benefits-audit", "Domain": "Partner Program", "What it does": "Finds partners consuming benefits above their tier, or leaving entitled MDF and vouchers unused"},
        {"Skill": "/migration-pipeline", "Domain": "Partner Program", "What it does": "Reads the migrations motion: enrolled partners, sourced migration pipeline, regs in flight"},
        {"Skill": "/solution-launch-check", "Domain": "Partner Program", "What it does": "Readiness gate for a partner-built solution: certifications, references, listing quality"},
        {"Skill": "/board-snapshot", "Domain": "Partner Program", "What it does": "Board-ready partner slide: sourced %, tier moves, top movers, risks — same definitions, every time"},
        {"Skill": "/win-story", "Domain": "Partner Program", "What it does": "Turns a closed-won deal into a co-marketing-ready win story with verified figures"},
    ])
    with st.expander("**Every skill, one line each**"):
        st.dataframe(skill_detail, hide_index=True, use_container_width=True)

    # --- Triggers: the nervous system ---
    st.markdown("#### The triggers: what makes it run itself")
    st.markdown("Skills are the muscles; triggers are the nervous system. Each one turns a business signal into either immediate context or retro evidence.")

    triggers = pd.DataFrame([
        {"Trigger": "Session starts", "Fires": "Hook injects rock statuses + scorecard headlines (sourced, attributed, deal regs, reds)", "So that": "No session ever starts cold", "Status": "live in this repo"},
        {"Trigger": "Session ends", "Fires": "Hook appends one line to the session log", "So that": "The retro has evidence, not anecdotes", "Status": "live in this repo"},
        {"Trigger": "Deal reg submitted", "Fires": "/deal-reg-triage runs the conflict check; approval starts the 90-day protection clock", "So that": "The reg desk answers in hours, not weeks of escalation", "Status": "org scale"},
        {"Trigger": "Gold table written", "Fires": "Health rules re-run; deltas posted to the scorecard plan", "So that": "A partner going red is noticed the day it happens", "Status": "org scale"},
        {"Trigger": "PVS crosses a tier line at half-close", "Fires": "/tier-review drafts the move memo with the benefits delta", "So that": "Tier moves are explainable from the score, never negotiated ad hoc", "Status": "org scale"},
        {"Trigger": "QBR overdue >120 days", "Fires": "/health-digest escalates; QBR milestone opens on the plan", "So that": "Coverage gaps surface before the partner churns", "Status": "org scale"},
        {"Trigger": "Monthly retro", "Fires": "/improve-setup reads logs + plans, proposes diff-style edits", "So that": "The system rewrites itself as priorities change", "Status": "live in this repo"},
    ])
    st.dataframe(triggers, hide_index=True, use_container_width=True)

    # --- A quarter in the life ---
    st.markdown("#### A quarter in the life")

    STORY = [
        ("Week 1", "Monday's session opens with the hook already flagging it: Lakeshore Consulting is red — NPS 44, no QBR in 188 days. <code>/partner-qbr Lakeshore</code> drafts the benchmark-backed brief in one command. The QBR is on the calendar by Thursday."),
        ("Week 2", "Vector and Northwind register the same migration opportunity. <code>/reg-conflict-check</code> reconstructs the touchpoint ledger: Vector sourced it, first touch 47 days earlier; Northwind keeps influence credit. Ruling drafted in minutes — historically that was a three-week escalation thread."),
        ("Week 6", "First monthly retro. <code>/improve-setup</code> reads the session log and calls it: co-sell prep was requested four times with no owning skill. It proposes <code>/co-sell-brief</code> under the partner-sales domain. Approved Tuesday, shipped Wednesday, demoed in Thursday's stand-up."),
        ("Week 9", "Half-close. <code>/scorecard-refresh</code> recomputes every Partner Value Score: Analytics Corp lands exactly on the Premier floor at 40. Per the dictionary it's flagged for tier review instead of auto-moved — <code>/tier-review</code> drafts the memo with the benefits delta either way: $50,000 MDF and the 72-hour co-sell SLA are on the line."),
        ("Week 12", "Leadership sets the H2 priority: migrations. The motion becomes a big rock, partners re-enroll in <code>active_motion</code>, and <code>/migration-pipeline</code> is proposed in the plan. By Monday the session hook is reporting migration pipeline at boot — the priority changed, the system absorbed it."),
    ]
    for story_week, story_text in STORY:
        st.markdown(f"""
        <div class="experience-card" style="padding: 1rem 1.3rem; margin-bottom: 0.6rem;">
            <strong style="color: #D97757;">{story_week}</strong>
            <span style="font-size: 0.9rem; color: #4a4a4a;"> — {story_text}</span>
        </div>
        """, unsafe_allow_html=True)

    st.caption("Synthetic story, real mechanics: every beat maps to a hook, a skill, or a plan that exists (or is proposed) in this repo — including Analytics Corp actually sitting at PVS 40 in the gold layer.")


# =============================================================================
# TAB 4 — ENABLEMENT
# =============================================================================

with tab_enable:
    st.markdown("""
    <div class="narrative-quote">
    Tools don't get adopted because they're good — they get adopted because they save someone's
    Tuesday. So the rollout starts from the team's most-hated recurring task: QBR prep for the
    PSMs, reg-conflict rulings for partner sales, tier-review season for the program team.
    </div>
    """, unsafe_allow_html=True)

    ROLLOUT = [
        ("Day 1 · Bootstrap", "Stand up the repo: memory file, scoped permissions, hooks. The first session already knows the partner book, the tier mix, and the active motion."),
        ("Day 30 · First rock", "One initiative the team already cares about, planned against its existing Jira epic. A pilot pod of one PSM and one partner-sales rep — not a mandate."),
        ("Day 60 · Skills from real asks", "The three most-repeated requests become skills. Each one gets demoed in stand-up the week it ships — adoption follows saved time."),
        ("Day 90 · Compounding", "Monthly retro: the AI reads its own session logs and proposes upgrades. Self-serve becomes the default across all three domains."),
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
            x=[22, 14, 12, 9],
            y=["/partner-qbr", "/deal-reg-triage", "/attribution-compare", "/scorecard-refresh"],
            orientation="h", marker_color=ACCENT,
            text=["22h", "14h", "12h", "9h"], textposition="outside",
        ))
        fig_saved.update_layout(xaxis=dict(range=[0, 26], title="hours / month, team-wide"))
        st.plotly_chart(_chart_layout(fig_saved, height=300), use_container_width=True,
                        config={"displayModeBar": False, "staticPlot": True})
        st.caption("Illustrative. /improve-setup doesn't save hours directly — it compounds the others.")

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
