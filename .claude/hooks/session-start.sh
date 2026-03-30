#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Session start: verifying environment..."

# Ensure scripts are executable
chmod +x "$CLAUDE_PROJECT_DIR/scripts/"*.sh

echo "Environment ready."
