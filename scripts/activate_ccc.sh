#!/bin/bash
# CCC Environment Activation Script
# Source this in any new Claude session for full permissions

export CCC_DIR="/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator"
export PATH="$HOME/.local/bin:$PATH"
export PYTHONPATH="$CCC_DIR/src:$PYTHONPATH"

# Activate CCC virtual environment
cd "$CCC_DIR"
source ccc_venv/bin/activate

echo "✅ CCC Environment Activated"
echo "📁 Working Directory: $(pwd)"
echo "🐍 Python: $(python --version)"
echo "📦 Pip: $(pip --version)"
echo "🔧 Available commands: git, python, pip, npm, node, curl, wget"

# Verify critical commands
echo "🔍 Command Verification:"
echo "  Git: $(git --version | head -1)"
echo "  Node: $(node --version 2>/dev/null || echo 'Not available')"
echo "  NPM: $(npm --version 2>/dev/null || echo 'Not available')"
echo "  Claude CLI: $(claude --version 2>/dev/null || echo 'Not available')"

# Load sudo password if available for autonomous operations
if [ -f "sudo_password.txt" ]; then
    export SUDO_PASSWORD=$(cat sudo_password.txt)
    echo "🔑 Sudo password loaded for autonomous operations"
fi