#!/usr/bin/env bash
# Life Ops — Net Worth Snapshot
# Pulls account balances and calculates total net worth
# Runs: weekdays at 7 AM

set -euo pipefail

DATA_DIR="${HOME}/.hermes/agentlife/data"
mkdir -p "$DATA_DIR"

# ── Pull from Plaid if configured ───────────────────────────────
# Placeholder for Plaid API integration
# When configured, this calls the Plaid API and aggregates balances

# ── Generate snapshot ───────────────────────────────────────────
SNAPSHOT_FILE="${DATA_DIR}/net-worth.json"

# Placeholder: if no data yet, create default
if [ ! -f "$SNAPSHOT_FILE" ]; then
  cat > "$SNAPSHOT_FILE" << EOF
{
  "date": "$(date +%Y-%m-%d)",
  "total": 0,
  "accounts": [],
  "source": "not_configured"
}
EOF
fi

echo "Net worth data: $SNAPSHOT_FILE"