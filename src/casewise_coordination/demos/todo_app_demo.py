"""
Todo App Demo
Demonstrates CCC by building a complete Todo application
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, Any
import logging

from ..orchestrator import SessionOrchestrator
from ..tools.notifications import (
    notify_workflow_completed,
    notify_session_started,
    notify_session_completed
)


logger = logging.getLogger(__name__)


class TodoAppDemo:
    """
    Demonstrates CCC capabilities by building a Todo app
    with frontend, backend, and tests in parallel
    """
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.demo_workspace = self.workspace_root / "todo_app_demo"
        self.demo_workspace.mkdir(parents=True, exist_ok=True)
        
        # Initialize orchestrator with notification callback
        self.orchestrator = SessionOrchestrator(
            workspace_root=self.demo_workspace,
            max_parallel_sessions=3,
            dangerous_permissions=True,
            notification_callback=self._handle_notification
        )
        
        self.start_time = None
        self.sessions_created = []
    
    def _handle_notification(self, level: str, message: str):
        """Handle orchestrator notifications"""
        logger.info(f"[{level.upper()}] {message}")
        
        # Parse session events
        if "Started session" in message:
            session_id = message.split()[2]
            task = message.split("for")[1].strip() if "for" in message else "task"
            notify_session_started(session_id, task)
        
        elif "completed successfully" in message:
            session_id = message.split()[1]
            notify_session_completed(session_id, success=True)
        
        elif "failed" in message and "Session" in message:
            session_id = message.split()[1]
            notify_session_completed(session_id, success=False)
    
    async def run(self) -> Dict[str, Any]:
        """Run the Todo app demo"""
        logger.info("Starting Todo App Demo")
        self.start_time = time.time()
        
        # Define the three parallel tasks
        tasks = [
            {
                "name": "backend",
                "component": "backend",
                "prompt": self._get_backend_prompt(),
                "timeout": 2400  # 40 minutes
            },
            {
                "name": "frontend",
                "component": "frontend",
                "prompt": self._get_frontend_prompt(),
                "timeout": 2400
            },
            {
                "name": "tests",
                "component": "testing",
                "prompt": self._get_testing_prompt(),
                "timeout": 1800  # 30 minutes
            }
        ]
        
        try:
            # Execute workflow
            result = self.orchestrator.execute_workflow(
                workflow_name="Todo App Demo",
                tasks=tasks,
                parallel=True
            )
            
            # Calculate duration
            duration = time.time() - self.start_time
            duration_minutes = duration / 60
            
            # Send completion notification
            success = result.get("success", False)
            notify_workflow_completed("Todo App Demo", success, duration_minutes)
            
            # Consolidate results
            if success:
                consolidated = self.orchestrator.consolidate_results(
                    session_ids=[t["session_id"] for t in result["tasks"].values()],
                    output_dir=self.demo_workspace / "final_app"
                )
                result["consolidated"] = consolidated
            
            result["duration_minutes"] = duration_minutes
            
            # Generate summary
            result["summary"] = self._generate_summary(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise
        
        finally:
            # Save orchestrator state
            self.orchestrator.save_state()
    
    def _get_backend_prompt(self) -> str:
        """Get backend task prompt"""
        return """Create a complete Todo API backend with FastAPI.

Requirements:
1. FastAPI application with proper structure
2. Todo model with: id, title, description, completed, created_at, updated_at
3. CRUD endpoints:
   - GET /todos - List all todos with optional filtering
   - GET /todos/{id} - Get single todo
   - POST /todos - Create new todo
   - PUT /todos/{id} - Update todo
   - DELETE /todos/{id} - Delete todo
4. In-memory storage (dict) for simplicity
5. Proper error handling and validation
6. CORS enabled for frontend access
7. Health check endpoint at /health
8. OpenAPI documentation

Create a complete, working API that can be run with:
uvicorn app.main:app --reload

Include a README with API documentation and example requests."""
    
    def _get_frontend_prompt(self) -> str:
        """Get frontend task prompt"""
        return """Create a complete Todo application frontend with React and TypeScript.

Requirements:
1. Modern React app with TypeScript and Vite
2. Clean, responsive UI with a pleasant design
3. Features:
   - Display list of todos
   - Add new todo with title and description
   - Mark todos as complete/incomplete
   - Edit existing todos
   - Delete todos
   - Filter by status (all/active/completed)
4. Use fetch or axios to connect to backend API at http://localhost:8000
5. Proper loading and error states
6. Use modern React patterns (hooks, functional components)
7. Basic styling with CSS modules or styled-components

The app should be production-ready and run with:
npm run dev

Include a README with setup instructions and screenshots descriptions."""
    
    def _get_testing_prompt(self) -> str:
        """Get testing task prompt"""
        return """Create comprehensive tests for both the Todo API backend and React frontend.

Note: You're working in parallel with backend and frontend sessions. 
Assume standard Todo app structure.

Requirements:

Backend Tests (pytest):
1. Test all CRUD operations
2. Test validation and error cases
3. Test edge cases (empty lists, invalid IDs, etc.)
4. Use pytest fixtures for test data
5. Aim for >80% coverage

Frontend Tests (Jest + React Testing Library):
1. Component rendering tests
2. User interaction tests (add, edit, delete)
3. API integration tests (mocked)
4. Error handling tests
5. Accessibility tests

Create well-organized test suites that can be run with:
- Backend: pytest
- Frontend: npm test

Include a test report summarizing coverage and recommendations."""
    
    def _generate_summary(self, result: Dict[str, Any]) -> str:
        """Generate a summary of the demo results"""
        summary = []
        summary.append("=" * 60)
        summary.append("TODO APP DEMO SUMMARY")
        summary.append("=" * 60)
        
        summary.append(f"\nDuration: {result['duration_minutes']:.1f} minutes")
        summary.append(f"Success: {'✅ Yes' if result['success'] else '❌ No'}")
        
        summary.append("\nSessions:")
        for task_name, task_result in result["tasks"].items():
            status = "✅" if task_result["success"] else "❌"
            summary.append(f"  {status} {task_name}: {task_result['session_id']}")
            summary.append(f"     Files created: {len(task_result['files_created'])}")
            summary.append(f"     Execution time: {task_result['execution_time']:.1f}s")
        
        if result.get("consolidated"):
            summary.append(f"\nConsolidated output: {result['consolidated']['output_dir']}")
            summary.append(f"Total files collected: {len(result['consolidated']['files_collected'])}")
        
        summary.append("\nNext steps:")
        summary.append("1. cd to the final_app directory")
        summary.append("2. Start the backend: cd backend && uvicorn app.main:app")
        summary.append("3. Start the frontend: cd frontend && npm install && npm run dev")
        summary.append("4. Run tests: cd tests && pytest (backend) or npm test (frontend)")
        
        return "\n".join(summary)
    
    def cleanup(self, keep_files: bool = True):
        """Cleanup demo resources"""
        self.orchestrator.terminate_all()
        
        if not keep_files:
            import shutil
            shutil.rmtree(self.demo_workspace)
            logger.info("Cleaned up demo workspace")