#!/usr/bin/env python3
"""
FastMCP server for TanaChat
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastmcp import FastMCP

    mcp = FastMCP("tanachat")

    # Import tools with fallback
    try:
        from src.tools import auth

        mcp.add_tool(auth.check_auth_status)
    except ImportError:

        @mcp.tool()
        async def check_auth_status() -> dict:
            """Check authentication status"""
            return {"status": "error", "message": "Auth tools not available"}

    try:
        from src.tools import spaces

        mcp.add_tool(spaces.list_spaces_files)
    except ImportError:

        @mcp.tool()
        async def list_spaces_files() -> dict:
            """List files in Spaces"""
            return {"files": [], "message": "Spaces tools not available"}

    try:
        from src.tools import tana

        mcp.add_tool(tana.validate_tana_file)
    except ImportError:

        @mcp.tool()
        async def validate_tana_file(content: str) -> dict:
            """Validate a Tana file"""
            return {"valid": False, "message": "Tana tools not available"}

except ImportError as e:
    print(f"Error importing fastmcp: {e}")
    print("Please install with: pip install fastmcp")
    sys.exit(1)

# Export the FastMCP instance as app for compatibility
app = mcp

if __name__ == "__main__":
    import sys
    # Run the FastMCP server with command-line interface
    import subprocess
    subprocess.run([sys.executable, "-m", "fastmcp", "run", "--host", "0.0.0.0", "--port", "8000"])
