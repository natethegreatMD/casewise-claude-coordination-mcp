# CCC - Claude Code Coordinator

Mike's personal Claude Code orchestration system for CasewiseMD development.

## 🚀 Quick Start

### Watch Live Sessions (ESSENTIAL!)
```bash
# In Ubuntu/WSL terminal:
cd /mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude\ Code\ Coordinator
./scripts/watch_ccc.sh
```

### Activate Environment
```bash
source scripts/activate_ccc.sh
```

### Orchestrator Handoff (When hitting context limits)
```bash
./scripts/orchestrator_handoff.sh
```

## 📁 Directory Structure

```
CCC/
├── CLAUDE.md           # Main project documentation
├── README.md           # This file
├── scripts/            # All executable scripts
│   ├── watch_ccc.sh    # Live monitoring (MUST HAVE!)
│   ├── orchestrator_handoff.sh  # Hand off to new orchestrator
│   └── ...            # Other utility scripts
├── src/               # CCC source code (to be built)
├── docs/              # Documentation
├── demos/             # Proof of concept demos
└── proofs/            # Test results proving CCC works
```

## ✅ Proven Capabilities

- Spawn multiple Claude sessions with `subprocess`
- Full autonomy with `--dangerously-skip-permissions`
- Live monitoring of parallel sessions
- Orchestrator handoff before context limits

## 🎯 Current Mission

Build the complete CCC MCP server to orchestrate multiple Claude sessions for CasewiseMD development.

---
*Last updated: 2025-07-16 @ 22:37 PST*