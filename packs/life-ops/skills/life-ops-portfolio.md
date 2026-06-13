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