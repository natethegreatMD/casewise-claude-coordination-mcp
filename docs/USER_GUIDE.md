# CCC User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Running Workflows](#running-workflows)
4. [Managing Sessions](#managing-sessions)
5. [Live Monitoring](#live-monitoring)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/natethegreatMD/casewise-claude-coordination-mcp.git
cd casewise-claude-coordination-mcp

# Run the installer
./install.sh

# Activate the environment
source activate_ccc.sh
```

### Quick Start

```bash
# Run the quickstart script
./quickstart.sh
```

This will guide you through:
- Running the Todo App demo
- Starting the orchestrator
- Exploring documentation

## Basic Usage

### Starting CCC

```bash
# Start the orchestrator
ccc start

# Check status
ccc status

# Stop the orchestrator
ccc stop
```

### Configuration

```bash
# View current configuration
ccc config

# Edit configuration
vim ~/ccc_workspace/ccc_config.json
```

Key configuration options:
- `max_parallel_sessions`: Maximum concurrent Claude sessions (default: 3)
- `dangerous_permissions`: Allow autonomous file operations (default: true)
- `default_timeout_minutes`: Session timeout (default: 30)

## Running Workflows

### List Available Workflows

```bash
ccc workflow list
```

Available workflows:
- `todo_app`: Complete Todo application with frontend/backend/tests
- `auth_system`: JWT authentication system
- `blog_platform`: Blog platform with editor and reader

### Run a Workflow

```bash
# Run Todo App workflow
ccc workflow run todo_app --name my-todo-app

# Run with sequential execution
ccc workflow run auth_system --name my-auth --sequential
```

### Monitor Progress

In another terminal:
```bash
./scripts/watch_ccc.sh
```

This shows real-time:
- Session creation
- File operations
- Progress updates
- Errors and completions

## Managing Sessions

### List Sessions

```bash
# List all sessions
ccc session list

# Filter by status
ccc session list --status running
ccc session list --status completed
```

### View Session Details

```bash
# Get session logs
ccc session logs ccc-backend-001

# Tail logs
ccc session logs ccc-frontend-002 --tail 100
```

### Session Lifecycle

1. **PENDING**: Session created but not started
2. **STARTING**: Session initializing
3. **RUNNING**: Actively working on task
4. **COMPLETED**: Successfully finished
5. **FAILED**: Encountered errors
6. **TERMINATED**: Manually stopped

## Live Monitoring

### Terminal Monitoring

```bash
# Start the live watcher
./scripts/watch_ccc.sh
```

Features:
- Real-time session activity
- File creation alerts
- Progress updates
- Error notifications

### Desktop Notifications

CCC sends desktop notifications for:
- Session starts
- Session completions
- Workflow completions
- Critical errors

Supported on:
- Linux (notify-send)
- macOS (osascript)
- Windows (PowerShell)

## Advanced Features

### Custom Workflows

Create custom workflow by combining tasks:

```python
from casewise_coordination import SessionOrchestrator

orchestrator = SessionOrchestrator(workspace_root="./my_workspace")

# Define custom tasks
tasks = [
    {
        "name": "api",
        "component": "backend",
        "prompt": "Create a REST API for user management",
        "timeout": 1800
    },
    {
        "name": "ui",
        "component": "frontend", 
        "prompt": "Create a user management UI",
        "timeout": 1800,
        "input": {"api_url": "http://localhost:8000"}
    }
]

# Execute workflow
result = orchestrator.execute_workflow(
    workflow_name="User Management",
    tasks=tasks,
    parallel=True
)
```

### Session Templates

CCC includes specialized templates:

- **Frontend**: React + TypeScript with Vite
- **Backend**: FastAPI + Pydantic
- **Testing**: pytest + Jest
- **Documentation**: Technical writing
- **Integration**: System integration

Templates provide:
- Optimized prompts
- Environment setup
- Success validation
- Best practices

### Inter-Session Communication

Sessions communicate through:
- Shared state files
- Dependency tracking
- Result consolidation

Example dependency chain:
```
Backend API → Frontend UI → Integration Tests
     ↓              ↓              ↓
   Models      Components      Test Suite
```

## Troubleshooting

### Common Issues

**Sessions not starting**
- Check Claude CLI is installed: `claude --version`
- Verify permissions: `./scripts/verify_permissions.sh`
- Check logs: `tail -f ~/ccc_workspace/orchestrator.log`

**Files not created**
- Ensure `dangerous_permissions` is enabled
- Check session has write access to workspace
- Review session logs for errors

**Notifications not working**
- Linux: Install `notify-send`
- macOS: Enable terminal notifications
- Windows: Run as administrator

### Debug Mode

```bash
# Start orchestrator in debug mode
CCC_LOG_LEVEL=DEBUG ccc start

# View detailed logs
tail -f ~/ccc_workspace/orchestrator.log
```

### Getting Help

1. Check session logs for specific errors
2. Review orchestrator state: `ccc status`
3. Open an issue on GitHub with:
   - CCC version
   - Error messages
   - Session logs
   - Steps to reproduce

## Best Practices

1. **Start Small**: Test with simple workflows first
2. **Monitor Progress**: Always run watcher in parallel
3. **Check Dependencies**: Ensure tasks have clear dependencies
4. **Review Output**: Validate session results before integration
5. **Clean Workspaces**: Remove old session data periodically

## Examples

### Building a Blog Platform

```bash
# Run the blog platform workflow
ccc workflow run blog_platform --name my-blog

# Monitor progress
./scripts/watch_ccc.sh

# After completion, check results
cd ~/ccc_workspace/my-blog/final_app
ls -la
```

### Creating Documentation

```bash
# Create a documentation session
ccc session create \
  --name docs \
  --component documentation \
  --prompt "Document the Todo API with examples"
```

---

For more information, see:
- [Architecture Documentation](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Contributing Guide](../CONTRIBUTING.md)