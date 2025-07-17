"""
Session Orchestrator
The master controller that manages multiple Claude sessions
"""

import asyncio
import logging
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from concurrent.futures import ThreadPoolExecutor
import threading

from ..session import ClaudeSession, SessionState, SessionStatus
from ..state import OrchestratorState
from .task_distribution import TaskDistributor


logger = logging.getLogger(__name__)


class SessionOrchestrator:
    """
    Master orchestrator for CCC
    Manages multiple Claude sessions working on coordinated tasks
    """
    
    def __init__(
        self,
        workspace_root: Path,
        max_parallel_sessions: int = 3,
        dangerous_permissions: bool = True,
        notification_callback: Optional[Callable[[str, str], None]] = None
    ):
        """
        Initialize the orchestrator
        
        Args:
            workspace_root: Root directory for all session workspaces
            max_parallel_sessions: Maximum concurrent sessions
            dangerous_permissions: Use --dangerously-skip-permissions
            notification_callback: Callback for notifications (level, message)
        """
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        
        # Session management
        self.sessions: Dict[str, ClaudeSession] = {}
        self.max_parallel_sessions = max_parallel_sessions
        self.dangerous_permissions = dangerous_permissions
        self.session_counter = 0
        
        # State tracking
        self.state = OrchestratorState(
            orchestrator_id=f"ccc-orchestrator-{int(time.time())}",
            workspace_root=self.workspace_root
        )
        
        # Task distribution
        self.task_distributor = TaskDistributor()
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=max_parallel_sessions + 2)
        self.monitor_thread: Optional[threading.Thread] = None
        self.running = False
        
        # Callbacks
        self.notification_callback = notification_callback
        
        # Logging
        self._setup_logging()
        
        logger.info(f"Orchestrator initialized with workspace: {workspace_root}")
        self._notify("info", "CCC Orchestrator initialized and ready")
    
    def _setup_logging(self):
        """Setup orchestrator logging"""
        log_file = self.workspace_root / "orchestrator.log"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Configure root logger for orchestrator
        orc_logger = logging.getLogger("casewise_coordination.orchestrator")
        orc_logger.addHandler(handler)
        orc_logger.setLevel(logging.DEBUG)
    
    def _notify(self, level: str, message: str):
        """Send notification"""
        logger.log(
            getattr(logging, level.upper(), logging.INFO),
            message
        )
        
        if self.notification_callback:
            self.notification_callback(level, message)
        
        # Add to state
        self.state.add_notification(f"[{level.upper()}] {message}")
    
    def create_session(
        self,
        task_name: str,
        component: str,
        task_prompt: str,
        input_data: Optional[Dict[str, Any]] = None,
        timeout_seconds: int = 1800,
        env_vars: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Create a new Claude session
        
        Args:
            task_name: Name of the task (e.g., "auth")
            component: Component type (e.g., "frontend", "backend")
            task_prompt: The instructions for Claude
            input_data: Optional input specifications
            timeout_seconds: Session timeout
            env_vars: Additional environment variables
            
        Returns:
            str: Session ID
        """
        # Generate session ID
        self.session_counter += 1
        session_id = f"ccc-{task_name}-{component}-{self.session_counter:03d}"
        
        # Check capacity
        active_count = len([s for s in self.sessions.values() 
                          if s.state.status in [SessionStatus.RUNNING, SessionStatus.STARTING]])
        
        if active_count >= self.max_parallel_sessions:
            self._notify("warning", f"At capacity ({active_count} sessions), queuing {session_id}")
            # Could implement queuing here
        
        # Create session
        session = ClaudeSession(
            session_id=session_id,
            task_name=task_name,
            component=component,
            workspace_root=self.workspace_root / "sessions",
            dangerous_permissions=self.dangerous_permissions,
            timeout_seconds=timeout_seconds,
            env_vars=env_vars
        )
        
        # Set callbacks
        session.set_state_callback(self._on_session_state_change)
        session.set_output_callback(lambda line: self._on_session_output(session_id, line))
        
        # Store session
        self.sessions[session_id] = session
        self.state.active_sessions.append(session_id)
        
        # Start session
        success = session.start(task_prompt, input_data)
        
        if success:
            self._notify("success", f"Started session {session_id} for {task_name}/{component}")
        else:
            self._notify("error", f"Failed to start session {session_id}")
        
        return session_id
    
    def _on_session_state_change(self, state: SessionState):
        """Handle session state changes"""
        self._notify("info", f"Session {state.session_id} changed to {state.status.value}")
        
        # Update orchestrator state
        self.state.session_states[state.session_id] = state.to_dict()
        
        # Handle completion
        if state.status in [SessionStatus.COMPLETED, SessionStatus.FAILED]:
            self._handle_session_completion(state)
        
        # Handle retries
        elif state.status == SessionStatus.FAILED and state.should_retry():
            self._notify("warning", f"Session {state.session_id} failed, retrying...")
            self._retry_session(state.session_id)
    
    def _on_session_output(self, session_id: str, line: str):
        """Handle session output"""
        # Could parse for specific patterns, progress updates, etc.
        if "error" in line.lower():
            self.state.error_count += 1
        
        # Look for file creation patterns
        if "created" in line.lower() or "wrote" in line.lower():
            self._notify("info", f"{session_id}: {line}")
    
    def _handle_session_completion(self, state: SessionState):
        """Handle completed session"""
        if state.status == SessionStatus.COMPLETED:
            self.state.completed_sessions.append(state.session_id)
            self._notify("success", f"Session {state.session_id} completed successfully")
            
            # Check if all sessions for a task are complete
            self._check_task_completion(state.task_name)
            
        else:
            self.state.failed_sessions.append(state.session_id)
            self._notify("error", f"Session {state.session_id} failed: {state.last_error}")
    
    def _check_task_completion(self, task_name: str):
        """Check if all sessions for a task are complete"""
        task_sessions = [s for s in self.sessions.values() if s.state.task_name == task_name]
        
        if all(s.state.status == SessionStatus.COMPLETED for s in task_sessions):
            self._notify("success", f"All sessions for task '{task_name}' completed!")
            # Could trigger next phase or consolidation here
    
    def _retry_session(self, session_id: str):
        """Retry a failed session"""
        session = self.sessions.get(session_id)
        if not session:
            return
        
        # Increment retry count
        session.state.retry_count += 1
        
        # Restart with same parameters
        task_prompt = session.state.task_description
        input_data = session.state.input_spec
        
        # Add retry context
        retry_prompt = f"""[RETRY ATTEMPT {session.state.retry_count}]
Previous error: {session.state.last_error}

Original task:
{task_prompt}"""
        
        session.start(retry_prompt, input_data)
    
    def execute_workflow(
        self,
        workflow_name: str,
        tasks: List[Dict[str, Any]],
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a complete workflow with multiple tasks
        
        Args:
            workflow_name: Name of the workflow
            tasks: List of task definitions
            parallel: Execute tasks in parallel or sequentially
            
        Returns:
            Dict: Workflow execution results
        """
        self._notify("info", f"Starting workflow: {workflow_name}")
        self.state.current_workflow = workflow_name
        workflow_start = time.time()
        
        results = {
            "workflow": workflow_name,
            "started_at": datetime.now().isoformat(),
            "tasks": {},
            "success": True
        }
        
        if parallel:
            # Start all tasks in parallel
            futures = []
            for task in tasks:
                future = self.executor.submit(
                    self._execute_task,
                    task
                )
                futures.append((task["name"], future))
            
            # Collect results
            for task_name, future in futures:
                try:
                    result = future.result(timeout=3600)  # 1 hour timeout
                    results["tasks"][task_name] = result
                except Exception as e:
                    results["tasks"][task_name] = {"error": str(e)}
                    results["success"] = False
                    
        else:
            # Execute sequentially
            for task in tasks:
                result = self._execute_task(task)
                results["tasks"][task["name"]] = result
                
                if not result.get("success"):
                    results["success"] = False
                    break  # Stop on first failure
        
        results["completed_at"] = datetime.now().isoformat()
        results["duration_seconds"] = time.time() - workflow_start
        
        self._notify(
            "success" if results["success"] else "error",
            f"Workflow '{workflow_name}' {'completed' if results['success'] else 'failed'}"
        )
        
        return results
    
    def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task"""
        task_name = task["name"]
        component = task.get("component", "general")
        prompt = task["prompt"]
        input_data = task.get("input", {})
        timeout = task.get("timeout", 1800)
        
        # Create and start session
        session_id = self.create_session(
            task_name=task_name,
            component=component,
            task_prompt=prompt,
            input_data=input_data,
            timeout_seconds=timeout
        )
        
        session = self.sessions[session_id]
        
        # Wait for completion
        success = session.wait_for_completion()
        
        # Collect results
        result = {
            "session_id": session_id,
            "success": success,
            "files_created": session.state.files_created,
            "execution_time": session.state.execution_time_seconds,
            "workspace": str(session.workspace)
        }
        
        if not success:
            result["error"] = session.state.last_error
            
        return result
    
    def consolidate_results(
        self,
        session_ids: List[str],
        output_dir: Path
    ) -> Dict[str, Any]:
        """
        Consolidate results from multiple sessions
        
        Args:
            session_ids: List of session IDs to consolidate
            output_dir: Directory to copy results to
            
        Returns:
            Dict: Consolidation summary
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        consolidation = {
            "session_ids": session_ids,
            "output_dir": str(output_dir),
            "files_collected": [],
            "errors": []
        }
        
        for session_id in session_ids:
            session = self.sessions.get(session_id)
            if not session:
                consolidation["errors"].append(f"Session {session_id} not found")
                continue
            
            # Copy workspace files
            session_output = output_dir / session_id
            session_output.mkdir(exist_ok=True)
            
            for file in session.get_workspace_files():
                relative = file.relative_to(session.workspace)
                dest = session_output / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                import shutil
                shutil.copy2(file, dest)
                consolidation["files_collected"].append(str(dest))
        
        self._notify("info", f"Consolidated {len(consolidation['files_collected'])} files")
        return consolidation
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "orchestrator_id": self.state.orchestrator_id,
            "uptime_seconds": (datetime.now() - self.state.started_at).total_seconds(),
            "total_sessions": len(self.sessions),
            "active_sessions": len([s for s in self.sessions.values() 
                                  if s.state.status == SessionStatus.RUNNING]),
            "completed_sessions": len(self.state.completed_sessions),
            "failed_sessions": len(self.state.failed_sessions),
            "current_workflow": self.state.current_workflow,
            "session_details": {
                sid: {
                    "status": s.state.status.value,
                    "progress": s.state.progress_percent,
                    "current_activity": s.state.current_activity
                }
                for sid, s in self.sessions.items()
            }
        }
    
    def terminate_all(self, force: bool = False):
        """Terminate all sessions"""
        self._notify("warning", "Terminating all sessions...")
        
        for session in self.sessions.values():
            session.terminate(force=force)
        
        self.running = False
        self.executor.shutdown(wait=True)
        
        self._notify("info", "All sessions terminated")
    
    def save_state(self, filepath: Optional[Path] = None):
        """Save orchestrator state"""
        if filepath is None:
            filepath = self.workspace_root / "orchestrator_state.json"
        
        self.state.save(filepath)
        
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.terminate_all()
        self.save_state()