#!/usr/bin/env python3
"""
CCC Live Watcher - Run this in another terminal to watch CCC sessions live!
Similar to 'tail -f' but for CCC sessions

ESSENTIAL TOOL for CCC - Mike must have this running to monitor parallel sessions
"""

import time
import sys
import os
from pathlib import Path
from datetime import datetime

def watch_ccc_sessions(base_path):
    """Watch all CCC session activity live"""
    
    base = Path(base_path)
    print("🔴 CCC LIVE WATCHER")
    print("=" * 60)
    print(f"Watching: {base}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    known_files = {}
    
    try:
        while True:
            # Find all log files
            log_files = list(base.rglob("*session*log*.txt"))
            
            for log_file in log_files:
                # Track file size to detect new content
                current_size = log_file.stat().st_size
                
                if log_file not in known_files:
                    known_files[log_file] = 0
                    print(f"\n📁 New session log: {log_file}")
                
                if current_size > known_files[log_file]:
                    # Read new content
                    with open(log_file, 'r') as f:
                        f.seek(known_files[log_file])
                        new_content = f.read()
                        
                    if new_content.strip():
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {log_file.parent.name}:")
                        for line in new_content.strip().split('\n'):
                            print(f"  │ {line}")
                    
                    known_files[log_file] = current_size
            
            # Also watch for new files in session workspaces
            session_dirs = [d for d in base.rglob("session_*") if d.is_dir()]
            for session_dir in session_dirs:
                for file in session_dir.iterdir():
                    if file.suffix in ['.py', '.txt', '.json'] and file not in known_files:
                        known_files[file] = True
                        print(f"\n✨ New file in {session_dir.name}: {file.name}")
            
            time.sleep(0.5)  # Check every 0.5 seconds
            
    except KeyboardInterrupt:
        print("\n\n👋 Watcher stopped")


def create_watcher_script():
    """Create a convenient shell script to run the watcher"""
    
    script = Path("/mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude Code Coordinator/watch_ccc.sh")
    script.write_text("""#!/bin/bash
# CCC Live Watcher - Run this to watch CCC sessions in real-time

echo "🔍 CCC Live Watcher"
echo "=================="
echo "This will watch all CCC session activity in real-time"
echo ""

# Default to watching the current directory
WATCH_DIR="${1:-./}"

# Activate the environment if needed
if [ -f "activate_ccc.sh" ]; then
    source activate_ccc.sh
fi

# Run the watcher
python ccc_live_watcher.py "$WATCH_DIR"
""")
    script.chmod(0o755)
    print(f"✅ Created watcher script: {script}")
    print(f"   Run it with: ./watch_ccc.sh")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run as watcher
        watch_ccc_sessions(sys.argv[1])
    else:
        # Create the convenience script
        create_watcher_script()
        
        print("\n💡 HOW TO WATCH CCC SESSIONS LIVE:")
        print("=" * 60)
        print("1. In THIS terminal: Run CCC to spawn Claude sessions")
        print("2. In ANOTHER terminal: Run ./watch_ccc.sh")
        print("3. You'll see real-time activity from all sessions!")
        print("\nOr run directly:")
        print("  python ccc_live_watcher.py /path/to/ccc/workspace")
        print("=" * 60)