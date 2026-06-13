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