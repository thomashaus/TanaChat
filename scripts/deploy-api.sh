#!/bin/bash
set -e

echo "🚀 Deploying api to DigitalOcean App Platform..."

# Check for doctl
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI required. Install: brew install doctl"
    exit 1
fi

# Run tests first
echo "🧪 Running tests..."
cd api
uv run pytest -v --tb=short
cd ..

echo ""
echo "🌐 Deploying to DO App Platform..."
# Uncomment and configure when ready:
# doctl apps create-deployment YOUR_APP_ID

echo ""
echo "✅ api deployment initiated!"
echo ""
echo "Check status at: https://cloud.digitalocean.com/apps"
