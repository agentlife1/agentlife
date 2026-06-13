#!/usr/bin/env python3
"""Calendar Ops Helper — calendar analysis, meeting load, focus time.

Tracks meeting patterns and suggests focus time.
For Google Calendar integration, see: https://developers.google.com/calendar/api/quickstart/python

Usage:
  calendar-ops.py audit          # Analyze calendar for meeting load
  calendar-ops.py focus          # Suggest focus time blocks
  calendar-ops.py add <time> <event>  # Log a manual event
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any

DATA_DIR = Path.home() / ".hermes" / "agentlife" / "data" / "calendar"
EVENTS_FILE = DATA_DIR / "events.json"


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_events() -> list[dict]:
    if EVENTS_FILE.exists():
        return json.loads(EVENTS_FILE.read_text())
    return []


def save_events(events: list):
    EVENTS_FILE.write_text(json.dumps(events, indent=2))


def cmd_audit(args: list[str]):
    """Analyze calendar for meeting load."""
    events = load_events()
    today = date.today()
    week_events = [e for e in events
                   if datetime.fromisoformat(e["date"]).date() >= today - timedelta(days=7)]

    print(f"\n{'=' * 40}")
    print(f"  TIME AUDIT — Last 7 Days")
    print(f"{'=' * 40}")

    if not week_events:
        print("  No events logged. Add events with:")
        print("  calendar-ops.py add '14:00-15:00' 'Team standup'")
    else:
        total_meeting_hours = 0
        for e in week_events:
            dur = e.get("duration_minutes", 60)
            total_meeting_hours += dur
            print(f"  {e['date'][:10]} {e.get('event','?')} ({dur}min)")

        avg_daily = total_meeting_hours / 7
        print(f"\n  Total meeting time: {total_meeting_hours} min ({total_meeting_hours/60:.1f}h)")
        print(f"  Daily avg: {avg_daily:.0f} min ({avg_daily/60:.1f}h)")
        load_pct = avg_daily / (8 * 60) * 100
        if load_pct > 60:
            print(f"  ⚠ Meeting load: {load_pct:.0f}% — above 60% threshold")
        else:
            print(f"  ✓ Meeting load: {load_pct:.0f}% — healthy")
    print()


def cmd_focus(args: list[str]):
    """Suggest focus time blocks."""
    events = load_events()
    today = date.today()
    today_events = [e for e in events
                    if datetime.fromisoformat(e["date"]).date() == today]

    print(f"\n{'=' * 40}")
    print(f"  FOCUS TIME — {today}")
    print(f"{'=' * 40}")

    if not today_events:
        print("  No events today — full day for focus!")
        print("  Suggested blocks:")
        print("    09:00-12:00  (3h deep work)")
        print("    14:00-17:00  (3h deep work)")
    else:
        total_meeting = sum(e.get("duration_minutes", 60) for e in today_events)
        available = 8 * 60 - total_meeting
        print(f"  Meetings: {total_meeting} min ({total_meeting/60:.1f}h)")
        print(f"  Available: {available} min ({available/60:.1f}h)")
        if available > 120:
            print(f"  Focus time available: {available} min ✓")
        else:
            print(f"  ⚠ Only {available} min focus time available")
    print()


def cmd_add(args: list[str]):
    """Log a manual event."""
    if len(args) < 2:
        print("Usage: calendar-ops.py add <time> <event> [duration_min]")
        return
    time_str = args[0]
    event_name = " ".join(args[1:-1]) if len(args) > 2 else args[1]
    duration = int(args[-1]) if len(args) > 2 and args[-1].isdigit() else 60

    entry = {
        "date": datetime.now().isoformat(),
        "event": event_name,
        "time": time_str,
        "duration_minutes": duration,
    }
    events = load_events()
    events.append(entry)
    save_events(events)
    print(f"Logged: {event_name} @ {time_str} ({duration}min)")


def main():
    ensure_dirs()
    if len(sys.argv) < 2:
        print("Calendar Ops — usage:")
        print(f"  {sys.argv[0]} audit")
        print(f"  {sys.argv[0]} focus")
        print(f"  {sys.argv[0]} add <time> <event> [duration_min]")
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {"audit": cmd_audit, "focus": cmd_focus, "add": cmd_add}
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()