"""Authentication tools for MCP"""

from fastmcp import tool


@tool()
async def check_auth_status() -> dict:
    """Check authentication status"""
    return {"status": "placeholder", "message": "Authentication tools not implemented yet"}
