---
name: life-ops-portfolio
description: "Portfolio tracking — account aggregation, net worth, allocation, rebalance alerts"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: life-ops
    tier: 3
    use_case: portfolio-tracking
    cron: daily-net-worth
---

# Portfolio Tracking

Track your investment portfolio across accounts, monitor asset allocation, and get rebalance alerts.

## Features

- **Daily Net Worth Snapshot** — pull balances from linked accounts, calculate total
- **Asset Allocation** — breakdown by asset class (stocks, bonds, crypto, cash)
- **Rebalance Alerts** — notify when an asset class deviates from target by more than threshold
- **Performance Tracking** — track daily/weekly/monthly P&L

## Configuration

Configured in the Portfolio Tracking use case:
- Plaid API keys (optional — for automated account aggregation)
- Account list (or auto-discovered via Plaid)
- Rebalance tolerance (default: 10%)
- Threshold alerts (default: 5% daily drop)

## Cron Integration

Runs daily at 7 AM weekdays via `daily-net-worth` cron. Data feeds into the morning Daily Brief.

## Manual Use

```
Check my portfolio and net worth.
Show my asset allocation.
Alert me if my portfolio drops more than 5%. 
```

## Sample Output

```
📊 Portfolio Summary
  Net Worth: $2,849,312
  Day Change: +$1,847 (+0.07%)

  Asset Allocation:
  ┌──────────────────┬──────────┬──────────┬────────┐
  │ Asset            │ Current  │ Target   │ Status │
  ├──────────────────┼──────────┼──────────┼────────┤
  │ US Stocks        │ 58%      │ 60%      │ ✓ OK   │
  │ Intl Stocks      │ 22%      │ 20%      │ ✓ OK   │
  │ Bonds            │ 8%       │ 10%      │ ⚠ Low  │
  │ Cash             │ 12%      │ 10%      │ ⚠ High │
  └──────────────────┴──────────┴──────────┴────────┘
```

## MCP Integration

Portfolio tracking has the broadest MCP toolset in the Life Ops
persona, because real portfolio work is "ask a question, get a live
structured answer" — exactly the shape MCP is built for. Without MCP,
the use case falls back to a CSV of balances you maintain by hand;
with MCP, balances update themselves and the agent can answer follow-up
questions (allocation, drift, P&L) instantly.

### Recommended MCP servers

| Server | What it unlocks | Needs an API key? |
|--------|-----------------|-------------------|
| **yahoo_finance** | Real-time and historical quotes for stocks, ETFs, mutual funds, indices, crypto | No |
| **plaid** | Direct holdings + balances from linked brokerages, banks, retirement accounts | Yes (Plaid dashboard) |
| **sqlite** | Local history DB of net-worth snapshots and allocation snapshots | No |
| **web_search** | Live news and earnings headlines to explain daily moves | Yes (Tavily) |
| **time** | Correct timestamps for snapshots and time-weighted return calculations | No |

### How the agent uses MCP for this skill

- **Daily Net Worth Snapshot** — the agent calls Plaid for account
  balances *and* Yahoo Finance for unlinked positions, sums them, and
  writes the snapshot to the SQLite history DB. No manual entry.
- **Asset Allocation** — pulls current positions from Plaid, pulls
  prices from Yahoo Finance, groups by asset class, and compares
  against the targets from `config.alerts.rebalance_tolerance_pct`.
- **Rebalance Alerts** — runs the drift calculation against the *live*
  portfolio, not yesterday's CSV, so an alert fires the moment you
  cross the threshold (e.g. bonds drift below 8% → notify at next
  brief).
- **Performance Tracking** — pairs the SQLite snapshot history with
  Yahoo Finance historical data to compute time-weighted return, P&L
  in absolute dollars, and P&L adjusted for deposits/withdrawals.
- **Threshold Drops** — when `threshold_drop_pct` triggers, the agent
  pulls web-search context so the alert includes *why* the market
  moved, not just *that* it did.

### How to enable

1. Copy server configs from `packs/base/mcp/` (or the snippets in
   `packs/life-ops/use-cases/portfolio-tracking.yaml` under
   `mcp.alternatives`) into `~/.hermes/config.yaml` under
   `mcp_servers:`.
2. Set `mcp.enabled: true` in
   `packs/life-ops/use-cases/portfolio-tracking.yaml`.
3. Restart Hermes and verify with `hermes tools list | grep mcp_`.

For the full conceptual overview and security notes, see
[`guides/mcp-integration.md`](../../../../guides/mcp-integration.md).