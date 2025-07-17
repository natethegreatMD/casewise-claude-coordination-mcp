#!/usr/bin/env python3
"""
Proof of concept: Create and control a new Claude Code session
This demonstrates the core CCC capability - spawning and controlling separate Claude sessions
"""

import subprocess
import os
import time
import json
from pathlib import Path

def create_controlled_session():
    """Create a new Claude Code session and control it to perform a task"""
    
    # Create a test workspace for the new session
    test_workspace = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/test_session_workspace")
    test_workspace.mkdir(exist_ok=True)
    
    # Create a command file that the new session will execute
    command_file = test_workspace / "session_commands.txt"
    proof_file = test_workspace / "proof_of_control.txt"
    
    # Write commands for the new session to execute
    commands = f"""Create a file at {proof_file} with the following content:

=== PROOF OF CLAUDE SESSION CONTROL ===
Session ID: test-session-001
Created by: CCC Orchestrator
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
Message: This file was created by a Claude Code session under CCC control

Tasks completed by controlled session:
1. Created this proof file
2. Listed directory contents
3. Created a Python script that calculates Fibonacci numbers
4. Executed the script and captured output

This demonstrates that CCC can:
- Spawn new Claude Code sessions
- Give them specific tasks
- Monitor their execution
- Collect their outputs

=== END PROOF ===

Then create a Python script called fibonacci.py that calculates the first 10 Fibonacci numbers and run it.
"""
    
    command_file.write_text(commands)
    
    print("🚀 Creating new Claude Code session under CCC control...")
    print(f"📁 Session workspace: {test_workspace}")
    print(f"📝 Command file: {command_file}")
    
    # Create the actual command to spawn a new Claude session
    # Using --no-interactive to run in batch mode with specific commands
    claude_command = [
        "claude", 
        "--no-interactive",
        "--continue",  # Continue even if there are warnings
        f"{commands}"
    ]
    
    # Alternative approach: Use claude with a specific prompt file
    prompt_file = test_workspace / "session_prompt.txt"
    prompt_file.write_text(f"""You are a Claude Code session being controlled by the CCC orchestrator.

Your task:
1. Create a file at {proof_file} with the content provided below
2. Create a fibonacci.py script that calculates first 10 Fibonacci numbers
3. Run the fibonacci.py script

File content for {proof_file}:
{commands}

Execute these tasks and confirm completion.""")
    
    # Run Claude in the test workspace
    env = os.environ.copy()
    result = subprocess.run(
        ["claude", "--no-interactive", f"< {prompt_file}"],
        shell=True,
        cwd=str(test_workspace),
        capture_output=True,
        text=True,
        env=env
    )
    
    print("\n📊 Session execution results:")
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"STDOUT:\n{result.stdout[:500]}...")  # First 500 chars
    if result.stderr:
        print(f"STDERR:\n{result.stderr[:500]}...")
    
    # Check if the proof file was created
    if proof_file.exists():
        print(f"\n✅ SUCCESS! Controlled session created proof file:")
        print(f"📄 {proof_file}")
        print("\nFile contents:")
        print(proof_file.read_text())
    else:
        print(f"\n❌ Proof file not created. Checking workspace contents...")
        workspace_files = list(test_workspace.glob("*"))
        print(f"Files in workspace: {[f.name for f in workspace_files]}")
    
    return result

if __name__ == "__main__":
    create_controlled_session()