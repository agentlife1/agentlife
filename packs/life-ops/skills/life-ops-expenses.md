---
name: life-ops-expenses
description: "Expense tracking — auto-categorization, spending digest, budget vs actual"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: life-ops
    tier: 3
    use_case: expense-tracking
    cron: weekly-spending-digest
---

# Expense Tracking

Auto-categorize your spending, track monthly burn, and compare against budget.

## Features

- **Auto-Categorization** — transactions sorted into categories (food, transport, housing, etc.)
- **Weekly Spending Digest** — summary of the week's spending with category breakdown
- **Budget vs Actual** — compare monthly spending against budget targets
- **Trend Analysis** — spending patterns over time (month-over-month, year-over-year)

## Configuration

Configured in the Expense Tracking use case:
- Budget categories and monthly targets
- Sync provider (Actual Budget, Firefly III, or manual CSV import)
- Notification preferences (digest frequency, alert thresholds)

## Cron Integration

- `weekly-spending-digest`: Monday at 9 AM
- `monthly-budget-report`: 1st of month at 10 AM

Feeds into the Daily Brief.

## Manual Use

```
How much did I spend this week?
Show my spending by category this month.
Am I on track for my budget?
Alert me if I'm over budget in any category.
```

## MCP Integration

Expense tracking is one of the highest-value MCP integrations in the
Life Ops persona, because the work is overwhelmingly about moving
structured financial data around — exactly what MCP tools are good at.
Without MCP, you're either hand-entering transactions or maintaining a
careful CSV pipeline. With MCP, the agent can pull transactions directly
from your bank/credit-card APIs, scrape portals that have no API, and
maintain a local DB that powers the digest automatically.

### Recommended MCP servers

| Server | What it unlocks | Needs an API key? |
|--------|-----------------|-------------------|
| **plaid** | Direct bank, credit card, and brokerage transaction feeds | Yes (Plaid dashboard) |
| **actual_budget** | Two-way sync with self-hosted Actual Budget | No (server URL + password) |
| **puppeteer** | Browser automation for portals without APIs (Amazon, Venmo, small-bank statements) | No |
| **sqlite** | Local transactions, category rules, and budget targets DB | No |
| **web_search** | Look up unfamiliar merchants during categorization | Yes (Tavily) |

### How the agent uses MCP for this skill

- **Auto-categorization** — when a new transaction comes in, the agent
  cross-references your rules in the SQLite DB, then falls back to
  web-searching the merchant to assign the right category. New rules
  are learned and saved automatically.
- **Weekly Spending Digest** — pulls the week's transactions from
  Plaid/Actual directly, so the digest reflects charges that settled
  *this morning* — not just what was in the CSV at midnight.
- **Budget vs Actual** — reads the live transaction DB instead of
  waiting for a batch import, so the "am I on track?" question gets a
  real answer.
- **Trend Analysis** — with months of data in SQLite, the agent can
  spot category drift (e.g. "dining is up 22% MoM for three months")
  and surface it in the daily brief.

### How to enable

1. Copy the server configs you want from `packs/base/mcp/` (Plaid,
   Actual, Puppeteer, SQLite) — or the snippets in
   `packs/life-ops/use-cases/expense-tracking.yaml` under
   `mcp.alternatives` — into `~/.hermes/config.yaml` under
   `mcp_servers:`.
2. Set `mcp.enabled: true` in
   `packs/life-ops/use-cases/expense-tracking.yaml`.
3. Restart Hermes and verify with `hermes tools list | grep mcp_`.

For the full conceptual overview and security notes, see
[`guides/mcp-integration.md`](../../../../guides/mcp-integration.md).