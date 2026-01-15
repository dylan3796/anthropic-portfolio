"""
Dylan Ram - Interactive Portfolio
Built with Claude Code for the Anthropic Product Operations Manager application.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.sample_data import (
    PARTNER_DATA,
    SAMPLE_DEAL,
    ATTRIBUTION_MODELS,
    REVENUE_TIMELINE,
    PROJECT_METRICS
)

# Page configuration
st.set_page_config(
    page_title="Dylan Ram | Product Operations",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Anthropic-inspired design
st.markdown("""
<style>
    /* Main background and typography */
    .stApp {
        background-color: #FAFAF9;
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Headers */
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

    /* Subtle dividers */
    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 3rem 0;
    }

    /* Cards/containers */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Links */
    a {
        color: #D97757;
        text-decoration: none;
    }

    a:hover {
        color: #c4624a;
        text-decoration: underline;
    }

    /* Custom badge */
    .claude-badge {
        display: inline-block;
        background: linear-gradient(135deg, #D97757 0%, #E89B7B 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 1rem 0;
    }

    /* Quote blocks */
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

    /* Experience cards */
    .experience-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background-color: #f0f0f0;
        color: #4a4a4a;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }

    /* Project metrics */
    .metric-highlight {
        text-align: center;
        padding: 1rem;
    }

    .metric-number {
        font-size: 2.5rem;
        font-weight: 600;
        color: #D97757;
    }

    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }

    /* Role fit table */
    .fit-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HERO SECTION
# =============================================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; border: none;">Dylan Ram</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 1rem;">
        Strategy & Operations Leader
    </p>
    <span class="claude-badge">This portfolio was built with Claude Code</span>
</div>
""", unsafe_allow_html=True)

# Contact links
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    link_col1, link_col2, link_col3 = st.columns(3)
    with link_col1:
        st.markdown("[LinkedIn](https://linkedin.com/in/dylanram)")
    with link_col2:
        st.markdown("[dylanmr96@gmail.com](mailto:dylanmr96@gmail.com)")
    with link_col3:
        st.markdown("916-690-5681")

st.markdown("---")


# =============================================================================
# WHY CLAUDE CODE NARRATIVE
# =============================================================================

st.markdown("## The Future of Building")

st.markdown("""
<div class="narrative-quote">
"The best tools don't just make us faster—they change what we believe is possible."
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    I've spent my career at the intersection of strategy and systems—building the operational
    infrastructure that turns ideas into outcomes. At Databricks, I built attribution systems,
    executive dashboards, and AI-powered reporting tools. At Salesforce, I automated forecasting
    and designed territory carving scripts that became the foundation of our GTM.

    **Then I started building with Claude Code.**

    What I discovered wasn't just a productivity tool—it was a fundamental shift in how ideas
    become reality. The Attribution MVP project on my desktop? 18,500 lines of production-ready
    Python, built in weeks instead of months. Not because I wrote code faster, but because I
    could *think* faster. Claude Code handles the syntax; I focus on the architecture, the
    edge cases, the business logic that actually matters.

    This is why I want to work on Claude Code at Anthropic. I've experienced firsthand how this
    tool transforms builders—and I want to help shape what comes next.
    """)

with col2:
    st.markdown("""
    #### What Claude Code Changes

    **From writing to directing**
    Less time on syntax, more time on intent.

    **From sequential to parallel**
    Explore multiple approaches simultaneously.

    **From knowing to learning**
    Tackle unfamiliar domains with confidence.

    **From gatekept to accessible**
    Lower the barrier from idea to execution.
    """)

st.markdown("---")


# =============================================================================
# PROFESSIONAL BACKGROUND
# =============================================================================

st.markdown("## Experience")

# Databricks
with st.expander("**Databricks** — Partner Strategy & Ops Manager (Aug 2021 - Present)", expanded=True):
    st.markdown("*Promoted Feb 2023, first Partner S&O Hire*")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Attribution & Analytics**
        - Scaled partner attribution systems in Salesforce, SQL, and Spark to track bookings,
          consumption, and pipeline across a two-sided marketplace
        - Built standardized partner datasets adopted company-wide, powering 10+ executive
          and team dashboards
        - Designed Partner Executive & Partner Scorecard as the single source of truth
        """)

    with col2:
        st.markdown("""
        **AI & Automation**
        - Deployed AI-driven reporting agents (Newsletter Agent, FAQ Agent) for automated
          Q&A, insights, and notifications
        - Integrated LLM workflows into metric distribution

        **Strategic Leadership**
        - Shaped Partner Value Score and Partner Tiering framework with global alignment
        - Led annual quota-setting, aligning Sales, Finance, and Partner Leadership
        """)

# Salesforce
with st.expander("**Salesforce** — SMB Sales Strategy & Operations Analyst (Jul 2019 - Aug 2021)"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Technical**
        - Automated reporting and forecasting using G Suite APIs and Python
        - Developed territory carving Python script incorporating sales guiding principles—became
          the basis of our GTM
        - Led Tableau migration with enablement and data governance
        """)

    with col2:
        st.markdown("""
        **Strategic**
        - Direct business partner to the $250M AMER SMB Central business
        - Provided guidance to AVP/VP/RMs on territory design, account prioritization
        - Crafted FY22 GTM guiding principles: customer continuity, account proximity,
          industry mix, top accounts
        """)

# Education
with st.expander("**Education** — UC Santa Barbara"):
    st.markdown("""
    **Bachelor of Arts in Economics & Accounting**
    - Dean's Honors, AP Scholar with Distinction
    """)

# Skills
st.markdown("#### Technical Skills")
skills = ["Python", "SQL", "PySpark", "Salesforce", "Tableau", "Excel/GSheets", "Pandas", "Plotly"]
skill_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
st.markdown(f'<div style="margin: 1rem 0;">{skill_html}</div>', unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# FEATURED PROJECT: ATTRIBUTION MVP
# =============================================================================

st.markdown("## Featured Project: Attribution MVP")

st.markdown("""
<div class="narrative-quote">
Built with Claude Code — a full-stack SaaS MVP for partner revenue attribution,
demonstrating both technical depth and business understanding.
</div>
""", unsafe_allow_html=True)

# Project metrics
metric_cols = st.columns(4)
metrics = [
    ("18,500+", "Lines of Python"),
    ("8", "Attribution Models"),
    ("3", "Customer Segments"),
    ("15+", "Database Tables")
]

for col, (value, label) in zip(metric_cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="metric-number">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# Interactive attribution model comparison
st.markdown("### Interactive: Attribution Model Comparison")
st.markdown("""
Different attribution models answer the question "who deserves credit?" in different ways.
Select a model to see how a $150,000 deal would be attributed across four partners.
""")

# Model selector
selected_model = st.selectbox(
    "Select Attribution Model",
    list(ATTRIBUTION_MODELS.keys()),
    index=2  # Default to Time Decay
)

model_data = ATTRIBUTION_MODELS[selected_model]

# Description
st.info(model_data['description'])

# Visualization
results_df = pd.DataFrame([
    {'Partner': k, 'Attribution': v}
    for k, v in model_data['results'].items()
])

# Create horizontal bar chart
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

# Architecture overview
st.markdown("### System Architecture")

arch_col1, arch_col2 = st.columns(2)

with arch_col1:
    st.markdown("""
    **Core Engine**
    - Rule-based attribution with JSON configuration
    - 8 models: Equal, Role-Weighted, Time Decay, First/Last Touch, Linear, U-Shaped, Activity-Weighted
    - Split cap enforcement (never exceed 100%)
    - Immutable ledger with full audit trail
    """)

with arch_col2:
    st.markdown("""
    **Platform Features**
    - Multi-segment customer support (3 tiers)
    - Salesforce OAuth integration
    - Partner self-service portal
    - AI-powered inference engine for indirect attribution
    - PDF/Excel/CSV exports with custom formatting
    """)

# Claude Code callout
st.markdown("### Built with Claude Code")

cc_col1, cc_col2 = st.columns(2)

with cc_col1:
    st.markdown("""
    **What Claude Code Enabled**
    - Complex inference engine with time decay and proximity scoring
    - Multi-source conflict resolution (priority, merge, manual review modes)
    - Production-ready error handling and logging
    - Comprehensive test suite with edge cases
    """)

with cc_col2:
    st.markdown("""
    **Development Velocity**
    - Traditional estimate: 4-6 months
    - With Claude Code: 3 weeks
    - Not just faster typing—faster *thinking*
    - Explored architectural alternatives in real-time
    """)

st.markdown("---")


# =============================================================================
# ROLE FIT ANALYSIS
# =============================================================================

st.markdown("## Role Fit: Product Operations Manager, Claude Code")

st.markdown("""
<div class="narrative-quote">
I've experienced firsthand what makes Claude Code powerful—and I have ideas for what Product Ops could build next.
</div>
""", unsafe_allow_html=True)

# Fit table
fit_data = [
    ("5+ years product ops / program management", "5.5 years at Databricks + Salesforce in Strategy & Ops roles"),
    ("Direct experience building with AI tools", "AI reporting agents at Databricks; this portfolio + Attribution MVP with Claude Code"),
    ("Building processes from 0 to 1", "Partner Value Score, Partner Tiering framework, attribution system architecture"),
    ("Cross-functional influence without authority", "Aligned Sales, Finance, and Partner Leadership on quota-setting and metrics"),
    ("User metrics and dashboards", "Executive dashboards, partner scorecards, standardized datasets powering 10+ dashboards"),
    ("Launch coordination", "Annual quota-setting process, partner program rollouts, tool migrations"),
    ("Mission alignment", "Deeply invested in AI that amplifies human capability—evident in my work and side projects"),
]

st.markdown('<div class="fit-table">', unsafe_allow_html=True)

for requirement, experience in fit_data:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**{requirement}**")
    with col2:
        st.markdown(experience)
    st.markdown("<hr style='margin: 0.5rem 0; border-color: #f0f0f0;'>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# CONTACT
# =============================================================================

st.markdown("## Let's Connect")

contact_col1, contact_col2 = st.columns([2, 1])

with contact_col1:
    st.markdown("""
    I'm excited about the opportunity to help scale Claude Code's impact—shaping the product
    operations that turn user feedback into features, metrics into decisions, and launches
    into moments that matter.

    **Let's discuss how I can contribute.**
    """)

with contact_col2:
    st.markdown("""
    **Dylan Ram**

    [dylanmr96@gmail.com](mailto:dylanmr96@gmail.com)

    [linkedin.com/in/dylanram](https://linkedin.com/in/dylanram)

    916-690-5681
    """)

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem 0 1rem 0; color: #999; font-size: 0.85rem;">
    Built with Claude Code | January 2025
</div>
""", unsafe_allow_html=True)
