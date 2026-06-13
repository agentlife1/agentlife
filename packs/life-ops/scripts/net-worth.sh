#!/usr/bin/env bash
# Life Ops — Net Worth Snapshot
# Uses portfolio-tracker.py to record daily balances
# Runs: weekdays at 7 AM

set -euo pipefail

TRACKER="${HOME}/agentlife/framework/packs/life-ops/helpers/portfolio-tracker.py"

if [ -f "$TRACKER" ]; then
  python3 "$TRACKER" snapshot
else
  echo "Portfolio tracker not found at $TRACKER"
  echo "Run 'python3 $TRACKER add ...' to configure accounts"
fi