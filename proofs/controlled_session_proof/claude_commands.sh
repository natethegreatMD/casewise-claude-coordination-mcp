#!/bin/bash
cd "/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/controlled_session_proof"
cat << 'EOF' | claude --continue
Please do the following to prove you are being controlled by CCC:

1. Create a file called 'proof_of_control.txt' with this content:
   === CLAUDE SESSION UNDER CCC CONTROL ===
   Time: [current time]
   Message: I am a Claude Code session being controlled by the CCC orchestrator
   Task: Creating proof of concept files
   === END ===

2. Create a Python script called 'controlled_work.py' that:
   - Prints "Hello from CCC-controlled Claude!"
   - Calculates factorial of 10
   - Writes the result to 'result.txt'

3. Run the Python script

This will prove that CCC can spawn and control Claude sessions.
EOF
