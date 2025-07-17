#!/usr/bin/env python3
"""
CCC Session Control Demonstration
Shows how to spawn and control separate Claude Code sessions
"""

import subprocess
import os
import time
import threading
import queue
from pathlib import Path

class ClaudeSessionController:
    """Controls a Claude Code session as a subprocess"""
    
    def __init__(self, session_id, workspace_path):
        self.session_id = session_id
        self.workspace = Path(workspace_path)
        self.workspace.mkdir(exist_ok=True)
        self.process = None
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        
    def start_session(self):
        """Start a new Claude Code session in subprocess"""
        print(f"🚀 Starting Claude session: {self.session_id}")
        print(f"📁 Workspace: {self.workspace}")
        
        # Start Claude in interactive mode
        self.process = subprocess.Popen(
            ["claude", "--continue"],  # Skip welcome message
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.workspace),
            bufsize=1
        )
        
        # Start output reader thread
        self.output_thread = threading.Thread(target=self._read_output)
        self.output_thread.daemon = True
        self.output_thread.start()
        
        time.sleep(2)  # Give Claude time to start
        print(f"✅ Session {self.session_id} started (PID: {self.process.pid})")
        
    def _read_output(self):
        """Read output from Claude session"""
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line:
                self.output_queue.put(line.strip())
    
    def send_command(self, command):
        """Send a command to the Claude session"""
        if self.process and self.process.poll() is None:
            print(f"\n📤 Sending to {self.session_id}: {command}")
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            time.sleep(1)  # Give time to process
            
            # Collect output
            output_lines = []
            while not self.output_queue.empty():
                output_lines.append(self.output_queue.get())
            
            if output_lines:
                print(f"📥 Response from {self.session_id}:")
                for line in output_lines:
                    print(f"   {line}")
            
            return output_lines
    
    def create_proof_file(self):
        """Have the session create a proof file"""
        proof_content = f"""=== CCC CONTROLLED SESSION PROOF ===
Session ID: {self.session_id}
Created: {time.strftime('%Y-%m-%d %H:%M:%S')}
PID: {self.process.pid if self.process else 'N/A'}

This file was created by a Claude Code session
that is being controlled by the CCC orchestrator.

The orchestrator can:
1. Spawn multiple Claude sessions
2. Send them commands
3. Monitor their outputs
4. Coordinate their work

This is session {self.session_id} reporting success!
=== END PROOF ==="""
        
        command = f'Create a file called proof_{self.session_id}.txt with this exact content:\n{proof_content}'
        return self.send_command(command)
    
    def stop_session(self):
        """Stop the Claude session"""
        if self.process:
            print(f"\n🛑 Stopping session {self.session_id}")
            self.process.terminate()
            self.process.wait()
            print(f"✅ Session {self.session_id} stopped")


def demonstrate_session_control():
    """Demonstrate controlling multiple Claude sessions"""
    print("=== CCC Session Control Demonstration ===\n")
    
    # Create workspace for our test
    base_workspace = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/ccc_demo")
    base_workspace.mkdir(exist_ok=True)
    
    # Create controller for a test session
    controller = ClaudeSessionController(
        "test-001",
        base_workspace / "session_test_001"
    )
    
    try:
        # Start the session
        controller.start_session()
        
        # Send some commands
        print("\n📋 Sending test commands to controlled session...")
        
        # Command 1: Create a simple file
        controller.send_command("Create a file called hello.txt that contains 'Hello from CCC-controlled Claude session!'")
        time.sleep(3)
        
        # Command 2: Create a Python script
        controller.send_command("Create a Python script called demo.py that prints the first 5 prime numbers")
        time.sleep(3)
        
        # Command 3: Create the proof file
        controller.create_proof_file()
        time.sleep(3)
        
        # Check what files were created
        print("\n📂 Checking created files:")
        created_files = list(controller.workspace.glob("*"))
        for f in created_files:
            print(f"  ✓ {f.name}")
            if f.suffix == ".txt":
                print(f"    Content: {f.read_text()[:100]}...")
        
    finally:
        # Stop the session
        controller.stop_session()
    
    print("\n✨ Demonstration complete!")
    print("This proves CCC can spawn and control separate Claude Code sessions.")


def demonstrate_parallel_sessions():
    """Advanced demo: Control multiple sessions in parallel"""
    print("\n=== Advanced: Parallel Session Control ===\n")
    
    base_workspace = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/ccc_parallel_demo")
    base_workspace.mkdir(exist_ok=True)
    
    # Create multiple session controllers
    sessions = []
    for i in range(3):
        controller = ClaudeSessionController(
            f"parallel-{i:03d}",
            base_workspace / f"session_{i:03d}"
        )
        sessions.append(controller)
    
    try:
        # Start all sessions
        print("🚀 Starting 3 parallel Claude sessions...")
        for session in sessions:
            session.start_session()
            time.sleep(1)
        
        # Give each session a different task
        tasks = [
            "Create a file called task.txt with 'I am session 0 working on frontend tasks'",
            "Create a file called task.txt with 'I am session 1 working on backend tasks'", 
            "Create a file called task.txt with 'I am session 2 working on testing tasks'"
        ]
        
        print("\n📋 Sending different tasks to each session...")
        for session, task in zip(sessions, tasks):
            session.send_command(task)
            time.sleep(2)
        
        # Check results
        print("\n📊 Results from parallel sessions:")
        for session in sessions:
            task_file = session.workspace / "task.txt"
            if task_file.exists():
                print(f"  ✓ Session {session.session_id}: {task_file.read_text().strip()}")
        
    finally:
        # Stop all sessions
        print("\n🛑 Stopping all sessions...")
        for session in sessions:
            session.stop_session()
    
    print("\n✨ Parallel control demonstration complete!")


if __name__ == "__main__":
    # Simple demonstration
    demonstrate_session_control()
    
    # Advanced parallel demonstration
    # demonstrate_parallel_sessions()  # Uncomment to run