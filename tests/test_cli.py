"""
Test CCC CLI functionality
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner

from casewise_coordination.cli import cli


class TestCCCCLI(unittest.TestCase):
    """Test the CCC CLI"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
        self.test_workspace = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)
    
    def test_cli_help(self):
        """Test CLI help command"""
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Claude Code Coordinator', result.output)
        self.assertIn('Orchestrate multiple Claude sessions', result.output)
    
    def test_version_command(self):
        """Test version command"""
        result = self.runner.invoke(cli, ['version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('CCC - Claude Code Coordinator', result.output)
        self.assertIn('v0.1.0', result.output)
    
    def test_status_command_no_orchestrator(self):
        """Test status command when no orchestrator is running"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['--workspace', '.', 'status'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('No active orchestrator found', result.output)
    
    def test_status_command_with_orchestrator(self):
        """Test status command with running orchestrator"""
        with self.runner.isolated_filesystem():
            # Create mock orchestrator state
            Path('orchestrator').mkdir(parents=True)
            state = {
                'orchestrator_id': 'test-123',
                'started_at': '2025-01-01T00:00:00',
                'active_sessions': ['session-1', 'session-2'],
                'completed_sessions': ['session-0'],
                'failed_sessions': []
            }
            
            with open('orchestrator/orchestrator_state.json', 'w') as f:
                json.dump(state, f)
            
            result = self.runner.invoke(cli, ['--workspace', '.', 'status'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('test-123', result.output)
            self.assertIn('Active Sessions: 2', result.output)
            self.assertIn('Completed: 1', result.output)
    
    def test_config_command(self):
        """Test config command"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['--workspace', '.', 'config'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('max_parallel_sessions', result.output)
            self.assertIn('dangerous_permissions', result.output)
    
    def test_workflow_list_command(self):
        """Test workflow list command"""
        result = self.runner.invoke(cli, ['workflow', 'list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('todo_app', result.output)
        self.assertIn('auth_system', result.output)
        self.assertIn('blog_platform', result.output)
    
    def test_workflow_run_command(self):
        """Test workflow run command"""
        # Test without confirmation
        result = self.runner.invoke(
            cli, 
            ['workflow', 'run', 'todo_app', '--name', 'my-app'],
            input='n\n'
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Workflow cancelled', result.output)
        
        # Test with confirmation
        result = self.runner.invoke(
            cli,
            ['workflow', 'run', 'todo_app', '--name', 'my-app'],
            input='y\n'
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Workflow started', result.output)
    
    def test_session_list_command(self):
        """Test session list command"""
        with self.runner.isolated_filesystem():
            # No sessions
            result = self.runner.invoke(cli, ['--workspace', '.', 'session', 'list'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('No sessions found', result.output)
            
            # With sessions
            Path('orchestrator/sessions/session-1').mkdir(parents=True)
            state = {
                'session_id': 'session-1',
                'status': 'running',
                'task_name': 'Test Task',
                'component': 'backend',
                'progress_percent': 50,
                'files_created': ['test.py']
            }
            
            with open('orchestrator/sessions/session-1/session_state.json', 'w') as f:
                json.dump(state, f)
            
            result = self.runner.invoke(cli, ['--workspace', '.', 'session', 'list'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('session-1', result.output)
            self.assertIn('Test Task', result.output)
            self.assertIn('50%', result.output)
    
    def test_session_logs_command(self):
        """Test session logs command"""
        with self.runner.isolated_filesystem():
            # No logs
            result = self.runner.invoke(cli, ['--workspace', '.', 'session', 'logs', 'session-1'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('No logs found', result.output)
            
            # With logs
            Path('orchestrator/sessions/session-1').mkdir(parents=True)
            log_content = "Line 1\nLine 2\nLine 3\n"
            with open('orchestrator/sessions/session-1/session.log', 'w') as f:
                f.write(log_content)
            
            result = self.runner.invoke(cli, ['--workspace', '.', 'session', 'logs', 'session-1'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Line 1', result.output)
            self.assertIn('Line 3', result.output)
    
    def test_demo_command(self):
        """Test demo command"""
        # Without confirmation
        result = self.runner.invoke(cli, ['demo'], input='n\n')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Demo cancelled', result.output)
        
        # With confirmation
        result = self.runner.invoke(cli, ['demo'], input='y\n')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Demo started', result.output)
    
    @patch('subprocess.Popen')
    def test_start_command(self, mock_popen):
        """Test start command"""
        mock_process = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['--workspace', '.', 'start'])
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Orchestrator started', result.output)
            self.assertIn('12345', result.output)
    
    def test_cli_workspace_option(self):
        """Test workspace option"""
        with self.runner.isolated_filesystem():
            # Custom workspace
            result = self.runner.invoke(cli, ['--workspace', 'custom_ws', 'config'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(Path('custom_ws').exists())
            self.assertTrue(Path('custom_ws/ccc_config.json').exists())


if __name__ == "__main__":
    unittest.main()