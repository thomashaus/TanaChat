#!/bin/bash
set -e

echo "🚀 Deploying www to DigitalOcean App Platform..."

# Check for doctl
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI required. Install: brew install doctl"
    exit 1
fi

# Build first
echo "📦 Building www..."
cd app
npm run build

echo ""
echo "🌐 Deploying to DO App Platform..."
# Uncomment and configure when ready:
# doctl apps create-deployment YOUR_APP_ID

echo ""
echo "✅ www deployment initiated!"
echo ""
echo "Check status at: https://cloud.digitalocean.com/apps"
