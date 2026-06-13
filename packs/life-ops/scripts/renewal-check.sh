#!/usr/bin/env bash
# Life Ops — Subscription Renewal Check
set -euo pipefail
HELPER="${HOME}/agentlife/framework/packs/life-ops/helpers/subscription-manager.py"
[ -f "$HELPER" ] && python3 "$HELPER" due 14 || echo "Subscription manager not found at $HELPER"