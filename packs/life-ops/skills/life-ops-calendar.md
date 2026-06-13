---
name: life-ops-calendar
description: "Calendar optimization — time audit, meeting load, focus time suggestions"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: life-ops
    tier: 3
    use_case: calendar-ops
    cron: daily-calendar-brief
---

# Calendar Ops

Audit your calendar, track meeting load, and reclaim focus time.

## Features

- **Daily Calendar Brief** — today's events, meeting load percentage
- **Meeting Overload Alerts** — notify when meetings exceed configured threshold (default: 60%)
- **Focus Time Suggestions** — identify gaps for deep work
- **Weekly Time Audit** — breakdown of how time was spent (meetings, focus, admin, 1:1s)

## Configuration

Configured in the Calendar Ops use case:
- Working hours (default: 9 AM — 5 PM)
- Meeting overload threshold (default: 60%)
- Excluded calendars (holidays, personal)

## Cron Integration

- `daily-calendar-brief`: Weekdays at 6 AM — feeds into Daily Brief
- `weekly-time-audit`: Monday at 8 AM

## Manual Use

```
What does my calendar look like today?
How much time did I spend in meetings this week?
Find me 3 hours of focus time this afternoon.
```