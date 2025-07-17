"""
Test session templates
"""

import unittest
from pathlib import Path

from casewise_coordination.templates import (
    FrontendTemplate,
    BackendTemplate,
    TestingTemplate,
    DocumentationTemplate,
    IntegrationTemplate
)


class TestSessionTemplates(unittest.TestCase):
    """Test all session templates"""
    
    def test_frontend_template(self):
        """Test frontend template generation"""
        template = FrontendTemplate()
        
        # Test basic prompt
        context = {
            "task_name": "Todo App",
            "requirements": ["React", "TypeScript", "CRUD operations"]
        }
        prompt = template.create_prompt(
            task_description="Build a todo list UI",
            context=context
        )
        
        self.assertIn("Frontend Developer", prompt)
        self.assertIn("Todo App", prompt)
        self.assertIn("React", prompt)
        self.assertIn("TypeScript", prompt)
    
    def test_backend_template(self):
        """Test backend template generation"""
        template = BackendTemplate()
        
        context = {
            "task_name": "API Service",
            "requirements": ["FastAPI", "CRUD", "Authentication"]
        }
        prompt = template.create_prompt(
            task_description="Build REST API",
            context=context
        )
        
        self.assertIn("Backend Developer", prompt)
        self.assertIn("FastAPI", prompt)
        self.assertIn("Python", prompt)
    
    def test_testing_template(self):
        """Test testing template generation"""
        template = TestingTemplate()
        
        context = {
            "task_name": "Test Suite",
            "requirements": ["Unit tests", "Integration tests"]
        }
        prompt = template.create_prompt(
            task_description="Create comprehensive tests",
            context=context
        )
        
        self.assertIn("Testing Specialist", prompt)
        self.assertIn("pytest", prompt)
    
    def test_documentation_template(self):
        """Test documentation template generation"""
        template = DocumentationTemplate()
        
        context = {
            "task_name": "API Docs",
            "requirements": ["OpenAPI", "Examples"]
        }
        prompt = template.create_prompt(
            task_description="Document the API",
            context=context
        )
        
        self.assertIn("Documentation Specialist", prompt)
        
    def test_integration_template(self):
        """Test integration template generation"""
        template = IntegrationTemplate()
        
        context = {
            "task_name": "System Integration",
            "requirements": ["Docker", "CI/CD"]
        }
        prompt = template.create_prompt(
            task_description="Integrate all components",
            context=context
        )
        
        self.assertIn("Integration Specialist", prompt)
    
    def test_template_consistency(self):
        """Test all templates have consistent interface"""
        templates = [
            FrontendTemplate(),
            BackendTemplate(),
            TestingTemplate(),
            DocumentationTemplate(),
            IntegrationTemplate()
        ]
        
        for template in templates:
            # All should have these methods
            self.assertTrue(hasattr(template, 'create_prompt'))
            self.assertTrue(hasattr(template, 'create_base_prompt'))
            self.assertTrue(hasattr(template, 'format_context'))
            
            # All should return proper types
            context = {"task_name": "Test"}
            prompt = template.create_prompt("Test desc", context)
            self.assertIsInstance(prompt, str)
    
    def test_template_properties(self):
        """Test template properties"""
        template = FrontendTemplate()
        
        # Test template has proper attributes
        self.assertEqual(template.template_type, "frontend")
        self.assertEqual(template.template_name, "Frontend Development")
        self.assertTrue(hasattr(template, 'default_timeout'))
        self.assertTrue(hasattr(template, 'required_packages'))
    
    def test_template_timeouts(self):
        """Test template timeout settings"""
        # Each template should have appropriate timeouts
        frontend = FrontendTemplate()
        backend = BackendTemplate()
        testing = TestingTemplate()
        docs = DocumentationTemplate()
        integration = IntegrationTemplate()
        
        # Frontend tasks typically take longer
        self.assertGreater(frontend.default_timeout, 1800)  # > 30 min
        self.assertGreater(backend.default_timeout, 1800)   # > 30 min
        self.assertGreater(testing.default_timeout, 1200)   # > 20 min


if __name__ == "__main__":
    unittest.main()