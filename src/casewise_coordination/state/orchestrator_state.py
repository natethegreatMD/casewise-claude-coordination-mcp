"""
Orchestrator State
Tracks the overall state of the CCC orchestrator
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json


@dataclass
class OrchestratorState:
    """Complete state of the orchestrator"""
    
    orchestrator_id: str
    workspace_root: Path
    started_at: datetime = field(default_factory=datetime.now)
    
    # Session tracking
    active_sessions: List[str] = field(default_factory=list)
    completed_sessions: List[str] = field(default_factory=list)
    failed_sessions: List[str] = field(default_factory=list)
    session_states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Workflow tracking
    current_workflow: Optional[str] = None
    workflow_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metrics
    total_sessions_created: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    error_count: int = 0
    
    # Notifications and logs
    notifications: List[str] = field(default_factory=list)
    important_events: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_notification(self, message: str):
        """Add a notification with timestamp"""
        self.notifications.append(f"{datetime.now().isoformat()} - {message}")
    
    def add_event(self, event_type: str, details: Dict[str, Any]):
        """Add an important event"""
        self.important_events.append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "orchestrator_id": self.orchestrator_id,
            "workspace_root": str(self.workspace_root),
            "started_at": self.started_at.isoformat(),
            "active_sessions": self.active_sessions,
            "completed_sessions": self.completed_sessions,
            "failed_sessions": self.failed_sessions,
            "session_states": self.session_states,
            "current_workflow": self.current_workflow,
            "workflow_history": self.workflow_history,
            "total_sessions_created": self.total_sessions_created,
            "total_tasks_completed": self.total_tasks_completed,
            "total_tasks_failed": self.total_tasks_failed,
            "error_count": self.error_count,
            "notifications": self.notifications[-100:],  # Keep last 100
            "important_events": self.important_events[-50:]  # Keep last 50
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrchestratorState":
        """Create from dictionary"""
        data["started_at"] = datetime.fromisoformat(data["started_at"])
        data["workspace_root"] = Path(data["workspace_root"])
        
        # Filter to valid fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    
    def save(self, filepath: Path):
        """Save state to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: Path) -> "OrchestratorState":
        """Load state from JSON file"""
        with open(filepath) as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def get_summary(self) -> str:
        """Get a summary of orchestrator state"""
        uptime = (datetime.now() - self.started_at).total_seconds()
        hours = uptime / 3600
        
        return f"""Orchestrator State Summary
========================
ID: {self.orchestrator_id}
Uptime: {hours:.1f} hours
Active Sessions: {len(self.active_sessions)}
Completed: {len(self.completed_sessions)}
Failed: {len(self.failed_sessions)}
Current Workflow: {self.current_workflow or 'None'}
Total Errors: {self.error_count}
"""