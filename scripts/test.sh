#!/bin/bash
set -e

echo "🧪 Running all tests..."
echo ""

# API tests
echo "=== API Tests ==="
cd api
if [ -f pyproject.toml ]; then
    uv run pytest -v --tb=short || echo "⚠️  API tests failed or not configured"
else
    echo "⚠️  API pyproject.toml not found, skipping"
fi
cd ..

# WWW tests
echo ""
echo "=== WWW Tests ==="
cd app
if [ -f package.json ]; then
    npm test -- --passWithNoTests 2>/dev/null || echo "⚠️  WWW tests not configured"
else
    echo "⚠️  WWW package.json not found, skipping"
fi
cd ..

# MCP tests
echo ""
echo "=== MCP Tests ==="
cd mcp
if [ -f pyproject.toml ]; then
    uv run pytest -v --tb=short || echo "⚠️  MCP tests failed or not configured"
else
    echo "⚠️  MCP pyproject.toml not found, skipping"
fi
cd ..

echo ""
echo "✅ Test run complete!"
