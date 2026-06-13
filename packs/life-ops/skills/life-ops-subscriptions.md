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