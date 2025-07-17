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