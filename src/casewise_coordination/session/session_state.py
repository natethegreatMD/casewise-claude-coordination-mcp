"""
Session State Management
Tracks state, progress, and health of Claude sessions
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import json


class SessionStatus(Enum):
    """Session lifecycle states"""
    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"
    RETRY = "retry"


@dataclass
class SessionState:
    """Complete state of a Claude session"""
    session_id: str
    task_name: str
    component: str
    status: SessionStatus
    workspace: Path
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    pid: Optional[int] = None
    
    # Task details
    task_description: str = ""
    input_spec: Dict[str, Any] = field(default_factory=dict)
    output_spec: Dict[str, Any] = field(default_factory=dict)
    
    # Progress tracking
    progress_percent: int = 0
    current_activity: str = "Initializing"
    files_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    
    # Error handling
    error_count: int = 0
    last_error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    # Communication
    messages: List[Dict[str, Any]] = field(default_factory=list)
    notifications: List[str] = field(default_factory=list)
    
    # Performance metrics
    tokens_used: int = 0
    execution_time_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "session_id": self.session_id,
            "task_name": self.task_name,
            "component": self.component,
            "status": self.status.value,
            "workspace": str(self.workspace),
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "pid": self.pid,
            "task_description": self.task_description,
            "input_spec": self.input_spec,
            "output_spec": self.output_spec,
            "progress_percent": self.progress_percent,
            "current_activity": self.current_activity,
            "files_created": self.files_created,
            "files_modified": self.files_modified,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "retry_count": self.retry_count,
            "messages": self.messages,
            "notifications": self.notifications,
            "tokens_used": self.tokens_used,
            "execution_time_seconds": self.execution_time_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionState":
        """Create from dictionary"""
        # Convert string dates back to datetime
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("started_at"):
            data["started_at"] = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        
        # Convert status string to enum
        data["status"] = SessionStatus(data["status"])
        
        # Convert workspace to Path
        data["workspace"] = Path(data["workspace"])
        
        # Remove non-field keys
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    
    def save(self, filepath: Optional[Path] = None):
        """Save state to JSON file"""
        if filepath is None:
            filepath = self.workspace / "session_state.json"
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: Path) -> "SessionState":
        """Load state from JSON file"""
        with open(filepath) as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def add_message(self, message_type: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to session history"""
        self.messages.append({
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "content": content,
            "metadata": metadata or {}
        })
    
    def update_progress(self, percent: int, activity: str):
        """Update progress indicators"""
        self.progress_percent = min(100, max(0, percent))
        self.current_activity = activity
        self.add_message("progress", f"{activity} ({percent}%)")
    
    def mark_started(self):
        """Mark session as started"""
        self.status = SessionStatus.RUNNING
        self.started_at = datetime.now()
        self.add_message("lifecycle", "Session started")
    
    def mark_completed(self, success: bool = True):
        """Mark session as completed"""
        self.status = SessionStatus.COMPLETED if success else SessionStatus.FAILED
        self.completed_at = datetime.now()
        
        if self.started_at:
            self.execution_time_seconds = (self.completed_at - self.started_at).total_seconds()
        
        self.add_message("lifecycle", f"Session {'completed' if success else 'failed'}")
    
    def should_retry(self) -> bool:
        """Check if session should be retried"""
        return (
            self.status == SessionStatus.FAILED and 
            self.retry_count < self.max_retries and
            self.error_count > 0
        )