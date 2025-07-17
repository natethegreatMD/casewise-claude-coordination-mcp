# CasewiseMD Claude Code Coordination MCP - Setup Instructions

## For New Claude Code Session

Create this exact file structure and content:

### 1. Create Directory Structure

```bash
mkdir -p /mnt/c/Users/Mike/Documents/casewise-claude-coordination-mcp
cd /mnt/c/Users/Mike/Documents/casewise-claude-coordination-mcp

# Create initial structure
mkdir -p src/casewise_coordination/{orchestrator,templates,tools,sessions}
mkdir -p examples docs tests
touch README.md pyproject.toml
touch src/casewise_coordination/__init__.py
```

### 2. Initialize Git Repository

```bash
git init
git remote add origin https://github.com/natethegreatMD/casewise-claude-coordination-mcp.git
```

### 3. Create CLAUDE.md (COPY THIS EXACTLY)

---START CLAUDE.md---
# CasewiseMD Claude Code Coordination MCP (CCC) - AI Assistant Guide

## Project Overview
- **What**: Custom Claude Code coordination MCP server built specifically for CasewiseMD development
- **Abbreviation**: CCC (Claude Code Coordinator) - shorthand for this coordination system
- **Goal**: Enable multiple Claude Code sessions to work together on CasewiseMD medical platform
- **Architecture**: MCP server + orchestrator pattern + Claude Code CLI integration
- **Owner**: Mike (natethegreatMD) - personal development tool for CasewiseMD project

## Working Context
- **Location**: Local development only - this is Mike's personal development tool
- **Integration**: Uses Claude Code CLI, not web Claude
- **Target**: Mike's CasewiseMD development workflow specifically
- **Medical Context**: Built exclusively for CasewiseMD medical education platform
- **Development Approach**: **NO BOUNDARIES** - Full force development until CCC is fully working
- **Authorization**: Complete autonomy to implement, test, and deploy entire CCC system

## Core Concept

### Multi-Claude Code Orchestration for CasewiseMD (CCC Architecture)
Instead of a single Claude Code session trying to handle massive CasewiseMD features, the CCC coordinates multiple specialized sessions:

```
CCC Orchestrator Claude Code Session (Mike's main session)
├── CasewiseMD Frontend Specialist (React/TypeScript/OHIF viewer)
├── CasewiseMD Backend Specialist (FastAPI/MCP agents/AI grading)  
├── CasewiseMD Testing Specialist (pytest/integration/medical accuracy)
├── CasewiseMD Documentation Specialist (CLAUDE.md/technical docs)
└── CasewiseMD Integration Specialist (VPS deployment/Docker/nginx)
```

### Full Force Development Approach 
- **NO BOUNDARIES**: Complete autonomy to build entire CCC system from scratch
- **Full Implementation**: Build all components, test thoroughly, make it production-ready
- **No Approval Gates**: Implement, test, and iterate rapidly without stopping for permission
- **End Goal**: Fully functional CCC system ready for immediate CasewiseMD coordination
- Each specialized session gets **one large CasewiseMD feature or component**
- Sessions work independently but coordinate through CCC orchestrator
- Complete system integration with proper error handling and recovery

## Technical Architecture

### CCC MCP Server Components
1. **Session Orchestrator**: Manages multiple Claude Code instances with full lifecycle control
2. **Task Templates**: Predefined task patterns for different CasewiseMD specializations
3. **Progress Tracking**: Real-time session states and completion monitoring
4. **Communication Layer**: Inter-session message passing and coordination
5. **Human Interface**: Streamlined coordination with minimal interruption
6. **Auto-Recovery**: Automatic session restart and state recovery mechanisms
7. **Performance Monitoring**: Resource usage and session health tracking

### Claude Code Integration (CCC CLI Interface)
- Uses `claude-cli` for programmatic session management and control
- Each session has isolated terminal/workspace with specialized context
- Shared context through CCC MCP server state and coordination
- Git-based coordination for code changes and branch management
- Automated session spawning, monitoring, and lifecycle management
- Inter-session communication through CCC message passing system

## Directory Structure
```
casewise-claude-coordination-mcp/
├── CLAUDE.md                  # This file (project guide)
├── README.md                  # Basic documentation
├── pyproject.toml             # Python project config
├── src/casewise_coordination/
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── session_manager.py # Claude Code session management
│   │   ├── casewise_coordinator.py# CasewiseMD task distribution
│   │   └── progress_tracker.py# Session progress monitoring
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── casewise_frontend.py    # CasewiseMD React/OHIF specialist
│   │   ├── casewise_backend.py     # CasewiseMD FastAPI/MCP specialist
│   │   ├── casewise_testing.py     # CasewiseMD testing specialist
│   │   ├── casewise_docs.py        # CasewiseMD documentation specialist
│   │   └── casewise_integration.py # CasewiseMD VPS/Docker specialist
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── session_tools.py   # MCP tools for session control
│   │   ├── casewise_git_tools.py   # CasewiseMD Git coordination
│   │   └── progress_tools.py  # Progress reporting tools
│   └── sessions/
│       ├── __init__.py
│       ├── claude_interface.py# Claude Code CLI integration
│       └── session_state.py  # Session state management
├── examples/
│   ├── casewise_feature_workflow.py   # New feature development
│   ├── casewise_bug_fix_workflow.py   # Bug fix coordination
│   └── casewise_refactor_workflow.py  # Architecture refactoring
├── docs/
│   ├── casewise_architecture.md    # CasewiseMD-specific architecture
│   ├── casewise_workflows.md       # CasewiseMD development workflows
│   └── claude_code_integration.md  # Claude Code CLI integration
└── tests/
    ├── test_casewise_orchestrator.py
    ├── test_casewise_sessions.py
    └── test_casewise_integration.py
```

## Implementation Strategy - FULL FORCE APPROACH

### PHASE 1: Core CCC Infrastructure (IMMEDIATE PRIORITY)
- **Status**: **FULL IMPLEMENTATION MODE** - No boundaries, complete autonomy
- **Goal**: Complete working CCC MCP server with all core functionality
- **Approach**: Build, test, iterate rapidly until fully functional
- **Tasks**:
  - [ ] Set up complete MCP server framework with all dependencies
  - [ ] Implement full session creation/management/lifecycle control
  - [ ] Create robust Claude Code CLI integration layer with error handling
  - [ ] Build complete orchestrator patterns with coordination logic
  - [ ] Implement inter-session communication and state management
  - [ ] Add monitoring, logging, and debugging capabilities
  - [ ] Create CLI tools for CCC management and control

### PHASE 2: Specialized Session Templates (IMMEDIATE IMPLEMENTATION)
- **Status**: **PARALLEL DEVELOPMENT** - Build all templates simultaneously
- **Goal**: Complete set of working CasewiseMD specialist session templates
- **Tasks**:
  - [ ] CasewiseMD Frontend Specialist (React/TypeScript/OHIF focus)
  - [ ] CasewiseMD Backend Specialist (FastAPI/Python/MCP agents focus)
  - [ ] CasewiseMD Testing Specialist (pytest/integration/medical accuracy focus)
  - [ ] CasewiseMD Documentation Specialist (CLAUDE.md/technical docs focus)
  - [ ] CasewiseMD Integration Specialist (VPS/Docker/nginx deployment focus)

### PHASE 3: CCC-CasewiseMD Integration (IMMEDIATE TESTING)
- **Status**: **FULL INTEGRATION MODE** - Complete system testing
- **Goal**: End-to-end working coordination for live CasewiseMD development
- **Tasks**:
  - [ ] Medical platform specific workflows and coordination patterns
  - [ ] Multi-environment coordination (prod/dev) with existing infrastructure
  - [ ] Integration with existing CasewiseMD tooling and deployment scripts
  - [ ] Live testing with actual CasewiseMD features and bug fixes

### PHASE 4: Production Deployment (IMMEDIATE OPERATIONALIZATION)
- **Status**: **PRODUCTION READY TARGET** - Deploy and operationalize
- **Goal**: CCC running as Mike's primary CasewiseMD development tool
- **Tasks**:
  - [ ] Parallel session execution with resource management
  - [ ] Conflict resolution and automatic error recovery
  - [ ] Advanced progress tracking and session health monitoring
  - [ ] Performance optimization and resource management
  - [ ] Documentation and operational procedures

## Key Design Principles

### 1. Human-in-the-Loop
- Human provides high-level direction at task boundaries
- Sessions complete full tasks before handoff
- Clear checkpoints for approval/direction changes
- No autonomous cross-session decisions

### 2. Large Task Focus
- Each session gets substantial, well-defined work
- Avoid micro-management of individual sessions
- Sessions work independently within their scope
- Progress reported at meaningful milestones

### 3. Git-Based Coordination
- All work coordinated through Git branches
- Sessions work on isolated branches
- Orchestrator manages merges and conflicts
- Human approves all integration points

### 4. Specialization Over Generalization
- Sessions have clear roles and expertise areas
- Templates provide specialized context and tools
- Better results through focused expertise
- Easier to debug and improve specific areas

## Integration with CasewiseMD

### Current CasewiseMD Context
- **Architecture**: FastAPI backend, React frontend, OHIF viewer, Orthanc DICOM
- **Environments**: Production + Development on VPS (143.244.154.89)
- **Recent Work**: MCP backend refactor completed and tested
- **Current Branch**: refactor/mcp-backend (ready for production merge)
- **Documentation**: Comprehensive technical docs in MCP_REFACTOR_SUMMARY.md

### Coordination Scenarios
1. **New Feature Development**: Frontend + Backend + Testing sessions
2. **Bug Fixes**: Diagnostic + Implementation + Testing sessions  
3. **Architecture Refactoring**: Planning + Implementation + Migration sessions
4. **Documentation Updates**: Analysis + Writing + Review sessions

## Development Workflow

### Starting a Coordinated Project
1. **Human**: Defines high-level project goals
2. **Orchestrator**: Breaks into specialized tasks
3. **Human**: Reviews and approves task breakdown
4. **Orchestrator**: Spins up specialized Claude Code sessions
5. **Sessions**: Work independently on assigned tasks
6. **Orchestrator**: Coordinates progress and handoffs
7. **Human**: Approves completions and provides direction

### Example: Adding Authentication to CasewiseMD
```
Mike's Task Breakdown for Authentication Feature:
├── CasewiseMD Backend Specialist: JWT auth + MCP agent integration
├── CasewiseMD Frontend Specialist: Login/logout UI + React state mgmt
├── CasewiseMD Testing Specialist: Auth tests + medical workflow validation
├── CasewiseMD Docs Specialist: Update CLAUDE.md + technical docs
└── CasewiseMD Integration Specialist: VPS deployment + nginx config

Mike's Workflow:
1. Backend specialist implements JWT with existing MCP architecture
2. Frontend specialist creates auth UI integrated with OHIF viewer
3. Testing specialist validates auth doesn't break medical workflows
4. Docs specialist updates all CasewiseMD documentation
5. Integration specialist deploys to both dev and prod environments
6. Mike reviews and approves each phase
```

## Tools and Technologies

### Core Stack
- **MCP Server**: Python-based Model Context Protocol server
- **Claude Code**: AI assistant with CLI and tool access
- **Git**: Version control and coordination
- **Python**: Primary implementation language

### Dependencies
- `mcp` - Model Context Protocol framework
- `asyncio` - Async session management
- `subprocess` - Claude Code CLI integration
- `gitpython` - Git repository management
- `pydantic` - Data validation and serialization

## Success Metrics

### Technical Metrics
- Session coordination latency < 5 seconds
- Successful task handoffs > 95%
- Git merge conflicts < 10% of handoffs
- Session crash recovery < 30 seconds

### Development Metrics  
- Reduced single-session context overflow
- Faster completion of multi-component features
- Improved code quality through specialization
- Better documentation coverage

## Future Enhancements

### Advanced Coordination
- **Parallel Execution**: Multiple sessions working simultaneously
- **Dependency Management**: Smart task ordering and blocking
- **Resource Management**: Session capacity and load balancing
- **Conflict Resolution**: Automated merge conflict handling

### Integration Expansions
- **VS Code Extension**: IDE integration for coordination
- **CI/CD Integration**: Automated testing and deployment
- **Project Templates**: Pre-built coordination patterns
- **Monitoring Dashboard**: Real-time session and progress tracking

## Current Status
- **Repository**: To be created at github.com/natethegreatMD/casewise-claude-coordination-mcp
- **Development Stage**: Core concept PROVEN - can spawn and control Claude sessions
- **Proven Capabilities**:
  - ✅ Spawn Claude sessions with subprocess
  - ✅ Make them autonomous with --dangerously-skip-permissions
  - ✅ Capture outputs and monitor progress
  - ✅ Live monitoring system working (./watch_ccc.sh)
  - ✅ Parallel session execution demonstrated
- **Next Steps**: Build complete MCP server and orchestration system
- **Timeline**: Ready for full implementation

## Critical Context Limit Considerations

### The 100k Token Wall
- **Limitation**: Orchestrator sessions hit ~100k token context limit
- **Cannot**: Spawn new orchestrator with --dangerously-skip-permissions at limit
- **Solution**: CCC architecture designed to handle this!

### Context Management Strategy
1. **Orchestrator** (main session): Manages high-level coordination
2. **Worker Sessions**: Don't need full context, just specific tasks
3. **State Persistence**: Save orchestrator state before hitting limits
4. **Session Handoff**: New orchestrator reads state and continues

### 🚨 CRITICAL: Handoff at 75k Tokens
**When to handoff**: At ~75k tokens (leaving 25k for detailed handoff)
**How to check**: Watch for context warnings or degraded performance

#### Handoff Process (Mike initiates)
1. **Mike notices ~75k tokens approaching**
2. **Mike says**: "Prepare handoff" or "Context getting full"
3. **Current orchestrator**:
   - Updates CLAUDE.md with EVERYTHING important
   - Documents all active work, decisions, discoveries
   - Lists exact next steps with full context
   - Updates todo list with detailed status
   - Creates any needed state files
4. **Mike runs**: `./scripts/orchestrator_handoff.sh`
5. **New orchestrator**: Reads CLAUDE.md and continues seamlessly

#### What to Document in Handoff (Use all 25k tokens!)
- **Completed work**: Every file created, every test run, all results
- **Current state**: What's working, what's not, what's in progress
- **Key discoveries**: Important findings, gotchas, solutions found
- **Active branches**: Git status, uncommitted changes, branch purposes
- **Next steps**: Detailed plan with specific files, functions, approaches
- **Session states**: Any active worker sessions and their tasks
- **Environment status**: Dependencies installed, config changes
- **Critical context**: Design decisions, architecture choices, reasons
- **Problems encountered**: What didn't work and why
- **Code snippets**: Important code that new orchestrator needs

### Self-Monitoring Protocol
Every 30 minutes, orchestrator should:
1. **Silently update** CONTEXT_STATUS.md with current estimate
2. **Self-test**: Try to recall early context (first files created, initial decisions)
3. **Update checkpoints**: Mark completed checks, add next reminder
4. **At 75k**: Start updating HANDOFF.md with extreme detail

The orchestrator won't mention these checks to Mike unless approaching 75k.

### Live Monitoring System
- **Location**: `/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator`
- **Run Command**: `./watch_ccc.sh` (in Ubuntu/WSL terminal)
- **What it shows**: Real-time activity from all CCC sessions
- **MUST HAVE**: Essential for watching parallel Claude sessions work

## For New Claude Code Sessions

When starting work on this project:
1. Read this entire CLAUDE.md for context
2. Check current git status and recent commits
3. Review existing code in src/claude_coordination/
4. Check examples/ for usage patterns
5. Read docs/ for technical architecture details

Key context to remember:
- This is **Mike's personal development tool** for CasewiseMD, not part of the medical platform
- Designed for **Claude Code specifically**, not web Claude
- Uses **large task focus** approach for CasewiseMD features, not micro-management
- **Mike-in-the-loop** at all major decision points
- Built specifically for **CasewiseMD development workflows** with medical accuracy focus
- **Git-based coordination** for CasewiseMD production/development branches

---
*Created: 2025-07-17 - Initial architecture and design*
*Next: Implement core MCP server and session management*
---END CLAUDE.md---

### 4. Create Initial README.md

```bash
# CasewiseMD Claude Code Coordination MCP

Mike's personal Claude Code coordination MCP server for CasewiseMD medical education platform development.

## Overview

Custom MCP server enabling Mike to coordinate multiple Claude Code sessions working together on CasewiseMD features. Instead of overwhelming a single session with complex medical platform features, work is distributed across specialized CasewiseMD-focused sessions that communicate through the MCP protocol.

## Quick Start

```bash
pip install casewise-coordination
casewise-coordination --help
```

## Example Usage

```python
from casewise_coordination import CasewiseOrchestrator

# Start coordinated CasewiseMD development
orchestrator = CasewiseOrchestrator()
await orchestrator.start_casewise_feature("Authentication System")
```

## Documentation

- [CasewiseMD Architecture](docs/casewise_architecture.md)
- [CasewiseMD Workflows](docs/casewise_workflows.md)  
- [Claude Code Integration](docs/claude_code_integration.md)

## License

MIT - Personal tool for CasewiseMD development
```

### 5. Create pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "casewise-coordination"
version = "0.1.0"
description = "Mike's CasewiseMD Claude Code coordination tool"
authors = [{name = "Mike (natethegreatMD)"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "mcp>=0.1.0",
    "asyncio",
    "pydantic>=2.0",
    "gitpython>=3.1",
]

[project.urls]
Homepage = "https://github.com/natethegreatMD/casewise-claude-coordination-mcp"
Repository = "https://github.com/natethegreatMD/casewise-claude-coordination-mcp"

[project.scripts]
casewise-coordination = "casewise_coordination.cli:main"
```

## Next Steps for New Claude Code Session

1. Create the GitHub repository
2. Set up the directory structure exactly as shown
3. Copy the CLAUDE.md content exactly
4. Begin implementing the core MCP server in `src/claude_coordination/server.py`
5. Focus on Claude Code CLI integration first

The new session will have everything it needs to start building the coordination system!