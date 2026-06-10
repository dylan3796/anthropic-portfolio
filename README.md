# Dylan Ram - Interactive Portfolio

Interactive portfolio built with Claude Code for the Anthropic Product Operations Manager application.

![Portfolio Preview](https://img.shields.io/badge/Built%20with-Claude%20Code-8A2BE2)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 Overview

A live, interactive portfolio showcasing my experience at the intersection of partner strategy, data operations, and product thinking. Built to demonstrate both technical capability and strategic insight through real project examples.

## ✨ Features

- **Partner Attribution Modeling** - Showcase of multi-touch attribution logic
- **Revenue Analytics** - Interactive visualizations of partner performance
- **Project Timeline** - Key achievements and impact metrics
- **Live Data Visualizations** - Plotly-powered charts and dashboards
- **Claude Code Operating System** - A working reference setup, parsed live by the app

## 🧠 Claude Code Architecture

This repo doubles as a working reference for running Claude Code as an operating
system rather than a chat tool: project memory (`CLAUDE.md`), a SessionStart hook
that injects business data into every session, long-horizon plans against big rocks
(`plans/big-rocks/`), per-rock skills (`.claude/skills/`), and a recursive
`/improve-setup` loop that reviews session evidence and edits the setup itself.
Everything is real and invocable — the Streamlit app parses these files at runtime.
Full walkthrough: [docs/claude-code-architecture.md](docs/claude-code-architecture.md).

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/dylan3796/anthropic-portfolio.git
cd anthropic-portfolio

# Install dependencies
pip install -r requirements.txt

# Run the portfolio
streamlit run app.py
```

Visit `http://localhost:8501` to view the portfolio.

## 🛠️ Built With

- **Streamlit** - Interactive web framework
- **Plotly** - Data visualization
- **Python** - Core logic and data processing
- **Claude Code** - Development assistant

## 📁 Project Structure

```
anthropic-portfolio/
├── app.py                       # Main portfolio application
├── CLAUDE.md                    # Claude Code project memory (bootstrap layer)
├── .claude/
│   ├── settings.json            # Permissions + hook wiring
│   ├── hooks/                   # SessionStart context injection, Stop session log
│   ├── skills/                  # attribution-compare, partner-qbr,
│   │                            #   scorecard-refresh, improve-setup
│   └── agents/                  # big-rock-planner subagent
├── plans/big-rocks/             # Long-horizon plans per strategic initiative
├── retros/                      # Session log + improvement-loop retros
├── docs/
│   └── claude-code-architecture.md  # Architecture walkthrough + diagram
├── data/
│   ├── sample_data.py           # Sample metrics and visualizations
│   ├── partner_metrics.csv      # Synthetic partner scorecard data
│   └── DATA_DICTIONARY.md       # Metric definitions (source of truth)
├── .streamlit/
│   └── config.toml              # Streamlit configuration
└── requirements.txt             # Python dependencies
```

## 🌐 Deployment

Deployed on [Streamlit Community Cloud](https://share.streamlit.io) (free):
sign in with GitHub → New app → repo `dylan3796/anthropic-portfolio`, branch
`main`, entrypoint `app.py`.

## 📫 Contact

Built by Dylan Ram  
Partner Strategy & Operations @ Databricks

---

*This portfolio was built with Claude Code to showcase the intersection of technical execution and strategic thinking.*
