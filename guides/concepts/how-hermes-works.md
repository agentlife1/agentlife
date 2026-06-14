# How Hermes Agent Works

*The agent framework that powers everything — explained without the jargon.*

---

## In One Sentence

Hermes Agent is the software that turns an AI model (like Claude or DeepSeek) from a chatbot that can only talk into an agent that can **do things** — run commands, access files, browse the web, and act on a schedule.

## What Hermes Provides

Think of Hermes as the **operating system for your AI agent**. Just like Windows or macOS manages your computer's hardware, Hermes manages:

### 🧠 Model Access
Hermes connects to 20+ AI models from different providers (OpenRouter, Anthropic, OpenAI, DeepSeek, Google, local models). You can switch models mid-conversation — no config changes needed.

### 🔧 Tool System
Hermes gives the AI access to real tools:
- Run terminal commands
- Read and write files
- Search the web
- Browse websites
- Send messages (Telegram, Discord, email)
- Generate images
- Delegate tasks to sub-agents

Each tool is a capability the AI can use when it decides it needs to.

### 💾 Memory
Hermes remembers across sessions. It stores facts about you (name, preferences, environment) and can recall past conversations. You don't have to reintroduce yourself every time.

### 🧩 Skills
Skills are reusable instruction sets Hermes can load. Think of them as pluggable expertise — load a "portfolio tracking" skill, and Hermes knows how to check your investments. Skills are what AgentLife creates and bundles into persona packs.

### ⏰ Cron (Scheduling)
Hermes can run tasks on a schedule without you being present. "Send me a daily brief at 7 AM" becomes a cron job that fires every weekday morning.

### 🔊 Gateway (Messaging)
Hermes connects to Telegram, Discord, Slack, WhatsApp, email, and more. You can chat with your agent from any platform, and it replies in the same place.

## The Key Insight: Hermes = Middleware

Hermes isn't the AI model. It's the **middleware** between the AI model and your world:

```
  AI Model (Claude, GPT, DeepSeek...)
         │ thinks and decides
         ▼
  Hermes Agent Framework
         │ provides tools and context
         ▼
  Your World (files, apps, accounts)
```

The AI does the thinking. Hermes does the doing. Your persona pack (AgentLife) dictates *what* to do.

## Why Hermes Instead of Building From Scratch?

Building an agent framework is a massive project. You'd need to build:
- Tool calling infrastructure
- Session management
- Memory persistence
- Multi-platform messaging
- Cron scheduling
- Model routing
- Sub-agent delegation
- Context compression
- Security controls

Hermes already does all of this. AgentLife focuses on what's unique — your **persona configuration** — and lets Hermes handle the infrastructure.

## What AgentLife Adds

AgentLife is a **persona layer on top of Hermes**. It provides:

- **Pre-built persona packs** (Life Ops, and more coming)
- **MCP server recommendations** per persona
- **Cron job configurations** for daily tasks
- **Skills** tuned to each persona
- **Guides** for setup and use
- **A CLI** to manage it all (`agentlife setup`, `agentlife verify`, `agentlife update`)

You install Hermes once. Then you install AgentLife persona packs to make it useful for your specific life.

## Architecture Summary

```
┌─────────────────────────────────────────────┐
│  AgentLife Persona Pack (this framework)     │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐│
│  │ Configs  │ │ Skills   │ │ MCP Servers  ││
│  │ & Cron   │ │ (expert  │ │ (tool access)││
│  │          │ │ guides)  │ │              ││
│  └──────────┘ └──────────┘ └──────────────┘│
├─────────────────────────────────────────────┤
│  Hermes Agent (the runtime)                 │
│  ┌──────────┐ ┌────────┐ ┌───────────────┐ │
│  │ Model    │ │ Tools  │ │ Gateways      │ │
│  │ Router   │ │ System │ │ (Telegram,    │ │
│  │          │ │        │ │  Discord...)  │ │
│  └──────────┘ └────────┘ └───────────────┘ │
├─────────────────────────────────────────────┤
│  MCP Servers (tool providers)               │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐  │
│  │ Time │ │Files │ │GitHub│ │ Finance  │  │
│  └──────┘ └──────┘ └──────┘ └──────────┘  │
└─────────────────────────────────────────────┘
```

---

**Next:** Learn how persona packs are organized → [The Three-Tier Model](three-tier-model.md)