#!/usr/bin/env python3
"""Portfolio Tracker — manual balance tracking with history and reports.

No external APIs required. Enter balances manually or import from CSV.
Stores data in ~/.hermes/agentlife/data/portfolio/

Usage:
  portfolio-tracker.py add     # Add/update an account balance
  portfolio-tracker.py snapshot # Daily snapshot of all accounts
  portfolio-tracker.py report   # Net worth summary report
  portfolio-tracker.py history  # Show balance history
  portfolio-tracker.py import   # Import from CSV
"""

import json
import csv
import sys
import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

DATA_DIR = Path.home() / ".hermes" / "agentlife" / "data" / "portfolio"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
HISTORY_FILE = DATA_DIR / "history.json"


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_accounts() -> dict[str, Any]:
    if ACCOUNTS_FILE.exists():
        return json.loads(ACCOUNTS_FILE.read_text())
    return {"accounts": [], "updated_at": None}


def save_accounts(data: dict):
    ACCOUNTS_FILE.write_text(json.dumps(data, indent=2))


def load_history() -> list[dict]:
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []


def save_history(history: list):
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def cmd_add(args: list[str]):
    """Add or update an account balance."""
    if len(args) < 2:
        print("Usage: portfolio-tracker.py add <name> <amount> [category]")
        print("   eg: portfolio-tracker.py add 'VTI' 85000 'US Stocks'")
        return

    name = args[0]
    try:
        amount = float(args[1])
    except ValueError:
        print(f"Invalid amount: {args[1]}")
        return
    category = args[2] if len(args) > 2 else "Uncategorized"

    data = load_accounts()
    accs = data["accounts"]

    # Update existing or add new
    for acc in accs:
        if acc["name"].lower() == name.lower():
            old_amount = acc["amount"]
            acc["amount"] = amount
            acc["category"] = category
            acc["updated_at"] = datetime.now().isoformat()
            print(f"Updated: {name} ${old_amount:,.2f} → ${amount:,.2f}")
            break
    else:
        accs.append({
            "name": name,
            "amount": amount,
            "category": category,
            "added_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        })
        print(f"Added: {name} ${amount:,.2f} [{category}]")

    data["updated_at"] = datetime.now().isoformat()
    save_accounts(data)


def cmd_snapshot(args: list[str]):
    """Take a daily snapshot of all account balances."""
    data = load_accounts()
    if not data["accounts"]:
        print("No accounts configured. Add some first:")
        print("  portfolio-tracker.py add 'Account Name' 100000 'Category'")
        return

    history = load_history()
    today = date.today().isoformat()

    # Check if snapshot already taken today
    for entry in history:
        if entry["date"] == today:
            print(f"Snapshot already exists for {today}")
            print(f"Total: ${entry['total']:,.2f}")
            return

    total = sum(a["amount"] for a in data["accounts"])
    snapshot = {
        "date": today,
        "total": round(total, 2),
        "accounts": [
            {"name": a["name"], "amount": a["amount"], "category": a["category"]}
            for a in data["accounts"]
        ],
    }

    history.append(snapshot)
    # Keep last 365 days
    if len(history) > 365:
        history = history[-365:]

    save_history(history)
    print(f"Snapshot saved: {today} — Net Worth: ${total:,.2f}")
    print(f"Accounts tracked: {len(data['accounts'])}")


def cmd_report(args: list[str]):
    """Print net worth summary."""
    data = load_accounts()
    history = load_history()

    if not data["accounts"] and not history:
        print("No portfolio data. Add accounts:")
        print("  portfolio-tracker.py add 'VTI' 85000 'US Stocks'")
        return

    print("=" * 50)
    print("           PORTFOLIO SUMMARY")
    print("=" * 50)

    if data["accounts"]:
        total = sum(a["amount"] for a in data["accounts"])
        print(f"\n📊 Current Net Worth: ${total:,.2f}")
        print(f"   Accounts: {len(data['accounts'])}")
        print()

        # Group by category
        cats: dict[str, float] = {}
        for a in data["accounts"]:
            cats[a["category"]] = cats.get(a["category"], 0) + a["amount"]

        print(f"{'Category':<20} {'Amount':>12} {'Alloc':>8}")
        print("-" * 42)
        for cat, amt in sorted(cats.items(), key=lambda x: -x[1]):
            pct = amt / total * 100 if total > 0 else 0
            print(f"{cat:<20} ${amt:>9,.2f} {pct:>7.1f}%")
        print("-" * 42)
        print(f"{'Total':<20} ${total:>9,.2f} {'100.0%':>8}")

    if history:
        first = history[0]
        last = history[-1]
        if len(history) > 1:
            change = last["total"] - first["total"]
            pct = change / first["total"] * 100 if first["total"] > 0 else 0
            print(f"\n📈 Since {first['date']}: ${change:+,.2f} ({pct:+.1f}%)")
            print(f"   Snapshots: {len(history)} days tracked")
    print()


def cmd_history(args: list[str]):
    """Show balance history."""
    history = load_history()
    if not history:
        print("No history. Run 'portfolio-tracker.py snapshot' daily.")
        return

    limit = int(args[0]) if args else 14
    print(f"\n{'Date':<14} {'Net Worth':>14} {'Change':>12}")
    print("-" * 42)
    prev = None
    for entry in history[-limit:]:
        total = entry["total"]
        change = ""
        if prev is not None:
            diff = total - prev
            change = f"${diff:+,.2f}"
        print(f"{entry['date']:<14} ${total:>10,.2f}  {change:>10}")
        prev = total
    print(f"\nShowing last {min(limit, len(history))} of {len(history)} days")


def cmd_import(args: list[str]):
    """Import accounts from CSV file.
    CSV format: name,amount,category
    """
    if not args:
        print("Usage: portfolio-tracker.py import <csv_file>")
        return

    csv_path = Path(args[0])
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return

    data = load_accounts()
    count = 0
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            name = row[0].strip()
            try:
                amount = float(row[1])
            except ValueError:
                continue
            category = row[2].strip() if len(row) > 2 else "Uncategorized"

            # Update existing or add
            for acc in data["accounts"]:
                if acc["name"].lower() == name.lower():
                    acc["amount"] = amount
                    acc["category"] = category
                    acc["updated_at"] = datetime.now().isoformat()
                    break
            else:
                data["accounts"].append({
                    "name": name,
                    "amount": amount,
                    "category": category,
                    "added_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                })
            count += 1

    data["updated_at"] = datetime.now().isoformat()
    save_accounts(data)
    print(f"Imported {count} accounts from {csv_path}")


def main():
    ensure_dirs()
    if len(sys.argv) < 2:
        print("Portfolio Tracker — usage:")
        print(f"  {sys.argv[0]} add <name> <amount> [category]")
        print(f"  {sys.argv[0]} snapshot")
        print(f"  {sys.argv[0]} report")
        print(f"  {sys.argv[0]} history [days]")
        print(f"  {sys.argv[0]} import <csv_file>")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "add": cmd_add,
        "snapshot": cmd_snapshot,
        "report": cmd_report,
        "history": cmd_history,
        "import": cmd_import,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()