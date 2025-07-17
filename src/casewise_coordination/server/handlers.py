"""
MCP Request Handlers
Handle specific types of requests for the CCC server
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from ..orchestrator import SessionOrchestrator, TaskDistributor
from ..session import SessionStatus
from ..templates import (
    FrontendTemplate, BackendTemplate, TestingTemplate,
    DocumentationTemplate, IntegrationTemplate
)


logger = logging.getLogger(__name__)


class SessionHandler:
    """Handles session-related requests"""
    
    def __init__(self, orchestrator: SessionOrchestrator):
        self.orchestrator = orchestrator
        self.templates = {
            "frontend": FrontendTemplate(),
            "backend": BackendTemplate(),
            "testing": TestingTemplate(),
            "documentation": DocumentationTemplate(),
            "integration": IntegrationTemplate()
        }
    
    async def create_session(
        self,
        task_name: str,
        component: str,
        prompt: str,
        timeout_seconds: int = 1800,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new session with appropriate template"""
        context = context or {}
        
        # Get template if available
        template = self.templates.get(component)
        
        if template:
            # Use template to enhance prompt
            enhanced_prompt = template.create_prompt(prompt, context)
            env_vars = template.get_env_vars()
            
            # Prepare workspace
            session_id = f"ccc-{task_name}-{component}-pending"
            workspace = self.orchestrator.workspace_root / "sessions" / session_id
            template.prepare_workspace(workspace)
            
            # Add setup script if needed
            setup = template.get_setup_script()
            if setup:
                enhanced_prompt = f"{setup}\n\n{enhanced_prompt}"
        else:
            # Use raw prompt
            enhanced_prompt = prompt
            env_vars = {}
        
        # Create session through orchestrator
        session_id = self.orchestrator.create_session(
            task_name=task_name,
            component=component,
            task_prompt=enhanced_prompt,
            input_data=context,
            timeout_seconds=timeout_seconds,
            env_vars=env_vars
        )
        
        logger.info(f"Created session {session_id} with {component} template")
        return session_id
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get detailed session status"""
        session = self.orchestrator.sessions.get(session_id)
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        state = session.get_state()
        
        return {
            "session_id": session_id,
            "status": state.status.value,
            "progress_percent": state.progress_percent,
            "current_activity": state.current_activity,
            "files_created": state.files_created,
            "execution_time": state.execution_time_seconds,
            "error_count": state.error_count,
            "last_error": state.last_error,
            "workspace": str(state.workspace)
        }
    
    async def terminate_session(self, session_id: str, force: bool = False):
        """Terminate a session"""
        session = self.orchestrator.sessions.get(session_id)
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.terminate(force=force)
        logger.info(f"Terminated session {session_id} (force={force})")
    
    async def list_sessions(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all sessions with optional filtering"""
        sessions = []
        
        for session_id, session in self.orchestrator.sessions.items():
            state = session.get_state()
            
            # Apply filter if specified
            if status_filter and state.status.value != status_filter:
                continue
            
            sessions.append({
                "session_id": session_id,
                "task_name": state.task_name,
                "component": state.component,
                "status": state.status.value,
                "progress": state.progress_percent,
                "created_at": state.created_at.isoformat(),
                "execution_time": state.execution_time_seconds
            })
        
        return sessions
    
    async def validate_session_output(self, session_id: str) -> Dict[str, Any]:
        """Validate session output using template"""
        session = self.orchestrator.sessions.get(session_id)
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        state = session.get_state()
        template = self.templates.get(state.component)
        
        if template:
            return template.validate_output(state.workspace)
        else:
            # Basic validation
            files = session.get_workspace_files()
            return {
                "success": len(files) > 0,
                "files_found": [str(f.relative_to(state.workspace)) for f in files],
                "warnings": ["No template available for validation"]
            }


class OrchestratorHandler:
    """Handles orchestrator-level requests"""
    
    def __init__(self, orchestrator: SessionOrchestrator):
        self.orchestrator = orchestrator
        self.task_distributor = TaskDistributor()
    
    async def execute_workflow(
        self,
        workflow_name: str,
        workflow_type: str = "todo_app",
        parallel: bool = True
    ) -> Dict[str, Any]:
        """Execute a complete workflow"""
        # Get workflow tasks
        task_definitions = self.task_distributor.get_workflow_tasks(workflow_type)
        
        if not task_definitions:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Analyze dependencies
        analysis = self.task_distributor.analyze_dependencies(task_definitions)
        
        # Estimate time
        time_estimate = self.task_distributor.estimate_total_time(task_definitions)
        
        logger.info(f"Starting workflow '{workflow_name}' with {len(task_definitions)} tasks")
        logger.info(f"Estimated time: {time_estimate['parallel_execution_minutes']} minutes")
        
        # Distribute tasks
        batches = self.task_distributor.distribute_tasks(
            task_definitions,
            max_parallel=self.orchestrator.max_parallel_sessions
        )
        
        # Convert to orchestrator format
        tasks = []
        for batch in batches:
            for task_def, prompt in batch:
                tasks.append({
                    "name": task_def.name,
                    "component": task_def.component,
                    "prompt": prompt,
                    "timeout": task_def.estimated_minutes * 60,
                    "input": {
                        "dependencies": task_def.dependencies,
                        "required_skills": task_def.required_skills
                    }
                })
        
        # Execute through orchestrator
        result = self.orchestrator.execute_workflow(
            workflow_name=workflow_name,
            tasks=tasks,
            parallel=parallel
        )
        
        # Add analysis to result
        result["analysis"] = analysis
        result["time_estimate"] = time_estimate
        
        return result
    
    async def get_workflow_templates(self) -> Dict[str, Any]:
        """Get available workflow templates"""
        templates = {}
        
        for name, tasks in self.task_distributor.task_templates.items():
            templates[name] = {
                "task_count": len(tasks),
                "components": list(set(t.component for t in tasks)),
                "estimated_minutes": sum(t.estimated_minutes for t in tasks),
                "tasks": [
                    {
                        "name": t.name,
                        "component": t.component,
                        "description": t.description,
                        "dependencies": t.dependencies
                    }
                    for t in tasks
                ]
            }
        
        return templates
    
    async def analyze_workflow(self, workflow_type: str) -> Dict[str, Any]:
        """Analyze a workflow before execution"""
        task_definitions = self.task_distributor.get_workflow_tasks(workflow_type)
        
        if not task_definitions:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        analysis = self.task_distributor.analyze_dependencies(task_definitions)
        time_estimate = self.task_distributor.estimate_total_time(task_definitions)
        
        return {
            "workflow_type": workflow_type,
            "task_count": len(task_definitions),
            "dependency_analysis": analysis,
            "time_estimate": time_estimate,
            "skill_requirements": list(set(
                skill 
                for task in task_definitions 
                for skill in task.required_skills
            ))
        }