#!/usr/bin/env bash
# AgentLife Installer — one-liner for any platform
# Usage: curl -sfSL https://agentlife.io/install.sh | bash

set -euo pipefail

echo "=== AgentLife Framework Installer ==="
echo "Detecting platform..."

# Platform detection
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
  Linux)
    if [ -f /etc/rpi-issue ]; then
      echo "  Detected: Raspberry Pi (Linux $ARCH)"
      PLATFORM="raspberry-pi"
    else
      echo "  Detected: Linux ($ARCH)"
      PLATFORM="linux"
    fi
    ;;
  Darwin)
    echo "  Detected: macOS ($ARCH)"
    PLATFORM="macos"
    ;;
  *)
    echo "  Unsupported platform: $OS"
    echo "  See https://agentlife.io/guides/ for manual install"
    exit 1
    ;;
esac

echo ""
echo "  Guide: https://agentlife.io/guides/$PLATFORM"
echo ""
echo "  Run 'agentlife setup' after installing Hermes to configure your persona."
echo ""

exit 0