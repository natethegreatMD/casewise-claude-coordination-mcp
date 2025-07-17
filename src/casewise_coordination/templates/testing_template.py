"""
Testing Session Template
Specialized template for comprehensive testing
"""

from pathlib import Path
from typing import Dict, Any, List
from .base_template import SessionTemplate


class TestingTemplate(SessionTemplate):
    """Template for testing sessions"""
    
    def __init__(self):
        super().__init__("testing", "Testing and QA")
        self.default_timeout = 2400  # 40 minutes
        self.required_packages = [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "httpx",  # For API testing
            "faker",  # For test data
        ]
        self.default_env_vars = {
            "TESTING": "true"
        }
    
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create testing-specific prompt"""
        base_prompt = self.create_base_prompt(
            "QA Engineer specializing in automated testing"
        )
        
        specific_prompt = f"""
{base_prompt}

Task: {task_description}

Testing Stack:
- pytest for Python testing
- Jest for JavaScript/TypeScript testing
- pytest-asyncio for async tests
- httpx for API testing
- faker for test data generation

{self.format_context(context)}

Testing Requirements:
1. Write comprehensive unit tests for all functions/methods
2. Create integration tests for API endpoints
3. Include both positive and negative test cases
4. Add edge case testing
5. Implement proper test fixtures and mocking
6. Aim for >80% code coverage
7. Include performance tests where relevant
8. Add proper test documentation

Test Structure:
```
tests/
  conftest.py         # Shared fixtures
  test_unit/          # Unit tests
    test_models.py
    test_services.py
    test_utils.py
  test_integration/   # Integration tests  
    test_api.py
    test_workflows.py
  test_e2e/          # End-to-end tests
    test_scenarios.py
  fixtures/          # Test data
    __init__.py
    data.py
```

Testing Guidelines:
1. Use descriptive test names that explain what is being tested
2. Follow AAA pattern: Arrange, Act, Assert
3. One assertion per test when possible
4. Use parametrize for testing multiple inputs
5. Mock external dependencies
6. Create realistic test data
7. Test error conditions thoroughly

For API Testing:
- Test all endpoints with valid data
- Test validation with invalid data
- Test authentication/authorization
- Test rate limiting (if applicable)
- Test concurrent requests
- Check response formats and status codes

For Frontend Testing:
- Test component rendering
- Test user interactions
- Test state management
- Test error boundaries
- Test accessibility

Create a test report that includes:
- Coverage statistics
- Test execution time
- Failed tests (if any)
- Recommendations for improvement

Begin by analyzing the code to test, then implement comprehensive tests."""
        
        return specific_prompt
    
    def _create_template_structure(self, workspace: Path) -> None:
        """Create testing-specific directory structure"""
        tests_dir = workspace / "tests"
        
        # Create test subdirectories
        for subdir in ["test_unit", "test_integration", "test_e2e", "fixtures"]:
            (tests_dir / subdir).mkdir(parents=True, exist_ok=True)
            (tests_dir / subdir / "__init__.py").touch()
        
        # Create conftest.py
        (tests_dir / "conftest.py").touch()
        
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """Validate testing output"""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_found": [],
            "metrics": {}
        }
        
        # Check for tests directory
        tests_dir = workspace / "tests"
        if not tests_dir.exists():
            results["errors"].append("No tests directory found")
            results["success"] = False
            return results
        
        # Check for conftest.py
        conftest = tests_dir / "conftest.py"
        if not conftest.exists():
            results["warnings"].append("No conftest.py found")
        else:
            results["files_found"].append("tests/conftest.py")
        
        # Count test files
        test_files = list(tests_dir.rglob("test_*.py"))
        results["metrics"]["total_test_files"] = len(test_files)
        
        if not test_files:
            results["errors"].append("No test files found")
            results["success"] = False
        else:
            results["files_found"].extend([str(f.relative_to(workspace)) for f in test_files[:10]])
            
            # Count test functions
            test_count = 0
            for test_file in test_files:
                with open(test_file) as f:
                    content = f.read()
                    test_count += content.count("def test_")
                    test_count += content.count("async def test_")
            
            results["metrics"]["total_tests"] = test_count
            
            if test_count < 5:
                results["warnings"].append(f"Only {test_count} tests found, consider adding more")
        
        # Check for different test types
        unit_tests = list((tests_dir / "test_unit").glob("test_*.py")) if (tests_dir / "test_unit").exists() else []
        integration_tests = list((tests_dir / "test_integration").glob("test_*.py")) if (tests_dir / "test_integration").exists() else []
        
        results["metrics"]["unit_tests"] = len(unit_tests)
        results["metrics"]["integration_tests"] = len(integration_tests)
        
        if not unit_tests:
            results["warnings"].append("No unit tests found")
        if not integration_tests:
            results["warnings"].append("No integration tests found")
        
        # Check for coverage report
        coverage_files = list(workspace.glob("*coverage*"))
        if coverage_files:
            results["files_found"].append("Coverage report found")
        else:
            results["warnings"].append("No coverage report found")
        
        # Check for test documentation
        test_docs = [f for f in tests_dir.rglob("*.md") if "readme" in f.name.lower()]
        if not test_docs:
            results["warnings"].append("No test documentation found")
        
        return results
    
    def get_success_criteria(self) -> List[str]:
        """Testing-specific success criteria"""
        return [
            "Comprehensive test suite created",
            "Unit tests cover core functionality",
            "Integration tests verify workflows",
            "Both positive and negative cases tested",
            "Test fixtures properly organized",
            "Tests run successfully",
            "Good code coverage achieved (>70%)",
            "Test documentation provided"
        ]