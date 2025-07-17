"""
Claude Session Wrapper
Controls individual Claude Code sessions via subprocess
"""

import subprocess
import threading
import queue
import time
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable

from .session_state import SessionState, SessionStatus


logger = logging.getLogger(__name__)


class ClaudeSession:
    """
    Manages a single Claude Code session
    Handles spawning, communication, monitoring, and lifecycle
    """
    
    def __init__(
        self,
        session_id: str,
        task_name: str,
        component: str,
        workspace_root: Path,
        dangerous_permissions: bool = True,
        timeout_seconds: int = 3600,
        env_vars: Optional[Dict[str, str]] = None
    ):
        """
        Initialize a Claude session
        
        Args:
            session_id: Unique identifier for this session
            task_name: Name of the task (e.g., "auth", "api") 
            component: Component type (e.g., "frontend", "backend")
            workspace_root: Root directory for session workspaces
            dangerous_permissions: Use --dangerously-skip-permissions flag
            timeout_seconds: Maximum execution time
            env_vars: Additional environment variables
        """
        self.session_id = session_id
        self.workspace = workspace_root / session_id
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Initialize state
        self.state = SessionState(
            session_id=session_id,
            task_name=task_name,
            component=component,
            status=SessionStatus.PENDING,
            workspace=self.workspace
        )
        
        # Process management
        self.process: Optional[subprocess.Popen] = None
        self.dangerous_permissions = dangerous_permissions
        self.timeout_seconds = timeout_seconds
        self.env_vars = env_vars or {}
        
        # Communication
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        self.output_thread: Optional[threading.Thread] = None
        self.error_thread: Optional[threading.Thread] = None
        
        # Monitoring
        self.start_time: Optional[float] = None
        self.output_callback: Optional[Callable[[str], None]] = None
        self.state_callback: Optional[Callable[[SessionState], None]] = None
        
        # Logging
        self.log_file = self.workspace / "session.log"
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup session-specific logging"""
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger = logging.getLogger(f"claude_session.{self.session_id}")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def start(self, task_prompt: str, input_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Start the Claude session with a task
        
        Args:
            task_prompt: The prompt/instructions for Claude
            input_data: Optional input data for the task
            
        Returns:
            bool: True if started successfully
        """
        try:
            self.logger.info(f"Starting session {self.session_id}")
            self.state.task_description = task_prompt
            self.state.input_spec = input_data or {}
            self.state.status = SessionStatus.STARTING
            self.state.save()
            
            # Build command
            cmd = ["claude", "--continue"]
            if self.dangerous_permissions:
                cmd.append("--dangerously-skip-permissions")
            cmd.extend(["--print", task_prompt])
            
            # Setup environment
            env = os.environ.copy()
            env.update(self.env_vars)
            env["CCC_SESSION_ID"] = self.session_id
            env["CCC_WORKSPACE"] = str(self.workspace)
            
            # Start process
            self.process = subprocess.Popen(
                cmd,
                cwd=str(self.workspace),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env
            )
            
            self.state.pid = self.process.pid
            self.start_time = time.time()
            
            # Start output monitoring threads
            self.output_thread = threading.Thread(
                target=self._read_output,
                args=(self.process.stdout, "stdout")
            )
            self.error_thread = threading.Thread(
                target=self._read_output,
                args=(self.process.stderr, "stderr")
            )
            
            self.output_thread.daemon = True
            self.error_thread.daemon = True
            self.output_thread.start()
            self.error_thread.start()
            
            # Mark as running
            self.state.mark_started()
            self.state.save()
            
            self.logger.info(f"Session started with PID {self.process.pid}")
            self._notify_state_change()
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self._monitor_session)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start session: {e}")
            self.state.status = SessionStatus.FAILED
            self.state.last_error = str(e)
            self.state.error_count += 1
            self.state.save()
            self._notify_state_change()
            return False
    
    def _read_output(self, pipe, pipe_name: str):
        """Read output from subprocess pipe"""
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    line = line.rstrip()
                    self.output_queue.put((pipe_name, line))
                    self.logger.debug(f"{pipe_name}: {line}")
                    
                    # Log to file
                    with open(self.workspace / f"{pipe_name}.log", 'a') as f:
                        f.write(f"{datetime.now().isoformat()} - {line}\n")
                    
                    # Callback if set
                    if self.output_callback:
                        self.output_callback(line)
                        
        except Exception as e:
            self.logger.error(f"Error reading {pipe_name}: {e}")
    
    def _monitor_session(self):
        """Monitor session health and progress"""
        while self.process and self.process.poll() is None:
            # Check timeout
            if self.start_time:
                elapsed = time.time() - self.start_time
                if elapsed > self.timeout_seconds:
                    self.logger.warning("Session timeout reached")
                    self.terminate()
                    break
            
            # Update metrics
            self.state.execution_time_seconds = elapsed if self.start_time else 0
            
            # Check for created files
            self._scan_workspace_changes()
            
            # Save state periodically
            self.state.save()
            
            time.sleep(5)  # Check every 5 seconds
        
        # Session ended
        exit_code = self.process.returncode if self.process else -1
        success = exit_code == 0
        
        self.state.mark_completed(success)
        if not success:
            self.state.last_error = f"Process exited with code {exit_code}"
            self.state.error_count += 1
        
        self.state.save()
        self._notify_state_change()
        self.logger.info(f"Session ended with exit code {exit_code}")
    
    def _scan_workspace_changes(self):
        """Scan workspace for new/modified files"""
        try:
            current_files = set()
            for file in self.workspace.rglob("*"):
                if file.is_file() and not file.name.endswith('.log'):
                    current_files.add(str(file.relative_to(self.workspace)))
            
            # Update files created
            new_files = current_files - set(self.state.files_created)
            if new_files:
                self.state.files_created.extend(new_files)
                for file in new_files:
                    self.state.add_message("file_created", f"Created: {file}")
                    
        except Exception as e:
            self.logger.error(f"Error scanning workspace: {e}")
    
    def send_input(self, text: str):
        """Send input to the Claude session"""
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(text + "\n")
                self.process.stdin.flush()
                self.logger.info(f"Sent input: {text}")
                self.state.add_message("input", text)
                return True
            except Exception as e:
                self.logger.error(f"Failed to send input: {e}")
                return False
        return False
    
    def get_output(self, timeout: float = 0.1) -> List[tuple]:
        """Get recent output from session"""
        output = []
        deadline = time.time() + timeout
        
        while time.time() < deadline:
            try:
                item = self.output_queue.get(timeout=0.01)
                output.append(item)
            except queue.Empty:
                break
                
        return output
    
    def wait_for_completion(self, check_interval: float = 1.0) -> bool:
        """Wait for session to complete"""
        while self.process and self.process.poll() is None:
            time.sleep(check_interval)
        
        return self.state.status == SessionStatus.COMPLETED
    
    def terminate(self, force: bool = False):
        """Terminate the session"""
        if self.process:
            try:
                if force:
                    self.process.kill()
                    self.logger.warning("Force killed session")
                else:
                    self.process.terminate()
                    self.logger.info("Terminated session")
                    
                self.process.wait(timeout=5)
                
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.logger.warning("Had to force kill after terminate timeout")
                
            except Exception as e:
                self.logger.error(f"Error terminating session: {e}")
            
            self.state.status = SessionStatus.TERMINATED
            self.state.save()
            self._notify_state_change()
    
    def set_output_callback(self, callback: Callable[[str], None]):
        """Set callback for output lines"""
        self.output_callback = callback
    
    def set_state_callback(self, callback: Callable[[SessionState], None]):
        """Set callback for state changes"""
        self.state_callback = callback
    
    def _notify_state_change(self):
        """Notify about state change"""
        if self.state_callback:
            self.state_callback(self.state)
    
    def get_state(self) -> SessionState:
        """Get current session state"""
        return self.state
    
    def get_workspace_files(self) -> List[Path]:
        """Get all files created in workspace"""
        files = []
        for file in self.workspace.rglob("*"):
            if file.is_file() and not file.name.endswith('.log'):
                files.append(file)
        return files
    
    def cleanup(self, keep_files: bool = True):
        """Cleanup session resources"""
        self.terminate()
        
        if not keep_files and self.workspace.exists():
            import shutil
            shutil.rmtree(self.workspace)
            self.logger.info("Cleaned up workspace")
    
    def __repr__(self):
        return f"<ClaudeSession {self.session_id} [{self.state.status.value}]>"