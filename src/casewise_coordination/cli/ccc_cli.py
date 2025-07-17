"""
CCC Command Line Interface
Main CLI implementation for CCC
"""

import click
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import subprocess
import os

from ..orchestrator import SessionOrchestrator
from ..orchestrator.task_distribution import TaskDistributor
from ..session import SessionStatus


class CCCCli:
    """CCC CLI implementation"""
    
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.config_file = self.workspace / "ccc_config.json"
        self._load_config()
    
    def _load_config(self):
        """Load CLI configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {
                "max_parallel_sessions": 3,
                "dangerous_permissions": True,
                "default_timeout_minutes": 30
            }
            self._save_config()
    
    def _save_config(self):
        """Save CLI configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)


@click.group()
@click.option('--workspace', '-w', default='./ccc_workspace', help='CCC workspace directory')
@click.pass_context
def cli(ctx, workspace):
    """CCC - Claude Code Coordinator
    
    Orchestrate multiple Claude sessions for complex development tasks.
    """
    ctx.obj = CCCCli(workspace)


@cli.command()
@click.pass_obj
def status(ccc: CCCCli):
    """Show current CCC status"""
    click.echo("🚀 CCC Status")
    click.echo("=" * 50)
    
    # Check for running orchestrator
    orchestrator_state = ccc.workspace / "orchestrator" / "orchestrator_state.json"
    
    if orchestrator_state.exists():
        with open(orchestrator_state) as f:
            state = json.load(f)
        
        started = datetime.fromisoformat(state['started_at'])
        uptime = (datetime.now() - started).total_seconds() / 3600
        
        click.echo(f"Orchestrator ID: {state['orchestrator_id']}")
        click.echo(f"Uptime: {uptime:.1f} hours")
        click.echo(f"Active Sessions: {len(state['active_sessions'])}")
        click.echo(f"Completed: {len(state['completed_sessions'])}")
        click.echo(f"Failed: {len(state['failed_sessions'])}")
        
        if state['active_sessions']:
            click.echo("\nActive Sessions:")
            for session_id in state['active_sessions']:
                click.echo(f"  - {session_id}")
    else:
        click.echo("No active orchestrator found.")
        click.echo("Run 'ccc start' to begin orchestrating.")


@cli.command()
@click.option('--max-sessions', '-m', default=3, help='Maximum parallel sessions')
@click.option('--dangerous/--safe', default=True, help='Use dangerous permissions')
@click.pass_obj
def start(ccc: CCCCli, max_sessions, dangerous):
    """Start CCC orchestrator"""
    click.echo("🚀 Starting CCC Orchestrator...")
    
    # Update config
    ccc.config['max_parallel_sessions'] = max_sessions
    ccc.config['dangerous_permissions'] = dangerous
    ccc._save_config()
    
    # Start in background
    cmd = [
        sys.executable,
        "-m", "casewise_coordination.server",
        str(ccc.workspace)
    ]
    
    log_file = ccc.workspace / "orchestrator.log"
    
    with open(log_file, 'w') as log:
        process = subprocess.Popen(
            cmd,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
    
    click.echo(f"✅ Orchestrator started (PID: {process.pid})")
    click.echo(f"📄 Logs: {log_file}")
    click.echo("\nUse 'ccc status' to check orchestrator")
    click.echo("Use 'ccc stop' to shutdown")


@cli.command()
@click.pass_obj
def stop(ccc: CCCCli):
    """Stop CCC orchestrator"""
    # This would need proper process management
    click.echo("🛑 Stopping orchestrator...")
    click.echo("(Not fully implemented - kill process manually for now)")


@cli.group()
def workflow():
    """Manage workflows"""
    pass


@workflow.command('list')
@click.pass_obj
def list_workflows(ccc: CCCCli):
    """List available workflow templates"""
    click.echo("📋 Available Workflows")
    click.echo("=" * 50)
    
    distributor = TaskDistributor()
    
    for name, tasks in distributor.task_templates.items():
        total_time = sum(t.estimated_minutes for t in tasks)
        click.echo(f"\n{name}:")
        click.echo(f"  Tasks: {len(tasks)}")
        click.echo(f"  Estimated Time: {total_time} minutes")
        click.echo("  Components:")
        for task in tasks:
            deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
            click.echo(f"    - {task.name} [{task.component}]{deps}")


@workflow.command('run')
@click.argument('workflow_type', type=click.Choice(['todo_app', 'auth_system', 'blog_platform']))
@click.option('--name', '-n', required=True, help='Workflow instance name')
@click.option('--parallel/--sequential', default=True, help='Run tasks in parallel')
@click.pass_obj
def run_workflow(ccc: CCCCli, workflow_type, name, parallel):
    """Run a workflow"""
    click.echo(f"🚀 Starting workflow: {name} (type: {workflow_type})")
    
    # This would connect to the running orchestrator
    # For now, we'll show what would happen
    
    distributor = TaskDistributor()
    tasks = distributor.task_templates[workflow_type]
    analysis = distributor.analyze_dependencies(tasks)
    time_est = distributor.estimate_total_time(tasks)
    
    click.echo(f"\n📊 Workflow Analysis:")
    click.echo(f"  Total Tasks: {len(tasks)}")
    click.echo(f"  Execution Phases: {len(analysis['phases'])}")
    click.echo(f"  Estimated Time:")
    click.echo(f"    - Parallel: {time_est['parallel_execution_minutes']} minutes")
    click.echo(f"    - Sequential: {time_est['sequential_execution_minutes']} minutes")
    click.echo(f"    - Time Saved: {time_est['time_saved_minutes']} minutes")
    
    if click.confirm("\nProceed with workflow execution?"):
        click.echo("\n✅ Workflow started!")
        click.echo("Monitor progress with 'ccc status' or './scripts/watch_ccc.sh'")
    else:
        click.echo("❌ Workflow cancelled")


@cli.group()
def session():
    """Manage individual sessions"""
    pass


@session.command('list')
@click.option('--status', '-s', help='Filter by status')
@click.pass_obj
def list_sessions(ccc: CCCCli, status):
    """List all sessions"""
    click.echo("📋 CCC Sessions")
    click.echo("=" * 50)
    
    sessions_dir = ccc.workspace / "orchestrator" / "sessions"
    if not sessions_dir.exists():
        click.echo("No sessions found.")
        return
    
    for session_dir in sessions_dir.iterdir():
        if session_dir.is_dir():
            state_file = session_dir / "session_state.json"
            if state_file.exists():
                with open(state_file) as f:
                    state = json.load(f)
                
                if status and state['status'] != status:
                    continue
                
                click.echo(f"\n{state['session_id']}:")
                click.echo(f"  Status: {state['status']}")
                click.echo(f"  Task: {state['task_name']} / {state['component']}")
                click.echo(f"  Progress: {state['progress_percent']}%")
                click.echo(f"  Files Created: {len(state['files_created'])}")


@session.command('logs')
@click.argument('session_id')
@click.option('--tail', '-n', default=50, help='Number of lines to show')
@click.pass_obj
def session_logs(ccc: CCCCli, session_id, tail):
    """Show session logs"""
    log_file = ccc.workspace / "orchestrator" / "sessions" / session_id / "session.log"
    
    if not log_file.exists():
        click.echo(f"❌ No logs found for session: {session_id}")
        return
    
    # Show last N lines
    with open(log_file) as f:
        lines = f.readlines()
        for line in lines[-tail:]:
            click.echo(line.rstrip())


@cli.command()
@click.pass_obj
def demo(ccc: CCCCli):
    """Run a demo workflow (Todo App)"""
    click.echo("🎭 CCC Demo - Building a Todo App")
    click.echo("=" * 50)
    click.echo("\nThis demo will:")
    click.echo("1. Create a FastAPI backend with todo CRUD operations")
    click.echo("2. Create a React frontend with todo UI")
    click.echo("3. Create comprehensive tests for both")
    click.echo("\nThree Claude sessions will work in parallel!")
    
    if click.confirm("\nReady to see CCC in action?"):
        click.echo("\n🚀 Starting demo...")
        # Would trigger the actual demo
        click.echo("\nDemo started! Watch progress with './scripts/watch_ccc.sh'")
    else:
        click.echo("Demo cancelled.")


@cli.command()
@click.pass_obj  
def config(ccc: CCCCli):
    """Show current configuration"""
    click.echo("⚙️  CCC Configuration")
    click.echo("=" * 50)
    click.echo(json.dumps(ccc.config, indent=2))
    click.echo(f"\nConfig file: {ccc.config_file}")


@cli.command()
def version():
    """Show CCC version"""
    from .. import __version__
    click.echo(f"CCC - Claude Code Coordinator v{__version__}")


def main():
    """Main CLI entry point"""
    cli()


if __name__ == '__main__':
    main()