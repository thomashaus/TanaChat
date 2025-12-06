#!/bin/bash

echo "🔌 Starting MCP server in debug mode..."
echo ""
echo "This runs the server in stdio mode for direct testing."
echo "You can send JSON-RPC messages via stdin."
echo ""

cd mcp

# Load environment
if [ -f ../.env.local ]; then
    export $(grep -v '^#' ../.env.local | xargs)
fi

# Run the server
uv run python -m src.server
