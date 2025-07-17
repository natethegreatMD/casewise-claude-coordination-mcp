#!/usr/bin/env python3
"""
Spawn 3 Claude sessions in parallel for live monitoring demo
"""

import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

def spawn_claude_session(session_id, role, task, workspace):
    """Spawn a single Claude session with logging"""
    
    workspace = Path(workspace)
    workspace.mkdir(exist_ok=True)
    
    log_file = workspace / "session_activity_log.txt"
    
    def log(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {msg}\n"
        print(f"[{session_id}] {msg}")
        with open(log_file, "a") as f:
            f.write(log_line)
    
    log(f"🚀 Starting {role} session...")
    log(f"📁 Workspace: {workspace}")
    
    # Run Claude with the task
    start_time = time.time()
    
    result = subprocess.run(
        ["claude", "--print", "--continue", "--dangerously-skip-permissions", task],
        cwd=str(workspace),
        capture_output=True,
        text=True
    )
    
    elapsed = time.time() - start_time
    
    log(f"✅ Completed in {elapsed:.1f} seconds!")
    log(f"📊 Exit code: {result.returncode}")
    
    # Log what was created
    files_created = list(workspace.glob("*.py")) + list(workspace.glob("*.txt")) + list(workspace.glob("*.json"))
    if files_created:
        log(f"📄 Files created: {[f.name for f in files_created]}")
    
    return result


def run_parallel_sessions():
    """Run 3 Claude sessions in parallel"""
    
    print("🎭 SPAWNING 3 CLAUDE SESSIONS IN PARALLEL")
    print("=" * 60)
    print("Watch your monitoring terminal to see them all working!")
    print("=" * 60 + "\n")
    
    base = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/parallel_demo_live")
    base.mkdir(exist_ok=True)
    
    # Define 3 different sessions with different tasks
    sessions = [
        {
            "id": "frontend-01",
            "role": "React Frontend Specialist",
            "workspace": base / "session_frontend",
            "task": """You are a React frontend specialist (Session frontend-01).

Create these files to show you're working:

1. Create 'frontend_status.txt' with: "Frontend session active and building UI components..."

2. Create 'Button.tsx' with a simple React button component

3. Create 'LoginForm.tsx' with a basic login form component

4. Create 'frontend_complete.txt' with: "Frontend components ready! - Session frontend-01"

Work at a normal pace, creating each file one at a time."""
        },
        {
            "id": "backend-02", 
            "role": "FastAPI Backend Specialist",
            "workspace": base / "session_backend",
            "task": """You are a FastAPI backend specialist (Session backend-02).

Create these files to show you're working:

1. Create 'backend_status.txt' with: "Backend session active and building API endpoints..."

2. Create 'auth_endpoints.py' with basic JWT authentication endpoints

3. Create 'user_models.py' with Pydantic models for users

4. Create 'backend_complete.txt' with: "API endpoints ready! - Session backend-02"

Work at a normal pace, creating each file one at a time."""
        },
        {
            "id": "testing-03",
            "role": "Testing Specialist", 
            "workspace": base / "session_testing",
            "task": """You are a testing specialist (Session testing-03).

Create these files to show you're working:

1. Create 'testing_status.txt' with: "Testing session active and writing test cases..."

2. Create 'test_auth.py' with basic authentication tests

3. Create 'test_user_api.py' with user API endpoint tests

4. Create 'testing_complete.txt' with: "Test suite ready! - Session testing-03"

Work at a normal pace, creating each file one at a time."""
        }
    ]
    
    # Create dashboard
    dashboard = base / "live_dashboard.txt"
    
    def update_dashboard(status):
        content = f"""CCC LIVE DASHBOARD
Time: {datetime.now().strftime('%H:%M:%S')}
{'=' * 40}

Active Sessions:
{status}

Watch the magic happen!
"""
        dashboard.write_text(content)
    
    # Initial dashboard
    update_dashboard("🟡 All sessions starting...")
    
    # Start all sessions in parallel threads
    threads = []
    print("🚀 Launching all 3 sessions NOW...\n")
    
    for session in sessions:
        thread = threading.Thread(
            target=spawn_claude_session,
            args=(session["id"], session["role"], session["task"], session["workspace"])
        )
        thread.start()
        threads.append(thread)
        print(f"✓ Started {session['id']} ({session['role']})")
        time.sleep(0.5)  # Slight stagger to make monitoring easier
    
    print("\n📊 All sessions running! Check your monitor terminal!")
    print("You should see activity from all 3 sessions...\n")
    
    # Update dashboard while sessions run
    start_time = time.time()
    while any(t.is_alive() for t in threads):
        elapsed = int(time.time() - start_time)
        status_lines = []
        
        for i, session in enumerate(sessions):
            if threads[i].is_alive():
                status_lines.append(f"🟢 {session['id']}: Working... ({elapsed}s)")
            else:
                status_lines.append(f"✅ {session['id']}: Complete!")
        
        update_dashboard("\n".join(status_lines))
        time.sleep(1)
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ ALL SESSIONS COMPLETE!")
    print("=" * 60)
    
    # Show what each session created
    for session in sessions:
        workspace = Path(session["workspace"])
        files = list(workspace.glob("*"))
        print(f"\n{session['id']} created:")
        for f in files:
            print(f"  - {f.name}")
    
    print(f"\n📊 Check the dashboard: {dashboard}")
    print("🎉 You just watched 3 Claude sessions work in parallel!")


if __name__ == "__main__":
    run_parallel_sessions()