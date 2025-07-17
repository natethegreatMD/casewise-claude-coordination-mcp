# CCC Git Commit Strategy

## Versioning (Semantic Versioning)
- **MAJOR.MINOR.PATCH** (e.g., 0.1.0)
- **MAJOR**: Breaking changes to CCC architecture
- **MINOR**: New features (new agents, capabilities)
- **PATCH**: Bug fixes, documentation updates

## Commit Message Format
```
type(scope): Brief description

Detailed explanation of what changed and why.
- Bullet points for multiple changes
- Reference issues if applicable
- Include performance impacts
- Note any breaking changes

Affects: [components affected]
Testing: [what was tested]
```

## Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Maintenance tasks

## Scopes
- **orchestrator**: Session orchestration logic
- **cli**: Claude CLI integration
- **monitor**: Live monitoring system
- **templates**: Session templates
- **mcp**: MCP server components
- **scripts**: Utility scripts

## When to Commit & Push
1. **After each major component** is working
2. **Before starting new feature** (clean checkpoint)
3. **After successful tests** (proof it works)
4. **Before handoff** (always push before context limit)
5. **End of coding session** (even if WIP)

## Example Commits

### Feature
```
feat(orchestrator): Add parallel session execution with subprocess

Implemented SessionOrchestrator class that can spawn and manage multiple
Claude Code sessions in parallel using subprocess.Popen.
- Each session runs in isolated workspace
- Captures stdout/stderr in real-time
- Handles session lifecycle (start/stop/restart)
- Supports up to 10 concurrent sessions

Affects: src/orchestrator/session_manager.py
Testing: Spawned 3 parallel sessions successfully
```

### Fix
```
fix(monitor): Correct file watching path resolution

Fixed issue where live monitor couldn't find session logs in nested
directories. Now uses recursive glob pattern.
- Changed from single-level glob to rglob
- Added proper path normalization
- Handles Windows/WSL path differences

Affects: scripts/ccc_live_watcher.py
Testing: Monitored 5-level deep session directories
```

## Tag Strategy
- Tag releases: `v0.1.0`, `v0.2.0`, etc.
- Tag milestones: `milestone-orchestrator-complete`
- Tag before major refactors: `before-mcp-integration`