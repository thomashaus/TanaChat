"""Tana file management tools for MCP"""

from fastmcp import tool


@tool()
async def validate_tana_file(content: str) -> dict:
    """Validate a Tana file"""
    return {"valid": False, "message": "Tana tools not implemented yet"}
