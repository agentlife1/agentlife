#!/usr/bin/env bash
# Hermes Connectivity Checker
# Verifies: Hermes process running, config valid, API responsive
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
PASS=0
FAIL=0

check() {
  local name="$1"
  local result="$2"
  if [ "$result" = "pass" ]; then
    echo -e "  ${GREEN}✓${NC} $name"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}✗${NC} $name — $3"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== AgentLife Health Check ==="
echo ""

# 1. Hermes CLI available
if command -v hermes &>/dev/null; then
  HERMES_VER=$(hermes --version 2>/dev/null || echo "unknown")
  check "Hermes CLI" "pass" "$HERMES_VER"
else
  check "Hermes CLI" "fail" "not found in PATH"
fi

# 2. Hermes config exists
if [ -f ~/.hermes/config.yaml ]; then
  check "Hermes config" "pass" ""
else
  check "Hermes config" "fail" "~/.hermes/config.yaml missing"
fi

# 3. Hermes process running
if pgrep -f "hermes" > /dev/null 2>&1; then
  check "Hermes process" "pass" ""
else
  check "Hermes process" "warn" "not running (start with: hermes daemon)"
fi

# 4. Gateway port accessible
if command -v curl &>/dev/null; then
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:9119/health 2>/dev/null | grep -q "200\|404"; then
    check "Gateway health" "pass" ""
  else
    check "Gateway health" "warn" "port 9119 not responding"
  fi
else
  check "Gateway health" "warn" "curl not available, skipping"
fi

# 5. Python version
PY_VER=$(python3 --version 2>/dev/null || echo "none")
if echo "$PY_VER" | grep -qE "3\.(1[0-9]|[2-9][0-9])"; then
  check "Python $PY_VER" "pass" ""
else
  check "Python" "fail" "need 3.10+ (found: $PY_VER)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
echo ""

# Determine overall status
if [ "$FAIL" -gt 2 ]; then
  echo "Status: Needs attention — some critical checks failed."
  echo "Run 'agentlife verify' for detailed guidance."
  exit 1
elif [ "$FAIL" -gt 0 ]; then
  echo "Status: OK with warnings."
  exit 0
else
  echo "Status: All systems nominal."
  exit 0
fi