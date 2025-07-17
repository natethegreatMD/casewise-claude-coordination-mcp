"""
Frontend Session Template
Specialized template for React/TypeScript frontend development
"""

from pathlib import Path
from typing import Dict, Any, List
from .base_template import SessionTemplate


class FrontendTemplate(SessionTemplate):
    """Template for frontend development sessions"""
    
    def __init__(self):
        super().__init__("frontend", "Frontend Development")
        self.default_timeout = 2400  # 40 minutes
        self.required_packages = []  # Frontend uses npm
        self.default_env_vars = {
            "NODE_ENV": "development"
        }
    
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create frontend-specific prompt"""
        base_prompt = self.create_base_prompt(
            "Frontend Developer specializing in React and TypeScript"
        )
        
        specific_prompt = f"""
{base_prompt}

Task: {task_description}

Frontend Stack:
- React 18+ with TypeScript
- Modern hooks and functional components
- CSS Modules or styled-components for styling
- Vite for build tooling
- React Router for navigation (if needed)
- Axios or fetch for API calls

{self.format_context(context)}

Technical Requirements:
1. Use TypeScript with strict mode enabled
2. Create reusable, composable components
3. Implement proper state management (useState, useReducer, or Context)
4. Handle loading and error states
5. Make the UI responsive and accessible
6. Follow React best practices and conventions
7. Add prop validation with TypeScript interfaces

Project Structure:
```
src/
  components/     # Reusable components
  pages/         # Page components  
  hooks/         # Custom hooks
  utils/         # Utility functions
  types/         # TypeScript types/interfaces
  styles/        # Global styles
  services/      # API service functions
```

Start by creating a new React + TypeScript project with Vite:
```bash
npm create vite@latest . -- --template react-ts
npm install
```

Then implement the required functionality. Make sure to:
- Test the application runs correctly
- Ensure TypeScript has no errors
- Create a clean, modern UI
- Handle edge cases appropriately

Begin implementation now."""
        
        return specific_prompt
    
    def _create_template_structure(self, workspace: Path) -> None:
        """Create frontend-specific directory structure"""
        # Vite will create most of the structure
        (workspace / "design-docs").mkdir(exist_ok=True)
        
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """Validate frontend output"""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_found": []
        }
        
        # Check for package.json
        package_json = workspace / "package.json"
        if not package_json.exists():
            results["errors"].append("No package.json found")
            results["success"] = False
        else:
            results["files_found"].append("package.json")
        
        # Check for TypeScript config
        tsconfig = workspace / "tsconfig.json"
        if not tsconfig.exists():
            results["warnings"].append("No tsconfig.json found")
        else:
            results["files_found"].append("tsconfig.json")
        
        # Check for source files
        src_dir = workspace / "src"
        if not src_dir.exists():
            results["errors"].append("No src directory found")
            results["success"] = False
        else:
            # Check for key files
            tsx_files = list(src_dir.rglob("*.tsx"))
            ts_files = list(src_dir.rglob("*.ts"))
            
            if not tsx_files:
                results["errors"].append("No React components (.tsx files) found")
                results["success"] = False
            else:
                results["files_found"].extend([str(f.relative_to(workspace)) for f in tsx_files[:5]])
            
            # Check for App component
            app_files = [f for f in tsx_files if "app" in f.name.lower()]
            if not app_files:
                results["warnings"].append("No App component found")
        
        # Check for entry point
        if not (workspace / "index.html").exists():
            results["warnings"].append("No index.html found (required for Vite)")
        
        return results
    
    def get_success_criteria(self) -> List[str]:
        """Frontend-specific success criteria"""
        return [
            "React app created with TypeScript",
            "All components have proper TypeScript types",
            "Application runs without errors",
            "UI is responsive and styled",
            "Error boundaries implemented",
            "Loading states handled",
            "API integration works (if applicable)"
        ]