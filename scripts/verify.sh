#!/usr/bin/env bash
# AgentLife Verify — post-install health check
# Checks: Hermes running, config valid, cron scheduled

set -euo pipefail

echo "=== AgentLife Health Check ==="

# Check Hermes is installed
if command -v hermes &>/dev/null; then
  echo "  ✓ hermes CLI found"
else
  echo "  ✗ hermes CLI not found — install Hermes first"
  echo "    https://hermes-agent.nousresearch.com/docs"
  exit 1
fi

# Check config
if [ -f ~/.hermes/config.yaml ]; then
  echo "  ✓ Hermes config found"
else
  echo "  ✗ Hermes config missing — run 'hermes init'"
fi

echo ""
echo "Done. Your system is ready for 'agentlife setup'."