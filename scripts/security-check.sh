#!/bin/bash
set -e

# Security check script for TanaChat.ai
# This script runs comprehensive security checks

echo "🔒 Running comprehensive security checks for TanaChat.ai"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if gitleaks is installed
if ! command -v gitleaks &> /dev/null; then
    print_error "gitleaks is not installed"
    echo "Please install gitleaks:"
    echo "  brew install gitleaks  # macOS"
    echo "  Or visit: https://github.com/gitleaks/gitleaks"
    exit 1
fi

print_status "gitleaks is installed"

# Run gitleaks scan
echo ""
echo "1️⃣ Running gitleaks scan..."
if gitleaks detect --source . --verbose; then
    print_status "No secrets detected by gitleaks"
else
    print_error "Secrets detected! Please review the output above."
    exit 1
fi

# Check for sensitive files that shouldn't be committed
echo ""
echo "2️⃣ Checking for sensitive files..."

SENSITIVE_PATTERNS=(
    ".env.local"
    ".env.production"
    "claude_desktop_config.json"
    "*.pem"
    "*.key"
    "secrets/"
    "do-spaces-config.json"
    "api_keys.txt"
    "tokens.txt"
)

FOUND_SENSITIVE=0
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git ls-files | grep -q "$pattern"; then
        print_error "Sensitive file tracked by git: $pattern"
        FOUND_SENSITIVE=1
    fi
done

if [ $FOUND_SENSITIVE -eq 0 ]; then
    print_status "No sensitive files tracked by git"
fi

# Check temp directory
echo ""
echo "3️⃣ Checking temp directory..."
if git ls-files | grep -q "^temp/"; then
    print_error "Files in temp/ directory are tracked by git!"
    echo "Run: git rm -r --cached temp/ && git add temp/.gitkeep"
    exit 1
else
    print_status "temp/ directory is properly excluded"
fi

# Check .do directory
echo ""
echo "4️⃣ Checking .do directory..."
if git ls-files | grep -q "^.do/"; then
    print_error "Files in .do/ directory are tracked by git!"
    echo "This directory contains sensitive DigitalOcean configurations."
    echo "Run: git rm -r --cached .do/"
    exit 1
else
    print_status ".do/ directory is properly excluded"
fi

# Verify .gitignore covers critical files
echo ""
echo "5️⃣ Verifying .gitignore coverage..."

CRITICAL_IGNORES=(
    ".env.local"
    "claude_desktop_config.json"
    "temp/"
    ".do/"
    "*.key"
    "*.pem"
)

IGNORES_OK=0
for pattern in "${CRITICAL_IGNORES[@]}"; do
    if ! grep -q "^${pattern}" .gitignore; then
        print_warning "$pattern should be in .gitignore"
        IGNORES_OK=1
    fi
done

if [ $IGNORES_OK -eq 0 ]; then
    print_status ".gitignore properly configured"
fi

# Run additional checks if requested
if [ "$1" = "--deep" ]; then
    echo ""
    echo "6️⃣ Running deep security scan..."

    # Check for potential passwords in code
    echo "   Checking for potential passwords..."
    if grep -r -i "password\s*=\s*['\"][^'\"]{8,}" src/ --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null; then
        print_warning "Potential hardcoded passwords found"
    fi

    # Check for API keys patterns
    echo "   Checking for API key patterns..."
    if grep -r -E "(api_key|token)\s*=\s*['\"][A-Za-z0-9]{20,}" src/ --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null; then
        print_warning "Potential API keys found"
    fi
fi

echo ""
echo "=================================================="
if [ $FOUND_SENSITIVE -eq 0 ] && [ $IGNORES_OK -eq 0 ]; then
    print_status "All security checks passed! ✨"
    exit 0
else
    print_error "Security issues found. Please fix them before committing."
    exit 1
fi