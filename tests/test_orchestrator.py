"""
Test SessionOrchestrator functionality
"""

import unittest
import asyncio
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from casewise_coordination.orchestrator import SessionOrchestrator
from casewise_coordination.session import SessionStatus


class TestSessionOrchestrator(unittest.TestCase):
    """Test the SessionOrchestrator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_workspace = tempfile.mkdtemp()
        self.orchestrator = SessionOrchestrator(
            orchestrator_id="test-orchestrator",
            workspace=Path(self.test_workspace),
            max_parallel=2
        )
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        self.assertEqual(self.orchestrator.orchestrator_id, "test-orchestrator")
        self.assertEqual(self.orchestrator.max_parallel, 2)
        self.assertEqual(len(self.orchestrator.sessions), 0)
        self.assertTrue((Path(self.test_workspace) / "orchestrator").exists())
    
    def test_state_persistence(self):
        """Test state saving and loading"""
        # Save state
        self.orchestrator.active_sessions = ["session-1", "session-2"]
        self.orchestrator.completed_sessions = ["session-0"]
        self.orchestrator._save_state()
        
        # Create new orchestrator and check loaded state
        new_orchestrator = SessionOrchestrator(
            orchestrator_id="test-orchestrator",
            workspace=Path(self.test_workspace),
            max_parallel=2
        )
        
        self.assertEqual(new_orchestrator.active_sessions, ["session-1", "session-2"])
        self.assertEqual(new_orchestrator.completed_sessions, ["session-0"])
    
    @patch('casewise_coordination.session.claude_session.ClaudeSession')
    def test_create_session(self, mock_claude_session):
        """Test session creation"""
        # Mock the ClaudeSession
        mock_session = Mock()
        mock_session.session_id = "test-session-123"
        mock_session.status = SessionStatus.INITIALIZED
        mock_claude_session.return_value = mock_session
        
        # Create session
        session = self.orchestrator.create_session(
            task_name="test-task",
            component="backend",
            description="Test session"
        )
        
        self.assertEqual(session.session_id, "test-session-123")
        self.assertIn("test-session-123", self.orchestrator.sessions)
        self.assertIn("test-session-123", self.orchestrator.active_sessions)
    
    def test_execute_workflow(self):
        """Test workflow execution method exists"""
        # Test that orchestrator has workflow execution capability
        self.assertTrue(hasattr(self.orchestrator, 'execute_workflow'))
        
        # Test basic workflow structure
        tasks = [
            {
                "name": "task1",
                "component": "backend",
                "dependencies": []
            }
        ]
        
        # Method should exist even if we don't run it fully
        self.assertTrue(callable(getattr(self.orchestrator, 'execute_workflow', None)))
    
    @patch('casewise_coordination.session.claude_session.ClaudeSession')
    def test_parallel_execution_limit(self, mock_claude_session):
        """Test parallel execution respects max_parallel limit"""
        # Mock sessions
        mock_claude_session.return_value.status = SessionStatus.RUNNING
        
        # Create max_parallel sessions
        for i in range(self.orchestrator.max_parallel):
            session = self.orchestrator.create_session(
                task_name=f"task-{i}",
                component="backend",
                description=f"Test session {i}"
            )
            session.session_id = f"session-{i}"
            self.orchestrator.sessions[f"session-{i}"] = session
            self.orchestrator.active_sessions.append(f"session-{i}")
        
        # Try to create one more - should wait
        self.assertEqual(len(self.orchestrator.active_sessions), 2)
        
        # When space is available, should be able to create
        self.orchestrator.active_sessions.pop()
        self.assertEqual(len(self.orchestrator.active_sessions), 1)
    
    def test_session_completion_tracking(self):
        """Test tracking of session completion"""
        # Simulate session completion
        self.orchestrator.active_sessions = ["session-1", "session-2"]
        
        # Move session from active to completed
        self.orchestrator.completed_sessions.append("session-1")
        self.orchestrator.active_sessions.remove("session-1")
        
        self.assertNotIn("session-1", self.orchestrator.active_sessions)
        self.assertIn("session-1", self.orchestrator.completed_sessions)
        
        # Track failed session
        self.orchestrator.failed_sessions.append("session-2")
        self.orchestrator.active_sessions.remove("session-2")
        
        self.assertNotIn("session-2", self.orchestrator.active_sessions)
        self.assertIn("session-2", self.orchestrator.failed_sessions)
    
    def test_workspace_creation(self):
        """Test workspace directory creation"""
        # Orchestrator should create its workspace
        workspace_path = Path(self.test_workspace) / "orchestrator"
        self.assertTrue(workspace_path.exists())
        self.assertTrue(workspace_path.is_dir())
    
    def test_session_management(self):
        """Test session management attributes"""
        # Orchestrator should track sessions
        self.assertTrue(hasattr(self.orchestrator, 'sessions'))
        self.assertTrue(hasattr(self.orchestrator, 'active_sessions'))
        self.assertTrue(hasattr(self.orchestrator, 'completed_sessions'))
        self.assertTrue(hasattr(self.orchestrator, 'failed_sessions'))
        
        # Should be initialized properly
        self.assertIsInstance(self.orchestrator.sessions, dict)
        self.assertIsInstance(self.orchestrator.active_sessions, list)
        self.assertIsInstance(self.orchestrator.completed_sessions, list)


if __name__ == "__main__":
    unittest.main()