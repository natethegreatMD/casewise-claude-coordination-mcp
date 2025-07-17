#!/usr/bin/env python3
"""
Live monitoring of Claude sessions - watch them work in real-time!
"""

import subprocess
import threading
import time
import sys
from pathlib import Path
from datetime import datetime

class LiveClaudeMonitor:
    """Monitor Claude sessions in real-time"""
    
    def __init__(self, session_id, workspace):
        self.session_id = session_id
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)
        self.log_file = self.workspace / "session_live_log.txt"
        self.process = None
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] Session {self.session_id}: {message}"
        print(log_line)
        with open(self.log_file, "a") as f:
            f.write(log_line + "\n")
    
    def monitor_files(self):
        """Monitor workspace for file changes"""
        known_files = set()
        
        while self.process and self.process.poll() is None:
            current_files = set(self.workspace.glob("*"))
            new_files = current_files - known_files
            
            for new_file in new_files:
                self.log(f"📄 Created file: {new_file.name}")
                if new_file.suffix in ['.txt', '.py'] and new_file.stat().st_size < 500:
                    content = new_file.read_text()
                    self.log(f"   Content preview: {content[:100]}...")
            
            known_files = current_files
            time.sleep(0.5)
    
    def run_with_live_output(self, task):
        """Run Claude and stream output live"""
        self.log("🚀 Starting Claude session...")
        
        # Start Claude process
        self.process = subprocess.Popen(
            ["claude", "--print", "--continue", "--dangerously-skip-permissions", task],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.workspace),
            bufsize=1
        )
        
        self.log(f"✅ Process started (PID: {self.process.pid})")
        
        # Start file monitor in background
        monitor_thread = threading.Thread(target=self.monitor_files)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Read output line by line
        self.log("📥 Claude output:")
        for line in iter(self.process.stdout.readline, ''):
            if line:
                print(f"    │ {line.rstrip()}")
        
        self.process.wait()
        self.log(f"✅ Session completed (exit code: {self.process.returncode})")


def demo_live_monitoring():
    """Demo: Watch Claude work in real-time"""
    
    print("🎬 LIVE CLAUDE MONITORING DEMO")
    print("=" * 60)
    print("Watch as Claude works in real-time!")
    print("=" * 60)
    
    workspace = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/live_monitor_workspace")
    workspace.mkdir(exist_ok=True)
    
    # Task that will show progress
    task = """Please do these tasks one by one, creating each file separately:

1. First, create 'step1_starting.txt' with: "Starting work on CCC demo task..."

2. Then create 'fibonacci.py' with a function to calculate Fibonacci numbers

3. Create 'step2_progress.txt' with: "Fibonacci function created, moving to next task..."

4. Create 'prime_checker.py' with a function to check if a number is prime

5. Finally, create 'step3_complete.txt' with: "All tasks completed successfully!"

Take your time with each step."""
    
    monitor = LiveClaudeMonitor("live-001", workspace / "session_001")
    
    print(f"\n📋 Task for live monitoring:")
    print(task)
    print("\n" + "=" * 60)
    print("🔴 MONITORING LIVE - Watch below:")
    print("=" * 60 + "\n")
    
    monitor.run_with_live_output(task)
    
    print("\n" + "=" * 60)
    print("✅ Live monitoring complete!")
    print(f"📁 Check workspace: {monitor.workspace}")
    print(f"📄 Full log: {monitor.log_file}")


def demo_parallel_live_monitoring():
    """Advanced: Monitor multiple Claude sessions at once"""
    
    print("\n\n🎭 PARALLEL LIVE MONITORING (Multiple Sessions)")
    print("=" * 60)
    
    base = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/parallel_monitor_demo")
    base.mkdir(exist_ok=True)
    
    # Create a dashboard file that updates
    dashboard = base / "live_dashboard.txt"
    
    def update_dashboard(sessions_info):
        content = f"""CCC LIVE DASHBOARD - {datetime.now().strftime('%H:%M:%S')}
=====================================

Active Claude Sessions:
"""
        for info in sessions_info:
            content += f"\n{info}"
        
        dashboard.write_text(content)
        print(f"\n📊 Dashboard updated: {dashboard}")
    
    # Simulate what parallel monitoring would look like
    sessions_info = [
        "🟢 Session frontend-001: Creating React components...",
        "🟢 Session backend-001: Building FastAPI endpoints...",
        "🟡 Session testing-001: Writing test cases...",
        "⚪ Session docs-001: Waiting for tasks..."
    ]
    
    update_dashboard(sessions_info)
    
    print("\nIn the full CCC system, you could:")
    print("1. Watch live logs from all sessions")
    print("2. See files being created in real-time")
    print("3. Monitor progress dashboards")
    print("4. Get notifications when tasks complete")
    
    return dashboard


if __name__ == "__main__":
    # Run live monitoring demo
    demo_live_monitoring()
    
    # Show parallel monitoring concept
    dashboard = demo_parallel_live_monitoring()
    
    print("\n\n💡 LIVE MONITORING OPTIONS:")
    print("=" * 60)
    print("1. Stream Claude output line-by-line ✅")
    print("2. Watch files being created in real-time ✅")
    print("3. Live progress dashboard ✅")
    print("4. Parallel session monitoring ✅")
    print("\nYou can't see the actual terminal, but you CAN watch everything happen!")