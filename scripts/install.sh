#!/usr/bin/env bash
# AgentLife Installer — one-liner for any platform
# Usage: curl -sfSL https://agentlife.io/install.sh | bash
#
# What it does:
#   1. Detects platform (Linux/macOS/RPi/VPS/WSL)
#   2. Checks Python 3.10+
#   3. Installs pipx if missing
#   4. Installs Hermes Agent via pipx
#   5. Installs AgentLife framework
#   6. Runs agentlife setup

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────
RESET='\033[0m'
BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'

info()  { echo -e "  ${CYAN}•${RESET} $1"; }
ok()    { echo -e "  ${GREEN}✓${RESET} $1"; }
warn()  { echo -e "  ${YELLOW}⚠${RESET} $1"; }
fail()  { echo -e "  ${RED}✗${RESET} $1"; }
header(){ echo -e "\n${BOLD}${CYAN}$1${RESET}"; echo -e "${CYAN}──────────────────────${RESET}"; }

# ── Welcome ─────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}AgentLife Framework Installer${RESET}"
echo -e "${BLUE}  Your Life, Orchestrated by AI${RESET}"
echo ""

# ── Platform detection ─────────────────────────────────────────────
header "Detecting Platform"

OS="$(uname -s)"
ARCH="$(uname -m)"
IS_RPI=false
IS_WSL=false

case "$OS" in
  Linux)
    if [ -f /etc/rpi-issue ]; then
      IS_RPI=true
      ok "Raspberry Pi ($ARCH)"
      PLATFORM="raspberry-pi"
    elif grep -qi microsoft /proc/version 2>/dev/null; then
      IS_WSL=true
      ok "Windows WSL2 ($ARCH)"
      PLATFORM="windows-wsl"
    else
      ok "Linux ($ARCH)"
      PLATFORM="linux"
    fi
    ;;
  Darwin)
    ok "macOS ($ARCH)"
    PLATFORM="macos"
    ;;
  *)
    fail "Unsupported: $OS $ARCH"
    echo "  See https://agentlife.io/guides/ for manual install"
    exit 1
    ;;
esac

# ── Python check ───────────────────────────────────────────────────
header "Checking Python"

PYTHON=""
for cmd in python3.11 python3.10 python3; do
  if command -v "$cmd" &>/dev/null; then
    PY_VER=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+\.\d+' | head -1)
    MAJOR=$(echo "$PY_VER" | cut -d. -f1)
    MINOR=$(echo "$PY_VER" | cut -d. -f2)
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
      PYTHON="$cmd"
      ok "Python $PY_VER → $PYTHON"
      break
    else
      warn "Found Python $PY_VER but need 3.10+"
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  fail "Python 3.10+ not found"
  if [ "$PLATFORM" = "linux" ] || [ "$PLATFORM" = "raspberry-pi" ] || [ "$PLATFORM" = "windows-wsl" ]; then
    echo "  Install with: sudo apt install -y python3 python3-pip python3-venv"
  elif [ "$PLATFORM" = "macos" ]; then
    echo "  Install with: brew install python@3.11"
  fi
  echo "  See: https://agentlife.io/guides/$PLATFORM"
  exit 1
fi

# ── pipx check ─────────────────────────────────────────────────────
header "Setting Up pipx"

if command -v pipx &>/dev/null; then
  ok "pipx found"
else
  info "Installing pipx..."
  "$PYTHON" -m pip install --user pipx --quiet
  "$PYTHON" -m pipx ensurepath --quiet || true
  # Add to PATH for this session
  export PATH="$PATH:$HOME/.local/bin"
  if command -v pipx &>/dev/null; then
    ok "pipx installed"
  else
    fail "pipx install failed — try: $PYTHON -m pip install --user pipx"
    exit 1
  fi
fi

# ── Hermes install ─────────────────────────────────────────────────
header "Installing Hermes Agent"

if command -v hermes &>/dev/null; then
  HERMES_VER=$(hermes --version 2>/dev/null || echo "installed")
  ok "Hermes Agent already ($HERMES_VER)"
else
  info "Installing Hermes Agent (this may take a minute)..."
  pipx install hermes-agent --quiet 2>/dev/null || pipx install hermes-agent
  if command -v hermes &>/dev/null; then
    ok "Hermes Agent installed"
  else
    fail "Hermes install failed"
    info "Try manually: pipx install hermes-agent"
    exit 1
  fi
fi

# ── AgentLife framework ──────────────────────────────────────────
header "Installing AgentLife Framework"

if "$PYTHON" -c "import agentlife" 2>/dev/null; then
  ok "AgentLife already installed"
else
  info "Installing AgentLife..."
  pip install agentlife --quiet 2>/dev/null || pip install agentlife
  if "$PYTHON" -c "import agentlife" 2>/dev/null; then
    ok "AgentLife installed"
  else
    warn "pip install agentlife failed — using local framework"
    info "Framework is at: $HOME/agentlife/framework/"
    info "Run: cd ~/agentlife/framework && python3 -m agentlife.cli setup"
  fi
fi

# ── Start Hermes ─────────────────────────────────────────────────
header "Starting Hermes"

if pgrep -f "hermes daemon" &>/dev/null; then
  ok "Hermes is already running"
else
  info "Starting Hermes daemon..."
  hermes daemon &>/dev/null &
  sleep 2
  if pgrep -f "hermes" &>/dev/null; then
    ok "Hermes started"
  else
    warn "Could not start Hermes — start manually: hermes daemon"
  fi
fi

# ── AgentLife setup ───────────────────────────────────────────────
header "AgentLife Setup"

if command -v agentlife &>/dev/null || [ -f "$HOME/agentlife/framework/agentlife/cli.py" ]; then
  info "Run 'agentlife setup' to configure your persona"
  info "Or, if using the local framework:"
  info "  cd ~/agentlife/framework && python3 -m agentlife.cli setup"
else
  warn "agentlife CLI not in PATH — run: python3 -m agentlife.cli setup"
fi

# ── Done ──────────────────────────────────────────────────────────
header "Install Complete"
ok "Hermes Agent: installed"
ok "AgentLife: installed"
echo ""
echo -e "  ${BOLD}Next steps:${RESET}"
echo "  1. Run:  ${CYAN}agentlife setup${RESET}  (or the local equivalent)"
echo "  2. Run:  ${CYAN}agentlife verify${RESET}  (health check)"
echo "  3. See:  ${CYAN}https://agentlife.io/guides/$PLATFORM${RESET}"
echo ""