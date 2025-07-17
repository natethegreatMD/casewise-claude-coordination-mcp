#!/bin/bash
# CCC Orchestrator Handoff Script
# Launches a new orchestrator with full permissions when context limit approached

echo "🔄 CCC Orchestrator Handoff"
echo "=========================="
echo "This script hands off to a fresh orchestrator session"
echo ""

# Save current state
HANDOFF_FILE="orchestrator_handoff_state.md"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create handoff state file
cat > "$HANDOFF_FILE" << EOF
# CCC Orchestrator Handoff State
Generated: $TIMESTAMP

## Instructions for New Orchestrator
You are taking over as the CCC orchestrator. Continue building the Claude Code Coordinator.

## Current Status
- Core concept proven: Can spawn and control Claude sessions
- Live monitoring working: scripts/watch_ccc.sh
- Directory organized and cleaned
- Ready to build full MCP server

## Your Next Tasks
1. Continue from TODO list (see below)
2. Build the complete CCC MCP server
3. Implement session orchestration
4. Create specialized templates

## Active TODOs
$(cat CLAUDE.md | grep -A 20 "## Current Status" || echo "Check CLAUDE.md for current status")

## Key Commands
- Activate environment: source scripts/activate_ccc.sh
- Watch live sessions: ./scripts/watch_ccc.sh
- Verify permissions: ./scripts/verify_permissions.sh

## IMPORTANT
You have --dangerously-skip-permissions for full autonomy.
Continue with FULL FORCE development approach - no boundaries!
EOF

echo "✅ Handoff state saved to: $HANDOFF_FILE"
echo ""
echo "🚀 Launching new orchestrator..."
echo ""

# Launch new Claude with dangerous permissions and handoff context
claude --dangerously-skip-permissions --continue "I'm the new CCC orchestrator taking over. Read these files in order: 1) HANDOFF.md for acute/immediate context from previous orchestrator, 2) CLAUDE.md for project documentation. Continue building CCC with full autonomy. The previous orchestrator left detailed state in HANDOFF.md."