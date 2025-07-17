#!/usr/bin/env python3
"""
Context Monitor for CCC Orchestrator
Tracks approximate token usage and triggers handoff preparation
"""

import time
import json
from pathlib import Path
from datetime import datetime

class ContextMonitor:
    """Monitors context usage and alerts for handoff"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.checkpoint_file = Path("context_checkpoint.json")
        self.handoff_threshold = 75000  # tokens
        self.check_interval = 1800  # 30 minutes in seconds
        
        # Rough estimates
        self.base_context = 15000  # CLAUDE.md, initial setup
        self.tokens_per_minute = 500  # Conservative estimate
        self.tokens_per_file_read = 1000
        self.tokens_per_file_write = 500
        
        self.load_checkpoint()
    
    def load_checkpoint(self):
        """Load or create checkpoint"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file) as f:
                self.checkpoint = json.load(f)
        else:
            self.checkpoint = {
                "session_start": self.start_time.isoformat(),
                "estimated_tokens": self.base_context,
                "files_read": 0,
                "files_written": 0,
                "last_check": self.start_time.isoformat(),
                "interactions": 0
            }
            self.save_checkpoint()
    
    def save_checkpoint(self):
        """Save current state"""
        self.checkpoint["last_check"] = datetime.now().isoformat()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint, f, indent=2)
    
    def estimate_current_tokens(self):
        """Estimate current token usage"""
        elapsed_minutes = (datetime.now() - datetime.fromisoformat(
            self.checkpoint["session_start"]
        )).total_seconds() / 60
        
        time_tokens = elapsed_minutes * self.tokens_per_minute
        file_tokens = (
            self.checkpoint["files_read"] * self.tokens_per_file_read +
            self.checkpoint["files_written"] * self.tokens_per_file_write
        )
        
        return self.base_context + time_tokens + file_tokens
    
    def check_context(self):
        """Silent context check - returns True if approaching limit"""
        current_estimate = self.estimate_current_tokens()
        self.checkpoint["estimated_tokens"] = current_estimate
        
        if current_estimate >= self.handoff_threshold:
            # Create alert file for orchestrator
            alert_file = Path("CONTEXT_ALERT.txt")
            alert_file.write_text(f"""🚨 CONTEXT LIMIT APPROACHING 🚨

Estimated tokens: {current_estimate:,.0f} / 100,000
Threshold for handoff: {self.handoff_threshold:,.0f}

TIME TO PREPARE HANDOFF!
1. Update HANDOFF.md with current state
2. Save all work in progress  
3. Tell Mike to run ./scripts/orchestrator_handoff.sh

Created: {datetime.now().isoformat()}
""")
            return True
        
        # Update checkpoint silently
        self.save_checkpoint()
        return False
    
    def log_file_operation(self, operation="read"):
        """Track file operations for better estimates"""
        if operation == "read":
            self.checkpoint["files_read"] += 1
        else:
            self.checkpoint["files_written"] += 1
        self.checkpoint["interactions"] += 1
        
        # Check every N interactions
        if self.checkpoint["interactions"] % 10 == 0:
            self.check_context()


# Global instance for easy access
_monitor = None

def get_monitor():
    """Get or create monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = ContextMonitor()
    return _monitor

def silent_check():
    """Silent context check - call this periodically"""
    monitor = get_monitor()
    return monitor.check_context()

def log_read():
    """Log a file read operation"""
    get_monitor().log_file_operation("read")

def log_write():
    """Log a file write operation"""
    get_monitor().log_file_operation("write")


if __name__ == "__main__":
    # Test the monitor
    monitor = ContextMonitor()
    estimate = monitor.estimate_current_tokens()
    print(f"Current token estimate: {estimate:,.0f}")
    print(f"Handoff at: {monitor.handoff_threshold:,.0f}")
    print(f"Room left: {monitor.handoff_threshold - estimate:,.0f}")