#!/usr/bin/env bash
# Life Ops — Daily Brief (combined)
set -euo pipefail

DATE=$(date "+%A, %B %d, %Y")
echo "=== AgentLife Daily Brief ==="
echo "Date: $DATE"
echo ""

# Portfolio
echo "--- Portfolio ---"
TRACKER="${HOME}/agentlife/framework/packs/life-ops/helpers/portfolio-tracker.py"
[ -f "$TRACKER" ] && python3 "$TRACKER" snapshot 2>/dev/null && python3 "$TRACKER" report 2>/dev/null || echo "No portfolio data yet"

# Expenses
echo "--- Spending Today ---"
TRACKER="${HOME}/agentlife/framework/packs/life-ops/helpers/expense-tracker.py"
[ -f "$TRACKER" ] && python3 "$TRACKER" today 2>/dev/null || echo "No expense data yet"

# Calendar
echo "--- Calendar ---"
HELPER="${HOME}/agentlife/framework/packs/life-ops/helpers/calendar-ops.py"
[ -f "$HELPER" ] && python3 "$HELPER" audit 2>/dev/null || echo "No calendar events logged"

# Renewals
echo "--- Renewals ---"
HELPER="${HOME}/agentlife/framework/packs/life-ops/helpers/subscription-manager.py"
[ -f "$HELPER" ] && python3 "$HELPER" due 14 2>/dev/null || echo "No subscriptions configured"