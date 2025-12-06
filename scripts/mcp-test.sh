#!/bin/bash

echo "🔌 Testing MCP server..."
echo ""

cd mcp

# Check if pyproject.toml exists
if [ ! -f pyproject.toml ]; then
    echo "⚠️  MCP pyproject.toml not found"
    exit 1
fi

# Run pytest if tests exist
if [ -d tests ] && [ "$(ls -A tests/*.py 2>/dev/null)" ]; then
    echo "Running MCP server tests..."
    uv run pytest -v tests/
else
    echo "⚠️  No tests found in mcp/tests/"
fi

echo ""
echo "Testing server imports..."
uv run python -c "from src.server import mcp; print('✅ Server imports successfully')" 2>/dev/null || \
    echo "⚠️  Could not import server (may not be configured yet)"

echo ""
echo "To test interactively, use: make mcp-debug"
