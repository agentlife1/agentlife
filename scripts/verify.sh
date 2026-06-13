#!/usr/bin/env bash
# AgentLife Verify — post-install health check
# Usage: agentlife verify  (or standalone)
#
# Checks:
#   - Hermes CLI available
#   - Hermes config file exists
#   - Hermes process running
#   - Gateway port responsive
#   - Python version OK
#   - AgentLife config present

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────
RESET='\033[0m'
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'

ok()   { echo -e "  ${GREEN}✓${RESET} $1"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}✗${RESET} $1"; FAIL=$((FAIL + 1)); }
warn() { echo -e "  ${YELLOW}⚠${RESET} $1"; WARN=$((WARN + 1)); }

PASS=0
FAIL=0
WARN=0

echo ""
echo -e "${BOLD}${CYAN}AgentLife Health Check${RESET}"
echo -e "${CYAN}──────────────────────────${RESET}"
echo ""

# 1. Hermes CLI
if command -v hermes &>/dev/null; then
  VER=$(hermes --version 2>/dev/null || echo "installed")
  ok "Hermes CLI ($VER)"
else
  fail "Hermes CLI — not found in PATH"
fi

# 2. Hermes config
if [ -f "$HOME/.hermes/config.yaml" ]; then
  ok "Hermes config (~/.hermes/config.yaml)"
else
  fail "Hermes config — ~/.hermes/config.yaml missing"
fi

# 3. Hermes process
if pgrep -f "hermes" &>/dev/null; then
  ok "Hermes process (running)"
else
  warn "Hermes process — not running (start: hermes daemon)"
fi

# 4. Gateway health
if command -v curl &>/dev/null; then
  HTTP=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9119/health 2>/dev/null || echo "000")
  if [ "$HTTP" != "000" ]; then
    ok "Gateway (port 9119 — HTTP $HTTP)"
  else
    warn "Gateway — port 9119 not responding"
  fi
else
  warn "Gateway — skip (curl not available)"
fi

# 5. Python version
PY_VER=$(python3 --version 2>/dev/null || echo "none")
PY_MAJOR=$(echo "$PY_VER" | grep -oP '\d+' | head -1)
PY_MINOR=$(echo "$PY_VER" | grep -oP '\d+\.\K\d+' | head -1)
if [ "$PY_MAJOR" = "3" ] && [ "$PY_MINOR" -ge 10 ] 2>/dev/null; then
  ok "Python $PY_VER"
else
  fail "Python — need 3.10+, found $PY_VER"
fi

# 6. AgentLife config
if [ -f "$HOME/.hermes/agentlife/config.json" ]; then
  PERSONAS=$(python3 -c "import json; d=json.load(open('$HOME/.hermes/agentlife/config.json')); print(d.get('display_name','?'))" 2>/dev/null || echo "configured")
  ok "AgentLife config ($PERSONAS)"
else
  fail "AgentLife config — run 'agentlife setup' first"
fi

# 7. Framework configs valid
FRAMEWORK_DIR="$HOME/agentlife/framework"
VALIDATOR="$FRAMEWORK_DIR/packs/base/scripts/config-validate.py"
if [ -f "$VALIDATOR" ]; then
  if python3 "$VALIDATOR" &>/dev/null; then
    ok "Pack configs (all valid)"
  else
    fail "Pack configs — validation errors (run: python3 $VALIDATOR)"
  fi
else
  warn "Config validator — not found at $VALIDATOR"
fi

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}──────────────────────────${RESET}"
TOTAL=$((PASS + FAIL + WARN))
if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
  echo -e "  ${GREEN}✓${RESET} ${BOLD}All $PASS checks passed${RESET}"
  exit 0
elif [ "$FAIL" -eq 0 ]; then
  echo -e "  ${YELLOW}⚠${RESET} ${BOLD}$PASS passed, $WARN warnings${RESET}"
  exit 0
else
  echo -e "  ${RED}✗${RESET} ${BOLD}$PASS passed, $FAIL failed, $WARN warnings${RESET}"
  exit 1
fi