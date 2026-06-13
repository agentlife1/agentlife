# AgentLife Framework

**Your Life, Orchestrated by AI.**

AgentLife is an open-source configuration layer that sits on top of [Hermes Agent](https://hermes-agent.nousresearch.com) — turning a general-purpose AI agent into your personal AI operating system, tailored to how you live and work.

## What is AgentLife?

| Layer | What it does |
|-------|-------------|
| **Hermes Agent** | The agent runtime — installs on your own infrastructure |
| **AgentLife Framework** | Persona packs, configs, cron jobs, and skills that configure Hermes for your life |

Pick a **persona** (or combine several), and AgentLife configures Hermes with the right tools, schedules, and automations.

## Personas

| Persona | For |
|---------|-----|
| **Life Ops** | Managing finances, calendar, subscriptions, and daily operations |
| Indie Hacker | Building and shipping products faster |
| Knowledge Worker | Research, docs, note-taking, synthesis |
| Enterprise Architect | System design, architecture reviews |
| Hobbyist | Personal projects, making, learning |
| Creator | Content creation, media production |
| Student | Coursework, research, study planning |

## Quick Start

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

Or if you already have Hermes:

```bash
pip install agentlife
agentlife setup
```

## Project Structure

```
agentlife/
├── agentlife/          # Python CLI package
│   └── cli.py          #  agentlife setup, update, verify
├── packs/              # Persona packs
│   ├── base/           # Tier 1 — shared config & skills
│   └── life-ops/       # Tier 2 — Life Ops persona
│       └── use-cases/  # Tier 3 — portfolio, expenses, etc.
├── guides/             # Platform install docs
├── scripts/            # One-liner installers
├── pyproject.toml
└── README.md
```

## License

MIT — do what you want with it. Built for everyone.