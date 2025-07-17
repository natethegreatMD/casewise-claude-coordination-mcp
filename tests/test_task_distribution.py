"""
Test task distribution functionality
"""

import unittest
from datetime import datetime, timedelta

from casewise_coordination.orchestrator.task_distribution import (
    TaskDistributor, Task
)


class TestTaskDistribution(unittest.TestCase):
    """Test the TaskDistributor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.distributor = TaskDistributor()
    
    def test_task_creation(self):
        """Test creating tasks"""
        task = Task(
            name="Build API",
            component="backend",
            description="Create REST API",
            estimated_minutes=30,
            dependencies=[]
        )
        
        self.assertEqual(task.name, "Build API")
        self.assertEqual(task.component, "backend")
        self.assertEqual(task.estimated_minutes, 30)
        self.assertEqual(len(task.dependencies), 0)
    
    def test_dependency_analysis(self):
        """Test dependency analysis"""
        tasks = [
            Task("task1", "backend", "Task 1", 10, []),
            Task("task2", "frontend", "Task 2", 15, ["task1"]),
            Task("task3", "testing", "Task 3", 20, ["task1", "task2"]),
            Task("task4", "docs", "Task 4", 5, ["task3"]),
        ]
        
        analysis = self.distributor.analyze_dependencies(tasks)
        
        # Check phases
        self.assertEqual(len(analysis['phases']), 4)
        self.assertEqual(analysis['phases'][0], ["task1"])
        self.assertEqual(analysis['phases'][1], ["task2"])
        self.assertEqual(analysis['phases'][2], ["task3"])
        self.assertEqual(analysis['phases'][3], ["task4"])
        
        # Check dependency graph
        self.assertIn("task1", analysis['dependency_graph'])
        self.assertIn("task2", analysis['dependency_graph']["task1"])
    
    def test_parallel_task_detection(self):
        """Test detection of parallel tasks"""
        tasks = [
            Task("api", "backend", "API", 30, []),
            Task("ui", "frontend", "UI", 30, []),
            Task("docs", "documentation", "Docs", 15, []),
            Task("tests", "testing", "Tests", 20, ["api", "ui"]),
        ]
        
        analysis = self.distributor.analyze_dependencies(tasks)
        
        # First phase should have 3 parallel tasks
        self.assertEqual(len(analysis['phases'][0]), 3)
        self.assertIn("api", analysis['phases'][0])
        self.assertIn("ui", analysis['phases'][0])
        self.assertIn("docs", analysis['phases'][0])
        
        # Second phase should have 1 task
        self.assertEqual(len(analysis['phases'][1]), 1)
        self.assertEqual(analysis['phases'][1][0], "tests")
    
    def test_time_estimation(self):
        """Test time estimation"""
        tasks = [
            Task("task1", "backend", "T1", 30, []),
            Task("task2", "frontend", "T2", 45, []),
            Task("task3", "testing", "T3", 20, ["task1", "task2"]),
        ]
        
        time_est = self.distributor.estimate_total_time(tasks)
        
        # Sequential: 30 + 45 + 20 = 95
        self.assertEqual(time_est['sequential_execution_minutes'], 95)
        
        # Parallel: max(30, 45) + 20 = 65
        self.assertEqual(time_est['parallel_execution_minutes'], 65)
        
        # Time saved: 95 - 65 = 30
        self.assertEqual(time_est['time_saved_minutes'], 30)
    
    def test_task_templates(self):
        """Test predefined task templates"""
        # Check todo_app template
        todo_tasks = self.distributor.task_templates['todo_app']
        self.assertTrue(len(todo_tasks) > 0)
        
        # Should have backend, frontend, and testing tasks
        components = [t.component for t in todo_tasks]
        self.assertIn('backend', components)
        self.assertIn('frontend', components)
        self.assertIn('testing', components)
        
        # Check auth_system template
        auth_tasks = self.distributor.task_templates['auth_system']
        self.assertTrue(len(auth_tasks) > 0)
        
        # Check blog_platform template
        blog_tasks = self.distributor.task_templates['blog_platform']
        self.assertTrue(len(blog_tasks) > 0)
    
    def test_distribute_to_sessions(self):
        """Test distributing tasks to sessions"""
        tasks = self.distributor.task_templates['todo_app']
        
        # Distribute with max 2 parallel
        distribution = self.distributor.distribute_tasks(tasks, max_parallel=2)
        
        self.assertIsInstance(distribution, list)
        self.assertTrue(len(distribution) > 0)
        
        # Each phase should have max 2 tasks
        for phase in distribution:
            self.assertLessEqual(len(phase['tasks']), 2)
    
    def test_circular_dependency_detection(self):
        """Test circular dependency detection"""
        tasks = [
            Task("task1", "backend", "T1", 10, ["task3"]),
            Task("task2", "frontend", "T2", 10, ["task1"]),
            Task("task3", "testing", "T3", 10, ["task2"]),
        ]
        
        # Should handle circular dependencies gracefully
        with self.assertRaises(Exception):
            self.distributor.analyze_dependencies(tasks)
    
    def test_task_priority(self):
        """Test task prioritization"""
        tasks = [
            Task("critical", "backend", "Critical", 10, [], priority="high"),
            Task("normal", "frontend", "Normal", 10, [], priority="medium"),
            Task("optional", "docs", "Optional", 10, [], priority="low"),
        ]
        
        # Distributor should consider priority
        sorted_tasks = self.distributor.sort_by_priority(tasks)
        
        self.assertEqual(sorted_tasks[0].name, "critical")
        self.assertEqual(sorted_tasks[-1].name, "optional")
    
    def test_resource_constraints(self):
        """Test handling resource constraints"""
        tasks = [
            Task("memory_heavy", "backend", "Heavy", 30, [], resources={"memory": "high"}),
            Task("cpu_heavy", "testing", "CPU", 20, [], resources={"cpu": "high"}),
            Task("light", "docs", "Light", 10, [], resources={}),
        ]
        
        # Should consider resource constraints
        distribution = self.distributor.distribute_with_resources(
            tasks, 
            max_memory_tasks=1,
            max_cpu_tasks=1
        )
        
        # Heavy tasks shouldn't run in parallel
        for phase in distribution:
            memory_tasks = [t for t in phase if t.resources.get("memory") == "high"]
            cpu_tasks = [t for t in phase if t.resources.get("cpu") == "high"]
            self.assertLessEqual(len(memory_tasks), 1)
            self.assertLessEqual(len(cpu_tasks), 1)


if __name__ == "__main__":
    unittest.main()