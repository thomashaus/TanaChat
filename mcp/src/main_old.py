"""Main entry point for TanaChat MCP server."""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.config import settings
from src.server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="TanaChat MCP Server",
    description="HTTP wrapper for TanaChat MCP server",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    """MCP request model."""
    method: str
    params: Dict[str, Any] = {}
    id: Any = None

class MCPResponse(BaseModel):
    """MCP response model."""
    result: Any = None
    error: Dict[str, Any] = None
    id: Any = None

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "TanaChat MCP Server",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    """Handle MCP requests."""
    try:
        # Convert to MCP protocol format
        mcp_request = {
            "jsonrpc": "2.0",
            "method": request.method,
            "params": request.params,
            "id": request.id
        }

        # Process the MCP request (simplified for now)
        # In a real implementation, you'd use the MCP protocol to communicate
        # with the actual MCP server process

        if request.method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "check_auth_status",
                        "description": "Check authentication status"
                    },
                    {
                        "name": "list_spaces_files",
                        "description": "List files in Spaces"
                    },
                    {
                        "name": "validate_tana_file",
                        "description": "Validate a Tana file"
                    }
                ]
            }
        else:
            result = {"message": f"Method {request.method} not yet implemented"}

        return MCPResponse(result=result, id=request.id)

    except Exception as e:
        logging.error(f"Error handling MCP request: {e}")
        return MCPResponse(
            error={
                "code": -1,
                "message": str(e)
            },
            id=request.id
        )

def main():
    """Run the HTTP server."""
    logging.info("Starting TanaChat MCP HTTP server...")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()