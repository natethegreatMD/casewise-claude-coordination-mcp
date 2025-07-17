# CCC Architecture Decisions

## Core Principles
1. **One Leader**: Orchestrator (me) is the sole architectural decision maker
2. **Autonomous Workers**: Sessions have `--dangerously-skip-permissions` by default
3. **Clear Boundaries**: Workers get narrow, specific tasks with success criteria
4. **Information Hiding**: Workers don't know about CCC or other sessions

## Session Hierarchy
```
CCC Orchestrator (Master)
├── Worker Sessions (Autonomous but bounded)
│   ├── Cannot spawn more Claude sessions
│   ├── Cannot make architectural decisions  
│   ├── Must follow orchestrator's design
│   └── Report progress via state files
```

## Naming Convention
Format: `ccc-[task]-[component]-[number]`
Examples:
- `ccc-auth-frontend-001`
- `ccc-api-backend-002`
- `ccc-unit-testing-003`

## Error Recovery Strategy
- **Tier 1 (Auto-retry)**: Syntax errors, missing imports, file not found
- **Tier 2 (Retry with guidance)**: Logic errors, wrong approach
- **Tier 3 (Fail gracefully)**: Non-critical features, nice-to-haves
- **Tier 4 (Alert & halt)**: Critical path failures, data corruption risks

## Communication Architecture
- **Star Topology**: All communication flows through orchestrator
- **State Files**: JSON-based progress reporting
- **No Peer-to-Peer**: Workers cannot communicate directly
- **Clear Contracts**: Input spec → Worker → Output spec

## Resource Access
- **Internet**: ✅ Authorized for all sessions
- **File System**: ✅ Full access within designated workspaces
- **Package Installation**: ✅ Can install any needed dependencies
- **External APIs**: ✅ Can fetch docs, examples, resources

## Optimal Approach
1. Start with 2-3 concurrent sessions maximum
2. Each session gets 20-30 minute focused tasks
3. Orchestrator coordinates and merges results
4. Desktop notifications for major events
5. Detailed logging for all operations

---
*Decided: 2025-07-16 @ 23:15 PST*
*These decisions guide all CCC development*