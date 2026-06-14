---
name: life-ops-daily-brief
description: "Morning brief — daily net worth, yesterday's spending, today's calendar, upcoming renewals"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: life-ops
    tier: 2
    cron: daily-brief
---

# Daily Brief

Your AI-powered morning briefing. Runs automatically each weekday morning, delivering a concise summary of your financial and calendar status.

## What It Reports

| Section | Source |
|---------|--------|
| **Net Worth** | Portfolio Tracking use case — latest account balances |
| **Spending Yesterday** | Expense Tracking use case — categorized transactions |
| **Today's Calendar** | Calendar Ops use case — meetings, events, focus time |
| **Upcoming Renewals** | Bill & Subscription use case — renewals in next 14 days |

## Sample Output

```
Good morning, Keith.

📊 Net Worth: $2,849,312 (+$1,847 since yesterday)
  Accounts tracked: 6

💳 Yesterday: $127.43 spent
  ☕ Coffee: $5.75
  🛒 Groceries: $64.20
  🚗 Gas: $57.48

📅 Today: 4 events, 3h 15m in meetings
  ⚠ Meeting load: 41% — good

🔔 Renewals this week:
  • Netflix ($15.99) — Jun 14
  • AWS ($47.23) — Jun 16

✅ 2.5h of focus time available
```

## Cron Integration

Configured automatically when Life Ops is selected. Runs weekdays at 6:30 AM. Delivered to your configured channel (Telegram/email/local).

## MCP Integration

The Daily Brief is the highest-leverage place to use MCP in the Life Ops
persona, because every section of the brief depends on a different data
source. With MCP enabled, the brief assembles itself from live data
across all four use cases in seconds. Without it, you wait for the
overnight shell scripts and a stale CSV snapshot.

### Which MCP servers feed which section

| Brief section | Source use case | Recommended MCP servers |
|---------------|-----------------|-------------------------|
| **Net Worth** | portfolio-tracking | `yahoo_finance`, `plaid`, `sqlite` |
| **Spending Yesterday** | expense-tracking | `plaid`, `actual_budget`, `sqlite` |
| **Today's Calendar** | calendar-ops | `google_calendar` *or* `caldav`, `time` |
| **Upcoming Renewals** | bill-subscriptions | `sqlite`, `gmail`, `puppeteer` |

### How the agent composes the brief with MCP

1. **Time anchor** — `mcp_time_get_current_time` pins the brief to *your*
   local timezone before pulling events, so the calendar section never
   shows "yesterday" by accident.
2. **Parallel data fetch** — Hermes can call multiple MCP tools in one
   turn, so the brief pulls portfolio, expenses, calendar, and renewals
   in parallel rather than serially.
3. **Cross-section reasoning** — because the agent has structured data
   from each tool, it can do things the shell scripts can't:
   - "Spending is up 18% — and two renewals are due this week; flag both."
   - "You have a 90-minute gap at 2pm and your portfolio dropped 3% —
     here's a market news summary."
4. **Self-healing fallback** — if any MCP server is unreachable, the
   corresponding section falls back to the use case's `fallback_mode`
   (CSV, manual entry, or a cached DB row) and the brief still ships on
   time.

### How to enable

This skill inherits the MCP configuration from each underlying use case.
Enable MCP on the use cases you want live data for:

```yaml
# packs/life-ops/use-cases/portfolio-tracking.yaml
mcp:
  enabled: true

# packs/life-ops/use-cases/expense-tracking.yaml
mcp:
  enabled: true

# packs/life-ops/use-cases/calendar-ops.yaml
mcp:
  enabled: true

# packs/life-ops/use-cases/bill-subscriptions.yaml
mcp:
  enabled: true
```

…and copy the server configs from `packs/base/mcp/` (or the
`mcp.alternatives` list in each use case YAML) into
`~/.hermes/config.yaml` under `mcp_servers:`.

For the full conceptual overview, see
[`guides/mcp-integration.md`](../../../../guides/mcp-integration.md).