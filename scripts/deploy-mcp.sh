#!/bin/bash
set -e

echo "🚀 Deploying mcp to DigitalOcean App Platform..."

# Check for doctl
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI required. Install: brew install doctl"
    exit 1
fi

# Run tests first
echo "🧪 Running tests..."
cd mcp
uv run pytest -v --tb=short
cd ..

echo ""
echo "🌐 Deploying to DO App Platform..."
# Uncomment and configure when ready:
# doctl apps create-deployment YOUR_APP_ID

echo ""
echo "✅ mcp deployment initiated!"
echo ""
echo "Check status at: https://cloud.digitalocean.com/apps"
