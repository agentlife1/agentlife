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