"""
Test ClaudeSession functionality
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

from casewise_coordination.session import ClaudeSession, SessionStatus


class TestClaudeSession(unittest.TestCase):
    """Test the ClaudeSession class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_workspace = tempfile.mkdtemp()
        self.session_id = "test-session-123"
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)
    
    def test_session_initialization(self):
        """Test session initialization"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace),
            dangerous_permissions=True
        )
        
        self.assertEqual(session.session_id, self.session_id)
        self.assertEqual(session.status, SessionStatus.INITIALIZED)
        self.assertTrue(session.dangerous_permissions)
        self.assertTrue((Path(self.test_workspace) / self.session_id).exists())
    
    def test_prompt_creation(self):
        """Test prompt file creation"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        prompt = "Test prompt content"
        session.create_prompt(prompt, task_name="test-task")
        
        prompt_file = session.workspace / self.session_id / "prompt.md"
        self.assertTrue(prompt_file.exists())
        
        content = prompt_file.read_text()
        self.assertIn("test-task", content)
        self.assertIn(prompt, content)
    
    @patch('subprocess.Popen')
    def test_start_session(self, mock_popen):
        """Test starting a Claude session"""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None  # Process is running
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        session.create_prompt("Test prompt")
        session.start()
        
        self.assertEqual(session.status, SessionStatus.RUNNING)
        self.assertIsNotNone(session.process)
        
        # Check command construction
        mock_popen.assert_called_once()
        cmd = mock_popen.call_args[0][0]
        self.assertIn("claude", cmd)
        self.assertIn("--dangerously-skip-permissions", cmd)
    
    def test_session_state_tracking(self):
        """Test session state tracking"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        # Update state
        session.update_state({
            "progress": 50,
            "current_task": "Building backend"
        })
        
        # Check state file
        state_file = session.workspace / self.session_id / "session_state.json"
        self.assertTrue(state_file.exists())
        
        with open(state_file) as f:
            state = json.load(f)
        
        self.assertEqual(state["progress"], 50)
        self.assertEqual(state["current_task"], "Building backend")
    
    def test_file_tracking(self):
        """Test tracking of created files"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        # Track some files
        files = [
            "/app/backend/main.py",
            "/app/frontend/App.tsx",
            "/app/tests/test_main.py"
        ]
        
        for file in files:
            session.track_file_created(file)
        
        self.assertEqual(len(session.files_created), 3)
        self.assertIn("/app/backend/main.py", session.files_created)
    
    @patch('subprocess.Popen')
    def test_session_monitoring(self, mock_popen):
        """Test session output monitoring"""
        # Mock process with output
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdout = Mock()
        mock_process.stdout.readline.side_effect = [
            "Starting task...\n",
            "Creating file: test.py\n",
            "Task complete\n",
            ""  # End of output
        ]
        mock_popen.return_value = mock_process
        
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        session.create_prompt("Test")
        session.start()
        
        # Monitor output
        outputs = []
        for _ in range(4):
            line = session.read_output()
            if line:
                outputs.append(line.strip())
        
        self.assertEqual(len(outputs), 3)
        self.assertIn("Starting task...", outputs)
    
    def test_error_handling(self):
        """Test error handling in session"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        # Try to start without prompt
        with self.assertRaises(Exception):
            session.start()
        
        # Test invalid status transitions
        session.status = SessionStatus.COMPLETED
        with self.assertRaises(Exception):
            session.start()
    
    def test_session_cleanup(self):
        """Test session cleanup"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        # Create some files
        session.create_prompt("Test")
        (session.workspace / self.session_id / "test_file.txt").write_text("test")
        
        # Cleanup
        session.cleanup(remove_files=True)
        
        # Check workspace is cleaned
        self.assertFalse((session.workspace / self.session_id).exists())
    
    def test_context_limits(self):
        """Test handling of context limits"""
        session = ClaudeSession(
            session_id=self.session_id,
            workspace=Path(self.test_workspace)
        )
        
        # Simulate approaching context limit
        session.estimated_tokens = 70000
        
        self.assertTrue(session.is_approaching_limit())
        
        # Prepare handoff
        handoff_data = session.prepare_handoff()
        
        self.assertIn("session_id", handoff_data)
        self.assertIn("task_name", handoff_data)
        self.assertIn("progress_percent", handoff_data)
        self.assertIn("files_created", handoff_data)


if __name__ == "__main__":
    unittest.main()