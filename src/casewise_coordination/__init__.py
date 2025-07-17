"""
CCC - Claude Code Coordinator
A professional MCP-based orchestration system for managing multiple Claude Code sessions
"""

__version__ = "0.1.0"
__author__ = "natethegreatMD"

from .orchestrator import SessionOrchestrator
from .session import ClaudeSession
from .server import CCCServer

__all__ = [
    "SessionOrchestrator",
    "ClaudeSession", 
    "CCCServer",
    "__version__"
]