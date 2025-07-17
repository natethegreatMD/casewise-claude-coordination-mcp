"""
Desktop Notifications for CCC
Cross-platform desktop notification support
"""

import sys
import subprocess
import logging
from typing import Optional
from pathlib import Path


logger = logging.getLogger(__name__)


class NotificationManager:
    """Manages desktop notifications across platforms"""
    
    def __init__(self):
        self.platform = sys.platform
        self.enabled = True
        self._check_availability()
    
    def _check_availability(self):
        """Check if notifications are available"""
        if self.platform == "linux":
            # Check for notify-send
            try:
                subprocess.run(["which", "notify-send"], 
                             check=True, capture_output=True)
            except:
                logger.warning("notify-send not found, notifications disabled")
                self.enabled = False
        
        elif self.platform == "darwin":  # macOS
            # Check for osascript
            try:
                subprocess.run(["which", "osascript"], 
                             check=True, capture_output=True)
            except:
                logger.warning("osascript not found, notifications disabled")
                self.enabled = False
        
        elif self.platform == "win32":
            # Windows notifications through PowerShell
            pass
        
        else:
            logger.warning(f"Unsupported platform for notifications: {self.platform}")
            self.enabled = False
    
    def send(
        self,
        title: str,
        message: str,
        urgency: str = "normal",
        icon: Optional[str] = None
    ) -> bool:
        """
        Send a desktop notification
        
        Args:
            title: Notification title
            message: Notification body
            urgency: low, normal, or critical
            icon: Path to icon (Linux only)
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            if self.platform == "linux":
                self._send_linux(title, message, urgency, icon)
            elif self.platform == "darwin":
                self._send_macos(title, message)
            elif self.platform == "win32":
                self._send_windows(title, message)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    def _send_linux(self, title: str, message: str, urgency: str, icon: Optional[str]):
        """Send notification on Linux using notify-send"""
        cmd = ["notify-send", title, message, f"--urgency={urgency}"]
        
        if icon and Path(icon).exists():
            cmd.extend(["--icon", icon])
        
        subprocess.run(cmd, check=True)
    
    def _send_macos(self, title: str, message: str):
        """Send notification on macOS using osascript"""
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], check=True)
    
    def _send_windows(self, title: str, message: str):
        """Send notification on Windows using PowerShell"""
        # PowerShell command for Windows 10+ notifications
        ps_script = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null

$template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>{title}</text>
            <text>{message}</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("CCC").Show($toast)
"""
        
        subprocess.run(
            ["powershell", "-Command", ps_script],
            check=True,
            capture_output=True
        )


# Global notification manager instance
_notification_manager = None


def get_notification_manager() -> NotificationManager:
    """Get the global notification manager"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager


def send_notification(
    title: str,
    message: str,
    urgency: str = "normal",
    icon: Optional[str] = None
) -> bool:
    """
    Send a desktop notification
    
    Args:
        title: Notification title
        message: Notification body
        urgency: low, normal, or critical
        icon: Path to icon (optional)
        
    Returns:
        bool: Success status
    """
    manager = get_notification_manager()
    return manager.send(title, message, urgency, icon)


# CCC-specific notification functions

def notify_session_started(session_id: str, task_name: str):
    """Notify that a session has started"""
    send_notification(
        "CCC Session Started",
        f"{session_id}\nTask: {task_name}",
        urgency="normal"
    )


def notify_session_completed(session_id: str, success: bool):
    """Notify that a session has completed"""
    status = "✅ Completed" if success else "❌ Failed"
    urgency = "normal" if success else "critical"
    
    send_notification(
        f"CCC Session {status}",
        session_id,
        urgency=urgency
    )


def notify_workflow_completed(workflow_name: str, success: bool, duration_minutes: float):
    """Notify that a workflow has completed"""
    status = "successfully" if success else "with errors"
    
    send_notification(
        "CCC Workflow Complete",
        f"{workflow_name} completed {status}\nDuration: {duration_minutes:.1f} minutes",
        urgency="normal" if success else "critical"
    )


def notify_error(error_message: str):
    """Notify about an error"""
    send_notification(
        "CCC Error",
        error_message,
        urgency="critical"
    )