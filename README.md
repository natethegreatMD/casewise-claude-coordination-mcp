# CCC - Claude Code Coordinator

> Orchestrate multiple Claude Code sessions to build complex software systems

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/natethegreatMD/casewise-claude-coordination-mcp)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

CCC (Claude Code Coordinator) enables you to orchestrate multiple Claude Code sessions working in parallel on complex development tasks. Instead of overwhelming a single Claude session, CCC intelligently distributes work across specialized sessions that collaborate to build complete systems.

## 🎯 Key Features

- **🤖 Multi-Session Orchestration**: Manage multiple Claude Code sessions working in parallel
- **📋 Smart Task Distribution**: Automatically analyzes dependencies and schedules tasks optimally  
- **👀 Live Monitoring**: Real-time progress tracking with `./scripts/watch_ccc.sh`
- **🔧 Specialized Templates**: Pre-configured templates for frontend, backend, testing, and more
- **🔔 Desktop Notifications**: Get notified of session progress and completions
- **🚀 One-Command Demos**: See CCC in action with `ccc demo`

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/natethegreatMD/casewise-claude-coordination-mcp.git
cd casewise-claude-coordination-mcp

# Run the quick start script
./quickstart.sh
```

This will:
1. Install CCC and dependencies
2. Set up your environment
3. Offer to run the Todo App demo
4. Show you live monitoring in action

## 📺 See It In Action

### Run the Todo App Demo

```bash
# Activate CCC environment
source activate_ccc.sh

# In terminal 1: Start live monitoring
./scripts/watch_ccc.sh

# In terminal 2: Run the demo
ccc demo
```

Watch as CCC orchestrates three Claude sessions to build:
- A FastAPI backend with full CRUD operations
- A React + TypeScript frontend with modern UI
- Comprehensive test suites for both

All in parallel, in about 30-40 minutes!

## 📖 Documentation

- [User Guide](docs/USER_GUIDE.md) - Complete usage instructions
- [Architecture](ARCHITECTURE_DECISIONS.md) - System design and decisions
- [API Reference](docs/API_REFERENCE.md) - Detailed API documentation
- [Contributing](CONTRIBUTING.md) - How to contribute to CCC

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Claude Code CLI installed
- Git

### Install from Source

```bash
# Clone and enter directory
git clone https://github.com/natethegreatMD/casewise-claude-coordination-mcp.git
cd casewise-claude-coordination-mcp

# Run installer
./install.sh

# Activate environment
source activate_ccc.sh
```

## 💻 Basic Usage

### Start the Orchestrator

```bash
# Start CCC orchestrator
ccc start

# Check status
ccc status
```

### Run a Workflow

```bash
# List available workflows
ccc workflow list

# Run a workflow
ccc workflow run todo_app --name my-todo-app
```

### Monitor Sessions

```bash
# In another terminal
./scripts/watch_ccc.sh
```

## 🏗️ Architecture

CCC uses a star topology where the orchestrator manages all sessions:

```
CCC Orchestrator (Master)
├── Frontend Session (React/TypeScript specialist)
├── Backend Session (FastAPI/Python specialist)
├── Testing Session (pytest/Jest specialist)
├── Documentation Session (Technical writing)
└── Integration Session (System integration)
```

Key principles:
- **One Leader**: Orchestrator makes all architectural decisions
- **Autonomous Workers**: Sessions work independently within bounds
- **Smart Scheduling**: Dependency analysis ensures correct execution order
- **Error Recovery**: Automatic retry logic with fallback strategies

## 🎨 Available Workflows

### Todo App
Complete todo application with:
- FastAPI backend with CRUD operations
- React frontend with modern UI
- Comprehensive test coverage

### Auth System  
JWT authentication system with:
- Secure backend implementation
- Login/register UI components
- Integration and security tests

### Blog Platform
Full blogging platform with:
- Post management API
- Rich text editor UI
- Search functionality
- Comment system

## 🔧 Advanced Features

### Custom Workflows

Create your own workflows by defining tasks:

```python
tasks = [
    {
        "name": "api",
        "component": "backend",
        "prompt": "Create a REST API for products",
        "timeout": 1800
    },
    {
        "name": "ui",
        "component": "frontend",
        "prompt": "Create product management UI",
        "dependencies": ["api"],
        "timeout": 1800
    }
]
```

### Session Templates

Specialized templates optimize each session type:
- **Frontend**: React + TypeScript + Vite setup
- **Backend**: FastAPI + Pydantic configuration
- **Testing**: pytest + Jest frameworks
- **Documentation**: Technical writing standards
- **Integration**: Docker + deployment setup

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Created by [@natethegreatMD](https://github.com/natethegreatMD) for accelerating development on the CasewiseMD medical education platform.

---

**Ready to orchestrate?** Run `./quickstart.sh` and watch the magic happen! 🎭