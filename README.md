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
git clone https://github.com/dylan3796/partner-ops.git
cd partner-ops

pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501`. Or open the repo in Claude Code: the
SessionStart hook injects the business context, and `/commissions-credit`,
`/attribution-compare`, `/partner-qbr`, and `/improve-setup` are live. The
crediting math has golden tests: `python3 tests/test_crediting.py`.

## 📁 Project Structure

```
partner-ops/
├── app.py                       # The walkthrough (Streamlit)
├── CLAUDE.md                    # Project memory + domain glossary (PSM/PAM, segments)
├── .claude/
│   ├── settings.json            # Permissions + hook wiring
│   ├── hooks/                   # SessionStart context injection, Stop session log
│   ├── skills/                  # commissions-credit (headline), attribution-compare,
│   │                            #   partner-qbr, improve-setup
│   └── agents/                  # big-rock-planner subagent
├── crediting/
│   └── engine.py                # Deterministic crediting engine (the money path)
├── tests/
│   └── test_crediting.py        # Golden tests / evals for the crediting math
├── notebooks/
│   └── scorecard_refresh.ipynb  # Analysis artifact: tier/health recompute
├── plans/big-rocks/             # Long-horizon plans per strategic initiative
├── retros/                      # Session log + improvement-loop retros
├── docs/
│   └── claude-code-architecture.md  # Architecture walkthrough + diagram
├── data/
│   ├── partner_metrics.csv      # The gold table (synthetic partner book)
│   ├── coverage_assignments.csv # Plain-English coverage sheet (the "Google Sheet")
│   ├── crediting_rules.json     # Codified crediting rules (generated)
│   ├── commission_deals.csv     # Closed deals actuals run against
│   ├── sample_data.py           # Attribution deal fixture
│   └── DATA_DICTIONARY.md       # Metric & schema definitions (source of truth)
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── requirements.txt             # App dependencies
└── requirements-dev.txt         # + pytest, for the tests
```

## 🌐 Deployment

Deployed on [Streamlit Community Cloud](https://share.streamlit.io) (free):
sign in with GitHub → New app → repo `dylan3796/partner-ops`, branch
`main`, entrypoint `app.py`.

## 📫 Contact

Dylan Ram · GTM Strategy & Ops
[dylanmr96@gmail.com](mailto:dylanmr96@gmail.com) ·
[linkedin.com/in/dylanram](https://linkedin.com/in/dylanram)
