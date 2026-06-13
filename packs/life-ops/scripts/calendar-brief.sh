#!/usr/bin/env bash
# Life Ops — Calendar Brief
set -euo pipefail
HELPER="${HOME}/agentlife/framework/packs/life-ops/helpers/calendar-ops.py"
[ -f "$HELPER" ] && python3 "$HELPER" audit || echo "Calendar helper not found at $HELPER"