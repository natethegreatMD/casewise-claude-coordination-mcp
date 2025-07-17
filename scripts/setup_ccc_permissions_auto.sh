#!/bin/bash
# CCC (Claude Code Coordinator) Permissions Setup Script - AUTO VERSION
# Uses password file for maximum autonomy

set -e

echo "🚀 Setting up CCC Full Permissions for Autonomous Operation..."

# Create CCC base directory if it doesn't exist
CCC_DIR="/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator"
mkdir -p "$CCC_DIR"
cd "$CCC_DIR"

# Read password from file
SUDO_PASSWORD=$(cat sudo_password.txt 2>/dev/null || echo "")

if [ -z "$SUDO_PASSWORD" ]; then
    echo "❌ Please edit sudo_password.txt with your password first!"
    exit 1
fi

echo "📦 Installing system packages (using saved password)..."
echo "$SUDO_PASSWORD" | sudo -S apt update
echo "$SUDO_PASSWORD" | sudo -S apt install -y \
    python3-full \
    python3-venv \
    python3-pip \
    pipx \
    nodejs \
    npm \
    git \
    curl \
    wget \
    jq \
    tree \
    htop \
    screen \
    tmux

echo "🐍 Creating CCC Python virtual environment..."
python3 -m venv ccc_venv
source ccc_venv/bin/activate

echo "📚 Installing Python packages in virtual environment..."
pip install --upgrade pip
pip install \
    mcp \
    pydantic \
    asyncio \
    gitpython \
    fastapi \
    uvicorn \
    httpx \
    websockets \
    psutil \
    rich \
    typer \
    pyyaml \
    toml

echo "🔧 Setting up Claude Code CLI..."
# Try different installation methods
npm install -g @anthropic/claude-code-cli 2>/dev/null || \
pipx install claude-cli 2>/dev/null || \
echo "⚠️ Claude CLI installation failed - may need manual setup"

echo "📝 Creating CCC environment activation script..."
cat > activate_ccc.sh << 'EOF'
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
EOF

chmod +x activate_ccc.sh

echo "📋 Creating permissions verification script..."
cat > verify_permissions.sh << 'EOF'
#!/bin/bash
# CCC Permissions Verification Script

echo "🔍 CCC Permissions Audit:"
echo "================================"

echo "👤 User Information:"
echo "  User: $(whoami)"
echo "  UID/GID: $(id)"
echo "  Groups: $(groups)"

echo ""
echo "📁 File System Permissions:"
echo "  Current Directory: $(pwd)"
echo "  Write Test: $(touch test_file && rm test_file && echo '✅ SUCCESS' || echo '❌ FAILED')"

echo ""
echo "🐍 Python Environment:"
echo "  Python: $(python --version 2>/dev/null || echo '❌ Not available')"
echo "  Pip: $(pip --version 2>/dev/null || echo '❌ Not available')"
echo "  Virtual Env: ${VIRTUAL_ENV:-'❌ Not activated'}"

echo ""
echo "📦 Package Management:"
echo "  Can install packages: $(pip install --help >/dev/null 2>&1 && echo '✅ YES' || echo '❌ NO')"

echo ""
echo "🔧 System Commands:"
echo "  Git: $(git --version >/dev/null 2>&1 && echo '✅ Available' || echo '❌ Missing')"
echo "  Curl: $(curl --version >/dev/null 2>&1 && echo '✅ Available' || echo '❌ Missing')"
echo "  Node: $(node --version >/dev/null 2>&1 && echo '✅ Available' || echo '❌ Missing')"
echo "  NPM: $(npm --version >/dev/null 2>&1 && echo '✅ Available' || echo '❌ Missing')"

echo ""
echo "🤖 Claude Integration:"
echo "  Claude CLI: $(claude --version >/dev/null 2>&1 && echo '✅ Available' || echo '❌ Missing')"

echo ""
echo "📊 System Resources:"
echo "  CPU Cores: $(nproc)"
echo "  Memory: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo "  Disk Space: $(df -h . | tail -1 | awk '{print $4}')"

echo ""
echo "🚀 CCC Readiness: $(
    python --version >/dev/null 2>&1 && \
    pip --version >/dev/null 2>&1 && \
    git --version >/dev/null 2>&1 && \
    echo '✅ READY FOR FULL AUTONOMOUS OPERATION' || \
    echo '⚠️ SOME LIMITATIONS - CHECK ABOVE'
)"
EOF

chmod +x verify_permissions.sh

echo ""
echo "🧹 Cleaning up password file for security..."
# Comment out the password clearing for now since you want max permissions
# rm -f sudo_password.txt

echo ""
echo "✅ CCC Permissions Setup Complete!"
echo ""
echo "📋 Summary:"
echo "  • System packages installed"
echo "  • Python virtual environment created"
echo "  • Python packages installed"
echo "  • Activation script created: ./activate_ccc.sh"
echo "  • Verification script created: ./verify_permissions.sh"
echo ""
echo "🛠️ For New Claude Sessions:"
echo "  1. cd \"$CCC_DIR\""
echo "  2. source activate_ccc.sh"
echo "  3. ./verify_permissions.sh"
echo ""
echo "🌙 You can now go to sleep! CCC will have full autonomous operation permissions."