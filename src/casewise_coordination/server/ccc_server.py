"""
CCC MCP Server
Main server implementation using the Model Context Protocol
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from mcp.server import Server, Request, Response
from mcp.server.types import Tool, ToolResult
from mcp.server.stdio import stdio_server

from ..orchestrator import SessionOrchestrator
from .handlers import SessionHandler, OrchestratorHandler


logger = logging.getLogger(__name__)


class CCCServer:
    """
    CCC MCP Server
    Provides tools for orchestrating Claude sessions
    """
    
    def __init__(self, workspace_root: Path, config: Optional[Dict[str, Any]] = None):
        """
        Initialize CCC Server
        
        Args:
            workspace_root: Root directory for workspaces
            config: Optional configuration
        """
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.config = config or {}
        self._load_config()
        
        # Initialize components
        self.orchestrator = SessionOrchestrator(
            workspace_root=self.workspace_root / "orchestrator",
            max_parallel_sessions=self.config.get("max_parallel_sessions", 3),
            dangerous_permissions=self.config.get("dangerous_permissions", True),
            notification_callback=self._handle_notification
        )
        
        # Initialize handlers
        self.session_handler = SessionHandler(self.orchestrator)
        self.orchestrator_handler = OrchestratorHandler(self.orchestrator)
        
        # MCP Server
        self.server = Server("ccc-server")
        self._register_tools()
        
        # State
        self.start_time = datetime.now()
        self._setup_logging()
        
        logger.info("CCC Server initialized")
    
    def _load_config(self):
        """Load configuration from file or environment"""
        config_file = self.workspace_root / "ccc_config.json"
        
        if config_file.exists():
            with open(config_file) as f:
                file_config = json.load(f)
                self.config.update(file_config)
        
        # Environment variables override
        import os
        if os.getenv("CCC_MAX_PARALLEL_SESSIONS"):
            self.config["max_parallel_sessions"] = int(os.getenv("CCC_MAX_PARALLEL_SESSIONS"))
        
        # Save current config
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _setup_logging(self):
        """Setup server logging"""
        log_file = self.workspace_root / "ccc_server.log"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        server_logger = logging.getLogger("casewise_coordination.server")
        server_logger.addHandler(handler)
        server_logger.setLevel(logging.DEBUG)
    
    def _handle_notification(self, level: str, message: str):
        """Handle orchestrator notifications"""
        logger.log(getattr(logging, level.upper(), logging.INFO), f"Orchestrator: {message}")
        
        # Could send desktop notifications here
        if level in ["error", "warning"]:
            # Important notifications
            pass
    
    def _register_tools(self):
        """Register MCP tools"""
        
        # Session Management Tools
        @self.server.tool("create_session")
        async def create_session(
            task_name: str,
            component: str,
            prompt: str,
            timeout_minutes: Optional[int] = 30,
            context: Optional[Dict[str, Any]] = None
        ) -> ToolResult:
            """Create a new Claude session"""
            try:
                session_id = await self.session_handler.create_session(
                    task_name=task_name,
                    component=component,
                    prompt=prompt,
                    timeout_seconds=timeout_minutes * 60,
                    context=context
                )
                
                return ToolResult(
                    success=True,
                    data={"session_id": session_id, "status": "started"}
                )
            except Exception as e:
                logger.error(f"Failed to create session: {e}")
                return ToolResult(success=False, error=str(e))
        
        @self.server.tool("get_session_status")
        async def get_session_status(session_id: str) -> ToolResult:
            """Get status of a session"""
            try:
                status = await self.session_handler.get_session_status(session_id)
                return ToolResult(success=True, data=status)
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        @self.server.tool("terminate_session")
        async def terminate_session(session_id: str, force: bool = False) -> ToolResult:
            """Terminate a session"""
            try:
                await self.session_handler.terminate_session(session_id, force)
                return ToolResult(success=True, data={"message": f"Session {session_id} terminated"})
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        # Workflow Tools
        @self.server.tool("execute_workflow")
        async def execute_workflow(
            workflow_name: str,
            workflow_type: str = "todo_app",
            parallel: bool = True
        ) -> ToolResult:
            """Execute a predefined workflow"""
            try:
                result = await self.orchestrator_handler.execute_workflow(
                    workflow_name=workflow_name,
                    workflow_type=workflow_type,
                    parallel=parallel
                )
                return ToolResult(success=True, data=result)
            except Exception as e:
                logger.error(f"Workflow execution failed: {e}")
                return ToolResult(success=False, error=str(e))
        
        @self.server.tool("get_orchestrator_status")
        async def get_orchestrator_status() -> ToolResult:
            """Get orchestrator status"""
            try:
                status = self.orchestrator.get_status()
                return ToolResult(success=True, data=status)
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        # Result Management Tools
        @self.server.tool("consolidate_results")
        async def consolidate_results(
            session_ids: List[str],
            output_name: str
        ) -> ToolResult:
            """Consolidate results from multiple sessions"""
            try:
                output_dir = self.workspace_root / "results" / output_name
                result = self.orchestrator.consolidate_results(session_ids, output_dir)
                return ToolResult(success=True, data=result)
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        @self.server.tool("list_sessions")
        async def list_sessions(
            status_filter: Optional[str] = None
        ) -> ToolResult:
            """List all sessions with optional status filter"""
            try:
                sessions = await self.session_handler.list_sessions(status_filter)
                return ToolResult(success=True, data={"sessions": sessions})
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        # Utility Tools
        @self.server.tool("get_server_info")
        async def get_server_info() -> ToolResult:
            """Get CCC server information"""
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            info = {
                "version": "0.1.0",
                "uptime_seconds": uptime,
                "workspace_root": str(self.workspace_root),
                "config": self.config,
                "orchestrator_status": self.orchestrator.get_status()
            }
            
            return ToolResult(success=True, data=info)
        
        logger.info(f"Registered {len(self.server._tools)} tools")
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting CCC MCP Server")
        
        try:
            # Run with stdio transport
            async with stdio_server(self.server):
                logger.info("CCC Server running on stdio")
                
                # Keep server running
                while True:
                    await asyncio.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            # Cleanup
            logger.info("Shutting down orchestrator")
            self.orchestrator.terminate_all()
            self.orchestrator.save_state()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.orchestrator.terminate_all()


async def main():
    """Main entry point for running the server"""
    import sys
    
    # Get workspace from argument or use default
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "ccc_workspace"
    
    # Create and run server
    server = CCCServer(workspace)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())