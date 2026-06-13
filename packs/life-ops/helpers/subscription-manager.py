#!/usr/bin/env python3
"""Subscription Manager — track recurring charges, renewal alerts.

Usage:
  subscription-manager.py add <name> <amount> <renewal_date> [category]
  subscription-manager.py list
  subscription-manager.py renewals    # Show upcoming renewals
  subscription-manager.py report      # Total monthly committed spend
  subscription-manager.py due         # Check what's due in 14 days
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any

DATA_DIR = Path.home() / ".hermes" / "agentlife" / "data" / "subscriptions"
SUBS_FILE = DATA_DIR / "subscriptions.json"


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_subs() -> list[dict]:
    if SUBS_FILE.exists():
        return json.loads(SUBS_FILE.read_text())
    return []


def save_subs(subs: list):
    SUBS_FILE.write_text(json.dumps(subs, indent=2))


def cmd_add(args: list[str]):
    if len(args) < 3:
        print("Usage: subscription-manager.py add <name> <amount> <renewal_date> [category]")
        print("  renewal_date format: 2026-07-15 or 15th")
        return
    name = args[0]
    try:
        amount = float(args[1])
    except ValueError:
        print(f"Invalid amount: {args[1]}")
        return
    renewal = args[2]
    category = args[3] if len(args) > 3 else "General"

    # Parse renewal date
    try:
        if renewal.endswith(("st", "nd", "rd", "th")):
            day = int(renewal[:-2])
            renewal_date = date.today().replace(day=day)
            if renewal_date < date.today():
                renewal_date = renewal_date.replace(year=renewal_date.year + 1) if renewal_date.month == 12 else renewal_date.replace(month=renewal_date.month + 1)
        else:
            renewal_date = datetime.strptime(renewal, "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        print(f"Invalid date: {renewal}")
        return

    sub = {
        "name": name,
        "amount": amount,
        "renewal_date": renewal_date.isoformat(),
        "category": category,
        "added_at": datetime.now().isoformat(),
    }
    subs = load_subs()
    subs.append(sub)
    save_subs(subs)
    print(f"Added: {name} ${amount:.2f}/mo (renews {renewal_date}) [{category}]")


def cmd_list(args: list[str]):
    subs = load_subs()
    if not subs:
        print("No subscriptions tracked. Add with:")
        print("  subscription-manager.py add 'Netflix' 15.99 '2026-07-15' 'Entertainment'")
        return

    print(f"\n{'=' * 50}")
    print("  SUBSCRIPTIONS")
    print(f"{'=' * 50}")
    total = 0
    for s in sorted(subs, key=lambda x: x["renewal_date"]):
        total += s["amount"]
        print(f"  {s['name']:<20} ${s['amount']:>6.2f}/mo  renews {s['renewal_date']}  [{s['category']}]")
    print(f"{'=' * 50}")
    print(f"  TOTAL: ${total:.2f}/mo (${total*12:.2f}/yr)")
    print()


def cmd_renewals(args: list[str]):
    """Show renewals in the next 30 days."""
    subs = load_subs()
    today = date.today()
    upcoming = []
    for s in subs:
        rd = datetime.strptime(s["renewal_date"], "%Y-%m-%d").date()
        days_until = (rd - today).days
        if 0 <= days_until <= 30:
            upcoming.append((s, days_until))
    upcoming.sort(key=lambda x: x[1])

    if not upcoming:
        print("No renewals in the next 30 days.")
        return

    print(f"\n{'=' * 50}")
    print(f"  UPCOMING RENEWALS — Next 30 Days")
    print(f"{'=' * 50}")
    for s, days in upcoming:
        print(f"  {s['name']:<20} ${s['amount']:>6.2f}  in {days:2d} days ({s['renewal_date']})")
    total = sum(s["amount"] for s, _ in upcoming)
    print(f"{'=' * 50}")
    print(f"  Due soon: ${total:.2f}")
    print()


def cmd_due(args: list[str]):
    """Show what's due in next N days (default: 14)."""
    lead = int(args[0]) if args else 14
    subs = load_subs()
    today = date.today()
    due = []
    for s in subs:
        rd = datetime.strptime(s["renewal_date"], "%Y-%m-%d").date()
        days_until = (rd - today).days
        if 0 <= days_until <= lead:
            due.append((s, days_until))
    due.sort(key=lambda x: x[1])

    if not due:
        print(f"No renewals due in the next {lead} days.")
        return

    print(f"\n🔔 Renewals Due Within {lead} Days:")
    for s, days in due:
        print(f"  {s['name']:<20} ${s['amount']:>6.2f}  in {days:2d} days")
    print()


def main():
    ensure_dirs()
    if len(sys.argv) < 2:
        print("Subscription Manager — usage:")
        print(f"  {sys.argv[0]} add <name> <amount> <renewal_date> [category]")
        print(f"  {sys.argv[0]} list")
        print(f"  {sys.argv[0]} renewals")
        print(f"  {sys.argv[0]} due [days]")
        print(f"  {sys.argv[0]} report")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        "add": cmd_add, "list": cmd_list,
        "renewals": cmd_renewals, "due": cmd_due,
    }
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()