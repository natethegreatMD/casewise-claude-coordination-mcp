"""
Task Distribution
Intelligently distributes tasks across Claude sessions
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class TaskDefinition:
    """Definition of a task for a Claude session"""
    name: str
    component: str
    description: str
    dependencies: List[str] = None
    priority: int = 5  # 1-10, higher is more important
    estimated_minutes: int = 30
    required_skills: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.required_skills is None:
            self.required_skills = []


class TaskDistributor:
    """
    Distributes tasks intelligently across sessions
    Handles dependencies, load balancing, and skill matching
    """
    
    def __init__(self):
        self.task_templates = self._load_task_templates()
        self.skill_matrix = self._load_skill_matrix()
    
    def _load_task_templates(self) -> Dict[str, List[TaskDefinition]]:
        """Load predefined task templates"""
        return {
            "todo_app": [
                TaskDefinition(
                    name="api",
                    component="backend",
                    description="Create FastAPI backend with CRUD operations for todos",
                    priority=8,
                    estimated_minutes=45,
                    required_skills=["python", "fastapi", "rest_api"]
                ),
                TaskDefinition(
                    name="frontend",
                    component="frontend", 
                    description="Create React frontend with todo list UI",
                    dependencies=["api"],
                    priority=7,
                    estimated_minutes=45,
                    required_skills=["react", "typescript", "ui"]
                ),
                TaskDefinition(
                    name="tests",
                    component="testing",
                    description="Create comprehensive tests for API and frontend",
                    dependencies=["api", "frontend"],
                    priority=6,
                    estimated_minutes=30,
                    required_skills=["testing", "pytest", "jest"]
                )
            ],
            "auth_system": [
                TaskDefinition(
                    name="jwt_auth",
                    component="backend",
                    description="Implement JWT authentication with FastAPI",
                    priority=9,
                    estimated_minutes=60,
                    required_skills=["python", "fastapi", "security", "jwt"]
                ),
                TaskDefinition(
                    name="user_models",
                    component="backend",
                    description="Create user models and database schema",
                    priority=9,
                    estimated_minutes=30,
                    required_skills=["python", "sqlalchemy", "database"]
                ),
                TaskDefinition(
                    name="login_ui",
                    component="frontend",
                    description="Create login/register UI components",
                    dependencies=["jwt_auth"],
                    priority=7,
                    estimated_minutes=45,
                    required_skills=["react", "typescript", "forms"]
                ),
                TaskDefinition(
                    name="auth_tests",
                    component="testing",
                    description="Test authentication flow end-to-end",
                    dependencies=["jwt_auth", "login_ui"],
                    priority=6,
                    estimated_minutes=45,
                    required_skills=["testing", "security", "integration"]
                )
            ],
            "blog_platform": [
                TaskDefinition(
                    name="post_api",
                    component="backend",
                    description="Create blog post CRUD API with categories and tags",
                    priority=8,
                    estimated_minutes=60,
                    required_skills=["python", "fastapi", "database"]
                ),
                TaskDefinition(
                    name="editor_ui",
                    component="frontend",
                    description="Create rich text editor for blog posts",
                    dependencies=["post_api"],
                    priority=8,
                    estimated_minutes=60,
                    required_skills=["react", "rich_text", "ui"]
                ),
                TaskDefinition(
                    name="reader_ui",
                    component="frontend",
                    description="Create blog reader interface with comments",
                    dependencies=["post_api"],
                    priority=7,
                    estimated_minutes=45,
                    required_skills=["react", "ui", "responsive"]
                ),
                TaskDefinition(
                    name="search",
                    component="backend",
                    description="Implement full-text search for blog posts",
                    dependencies=["post_api"],
                    priority=6,
                    estimated_minutes=45,
                    required_skills=["python", "search", "elasticsearch"]
                )
            ]
        }
    
    def _load_skill_matrix(self) -> Dict[str, Dict[str, int]]:
        """Load skill ratings for different component types"""
        return {
            "frontend": {
                "react": 10,
                "typescript": 9,
                "ui": 10,
                "forms": 8,
                "responsive": 9,
                "rich_text": 7
            },
            "backend": {
                "python": 10,
                "fastapi": 10,
                "database": 9,
                "rest_api": 10,
                "security": 8,
                "jwt": 8,
                "sqlalchemy": 8,
                "search": 7,
                "elasticsearch": 6
            },
            "testing": {
                "testing": 10,
                "pytest": 9,
                "jest": 8,
                "integration": 8,
                "security": 7
            }
        }
    
    def get_workflow_tasks(self, workflow_name: str) -> List[TaskDefinition]:
        """Get tasks for a workflow"""
        return self.task_templates.get(workflow_name, [])
    
    def analyze_dependencies(self, tasks: List[TaskDefinition]) -> Dict[str, Any]:
        """Analyze task dependencies and create execution plan"""
        # Build dependency graph
        dep_graph = {task.name: task.dependencies for task in tasks}
        task_map = {task.name: task for task in tasks}
        
        # Find tasks with no dependencies (can start immediately)
        initial_tasks = [task.name for task in tasks if not task.dependencies]
        
        # Topological sort for execution order
        execution_order = []
        completed = set()
        
        def can_execute(task_name: str) -> bool:
            deps = dep_graph.get(task_name, [])
            return all(dep in completed for dep in deps)
        
        # Build execution phases
        phases = []
        remaining = set(task.name for task in tasks)
        
        while remaining:
            phase = []
            for task_name in list(remaining):
                if can_execute(task_name):
                    phase.append(task_name)
                    remaining.remove(task_name)
            
            if not phase:
                # Circular dependency detected
                raise ValueError(f"Circular dependency detected in tasks: {remaining}")
            
            phases.append(phase)
            completed.update(phase)
        
        return {
            "phases": phases,
            "total_phases": len(phases),
            "parallelism": [len(phase) for phase in phases],
            "critical_path": self._find_critical_path(tasks, dep_graph)
        }
    
    def _find_critical_path(self, tasks: List[TaskDefinition], dep_graph: Dict[str, List[str]]) -> List[str]:
        """Find the critical path (longest dependency chain)"""
        task_map = {task.name: task for task in tasks}
        
        # Calculate earliest start times
        earliest_start = {}
        earliest_finish = {}
        
        # Topological order
        visited = set()
        order = []
        
        def visit(name: str):
            if name in visited:
                return
            visited.add(name)
            for dep in dep_graph.get(name, []):
                visit(dep)
            order.append(name)
        
        for task in tasks:
            visit(task.name)
        
        # Calculate forward pass
        for name in order:
            task = task_map[name]
            deps = dep_graph.get(name, [])
            
            if not deps:
                earliest_start[name] = 0
            else:
                earliest_start[name] = max(earliest_finish.get(dep, 0) for dep in deps)
            
            earliest_finish[name] = earliest_start[name] + task.estimated_minutes
        
        # Find path with maximum duration
        end_times = [(name, earliest_finish[name]) for name in order]
        critical_end = max(end_times, key=lambda x: x[1])[0]
        
        # Trace back critical path
        critical_path = []
        current = critical_end
        
        while current:
            critical_path.append(current)
            deps = dep_graph.get(current, [])
            if not deps:
                break
            
            # Find predecessor on critical path
            current = None
            for dep in deps:
                if earliest_finish.get(dep, 0) == earliest_start.get(critical_path[-1], 0):
                    current = dep
                    break
        
        return list(reversed(critical_path))
    
    def distribute_tasks(
        self,
        tasks: List[TaskDefinition],
        max_parallel: int = 3
    ) -> List[List[Tuple[TaskDefinition, str]]]:
        """
        Distribute tasks across sessions
        
        Returns:
            List of execution batches, each containing (task, prompt) tuples
        """
        analysis = self.analyze_dependencies(tasks)
        task_map = {task.name: task for task in tasks}
        
        batches = []
        
        for phase in analysis["phases"]:
            batch = []
            
            # Sort by priority within phase
            phase_tasks = sorted(
                [task_map[name] for name in phase],
                key=lambda t: t.priority,
                reverse=True
            )
            
            # Create prompts for each task
            for task in phase_tasks[:max_parallel]:
                prompt = self._create_task_prompt(task)
                batch.append((task, prompt))
            
            if batch:
                batches.append(batch)
            
            # Handle remaining tasks in phase if any
            remaining = phase_tasks[max_parallel:]
            while remaining:
                batch = []
                for task in remaining[:max_parallel]:
                    prompt = self._create_task_prompt(task)
                    batch.append((task, prompt))
                batches.append(batch)
                remaining = remaining[max_parallel:]
        
        return batches
    
    def _create_task_prompt(self, task: TaskDefinition) -> str:
        """Create a detailed prompt for a task"""
        prompt = f"""You are a {task.component} specialist working on the '{task.name}' component.

Task: {task.description}

Requirements:
- Create production-quality code
- Follow best practices for {', '.join(task.required_skills)}
- Include appropriate error handling
- Add comments for complex logic
- Create any necessary configuration files

"""
        
        if task.dependencies:
            prompt += f"""Dependencies:
This task depends on: {', '.join(task.dependencies)}
Assume these are already implemented and available.

"""
        
        # Add component-specific instructions
        if task.component == "frontend":
            prompt += """Frontend Guidelines:
- Use React with TypeScript
- Create reusable components
- Use modern hooks and functional components
- Include proper TypeScript types
- Style with CSS modules or styled-components
- Make it responsive and accessible
"""
        
        elif task.component == "backend":
            prompt += """Backend Guidelines:
- Use FastAPI with Python 3.8+
- Include Pydantic models for validation
- Add proper error handling and status codes
- Include OpenAPI documentation
- Follow RESTful conventions
- Use async/await where appropriate
"""
        
        elif task.component == "testing":
            prompt += """Testing Guidelines:
- Write comprehensive unit tests
- Include integration tests where appropriate
- Aim for high code coverage
- Use pytest for Python, Jest for JavaScript
- Include both positive and negative test cases
- Add performance tests if relevant
"""
        
        prompt += f"\nEstimated time: {task.estimated_minutes} minutes"
        prompt += "\n\nBegin implementation now. Create all necessary files in your workspace."
        
        return prompt
    
    def estimate_total_time(self, tasks: List[TaskDefinition]) -> Dict[str, float]:
        """Estimate total execution time"""
        analysis = self.analyze_dependencies(tasks)
        
        # Time for each phase (parallel execution)
        phase_times = []
        task_map = {task.name: task for task in tasks}
        
        for phase in analysis["phases"]:
            phase_tasks = [task_map[name] for name in phase]
            # Maximum time in parallel execution
            phase_time = max(task.estimated_minutes for task in phase_tasks)
            phase_times.append(phase_time)
        
        total_parallel = sum(phase_times)
        total_sequential = sum(task.estimated_minutes for task in tasks)
        
        return {
            "parallel_execution_minutes": total_parallel,
            "sequential_execution_minutes": total_sequential,
            "time_saved_minutes": total_sequential - total_parallel,
            "speedup_factor": total_sequential / total_parallel if total_parallel > 0 else 1
        }