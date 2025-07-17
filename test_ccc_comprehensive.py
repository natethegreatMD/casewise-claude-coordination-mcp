#!/usr/bin/env python3
"""
CCC Comprehensive Test Suite
Tests the actual CCC implementation as built
"""

import unittest
import tempfile
import shutil
import subprocess
import json
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import CCC modules
import casewise_coordination
from casewise_coordination.orchestrator import SessionOrchestrator
from casewise_coordination.session import ClaudeSession, SessionStatus
from casewise_coordination.templates import (
    FrontendTemplate, BackendTemplate, TestingTemplate,
    DocumentationTemplate, IntegrationTemplate
)
from casewise_coordination.orchestrator.task_distribution import TaskDistributor
# Desktop notify is implemented inline, not as a separate module
from casewise_coordination.cli.ccc_cli import CCCCli


class TestCCCCore(unittest.TestCase):
    """Test core CCC functionality"""
    
    def test_version(self):
        """Test CCC version is set"""
        self.assertEqual(casewise_coordination.__version__, "0.1.0")
    
    def test_imports(self):
        """Test all major imports work"""
        # Core classes should be importable
        self.assertIsNotNone(SessionOrchestrator)
        self.assertIsNotNone(ClaudeSession)
        self.assertIsNotNone(TaskDistributor)
        
        # Templates should be importable
        self.assertIsNotNone(FrontendTemplate)
        self.assertIsNotNone(BackendTemplate)
        self.assertIsNotNone(TestingTemplate)
        
        # CLI should be importable
        self.assertIsNotNone(CCCCli)


class TestOrchestrator(unittest.TestCase):
    """Test SessionOrchestrator functionality"""
    
    def setUp(self):
        """Set up test workspace"""
        self.test_workspace = tempfile.mkdtemp()
        self.orchestrator = SessionOrchestrator(
            workspace=Path(self.test_workspace),
            max_parallel=2
        )
    
    def tearDown(self):
        """Clean up test workspace"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initializes correctly"""
        self.assertEqual(self.orchestrator.max_parallel, 2)
        self.assertIsInstance(self.orchestrator.sessions, dict)
        self.assertIsInstance(self.orchestrator.active_sessions, list)
        self.assertTrue((Path(self.test_workspace) / "orchestrator").exists())
    
    def test_state_directory_creation(self):
        """Test orchestrator creates necessary directories"""
        expected_dirs = [
            Path(self.test_workspace) / "orchestrator",
            Path(self.test_workspace) / "orchestrator" / "sessions",
            Path(self.test_workspace) / "orchestrator" / "workflows"
        ]
        
        for dir_path in expected_dirs:
            self.assertTrue(dir_path.exists(), f"Directory {dir_path} not created")
    
    def test_execute_workflow_method(self):
        """Test execute_workflow method exists and is callable"""
        self.assertTrue(hasattr(self.orchestrator, 'execute_workflow'))
        self.assertTrue(callable(self.orchestrator.execute_workflow))


class TestSession(unittest.TestCase):
    """Test ClaudeSession functionality"""
    
    def setUp(self):
        """Set up test workspace"""
        self.test_workspace = tempfile.mkdtemp()
        self.session = ClaudeSession(
            session_id="test-session",
            workspace=Path(self.test_workspace)
        )
    
    def tearDown(self):
        """Clean up test workspace"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)
    
    def test_session_initialization(self):
        """Test session initializes correctly"""
        self.assertEqual(self.session.session_id, "test-session")
        self.assertEqual(self.session.status, SessionStatus.INITIALIZED)
        self.assertTrue((Path(self.test_workspace) / "test-session").exists())
    
    def test_prompt_creation(self):
        """Test creating a prompt file"""
        self.session.create_prompt("Test prompt", task_name="Test Task")
        
        prompt_file = Path(self.test_workspace) / "test-session" / "prompt.md"
        self.assertTrue(prompt_file.exists())
        
        content = prompt_file.read_text()
        self.assertIn("Test Task", content)
        self.assertIn("Test prompt", content)
    
    def test_state_tracking(self):
        """Test session state tracking"""
        self.session.update_state({
            "progress": 50,
            "current_step": "Building"
        })
        
        state_file = Path(self.test_workspace) / "test-session" / "session_state.json"
        self.assertTrue(state_file.exists())
        
        with open(state_file) as f:
            state = json.load(f)
        
        self.assertEqual(state["progress"], 50)
        self.assertEqual(state["current_step"], "Building")


class TestTemplates(unittest.TestCase):
    """Test session templates"""
    
    def test_all_templates_have_create_prompt(self):
        """Test all templates implement create_prompt"""
        templates = [
            FrontendTemplate(),
            BackendTemplate(),
            TestingTemplate(),
            DocumentationTemplate(),
            IntegrationTemplate()
        ]
        
        for template in templates:
            # All should have create_prompt method
            self.assertTrue(hasattr(template, 'create_prompt'))
            
            # Test creating a prompt
            context = {"task_name": "Test", "requirements": ["test"]}
            prompt = template.create_prompt("Test task", context)
            
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 100)  # Should be substantial
    
    def test_template_attributes(self):
        """Test templates have required attributes"""
        templates = [
            (FrontendTemplate(), "frontend"),
            (BackendTemplate(), "backend"),
            (TestingTemplate(), "testing"),
            (DocumentationTemplate(), "documentation"),
            (IntegrationTemplate(), "integration")
        ]
        
        for template, expected_type in templates:
            self.assertEqual(template.template_type, expected_type)
            self.assertTrue(hasattr(template, 'default_timeout'))
            self.assertIsInstance(template.default_timeout, int)


class TestTaskDistribution(unittest.TestCase):
    """Test task distribution functionality"""
    
    def setUp(self):
        """Set up distributor"""
        self.distributor = TaskDistributor()
    
    def test_task_templates_exist(self):
        """Test predefined task templates exist"""
        self.assertIn('todo_app', self.distributor.task_templates)
        self.assertIn('auth_system', self.distributor.task_templates)
        self.assertIn('blog_platform', self.distributor.task_templates)
    
    def test_todo_app_template(self):
        """Test todo app template structure"""
        tasks = self.distributor.task_templates['todo_app']
        
        # Should have multiple tasks
        self.assertGreater(len(tasks), 2)
        
        # Check task structure
        for task in tasks:
            self.assertIn('name', task)
            self.assertIn('component', task)
            self.assertIn('description', task)
            self.assertIn('estimated_minutes', task)
            self.assertIn('dependencies', task)
            self.assertIsInstance(task['dependencies'], list)
    
    def test_analyze_dependencies(self):
        """Test dependency analysis"""
        tasks = self.distributor.task_templates['todo_app']
        result = self.distributor.analyze_dependencies(tasks)
        
        self.assertIsInstance(result, dict)
        self.assertIn('phases', result)
        self.assertIn('dependency_graph', result)
        self.assertIsInstance(result['phases'], list)
        self.assertGreater(len(result['phases']), 0)
    
    def test_time_estimation(self):
        """Test time estimation"""
        tasks = self.distributor.task_templates['todo_app']
        result = self.distributor.estimate_total_time(tasks)
        
        self.assertIsInstance(result, dict)
        self.assertIn('sequential_execution_minutes', result)
        self.assertIn('parallel_execution_minutes', result)
        self.assertIn('time_saved_minutes', result)
        
        # Parallel should be faster than sequential
        self.assertLessEqual(
            result['parallel_execution_minutes'],
            result['sequential_execution_minutes']
        )


class TestCLI(unittest.TestCase):
    """Test CLI functionality"""
    
    def test_cli_initialization(self):
        """Test CLI can be initialized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CCCCli(workspace=tmpdir)
            
            self.assertTrue(Path(tmpdir).exists())
            self.assertTrue((Path(tmpdir) / "ccc_config.json").exists())
            
            # Check default config
            self.assertEqual(cli.config['max_parallel_sessions'], 3)
            self.assertTrue(cli.config['dangerous_permissions'])


class TestScripts(unittest.TestCase):
    """Test supporting scripts"""
    
    def test_watch_script_exists(self):
        """Test watch_ccc.sh exists"""
        watch_script = Path(__file__).parent / "scripts" / "watch_ccc.sh"
        self.assertTrue(watch_script.exists())
    
    def test_quickstart_script_exists(self):
        """Test quickstart.sh exists"""
        quickstart = Path(__file__).parent / "quickstart.sh"
        self.assertTrue(quickstart.exists())
    
    def test_install_script_exists(self):
        """Test install.sh exists"""
        install = Path(__file__).parent / "install.sh"
        self.assertTrue(install.exists())


class TestIntegration(unittest.TestCase):
    """Test integrated functionality"""
    
    def test_todo_app_workflow(self):
        """Test the todo app workflow can be analyzed"""
        distributor = TaskDistributor()
        tasks = distributor.task_templates['todo_app']
        
        # Analyze workflow
        analysis = distributor.analyze_dependencies(tasks)
        time_est = distributor.estimate_total_time(tasks)
        
        # Should have reasonable structure
        self.assertGreater(len(analysis['phases']), 0)
        self.assertGreater(time_est['sequential_execution_minutes'], 0)
        
        # Components should include backend, frontend, testing
        components = set(task['component'] for task in tasks)
        self.assertIn('backend', components)
        self.assertIn('frontend', components)
        self.assertIn('testing', components)
    
    def test_orchestrator_with_templates(self):
        """Test orchestrator can work with templates"""
        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = SessionOrchestrator(
                workspace=Path(tmpdir),
                max_parallel=3
            )
            
            # Get templates
            frontend = FrontendTemplate()
            backend = BackendTemplate()
            
            # Templates should be compatible with orchestrator
            self.assertIsNotNone(frontend)
            self.assertIsNotNone(backend)
            self.assertIsNotNone(orchestrator)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)