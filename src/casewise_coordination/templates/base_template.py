"""
Base Session Template
Abstract base class for all session templates
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path


class SessionTemplate(ABC):
    """
    Base class for session templates
    Defines the interface and common functionality
    """
    
    def __init__(self, name: str, component: str):
        self.name = name
        self.component = component
        self.default_timeout = 1800  # 30 minutes
        self.default_env_vars = {}
        self.required_packages = []
        self.setup_commands = []
    
    @abstractmethod
    def create_prompt(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Create the prompt for this session type
        
        Args:
            task_description: High-level task description
            context: Additional context (dependencies, requirements, etc.)
            
        Returns:
            str: Complete prompt for Claude
        """
        pass
    
    @abstractmethod
    def validate_output(self, workspace: Path) -> Dict[str, Any]:
        """
        Validate the output of the session
        
        Args:
            workspace: Path to session workspace
            
        Returns:
            Dict: Validation results with success flag and details
        """
        pass
    
    def get_setup_script(self) -> str:
        """Get setup commands to run before main task"""
        if not self.setup_commands and not self.required_packages:
            return ""
        
        script = "# Setup environment\n"
        
        if self.required_packages:
            script += f"pip install {' '.join(self.required_packages)}\n"
        
        for cmd in self.setup_commands:
            script += f"{cmd}\n"
        
        return script
    
    def get_env_vars(self) -> Dict[str, str]:
        """Get environment variables for session"""
        return self.default_env_vars.copy()
    
    def prepare_workspace(self, workspace: Path) -> None:
        """Prepare the workspace before session starts"""
        workspace.mkdir(parents=True, exist_ok=True)
        
        # Create standard directories
        (workspace / "src").mkdir(exist_ok=True)
        (workspace / "tests").mkdir(exist_ok=True)
        (workspace / "docs").mkdir(exist_ok=True)
        
        # Create template-specific structure
        self._create_template_structure(workspace)
    
    @abstractmethod
    def _create_template_structure(self, workspace: Path) -> None:
        """Create template-specific directory structure"""
        pass
    
    def create_base_prompt(self, role_description: str) -> str:
        """Create the base prompt common to all sessions"""
        return f"""You are a {self.component} specialist in a coordinated development team.

Your role: {role_description}

General Guidelines:
1. Create production-quality code with proper error handling
2. Follow best practices and design patterns
3. Include helpful comments but avoid over-commenting
4. Create all necessary files in your workspace
5. Test your code to ensure it works correctly
6. Use modern, up-to-date practices and libraries

You have full internet access to:
- Install packages as needed
- Look up documentation
- Research best practices
- Download resources

Your workspace is isolated and you have full autonomy to complete your task.
"""
    
    def format_context(self, context: Dict[str, Any]) -> str:
        """Format context information for the prompt"""
        sections = []
        
        if context.get("dependencies"):
            sections.append(f"Dependencies: {', '.join(context['dependencies'])}")
        
        if context.get("requirements"):
            sections.append("Requirements:")
            for req in context["requirements"]:
                sections.append(f"- {req}")
        
        if context.get("constraints"):
            sections.append("Constraints:")
            for constraint in context["constraints"]:
                sections.append(f"- {constraint}")
        
        if context.get("examples"):
            sections.append("Examples to follow:")
            for example in context["examples"]:
                sections.append(f"- {example}")
        
        return "\n".join(sections)
    
    def get_success_criteria(self) -> List[str]:
        """Get success criteria for validation"""
        return [
            "Code compiles/runs without errors",
            "All files are properly organized",
            "Basic functionality is implemented",
            "Error handling is present"
        ]