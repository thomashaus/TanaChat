#!/bin/bash
set -e

echo "🚀 Deploying TanaChat.ai to DigitalOcean..."

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI not found. Please install it first:"
    echo "   brew install doctl"
    exit 1
fi

# Check authentication
if ! doctl auth list &> /dev/null; then
    echo "❌ Not authenticated with DigitalOcean. Run: doctl auth init"
    exit 1
fi

# Deploy to App Platform
echo "📦 Deploying to App Platform..."
doctl apps create --spec .do/app.yaml

# Or update existing app
# APP_ID=$(doctl apps list --format ID --no-header | head -n 1)
# doctl apps update $APP_ID --spec .do/app.yaml

echo "✅ Deployment initiated!"
echo "🔗 View your app: https://cloud.digitalocean.com/apps"
