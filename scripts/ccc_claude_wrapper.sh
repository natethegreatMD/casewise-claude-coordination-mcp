#!/bin/bash
# CCC Claude Wrapper - Runs Claude commands without permission prompts
# This script should be run from a terminal where --dangerously-skip-permissions is already active

# Function to run Claude with full autonomy
run_claude_autonomous() {
    local session_name=$1
    local prompt=$2
    local working_dir=${3:-$(pwd)}
    
    echo "🚀 Starting autonomous Claude session: $session_name"
    echo "📋 Task: $prompt"
    echo "📁 Working directory: $working_dir"
    
    # Create session directory
    mkdir -p "$working_dir"
    cd "$working_dir"
    
    # Run Claude with all bypass flags
    claude --dangerously-skip-permissions \
           --print \
           --permission-mode bypassPermissions \
           "$prompt"
}

# Export function for use
export -f run_claude_autonomous

# If called with arguments, run immediately
if [ $# -gt 0 ]; then
    run_claude_autonomous "$@"
fi