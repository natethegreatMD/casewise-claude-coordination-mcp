#!/bin/bash
# CCC Installation Script
# Installs CCC and all dependencies

set -e  # Exit on error

echo "🚀 CCC (Claude Code Coordinator) Installation"
echo "============================================"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required (found $python_version)"
    exit 1
fi

echo "✅ Python $python_version found"

# Check if Claude CLI is installed
echo ""
echo "🔍 Checking for Claude CLI..."
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude CLI not found"
    echo "Please install Claude Code first: https://claude.ai/code"
    exit 1
fi

claude_version=$(claude --version 2>&1 | head -n1)
echo "✅ $claude_version found"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ -d "ccc_venv" ]; then
    echo "  Virtual environment already exists"
else
    python3 -m venv ccc_venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source ccc_venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install CCC in development mode
echo ""
echo "📦 Installing CCC..."
pip install -e .

# Create workspace directory
echo ""
echo "📁 Creating default workspace..."
mkdir -p ~/ccc_workspace

# Create shell activation script
echo ""
echo "🔧 Creating activation script..."
cat > activate_ccc.sh << 'EOF'
#!/bin/bash
# CCC Environment Activation

# Activate virtual environment
source ccc_venv/bin/activate

# Set environment variables
export CCC_WORKSPACE="${CCC_WORKSPACE:-~/ccc_workspace}"
export CCC_MAX_PARALLEL_SESSIONS="${CCC_MAX_PARALLEL_SESSIONS:-3}"

# Add scripts to PATH
export PATH="$PWD/scripts:$PATH"

echo "✅ CCC Environment Activated"
echo "📁 Workspace: $CCC_WORKSPACE"
echo "🚀 Run 'ccc --help' to get started"
EOF

chmod +x activate_ccc.sh

# Create desktop entry for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    desktop_file="$HOME/.local/share/applications/ccc.desktop"
    mkdir -p "$HOME/.local/share/applications"
    cat > "$desktop_file" << EOF
[Desktop Entry]
Name=CCC - Claude Code Coordinator
Comment=Orchestrate multiple Claude sessions
Exec=gnome-terminal -- bash -c "cd $PWD && source activate_ccc.sh && ccc status; exec bash"
Icon=$PWD/docs/ccc-icon.png
Terminal=true
Type=Application
Categories=Development;
EOF
    echo "✅ Desktop entry created"
fi

# Test installation
echo ""
echo "🧪 Testing installation..."
if python -c "import casewise_coordination; print(f'CCC v{casewise_coordination.__version__} imported successfully')"; then
    echo "✅ Import test passed"
else
    echo "❌ Import test failed"
    exit 1
fi

# Final instructions
echo ""
echo "✨ Installation Complete!"
echo "========================"
echo ""
echo "To start using CCC:"
echo "1. Activate the environment: source activate_ccc.sh"
echo "2. Check status: ccc status"
echo "3. Run demo: ccc demo"
echo "4. Start orchestrator: ccc start"
echo ""
echo "For live monitoring:"
echo "./scripts/watch_ccc.sh"
echo ""
echo "Happy orchestrating! 🎭"