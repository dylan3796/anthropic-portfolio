"""
AI as an Operating System — a live walkthrough.
The page describes an agentic AI setup; the repo it lives in IS that setup.
"""

import re
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data.sample_data import ATTRIBUTION_MODELS

REPO_ROOT = Path(__file__).parent
REPO_URL = "https://github.com/dylan3796/anthropic-portfolio"

# Page configuration
st.set_page_config(
    page_title="Dylan Ram | AI as an Operating System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS — Anthropic-inspired palette
st.markdown("""
<style>
    .stApp {
        background-color: #FAFAF9;
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1 {
        color: #1a1a1a;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    h2 {
        color: #2d2d2d;
        font-weight: 500;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e5e5;
    }

    h3 {
        color: #3d3d3d;
        font-weight: 500;
    }

    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 3rem 0;
    }

    a {
        color: #D97757;
        text-decoration: none;
    }

    a:hover {
        color: #c4624a;
        text-decoration: underline;
    }

    .narrative-quote {
        background-color: white;
        border-left: 3px solid #D97757;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 8px 8px 0;
        font-style: italic;
        color: #4a4a4a;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    .experience-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    .flow-step {
        background: white;
        border-top: 3px solid #D97757;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
        min-height: 150px;
    }

    .flow-arrow {
        text-align: center;
        font-size: 1.6rem;
        color: #D97757;
        padding-top: 3.2rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


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


# =============================================================================
# HERO
# =============================================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0 0.5rem 0;">
    <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem; border: none;">AI as an Operating System</h1>
    <p style="font-size: 1.15rem; color: #666; margin-bottom: 0.5rem;">
        A working blueprint for embedding agentic AI — Claude Code, Codex, or any harness —
        into how a team actually runs.
    </p>
    <p style="font-size: 0.95rem; color: #999;">
        Dylan Ram &nbsp;·&nbsp; GTM Strategy & Ops &nbsp;·&nbsp;
        <a href="mailto:dylanmr96@gmail.com">dylanmr96@gmail.com</a> &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/dylanram">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="narrative-quote">
Most teams use AI as a tool: open a chat, get an answer, lose the context. This is the
alternative — an operating system where data, plans, and playbooks persist, and the setup
improves itself. Everything on this page is real: the repo behind it is the implementation.
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# TENETS
# =============================================================================

st.markdown("## The Tenets")

TENETS = [
    ("Start with data", "Medallion in, answers out. Agents are only as trustworthy as the gold layer they read and the dictionary that defines it."),
    ("Context is owned; models are rented", "Vendors and models will change. Memory files, conventions, and metric definitions are the asset — they outlive any single tool."),
    ("Plans over prompts", "Strategic work lives in long-horizon plan docs — one per big rock, mapped to the epics the team already runs in Jira."),
    ("Skills encode the playbook", "Every repeated ask becomes a versioned, invocable skill, owned by exactly one plan. Tribal knowledge becomes infrastructure."),
    ("Least privilege is a feature", "What the agent may read, write, and push is a design decision, reviewed like code — not a default you inherit."),
    ("The setup improves itself", "Session evidence feeds retros that edit the memory, skills, and plans — the system compounds instead of decaying."),
]

for row_start in (0, 3):
    cols = st.columns(3)
    for col, (tenet_title, tenet_desc) in zip(cols, TENETS[row_start:row_start + 3]):
        with col:
            st.markdown(f"""
            <div class="experience-card" style="min-height: 160px;">
                <strong style="color: #D97757;">{tenet_title}</strong>
                <p style="font-size: 0.88rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{tenet_desc}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# ARCHITECTURE
# =============================================================================

st.markdown("## The Architecture")

FLOW = [
    ("1 · Data", "Medallion: bronze → silver → gold. One governed metric dictionary."),
    ("2 · Memory", "Project memory + hooks inject business context into every session."),
    ("3 · Plans", "One living plan per big rock — tied to a Jira epic."),
    ("4 · Skills", "Common tasks, hardened into invocable skills owned by plans."),
    ("5 · Recursion", "Retros review session evidence and edit layers 1–4."),
]

flow_cols = st.columns([5, 1, 5, 1, 5, 1, 5, 1, 5])
for i, (step_title, step_desc) in enumerate(FLOW):
    with flow_cols[i * 2]:
        st.markdown(f"""
        <div class="flow-step">
            <strong style="color: #D97757;">{step_title}</strong>
            <p style="font-size: 0.82rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{step_desc}</p>
        </div>
        """, unsafe_allow_html=True)
    if i < len(FLOW) - 1:
        with flow_cols[i * 2 + 1]:
            st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)

st.caption("Layer 5 loops back: approved retro edits flow into the data dictionary, memory, plans, and skills.")

st.markdown("#### Each layer, in this repo and at org scale")

arch_map = pd.DataFrame([
    {"Layer": "Data", "In this repo (live)": "data/partner_metrics.csv + DATA_DICTIONARY.md", "At org scale": "Lakehouse gold tables + a governed metric catalog (Unity Catalog, dbt metrics)"},
    {"Layer": "Memory", "In this repo (live)": "CLAUDE.md + SessionStart hook injecting scorecard headlines", "At org scale": "A memory file per repo + an org-wide conventions layer every agent boots with"},
    {"Layer": "Plans", "In this repo (live)": "plans/big-rocks/ — attribution, scorecard, planning", "At org scale": "One plan doc per Jira epic; milestones check off as stories close"},
    {"Layer": "Skills", "In this repo (live)": "/attribution-compare · /partner-qbr · /scorecard-refresh", "At org scale": "A skill per recurring deliverable: QBR briefs, pipeline reviews, forecast commentary"},
    {"Layer": "Recursion", "In this repo (live)": "Stop hook → retros/ → /improve-setup proposes edits", "At org scale": "A monthly ops retro where the AI proposes changes to its own setup"},
])
st.dataframe(arch_map, hide_index=True, use_container_width=True)

# Live registry — proof the page describes itself
st.markdown("#### Live registry")
st.caption("Parsed at runtime from this repo's actual plans/ and .claude/ directories — not hardcoded.")

setup_skills, setup_rocks = load_claude_setup()
if setup_skills or setup_rocks:
    reg_col1, reg_col2 = st.columns([1, 1])
    with reg_col1:
        st.dataframe(pd.DataFrame(setup_rocks), hide_index=True, use_container_width=True)
    with reg_col2:
        st.dataframe(pd.DataFrame(setup_skills), hide_index=True, use_container_width=True)
else:
    st.info(f"Setup files not present in this deployment — browse them on [GitHub]({REPO_URL}).")

st.markdown("---")


# =============================================================================
# WALKTHROUGH 1: SELF-SERVE ANALYTICS
# =============================================================================

st.markdown("## Walkthrough: Self-Serve Analytics")

st.markdown("""
<div class="narrative-quote">
The goal isn't a smarter chatbot — it's removing the analyst queue. Anyone on the team
gets governed answers, because the agent reads definitions instead of inventing them.
</div>
""", unsafe_allow_html=True)

ssa_col1, ssa_col2 = st.columns([1, 1])
with ssa_col1:
    st.markdown("""
    **1 · One source of numbers.** Gold tables + a data dictionary define every metric,
    threshold, and the fiscal calendar. If it's not defined there, it doesn't exist.

    **2 · Context is ambient.** A session-start hook injects the headlines — partner count,
    FY revenue, red flags — so every session opens already knowing the business.
    """)
with ssa_col2:
    st.markdown("""
    **3 · Skills answer the recurring questions.** `/partner-qbr Acme Consulting` drafts a
    benchmark-backed brief in seconds. No ticket, no queue, no stale deck.

    **4 · Governance holds.** Skills read thresholds from the dictionary; writes require a
    delta table and confirmation. Self-serve doesn't mean self-invented.
    """)

st.markdown("---")


# =============================================================================
# WALKTHROUGH 2: AI EMBEDDED IN GTM
# =============================================================================

st.markdown("## Walkthrough: AI Embedded in GTM")

st.markdown("""
Each GTM motion is a big rock with its own plan and skills: **attribution** owns the credit
logic, **scorecard** owns partner health and QBRs, **planning** owns quotas and territories.
Below — a live skill output: how `/attribution-compare` splits a $150,000 deal across four
partners under different models.
""")

selected_model = st.selectbox(
    "Attribution model",
    list(ATTRIBUTION_MODELS.keys()),
    index=2  # Default to Time Decay
)

model_data = ATTRIBUTION_MODELS[selected_model]
st.info(model_data['description'])

results_df = pd.DataFrame([
    {'Partner': k, 'Attribution': v}
    for k, v in model_data['results'].items()
])

fig = go.Figure()
fig.add_trace(go.Bar(
    x=results_df['Attribution'],
    y=results_df['Partner'],
    orientation='h',
    marker=dict(
        color=results_df['Attribution'],
        colorscale=[[0, '#fde8e0'], [0.5, '#e89b7b'], [1, '#D97757']],
        showscale=False
    ),
    text=results_df['Attribution'].apply(lambda x: f"${x:,.0f}"),
    textposition='outside'
))
fig.update_layout(
    xaxis_title="Attributed Revenue ($)",
    yaxis_title="",
    template='plotly_white',
    height=250,
    margin=dict(l=20, r=80, t=20, b=40),
    xaxis=dict(range=[0, max(results_df['Attribution']) * 1.2])
)
st.plotly_chart(fig, use_container_width=True)

st.caption("The model weights live in the attribution plan — the single source of truth — not in the skill or this page.")

st.markdown("---")


# =============================================================================
# ADOPTION
# =============================================================================

st.markdown("## Getting the Team to Actually Use It")

ADOPTION = [
    ("Day 1 · Bootstrap", "Stand up the repo: memory file, scoped permissions, hooks. The first session should already know the business."),
    ("Week 1 · First rock", "Pick one initiative the team already cares about. Write the plan against its existing Jira epic — don't invent new process."),
    ("Weeks 2–4 · Skills from real asks", "Harden the three most-repeated requests into skills. Demo each one in stand-up; adoption follows saved time, not mandates."),
    ("Monthly · Compound", "Run the retro. The AI proposes edits to its own setup as the business changes. Track skill invocations and time-to-answer."),
]

adopt_cols = st.columns(4)
for col, (adopt_title, adopt_desc) in zip(adopt_cols, ADOPTION):
    with col:
        st.markdown(f"""
        <div class="experience-card" style="min-height: 190px;">
            <strong style="color: #D97757;">{adopt_title}</strong>
            <p style="font-size: 0.85rem; color: #4a4a4a; margin: 0.5rem 0 0 0;">{adopt_desc}</p>
        </div>
        """, unsafe_allow_html=True)

with st.expander("**How the recursion works** — the part most setups skip"):
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

st.markdown("---")


# =============================================================================
# FOOTER
# =============================================================================

st.markdown(f"""
<div style="text-align: center; padding: 1rem 0; color: #666;">
    This page is its own reference implementation — every file it describes is in
    <a href="{REPO_URL}">the repo</a>:
    <a href="{REPO_URL}/blob/main/CLAUDE.md">CLAUDE.md</a> ·
    <a href="{REPO_URL}/blob/main/.claude/settings.json">settings.json</a> ·
    <a href="{REPO_URL}/blob/main/docs/claude-code-architecture.md">architecture deep-dive</a>
</div>
<div style="text-align: center; padding: 1rem 0; color: #999; font-size: 0.85rem;">
    Dylan Ram · Built with Claude Code · 2026
</div>
""", unsafe_allow_html=True)
