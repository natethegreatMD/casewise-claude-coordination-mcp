"""
CCC - Claude Code Coordinator
A professional orchestration system for managing multiple Claude Code sessions
"""

__version__ = "0.1.0"
__author__ = "natethegreatMD"

from .orchestrator import SessionOrchestrator
from .session import ClaudeSession

__all__ = [
    "SessionOrchestrator",
    "ClaudeSession", 
    "__version__"
]