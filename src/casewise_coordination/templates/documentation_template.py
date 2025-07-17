"""
Documentation Session Template
Specialized template for creating documentation
"""

from pathlib import Path
from typing import Dict, Any, List
from .base_template import SessionTemplate


class DocumentationTemplate(SessionTemplate):
    """Template for documentation sessions"""
    
    def __init__(self):
        super().__init__("documentation", "Documentation")
        self.default_timeout = 1800  # 30 minutes
    
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create documentation-specific prompt"""
        base_prompt = self.create_base_prompt(
            "Technical Writer specializing in developer documentation"
        )
        
        specific_prompt = f"""
{base_prompt}

Task: {task_description}

{self.format_context(context)}

Documentation Requirements:
1. Clear, concise technical writing
2. Code examples with explanations
3. API documentation with request/response examples
4. Installation and setup instructions
5. Troubleshooting section
6. Architecture diagrams (as ASCII art or Mermaid)

Create comprehensive documentation including:
- README.md with project overview
- API.md with endpoint documentation
- ARCHITECTURE.md with system design
- CONTRIBUTING.md with development guide
- Any other relevant documentation

Use proper Markdown formatting and make it developer-friendly.

Begin creating documentation now."""
        
        return specific_prompt
    
    def _create_template_structure(self, workspace: Path) -> None:
        """Create documentation structure"""
        (workspace / "docs").mkdir(exist_ok=True)
        (workspace / "examples").mkdir(exist_ok=True)
    
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """Validate documentation output"""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_found": []
        }
        
        # Check for README
        if not (workspace / "README.md").exists():
            results["errors"].append("No README.md found")
            results["success"] = False
        else:
            results["files_found"].append("README.md")
        
        # Check for other docs
        md_files = list(workspace.rglob("*.md"))
        if len(md_files) < 2:
            results["warnings"].append("Limited documentation found")
        
        results["files_found"].extend([str(f.relative_to(workspace)) for f in md_files])
        
        return results
    
    def get_success_criteria(self) -> List[str]:
        """Documentation-specific success criteria"""
        return [
            "Comprehensive README created",
            "API documentation complete",
            "Code examples included",
            "Clear setup instructions",
            "Well-structured content"
        ]