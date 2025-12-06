"""DigitalOcean Spaces tools for MCP"""

from fastmcp import tool


@tool()
async def list_spaces_files() -> dict:
    """List files in Spaces"""
    return {"files": [], "message": "Spaces tools not implemented yet"}
