#!/usr/bin/env bash
# Life Ops — Weekly Spending Digest
set -euo pipefail
TRACKER="${HOME}/agentlife/framework/packs/life-ops/helpers/expense-tracker.py"
[ -f "$TRACKER" ] && python3 "$TRACKER" week || echo "Expense tracker not found at $TRACKER"