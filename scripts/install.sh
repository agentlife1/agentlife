#!/usr/bin/env bash
# AgentLife Installer — one-liner for any platform
# Usage: curl -sfSL https://agentlife.io/install.sh | bash
#
# What this does, step by step:
#   1. Detects your operating system (Linux, macOS, Raspberry Pi)
#   2. Checks you have Python 3.10+ installed
#   3. Installs pipx (a tool to run Python apps in isolated environments)
#   4. Installs Hermes Agent (the AI agent runtime) via pipx
#   5. Clones the AgentLife framework from GitHub
#   6. Installs AgentLife CLI (the `agentlife` command)
#   7. Installs the MCP SDK (for connecting to tools)
#   8. Runs the setup wizard
#
# Each step has a comment explaining WHY. If something fails,
# the error message tells you exactly what to do.

set -euo pipefail

# ── Colors ─────────────────────────────────────────────────────
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

# ── Welcome ─────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}AgentLife Framework Installer${RESET}"
echo -e "${BLUE}  Turn Hermes Agent into your personal AI operator${RESET}"
echo ""

# ── Step 1: Detect what platform we're on ──────────────────────
# Different platforms have different package managers and quirks.
# We detect this upfront so we can give specific instructions.
header "Detecting Platform"

OS="$(uname -s)"
ARCH="$(uname -m)"
IS_RPI=false
IS_WSL=false
PLATFORM=""

case "$OS" in
  Linux)
    if [ -f /etc/rpi-issue ]; then
      IS_RPI=true
      ok "Raspberry Pi detected ($ARCH)"
      PLATFORM="raspberry-pi"
    elif grep -qi microsoft /proc/version 2>/dev/null; then
      IS_WSL=true
      ok "Windows WSL2 detected ($ARCH)"
      PLATFORM="windows-wsl"
    else
      ok "Linux detected ($ARCH)"
      PLATFORM="linux"
    fi
    ;;
  Darwin)
    ok "macOS detected ($ARCH)"
    PLATFORM="macos"
    ;;
  *)
    fail "Unsupported operating system: $OS $ARCH"
    echo "  See https://agentlife.io/guides/ for manual install instructions"
    exit 1
    ;;
esac

# ── Step 2: Check for Python 3.10+ ─────────────────────────────
# AgentLife and Hermes both need Python 3.10 or newer.
# We look for python3.11 first (fastest), then python3.10, then plain python3.
header "Checking Python"

PYTHON=""
for cmd in python3.11 python3.10 python3; do
  if command -v "$cmd" &>/dev/null; then
    PY_VER=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+\.\d+' | head -1)
    MAJOR=$(echo "$PY_VER" | cut -d. -f1)
    MINOR=$(echo "$PY_VER" | cut -d. -f2)
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
      PYTHON="$cmd"
      ok "Python $PY_VER found → $PYTHON"
      break
    else
      warn "Found Python $PY_VER but AgentLife needs 3.10+"
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  fail "Python 3.10+ not found. Install it first:"
  if [ "$PLATFORM" = "linux" ] || [ "$PLATFORM" = "raspberry-pi" ] || [ "$PLATFORM" = "windows-wsl" ]; then
    echo "  Ubuntu/Debian: sudo apt install -y python3 python3-pip python3-venv"
  elif [ "$PLATFORM" = "macos" ]; then
    echo "  macOS: brew install python@3.11"
  fi
  echo "  Full guide: https://agentlife.io/guides/$PLATFORM"
  exit 1
fi

# ── Step 3: Install pipx ───────────────────────────────────────
# pipx installs Python applications in isolated environments so
# they don't conflict with each other. Hermes will live in its own
# pipx environment. AgentLife will be in another.
header "Setting Up pipx"

if command -v pipx &>/dev/null; then
  ok "pipx already installed"
else
  info "Installing pipx (isolated Python app runner)..."
  "$PYTHON" -m pip install --user pipx --quiet
  "$PYTHON" -m pipx ensurepath --quiet || true
  # Add to PATH for this session so we can use it immediately
  export PATH="$PATH:$HOME/.local/bin"
  if command -v pipx &>/dev/null; then
    ok "pipx installed"
  else
    fail "pipx install failed — try: $PYTHON -m pip install --user pipx"
    exit 1
  fi
fi

# ── Step 4: Install Hermes Agent ───────────────────────────────
# Hermes is the runtime that gives the AI model tools, memory,
# and scheduling. Think of it as the operating system for your agent.
header "Installing Hermes Agent"

if command -v hermes &>/dev/null; then
  HERMES_VER=$(hermes --version 2>/dev/null || echo "installed")
  ok "Hermes Agent already installed ($HERMES_VER)"
else
  info "Installing Hermes Agent via pipx (this may take a minute)..."
  pipx install hermes-agent --quiet 2>/dev/null || pipx install hermes-agent
  if command -v hermes &>/dev/null; then
    ok "Hermes Agent installed successfully"
  else
    fail "Hermes install failed — try manually: pipx install hermes-agent"
    exit 1
  fi
fi

# ── Step 5: Clone AgentLife Framework ──────────────────────────
# AgentLife configures Hermes with persona packs. It lives in
# ~/agentlife/framework/ so you can edit the configs directly.
header "Installing AgentLife Framework"

AGENTLIFE_DIR="$HOME/agentlife"
FRAMEWORK_DIR="$AGENTLIFE_DIR/framework"

if [ -d "$FRAMEWORK_DIR" ]; then
  ok "AgentLife framework already present at $FRAMEWORK_DIR"
  info "Run 'cd $FRAMEWORK_DIR && git pull' for updates"
else
  info "Cloning AgentLife framework to $FRAMEWORK_DIR..."
  mkdir -p "$AGENTLIFE_DIR"
  git clone --depth 1 https://github.com/agentlife1/agentlife.git "$FRAMEWORK_DIR"
  if [ -d "$FRAMEWORK_DIR" ]; then
    ok "AgentLife framework cloned"
  else
    fail "Clone failed — try manually: git clone https://github.com/agentlife1/agentlife.git"
    exit 1
  fi
fi

# ── Step 6: Install AgentLife CLI ──────────────────────────────
# This installs the `agentlife` command so you can run
# "agentlife setup" instead of "python3 -m agentlife.cli setup".
header "Installing AgentLife CLI"

if "$PYTHON" -m pip install -e "$FRAMEWORK_DIR" --quiet 2>/dev/null; then
  ok "AgentLife CLI installed"
else
  # Fallback: try without quiet
  "$PYTHON" -m pip install -e "$FRAMEWORK_DIR"
  ok "AgentLife CLI installed"
fi

# Add to PATH if needed
if ! command -v agentlife &>/dev/null; then
  # Try to find it in user bin directories
  for BIN_DIR in "$HOME/.local/bin" "$HOME/Library/Python/3.11/bin" "$HOME/.local/lib/python3.*/site-packages"; do
    if [ -f "$BIN_DIR/agentlife" ]; then
      export PATH="$PATH:$BIN_DIR"
      break
    fi
  done
fi

# ── Step 7: Install MCP SDK ────────────────────────────────────
# The MCP SDK lets Hermes connect to MCP servers (tools). Without it,
# your agent won't be able to use time lookups, file access, etc.
header "Installing MCP SDK"

"$PYTHON" -m pip install mcp --quiet 2>/dev/null && ok "MCP SDK installed" || warn "MCP SDK not installed (optional — needed for MCP server support)"

# ── Step 8: Run Setup Wizard ───────────────────────────────────
header "AgentLife Setup"

echo ""
echo -e "  ${BOLD}All dependencies installed!${RESET}"
echo -e "  Now let's configure your agent."
echo ""

# Try CLI first, fall back to module
if command -v agentlife &>/dev/null; then
  agentlife setup
else
  info "Running setup via python module..."
  "$PYTHON" -m agentlife.cli setup
fi

# ── Done ────────────────────────────────────────────────────────
header "Install Complete"

# If setup ran successfully, don't show next steps (setup already did)
# Otherwise, show what to do next
if [ $? -eq 0 ]; then
  echo ""
  echo -e "  ${GREEN}✓${RESET} Hermes Agent: installed"
  echo -e "  ${GREEN}✓${RESET} AgentLife: installed and configured"
  echo -e "  ${GREEN}✓${RESET} MCP SDK: ready"
  echo ""
  echo -e "  ${BOLD}Your agent is live.${RESET}"
  echo "  Your daily brief will arrive at the schedule you set."
  echo "  Run 'agentlife verify' anytime to check health."
fi