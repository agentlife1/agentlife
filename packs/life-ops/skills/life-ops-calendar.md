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

## MCP Integration

This skill gets dramatically better when MCP servers are available, because
calendar data is the single most useful thing an AI agent can call into
instead of asking you to paste it in. The skill works fine without MCP —
it falls back to the shell scripts in `packs/life-ops/scripts/` and any
`.ics` feed you point it at — but the rich, real-time experience comes
from enabling the servers below.

### Recommended MCP servers

| Server | What it unlocks | Needs an API key? | Config snippet |
|--------|-----------------|-------------------|----------------|
| **google_calendar** | Read events from your real Google Calendar (multiple calendars, recurring events, attendees, locations) | Yes (Google OAuth) | `packs/base/mcp/` (community server) |
| **caldav** | Read any CalDAV calendar — Fastmail, iCloud, Nextcloud, Radicale, SOGo | No (use an app-specific password) | `uvx mcp-server-caldav` |
| **time** | Correct cross-timezone meeting math when you travel or work remote | No | `uvx mcp-server-time` |
| **sqlite** | Local history DB so the weekly audit can show trends over months/years | No | `uvx mcp-server-sqlite --db ~/agentlife/calendar.db` |

### How the agent uses MCP for this skill

- **Daily Calendar Brief** — calls `list_events` (Google/CalDAV) instead of
  asking you what your day looks like, then runs the meeting-load
  calculation against the result.
- **Meeting Overload Alerts** — live data means the alert fires the moment
  a new event pushes you over 60%, not the next morning.
- **Focus Time Suggestions** — the agent scans the actual event list and
  finds real gaps (not guesses) suitable for deep work.
- **Weekly Time Audit** — writes each event to the SQLite DB so the audit
  can break down time spent by category (meetings, focus, 1:1s, admin)
  *and* show how that's trending week-over-week.

### How to enable

1. Pick the calendar source you actually use (Google vs. CalDAV).
2. Copy the matching config from `packs/base/mcp/` (Google) or use the
   `mcp-server-caldav` snippet from the calendar-ops use case YAML into
   your `~/.hermes/config.yaml` under `mcp_servers:`.
3. Set `mcp.enabled: true` in
   `packs/life-ops/use-cases/calendar-ops.yaml`.
4. Restart Hermes — MCP discovery happens at startup.
5. Verify: `hermes tools list | grep mcp_`

For the full conceptual overview and security notes, see
[`guides/mcp-integration.md`](../../../../guides/mcp-integration.md).