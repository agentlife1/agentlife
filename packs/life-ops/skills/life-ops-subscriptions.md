---
name: life-ops-subscriptions
description: "Subscription management — renewal alerts, price tracking, total committed spend"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: life-ops
    tier: 3
    use_case: bill-subscriptions
    cron: renewal-check
---

# Bill & Subscription Management

Track all recurring charges, get renewal alerts, and monitor total committed monthly spend.

## Features

- **Subscription Inventory** — complete list of recurring charges
- **Renewal Alerts** — notify before subscriptions renew (configurable lead time, default: 14 days)
- **Price Increase Detection** — flag when a subscription price changes
- **Monthly Committed Spend** — total of all recurring charges

## Configuration

Configured in the Bill & Subscription use case:
- Subscription list (name, amount, renewal date, category)
- Alert lead time (default: 14 days)
- Provider: Wallos (self-hosted) or manual tracking

## Cron Integration

- `renewal-check`: Daily at 8 AM — checks for upcoming renewals
- `monthly-subscription-report`: 1st of month at 9 AM

Feeds into the Daily Brief.

## Manual Use

```
What subscriptions are renewing this week?
Show me my total monthly committed spend.
Alert me when any subscription price changes.
List all my subscriptions by category.
```

## MCP Integration

The subscription use case is where MCP turns a chore into a hands-off
system. Without MCP, you maintain a list and hope you remember to
update it; with MCP, the agent can discover subscriptions from your
inbox, check vendor sites for price changes, and keep a searchable
history automatically.

### Recommended MCP servers

| Server | What it unlocks | Needs an API key? |
|--------|-----------------|-------------------|
| **gmail** | Scan your inbox for receipts, renewal confirmations, and free-trial-ending emails to auto-discover subscriptions | Yes (Google OAuth) |
| **puppeteer** | Log into vendor portals, check renewal dates, detect price changes before they hit your statement | No |
| **sqlite** | Local DB of every subscription, its renewal date, full price history, category, and notes | No |
| **web_search** | Look up current public pricing to compare against what you're being charged | Yes (Tavily) |
| **time** | Correct renewal-date math across timezones and billing cycles | No |

### How the agent uses MCP for this skill

- **Subscription Inventory** — instead of asking you to enumerate
  every subscription, the agent scans Gmail for receipts and
  free-trial emails, writes each one to the SQLite DB with the
  amount and trial/renewal date, and prompts you only when it
  finds something ambiguous.
- **Renewal Alerts** — pulls the upcoming-renewals query from the
  live SQLite DB, so a cancellation you did yesterday is reflected
  in tomorrow's alert — not next month.
- **Price Increase Detection** — uses Puppeteer to log into vendor
  sites (or web_search to check public pricing) and compares
  against the SQLite price history. If Netflix raised you from
  $15.99 to $17.99, the next renewal-check fires an alert *with
  the dollar amount and the date of the change*.
- **Monthly Committed Spend** — sums the SQLite DB on demand and
  breaks it down by category, including subscriptions you forgot
  you were paying for.

### How to enable

1. Copy server configs from `packs/base/mcp/` (or the snippets in
   `packs/life-ops/use-cases/bill-subscriptions.yaml` under
   `mcp.alternatives`) into `~/.hermes/config.yaml` under
   `mcp_servers:`.
2. Set `mcp.enabled: true` in
   `packs/life-ops/use-cases/bill-subscriptions.yaml`.
3. Restart Hermes and verify with `hermes tools list | grep mcp_`.

For the full conceptual overview and security notes, see
[`guides/mcp-integration.md`](../../../../guides/mcp-integration.md).