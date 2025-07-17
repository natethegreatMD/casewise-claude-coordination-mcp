"""
Backend Session Template
Specialized template for FastAPI backend development
"""

from pathlib import Path
from typing import Dict, Any, List
from .base_template import SessionTemplate


class BackendTemplate(SessionTemplate):
    """Template for backend development sessions"""
    
    def __init__(self):
        super().__init__("backend", "Backend Development")
        self.default_timeout = 2400  # 40 minutes
        self.required_packages = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "python-dotenv",
            "httpx"  # For testing
        ]
        self.default_env_vars = {
            "ENVIRONMENT": "development"
        }
    
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create backend-specific prompt"""
        base_prompt = self.create_base_prompt(
            "Backend Developer specializing in FastAPI and Python"
        )
        
        specific_prompt = f"""
{base_prompt}

Task: {task_description}

Backend Stack:
- FastAPI (latest version)
- Python 3.8+
- Pydantic for data validation
- SQLAlchemy for database (if needed)
- Alembic for migrations (if needed)
- JWT for authentication (if needed)

{self.format_context(context)}

Technical Requirements:
1. Use async/await for all route handlers
2. Implement proper error handling with HTTP exceptions
3. Add comprehensive Pydantic models for request/response
4. Include CORS middleware configuration
5. Add OpenAPI documentation with descriptions
6. Implement proper logging
7. Follow RESTful API conventions
8. Add input validation and sanitization

Project Structure:
```
app/
  __init__.py
  main.py          # FastAPI app initialization
  config.py        # Configuration management
  models/          # Pydantic models
    __init__.py
    schemas.py     # Request/response schemas
  api/             # API routes
    __init__.py
    routes.py      # Route definitions
  core/            # Core functionality
    __init__.py
    security.py    # Security utilities (if needed)
  services/        # Business logic
    __init__.py
  utils/           # Utility functions
    __init__.py
tests/             # Test files
  __init__.py
  test_api.py
```

Setup Instructions:
1. Create virtual environment and install dependencies
2. Set up the FastAPI application structure
3. Implement the required endpoints
4. Add proper error handling and validation
5. Create a simple test to verify functionality

Include a README.md with:
- API endpoints documentation
- Setup instructions
- Example requests

Create a requirements.txt with all dependencies.

Begin implementation now."""
        
        return specific_prompt
    
    def _create_template_structure(self, workspace: Path) -> None:
        """Create backend-specific directory structure"""
        app_dir = workspace / "app"
        app_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        for subdir in ["models", "api", "core", "services", "utils"]:
            (app_dir / subdir).mkdir(exist_ok=True)
            (app_dir / subdir / "__init__.py").touch()
        
        # Create __init__.py in app
        (app_dir / "__init__.py").touch()
        
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """Validate backend output"""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_found": []
        }
        
        # Check for requirements.txt
        requirements = workspace / "requirements.txt"
        if not requirements.exists():
            results["errors"].append("No requirements.txt found")
            results["success"] = False
        else:
            results["files_found"].append("requirements.txt")
            # Check if FastAPI is in requirements
            with open(requirements) as f:
                content = f.read()
                if "fastapi" not in content:
                    results["errors"].append("FastAPI not in requirements.txt")
                    results["success"] = False
        
        # Check for main app file
        app_dir = workspace / "app"
        if not app_dir.exists():
            results["errors"].append("No app directory found")
            results["success"] = False
        else:
            main_py = app_dir / "main.py"
            if not main_py.exists():
                results["errors"].append("No app/main.py found")
                results["success"] = False
            else:
                results["files_found"].append("app/main.py")
        
        # Check for models
        models_dir = app_dir / "models"
        if models_dir.exists():
            py_files = list(models_dir.glob("*.py"))
            if len(py_files) <= 1:  # Only __init__.py
                results["warnings"].append("No model files found")
        
        # Check for API routes
        api_dir = app_dir / "api"
        if api_dir.exists():
            route_files = [f for f in api_dir.glob("*.py") if f.name != "__init__.py"]
            if not route_files:
                results["errors"].append("No API route files found")
                results["success"] = False
            else:
                results["files_found"].extend([str(f.relative_to(workspace)) for f in route_files])
        
        # Check for tests
        tests_dir = workspace / "tests"
        if not tests_dir.exists():
            results["warnings"].append("No tests directory found")
        else:
            test_files = list(tests_dir.glob("test_*.py"))
            if not test_files:
                results["warnings"].append("No test files found")
            else:
                results["files_found"].extend([str(f.relative_to(workspace)) for f in test_files])
        
        # Check for README
        if not (workspace / "README.md").exists():
            results["warnings"].append("No README.md found")
        
        return results
    
    def get_success_criteria(self) -> List[str]:
        """Backend-specific success criteria"""
        return [
            "FastAPI application created",
            "All endpoints have Pydantic models",
            "Proper error handling implemented", 
            "API documentation available at /docs",
            "CORS configured correctly",
            "Requirements.txt includes all dependencies",
            "Basic tests included",
            "Application runs without errors"
        ]