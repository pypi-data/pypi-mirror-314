from enum import Enum
import json
from typing import Sequence
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShellTools(str, Enum):
    EXECUTE_COMMAND = "execute_command"

class CommandResult(BaseModel):
    command: str
    output: str
    return_code: int

class ShellServer:
    def execute_command(self, command: str) -> CommandResult:
        """Execute a shell command and return the result"""
        logger.info(f"Executing command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            logger.debug(f"Command output: {result.stdout + result.stderr}")
            return CommandResult(
                command=command,
                output=result.stdout + result.stderr,
                return_code=result.returncode
            )
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            raise McpError(f"Command execution failed: {str(e)}")

async def serve() -> None:
    logger.info("Starting MCP shell server...")
    server = Server("mcp-shell")
    shell_server = ShellServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available shell tools."""
        logger.debug("Listing available tools")
        return [
            Tool(
                name=ShellTools.EXECUTE_COMMAND.value,
                display_name="Execute Shell Command",
                description="Execute a shell command and return its output",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Shell command to execute",
                        }
                    },
                    "required": ["command"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for shell command execution."""
        logger.info(f"Tool call received: {name} with arguments: {arguments}")
        try:
            if name == ShellTools.EXECUTE_COMMAND.value:
                command = arguments.get("command")
                if not command:
                    raise ValueError("Missing required argument: command")

                result = shell_server.execute_command(command)
                return [
                    TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
                ]
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            raise ValueError(f"Error executing shell command: {str(e)}")

    logger.info("Initializing server...")
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server started and ready to handle requests")
        await server.run(read_stream, write_stream, options) 