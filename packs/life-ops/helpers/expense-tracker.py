#!/usr/bin/env python3
"""Expense Tracker — manual expense logging with categorization and budgets.

Usage:
  expense-tracker.py add <amount> <category> [description]
  expense-tracker.py today      # Show today's spending
  expense-tracker.py week       # Show this week's spending
  expense-tracker.py month      # Show this month's spending
  expense-tracker.py report     # Budget vs actual report
  expense-tracker.py budget <category> <amount>  # Set monthly budget
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any

DATA_DIR = Path.home() / ".hermes" / "agentlife" / "data" / "expenses"
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_transactions() -> list[dict]:
    if TRANSACTIONS_FILE.exists():
        return json.loads(TRANSACTIONS_FILE.read_text())
    return []


def save_transactions(txns: list):
    TRANSACTIONS_FILE.write_text(json.dumps(txns, indent=2))


def load_budgets() -> dict[str, float]:
    if BUDGETS_FILE.exists():
        return json.loads(BUDGETS_FILE.read_text())
    return {}


def save_budgets(budgets: dict):
    BUDGETS_FILE.write_text(json.dumps(budgets, indent=2))


def cmd_add(args: list[str]):
    if len(args) < 2:
        print("Usage: expense-tracker.py add <amount> <category> [description]")
        return
    try:
        amount = float(args[0])
    except ValueError:
        print(f"Invalid amount: {args[0]}")
        return
    category = args[1]
    description = " ".join(args[2:]) if len(args) > 2 else ""

    txn = {
        "date": datetime.now().isoformat(),
        "amount": amount,
        "category": category,
        "description": description,
    }
    txns = load_transactions()
    txns.append(txn)
    save_transactions(txns)
    print(f"Added: ${amount:.2f} [{category}] {description}")


def _filter_txns(txns: list[dict], start: date, end: date) -> list[dict]:
    return [
        t for t in txns
        if start <= datetime.fromisoformat(t["date"]).date() <= end
    ]


def _print_txns(txns: list[dict], label: str):
    total = sum(t["amount"] for t in txns)
    by_cat: dict[str, float] = {}
    for t in txns:
        by_cat[t["category"]] = by_cat.get(t["category"], 0) + t["amount"]

    print(f"\n{'=' * 40}")
    print(f"  {label}")
    print(f"{'=' * 40}")
    print(f"  Total: ${total:,.2f}")
    print(f"  Transactions: {len(txns)}")
    if by_cat:
        print()
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
            pct = amt / total * 100 if total > 0 else 0
            print(f"  {cat:<20} ${amt:>8,.2f}  ({pct:.0f}%)")
    print()


def cmd_today(args: list[str]):
    txns = load_transactions()
    today = date.today()
    filtered = _filter_txns(txns, today, today)
    _print_txns(filtered, f"Today's Spending — {today}")


def cmd_week(args: list[str]):
    txns = load_transactions()
    today = date.today()
    start = today - timedelta(days=today.weekday())
    filtered = _filter_txns(txns, start, today)
    _print_txns(filtered, f"This Week — {start} to {today}")


def cmd_month(args: list[str]):
    txns = load_transactions()
    today = date.today()
    start = today.replace(day=1)
    filtered = _filter_txns(txns, start, today)
    _print_txns(filtered, f"This Month — {start.strftime('%B %Y')}")


def cmd_report(args: list[str]):
    txns = load_transactions()
    budgets = load_budgets()
    today = date.today()
    start = today.replace(day=1)

    filtered = _filter_txns(txns, start, today)
    total = sum(t["amount"] for t in filtered)
    by_cat: dict[str, float] = {}
    for t in filtered:
        by_cat[t["category"]] = by_cat.get(t["category"], 0) + t["amount"]

    print(f"\n{'=' * 50}")
    print(f"  BUDGET REPORT — {today.strftime('%B %Y')}")
    print(f"{'=' * 50}")
    print(f"  Spent: ${total:,.2f}")
    print()
    if budgets:
        print(f"{'Category':<20} {'Budget':>10} {'Actual':>10} {'Remain':>10}")
        print("-" * 52)
        all_cats = set(list(budgets.keys()) + list(by_cat.keys()))
        for cat in sorted(all_cats):
            b = budgets.get(cat, 0)
            a = by_cat.get(cat, 0)
            r = b - a
            status = "✓" if r >= 0 else "⚠ over"
            print(f"{cat:<20} ${b:>7,.2f} ${a:>7,.2f} ${r:>+7,.2f}  {status}")
        print("-" * 52)
        total_budget = sum(budgets.values())
        total_remain = total_budget - total
        print(f"{'Total':<20} ${total_budget:>7,.2f} ${total:>7,.2f} ${total_remain:>+7,.2f}")
    else:
        print("No budgets set. Set budgets with:")
        print("  expense-tracker.py budget <category> <amount>")
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
            pct = amt / total * 100 if total > 0 else 0
            print(f"  {cat:<20} ${amt:>8,.2f}  ({pct:.0f}%)")
    print()


def cmd_budget(args: list[str]):
    if len(args) < 2:
        print("Usage: expense-tracker.py budget <category> <amount>")
        return
    category = args[0]
    try:
        amount = float(args[1])
    except ValueError:
        print(f"Invalid amount: {args[1]}")
        return
    budgets = load_budgets()
    budgets[category] = amount
    save_budgets(budgets)
    print(f"Budget set: {category} = ${amount:,.2f}/month")


def main():
    ensure_dirs()
    if len(sys.argv) < 2:
        print("Expense Tracker — usage:")
        print(f"  {sys.argv[0]} add <amount> <category> [description]")
        print(f"  {sys.argv[0]} today")
        print(f"  {sys.argv[0]} week")
        print(f"  {sys.argv[0]} month")
        print(f"  {sys.argv[0]} report")
        print(f"  {sys.argv[0]} budget <category> <amount>")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        "add": cmd_add, "today": cmd_today, "week": cmd_week,
        "month": cmd_month, "report": cmd_report, "budget": cmd_budget,
    }
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()