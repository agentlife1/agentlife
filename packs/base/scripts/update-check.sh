#!/usr/bin/env bash
# AgentLife — Pack Update Checker
# Checks for new versions of installed persona packs
# Runs: weekly on Monday at 5 AM

set -euo pipefail

echo "=== AgentLife Pack Update Check ==="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

FRAMEWORK_DIR="${HOME}/agentlife/framework"

if [ ! -d "$FRAMEWORK_DIR/.git" ]; then
  echo "Framework not in a git repo — can't check for updates."
  echo "Clone the repo to get updates:"
  echo "  git clone https://github.com/agentlife/agentlife.git"
  exit 0
fi

cd "$FRAMEWORK_DIR"

# Fetch latest without merging
git fetch origin 2>/dev/null || { echo "Could not reach GitHub — check network"; exit 0; }

# Compare local vs remote
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
CURRENT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

if [ "$BEHIND" -gt 0 ]; then
  echo "Updates available: $BEHIND commit(s) behind"
  echo "Current: $CURRENT_HASH"
  echo "Run 'agentlife update' to pull the latest packs."
else
  echo "Up to date (commit $CURRENT_HASH)"
fi