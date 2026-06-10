# AI as an Operating System

A live walkthrough — built with Claude Code — of how to embed agentic AI
(Claude Code, Codex, or any harness) into how a team actually runs: from
folder structure to team adoption.

![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-8A2BE2)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 The idea

Most teams use AI as a tool: open a chat, get an answer, lose the context.
This repo demonstrates the alternative — an operating system in five layers:

1. **Data** — medallion architecture down to one governed metric dictionary
2. **Memory** — project context + hooks that inject business state into every session
3. **Plans** — long-horizon plan docs per big rock, mapped to Jira epics
4. **Skills** — common tasks hardened into versioned, invocable skills
5. **Recursion** — retros where the AI proposes edits to its own setup

The Streamlit app (`app.py`) is the walkthrough; the repo behind it is the
working implementation. The app parses the actual `.claude/` and `plans/`
files at runtime. Full deep-dive:
[docs/claude-code-architecture.md](docs/claude-code-architecture.md).

## 🚀 Quick Start

```bash
git clone https://github.com/dylan3796/anthropic-portfolio.git
cd anthropic-portfolio

pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501`. Or open the repo in Claude Code: the
SessionStart hook injects the business context, and `/attribution-compare`,
`/partner-qbr`, `/scorecard-refresh`, and `/improve-setup` are live.

## 📁 Project Structure

```
anthropic-portfolio/
├── app.py                       # The walkthrough (Streamlit)
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
│   ├── sample_data.py           # Attribution demo data
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

Dylan Ram · GTM Strategy & Ops
[dylanmr96@gmail.com](mailto:dylanmr96@gmail.com) ·
[linkedin.com/in/dylanram](https://linkedin.com/in/dylanram)
