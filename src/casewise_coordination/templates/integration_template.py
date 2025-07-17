"""
Integration Session Template
Specialized template for system integration and deployment
"""

from pathlib import Path
from typing import Dict, Any, List
from .base_template import SessionTemplate


class IntegrationTemplate(SessionTemplate):
    """Template for integration and deployment sessions"""
    
    def __init__(self):
        super().__init__("integration", "Integration & Deployment")
        self.default_timeout = 2400  # 40 minutes
    
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create integration-specific prompt"""
        base_prompt = self.create_base_prompt(
            "DevOps Engineer specializing in integration and deployment"
        )
        
        specific_prompt = f"""
{base_prompt}

Task: {task_description}

{self.format_context(context)}

Integration Requirements:
1. Combine components from different sessions
2. Ensure all parts work together
3. Create deployment configuration
4. Set up development environment
5. Create integration tests
6. Document deployment process

Key Tasks:
- Create docker-compose.yml if needed
- Set up environment variables
- Create startup scripts
- Integrate frontend with backend
- Configure CORS and networking
- Create health check endpoints
- Write deployment documentation

Ensure the complete system can be run with simple commands.

Begin integration work now."""
        
        return specific_prompt
    
    def _create_template_structure(self, workspace: Path) -> None:
        """Create integration structure"""
        (workspace / "scripts").mkdir(exist_ok=True)
        (workspace / "config").mkdir(exist_ok=True)
        (workspace / "docker").mkdir(exist_ok=True)
    
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """Validate integration output"""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_found": []
        }
        
        # Check for key integration files
        important_files = [
            "docker-compose.yml",
            "README.md",
            ".env.example"
        ]
        
        for filename in important_files:
            if (workspace / filename).exists():
                results["files_found"].append(filename)
            else:
                results["warnings"].append(f"No {filename} found")
        
        # Check for scripts
        scripts = list((workspace / "scripts").glob("*")) if (workspace / "scripts").exists() else []
        if not scripts:
            results["warnings"].append("No scripts found")
        
        return results
    
    def get_success_criteria(self) -> List[str]:
        """Integration-specific success criteria"""
        return [
            "All components integrated",
            "System runs with single command",
            "Environment configuration complete",
            "Health checks implemented",
            "Deployment documented"
        ]