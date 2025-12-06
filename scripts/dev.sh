#!/bin/bash

# Start all services in development mode
trap 'kill 0' EXIT

echo "🚀 Starting TanaChat development servers..."
echo ""

# Load environment
if [ -f .env.local ]; then
    export $(grep -v '^#' .env.local | xargs)
fi

echo "🌐 www: http://localhost:3000 (TanaChat Homepage)"
(cd app && npm run dev) &

echo "🔧 api: http://localhost:8000"
echo "📚 api docs: http://localhost:8000/docs"
(cd api && uv run uvicorn src.main:app --reload --port 8000) &

echo "🔌 mcp: running in background (use 'make mcp-debug' for testing)"
echo ""
echo "Press Ctrl+C to stop all services"

wait
