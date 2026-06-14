<p align="center">
  <img src="https://agentlife.io/assets/agentlife-logo-icon.png" alt="AgentLife" width="160">
</p>

<h1 align="center">AgentLife</h1>
<p align="center">
  <i>Your life, orchestrated by AI — an open-source persona framework for Hermes Agent.</i>
</p>

<p align="center">
  <a href="#-what-is-agentlife"><strong>What is this?</strong></a> ·
  <a href="#-quick-start"><strong>Quick Start</strong></a> ·
  <a href="#-persona-packs"><strong>Personas</strong></a> ·
  <a href="#-guides"><strong>Guides</strong></a> ·
  <a href="#-architecture"><strong>Architecture</strong></a> ·
  <a href="#-mcp-integration"><strong>MCP</strong></a> ·
  <a href="#-contributing"><strong>Contributing</strong></a>
</p>

---

## 🤔 What Is AgentLife?

AgentLife is a **persona configuration layer** for [Hermes Agent](https://hermes-agent.nousresearch.com) — the open-source AI agent framework.

**If you've ever thought:** "I want a personal AI agent that actually knows me, connects to my accounts, runs on my hardware, and works for me — not for a corporation" — this is that.

AgentLife bundles everything you need to turn Hermes Agent into a **personal AI operations system** for your finances, schedule, and daily life. Just install a persona pack and your agent instantly knows how to handle that domain.

### Who Is This For?

| You are... | AgentLife gives you... |
|------------|----------------------|
| **Tech-savvy, new to AI agents** | Guides from first principles, ready-to-use configs, no jargon |
| **Developer exploring agentic AI** | Reproducible persona packs, MCP integration, open-source foundation |
| **Privacy-conscious user** | Everything runs on *your* hardware. No cloud, no data mining, no vendor lock-in |
| **Lifehacker / productivity enthusiast** | Automated portfolio tracking, budget management, calendar ops, subscription monitoring |

### What Makes AgentLife Different?

| | Chatbots (ChatGPT, Claude) | Agent Platforms (OpenAI GPTs) | AgentLife |
|---|---|---|---|
| **Runs where?** | Cloud only | Cloud only | Your hardware |
| **Persistent memory?** | Session only | Limited | Full cross-session |
| **Scheduled tasks?** | No | No | ✅ Cron jobs |
| **Tool access?** | None | Limited built-ins | Any MCP server |
| **Open source?** | No | No | ✅ MIT License |
| **Your data?** | Their server | Their server | Your machine |

## 🚀 Quick Start

### Prerequisites

You need two things before AgentLife:

1. **An AI model provider** — we recommend [OpenRouter](https://openrouter.ai) (one key gives you access to 200+ models)
2. **Hermes Agent** — the agent framework (AgentLife configures it; Hermes runs it)

### Install Hermes Agent

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Follow the setup wizard to add your API key.

> **New to this?** Read the [Getting Started Guide](guides/getting-started.md) — it walks you through every step with explanations.

### Install AgentLife

```bash
# Coming from the one-liner:
# curl -sfSL https://agentlife.io/install.sh | bash

# Or clone and install manually:
git clone https://github.com/agentlife1/agentlife.git
cd agentlife
pip install -e .

# Run setup
agentlife setup
```

### Verify

```bash
agentlife verify
```

This checks:
- ✅ Hermes is installed and reachable
- ✅ Your API key is configured
- ✅ Persona pack files are valid
- ✅ MCP server dependencies are installed
- ✅ Cron jobs are registerable

## 🎭 Persona Packs

AgentLife uses a **three-tier model**: Base → Persona → Use Cases.

| Tier | Pack | Description | Status |
|------|------|-------------|--------|
| 1 | **Base** | Core connectivity, health checks, shared defaults | ✅ Included |
| 2 | **Life Ops** | Personal finance, calendar, subscriptions, daily ops | ✅ Available |
| 2 | **Work** | Email, tasks, meetings, project management | 🔜 Coming |
| 2 | **Health** | Fitness, nutrition, medical tracking | 🔜 Future |
| 2 | **Home** | Smart home, maintenance, groceries | 🔜 Future |
| 3 | *(Use Cases)* | Individual features within each persona | ✅ Per persona |

### Life Ops — The First Persona

Life Ops turns your agent into a personal operations engineer:

| Use Case | What It Does | MCP Integration |
|----------|-------------|-----------------|
| **Portfolio Tracking** | Net worth snapshots, asset allocation, rebalance alerts | Market data MCP servers |
| **Expense Tracking** | Spending categorization, budget vs. actual, trends | Financial data MCP |
| **Calendar Ops** | Daily agenda, time audit, focus suggestions | CalDAV/Google Calendar MCP |
| **Bills & Subscriptions** | Renewal tracking, 14-day alerts, annual cost totals | Billing data MCP |

**Enable what you need:**

```bash
agentlife setup --persona life-ops --use-cases portfolio,expenses,calendar
```

The Daily Brief cron job pulls everything together — every weekday morning you get:

```
📊 Morning Brief — June 13, 2026
  Net Worth: $2,849,312 (+0.07% today)
  Budget: $487/$400 dining (22% over — alert)
  Today's Calendar: 3 meetings, 1 focus block (2h)
  Renewals: Netflix ($15.99) in 7 days
```

## 📚 Guides

The `guides/` directory has everything from first principles to advanced setup:

| Guide | For |
|-------|-----|
| [Getting Started](guides/getting-started.md) | First-time users — step-by-step from zero to running |
| [Concepts: What Is an AI Agent?](guides/concepts/what-is-an-ai-agent.md) | "Wait, what even IS an AI agent?" |
| [Concepts: What Is MCP?](guides/concepts/what-is-mcp.md) | Understanding the Model Context Protocol |
| [Concepts: How Hermes Works](guides/concepts/how-hermes-works.md) | The agent framework explained |
| [Concepts: The Three-Tier Model](guides/concepts/three-tier-model.md) | How AgentLife organizes capabilities |
| [MCP Integration](guides/mcp-integration.md) | Adding and configuring MCP servers |
| [Install: Linux](guides/linux.md) | Ubuntu, Debian, Fedora, Arch |
| [Install: macOS](guides/macos.md) | Apple Silicon & Intel |
| [Install: Raspberry Pi](guides/raspberry-pi.md) | ARM-based setups |
| [Install: VPS](guides/vps.md) | Cloud server deployment |
| [Install: Docker](guides/docker.md) | Containerized setup |
| [Install: WSL](guides/windows-wsl.md) | Windows + WSL2 |

## 🏗 Architecture

```
┌──────────────────────────────────────────────────┐
│  AgentLife Persona Pack                           │
│  ┌─────────┐ ┌──────────┐ ┌───────────────────┐ │
│  │ configs │ │  skills   │ │  use-cases/       │ │
│  │ & cron  │ │  (.md)    │ │  cron jobs        │ │
│  └─────────┘ └──────────┘ └───────────────────┘ │
├──────────────────────────────────────────────────┤
│    Hermes Agent (the runtime)                     │
│  ┌───────────┐ ┌──────────┐ ┌────────────────┐  │
│  │   Model   │ │  Tools   │ │  Gateways       │  │
│  │   Router  │ │  System  │ │  (Telegram,     │  │
│  │           │ │          │ │   Discord...)   │  │
│  └───────────┘ └──────────┘ └────────────────┘  │
├──────────────────────────────────────────────────┤
│  MCP Servers (tool providers via stdio/HTTP)      │
│  ┌──────┐ ┌────────┐ ┌──────┐ ┌───────────────┐ │
│  │ Time │ │ Files  │ │GitHub│ │ Finance / etc │ │
│  └──────┘ └────────┘ └──────┘ └───────────────┘ │
└──────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Why |
|----------|-----|
| **Layer on Hermes, not standalone** | Hermes already handles models, tools, memory, scheduling — no need to rebuild that |
| **Persona packs are additive** | Install multiple personas — they merge. Your agent knows about finances AND work |
| **MCP as the tool standard** | One protocol for all tool access. Plug in any compatible server |
| **Open source (MIT)** | Fork it, modify it, redistribute it. No license restrictions |

## 🔌 MCP Integration

MCP (Model Context Protocol) is the universal standard for connecting AI agents to tools. AgentLife embraces MCP as a core principle:

- **Every persona pack includes MCP server recommendations**
- **The base pack ships with starter MCP configs** (time, filesystem)
- **Use cases can be powered by MCP servers** instead of custom scripts
- **All MCP servers connect via Hermes' built-in MCP client**

### Quick Example

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/me/data"]
```

Add this to your Hermes config, restart, and your agent has access to time and file system tools automatically.

📖 **[Full MCP Integration Guide →](guides/mcp-integration.md)**

## 🧩 Repository Structure

```
agentlife/
├── README.md                 # This file
├── pyproject.toml            # Python package config
├── LICENSE                   # MIT license
├── .gitignore
├── agentlife/
│   ├── __init__.py            # Package init
│   ├── cli.py                 # CLI commands (setup, verify, update)
│   └── config.py              # Config loading & validation
├── packs/
│   ├── base/                  # Tier 1 — foundation
│   │   ├── config.yaml
│   │   ├── mcp/               # Recommended MCP server configs
│   │   ├── scripts/
│   │   └── skills/
│   ├── life-ops/              # Tier 2 — Life Ops persona
│   │   ├── config.yaml
│   │   ├── helpers/           # Python scripts for use cases
│   │   ├── scripts/           # Shell scripts for cron jobs
│   │   ├── skills/            # Hermes skill definitions
│   │   └── use-cases/         # Use case configs
│   └── template/              # Template for new persona packs
├── guides/
│   ├── getting-started.md
│   ├── mcp-integration.md
│   ├── concepts/              # Beginner primers
│   │   ├── what-is-an-ai-agent.md
│   │   ├── what-is-mcp.md
│   │   ├── how-hermes-works.md
│   │   └── three-tier-model.md
│   ├── linux.md
│   ├── macos.md
│   ├── raspberry-pi.md
│   ├── vps.md
│   ├── docker.md
│   └── windows-wsl.md
└── scripts/
    ├── install.sh             # One-liner installer
    └── verify.sh              # Health check
```

## 🤝 Contributing

AgentLife is open source (MIT) and community-driven. Contributions welcome!

- **Report bugs** — open a [GitHub Issue](https://github.com/agentlife1/agentlife/issues)
- **Suggest features** — start a Discussion or open an Issue
- **Create a persona pack** — use the [template pack](packs/template/) to build your own
- **Improve docs** — PRs for guides, concepts, and README are always welcome

See [`packs/template/PULL_REQUEST_TEMPLATE/persona-pack.md`](.github/PULL_REQUEST_TEMPLATE/persona-pack.md) for persona pack submission guidelines.

## 📄 License

MIT License — see [LICENSE](LICENSE).

---

<p align="center">
  <sub>Published by <a href="https://agentlife.io">Agentic Life</a> — a nonprofit dedicated to democratizing AI agents for individuals.</sub>
</p>