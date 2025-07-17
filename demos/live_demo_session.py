#!/usr/bin/env python3
"""
Live demonstration: Spawn a Claude session RIGHT NOW and show what it does
"""

import subprocess
import time
from pathlib import Path

def spawn_claude_session_live():
    """Spawn a Claude session and show real-time what it's doing"""
    
    workspace = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/live_claude_demo")
    workspace.mkdir(exist_ok=True)
    
    print("🎬 LIVE DEMO: Spawning Claude Code Session")
    print("=" * 60)
    print("You won't see a new terminal window, but I'm controlling Claude behind the scenes!")
    print(f"Workspace: {workspace}")
    print("=" * 60)
    
    # Task for the live session
    task = """You are Claude session #42 being controlled by CCC. Please:

1. Create 'hello_from_session_42.py' that prints your session info and the current time

2. Create 'work_progress.txt' that shows:
   - Your session ID (#42)
   - What you're doing right now
   - A joke about being controlled by CCC

3. Run the Python script you created

Show that you're a real Claude session doing real work!"""
    
    print(f"\n🎯 TASK FOR CLAUDE SESSION #42:")
    print(task)
    print("\n" + "=" * 60)
    
    print("\n🚀 SPAWNING CLAUDE SESSION NOW...")
    print("⏳ Claude is working behind the scenes...\n")
    
    # Spawn Claude with the task
    start_time = time.time()
    
    result = subprocess.run(
        ["claude", "--print", "--continue", "--dangerously-skip-permissions", task],
        cwd=str(workspace),
        capture_output=True,
        text=True,
        env={'CLAUDE_SESSION_ID': '42'}  # Pass session ID via env
    )
    
    elapsed = time.time() - start_time
    
    print(f"✅ CLAUDE SESSION COMPLETED in {elapsed:.2f} seconds!")
    print("\n📥 CLAUDE'S RESPONSE:")
    print("-" * 60)
    if result.stdout:
        print(result.stdout)
    print("-" * 60)
    
    # Show what Claude created
    print("\n📂 FILES CREATED BY CLAUDE SESSION #42:")
    for file in sorted(workspace.glob("*")):
        print(f"\n📄 {file.name}:")
        print("─" * 40)
        if file.suffix in ['.py', '.txt'] and file.stat().st_size < 1000:
            print(file.read_text())
        print("─" * 40)
    
    # Run the Python script if it exists
    py_file = workspace / "hello_from_session_42.py"
    if py_file.exists():
        print("\n🏃 RUNNING THE SCRIPT CLAUDE CREATED:")
        run_result = subprocess.run(
            ["python", str(py_file)],
            capture_output=True,
            text=True
        )
        print(run_result.stdout)
    
    return workspace


if __name__ == "__main__":
    workspace = spawn_claude_session_live()
    
    print("\n" + "=" * 60)
    print("🎭 WHAT JUST HAPPENED:")
    print("=" * 60)
    print("1. I spawned a real Claude Code session (subprocess)")
    print("2. Claude ran in the background (no visible terminal)")
    print("3. Claude created files and wrote code")
    print("4. I collected all the outputs")
    print(f"5. Everything happened in: {workspace}")
    print("\nThis is how CCC will control multiple Claude sessions!")
    print("Each doing different parts of your CasewiseMD work!")
    print("=" * 60)