#!/bin/bash
set -e

# Usage: scripts/setup.sh [local|production]
TARGET=${1:-local}

echo "🚀 Setting up TanaChat.ai $TARGET environment..."

# Check for required tools
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required. Install from https://nodejs.org"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.12+ required"; exit 1; }

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Setup www
echo "📦 Setting up www..."
cd app && npm install && cd ..

# Setup directories based on target
if [ "$TARGET" = "production" ]; then
    echo "🏭 Production setup detected"
    # Additional production-specific setup can go here
else
    echo "🏠 Local development setup detected"
fi

# Setup mcp (main API)
echo "🔌 Setting up mcp..."
cd mcp && uv sync && cd ..

# Copy env files if they don't exist
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "📝 Created .env.local - please update with your credentials"
fi

# Install gitleaks if not present
if ! command -v gitleaks &> /dev/null; then
    echo "🔒 Installing gitleaks..."
    if command -v brew &> /dev/null; then
        brew install gitleaks
    else
        echo "⚠️  Please install gitleaks manually: https://github.com/gitleaks/gitleaks"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env.local with your DO credentials"
echo "  2. Run 'make dev' to start services"
echo "  3. Visit http://localhost:3000 (www)"
echo "  4. Visit http://localhost:8000/docs (api)"
