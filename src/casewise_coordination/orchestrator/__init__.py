"""
Session Orchestration
Coordinates multiple Claude sessions to work together on complex tasks
"""

from .session_orchestrator import SessionOrchestrator
from .task_distribution import TaskDistributor

__all__ = ["SessionOrchestrator", "TaskDistributor"]