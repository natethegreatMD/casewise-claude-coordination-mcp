#!/bin/bash
# CCC Live Watcher - Run this to watch CCC sessions in real-time

echo "🔍 CCC Live Watcher"
echo "=================="
echo "This will watch all CCC session activity in real-time"
echo ""

# Default to watching the current directory
WATCH_DIR="${1:-./}"

# Navigate to CCC root directory
CCC_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
cd "$CCC_ROOT"

# Activate the environment if needed
if [ -f "scripts/activate_ccc.sh" ]; then
    source scripts/activate_ccc.sh
fi

# Run the watcher
python scripts/ccc_live_watcher.py "$WATCH_DIR"
