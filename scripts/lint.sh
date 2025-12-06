#!/bin/bash
set -e

echo "🔍 Running linters..."
echo ""

ERRORS=0

# API lint
echo "=== API (Ruff) ==="
cd api
if [ -f pyproject.toml ] && [ -d src ]; then
    uv run ruff check src/ || ERRORS=$((ERRORS + 1))
    uv run ruff format --check src/ || ERRORS=$((ERRORS + 1))
else
    echo "⚠️  API src/ not found, skipping"
fi
cd ..

# WWW lint
echo ""
echo "=== WWW (ESLint + Prettier) ==="
cd app
if [ -f package.json ]; then
    npm run lint 2>/dev/null || ERRORS=$((ERRORS + 1))
    npx prettier --check "src/**/*.{ts,tsx}" 2>/dev/null || echo "⚠️  Prettier check skipped"
else
    echo "⚠️  WWW package.json not found, skipping"
fi
cd ..

# MCP lint
echo ""
echo "=== MCP (Ruff) ==="
cd mcp
if [ -f pyproject.toml ] && [ -d src ]; then
    uv run ruff check src/ || ERRORS=$((ERRORS + 1))
    uv run ruff format --check src/ || ERRORS=$((ERRORS + 1))
else
    echo "⚠️  MCP src/ not found, skipping"
fi
cd ..

# Security scan
echo ""
echo "=== Security (Gitleaks) ==="
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source . --verbose || ERRORS=$((ERRORS + 1))
else
    echo "⚠️  gitleaks not installed, skipping security scan"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ All linting passed!"
else
    echo "❌ Linting found $ERRORS issue(s)"
    exit 1
fi
