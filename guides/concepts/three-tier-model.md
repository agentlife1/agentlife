# The Three-Tier Model

*How AgentLife organizes capabilities from foundation to your daily life.*

---

AgentLife organizes everything into three tiers. Think of it like building a house:

| Tier | Name | Analogy | What You Get |
|------|------|---------|-------------|
| 1 | **Base** | The foundation and utilities | Hermes connection, health checks, shared config |
| 2 | **Persona** | The floor plan and rooms | A way of living (Life Ops, Work, Health, etc.) |
| 3 | **Use Cases** | The furniture and appliances | Specific tools (portfolio tracker, budget, calendar) |

## Tier 1: Base Pack

The Base Pack is always installed. It provides:

- **Hermes connectivity** — makes sure your agent can reach the AI model
- **Shared configuration** — default settings for model, toolsets, display
- **Health checks** — daily system monitoring so you know your agent is running
- **Update checks** — weekly check for new persona pack versions
- **Security baseline** — minimum safe defaults for all installations

You never think about the Base Pack. It's just there, keeping things running.

## Tier 2: Persona Packs

A persona pack is a complete configuration for an **area of your life**. Each one includes:

- **Skills** — your agent knows how to handle tasks in this domain
- **Cron jobs** — automated tasks that run on a schedule (daily brief, weekly reports)
- **MCP server configs** — tools the agent needs to access your accounts and data
- **Use cases** — specific configurations that you can enable individually

### Current Personas

| Persona | Focus | Coming |
|---------|-------|--------|
| **Life Ops** | Finances, calendar, subscriptions, daily operations | ✅ Now |
| **Work** | Email, tasks, meetings, project management | Future |
| **Health** | Fitness tracking, nutrition, medical records | Future |
| **Home** | Smart home, maintenance, grocery lists | Future |

You can install multiple personas. They merge together — your agent knows about your finances from Life Ops and your meetings from Work.

## Tier 3: Use Cases

Within each persona, use cases are the individual features you can turn on/off.

For Life Ops:

```
Life Ops Persona
├── Portfolio Tracking ───── track investments, net worth, rebalance alerts
├── Expense Tracking ─────── categorize spending, budget vs actual
├── Calendar Ops ─────────── daily agenda, time audits, focus suggestions
└── Bills & Subscriptions ── renewal tracking, 14-day alerts, annual cost
```

Each use case can be enabled independently. Maybe you want portfolio tracking but don't need calendar ops yet. That's fine — enable what you need, leave the rest.

## How Tiers Interact

```
Tier 1: Base
   │ provides: connectivity, health, shared defaults
   ▼
Tier 2: Persona (Life Ops)
   │ provides: skills, cron schedule, persona config
   ▼
Tier 3: Use Cases (Portfolio, Expenses, Calendar, Bills)
   │ provides: specific tool configs, job scripts
   ▼
Your daily experience ─── the agent works for you
```

A daily brief cron job (Tier 2) calls portfolio data (Tier 3), which uses Hermes tools (via Tier 1's health-checked infrastructure) and MCP servers (configured from recommendations in the persona).

## Why Three Tiers?

1. **Composability** — mix and match personas and use cases like LEGO bricks
2. **Progressive complexity** — start with one use case, add more over time
3. **Clean separation** — base doesn't change when you switch personas, personas don't repeat base config
4. **Beginner-friendly** — start with one use case, expand as you get comfortable

---

**Ready to start?** → [Getting Started Guide](../getting-started.md)