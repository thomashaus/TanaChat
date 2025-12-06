"""Main MCP server implementation for TanaChat."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tanachat")

# Initialize the MCP server
app = Server("tanachat")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the MCP server."""
    return [
        Tool(
            name="hello",
            description="A simple greeting tool that says hello",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet",
                    }
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="echo",
            description="Echo back any message you send",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back",
                    }
                },
                "required": ["message"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from the MCP client."""
    if name == "hello":
        name_arg = arguments.get("name", "World")
        return [
            TextContent(
                type="text",
                text=f"Hello, {name_arg}! Welcome to TanaChat!",
            )
        ]
    elif name == "echo":
        message = arguments.get("message", "")
        return [
            TextContent(
                type="text",
                text=f"Echo: {message}",
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """Run the MCP server."""
    logger.info("Starting TanaChat MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def run() -> None:
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
