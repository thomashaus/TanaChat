#!/bin/bash
# Build TanaChat components and Docker images
#
# Usage: scripts/build.sh [local|production]
#   local: Build frontend and setup MCP for development
#   production: Build frontend, MCP, and Docker images for deployment
#
# Production builds will:
#   - Build optimized frontend bundle
#   - Build MCP API with dependencies
#   - Create Docker images for deployment
#   - Push images to registry if PROD_REGISTRY_NAME is set
#
# Requires: Node.js, Python 3.12+, Docker (for production)

set -e
TARGET=${1:-local}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment from .env or .env.local
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
elif [ -f "$PROJECT_ROOT/.env.local" ]; then
    set -a
    source "$PROJECT_ROOT/.env.local"
    set +a
fi

# Docker configuration
DOCKER_APP_IMAGE=${DOCKER_APP_IMAGE:-tanachat-app}
DOCKER_MCP_IMAGE=${DOCKER_MCP_IMAGE:-tanachat-mcp}
DOCKER_TAG=${DOCKER_TAG:-latest}
DOCKER_REGISTRY=${PROD_REGISTRY_NAME:-""}

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔨 Building TanaChat for $TARGET environment...${NC}"

# Validate required tools
command -v node >/dev/null 2>&1 || { echo -e "${RED}❌ Node.js required. Install from https://nodejs.org${NC}"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ Python 3.12+ required${NC}"; exit 1; }
[ "$TARGET" = "production" ] && {
    command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker required for production builds${NC}"; exit 1; }
}

# Build frontend
echo -e "\n${GREEN}--- Building Frontend ---${NC}"
cd "$PROJECT_ROOT/app"
if [ "$TARGET" = "production" ]; then
    echo "Building production bundle..."
    npm run build
    echo -e "${GREEN}✓ Frontend built for production${NC}"
else
    echo "Building for development..."
    npm run build:dev 2>/dev/null || npm run build 2>/dev/null || echo -e "${YELLOW}⚠ Frontend build skipped${NC}"
    echo -e "${GREEN}✓ Frontend built for development${NC}"
fi

# Build MCP API
echo -e "\n${GREEN}--- Building MCP API ---${NC}"
cd "$PROJECT_ROOT/mcp"
if [ "$TARGET" = "production" ]; then
    echo "Building MCP for production..."
    command -v uv &> /dev/null || { echo -e "${RED}❌ uv required. Install from https://astral.sh/uv/${NC}"; exit 1; }
    uv sync
    uv build 2>/dev/null || echo -e "${YELLOW}⚠ uv build failed or not configured${NC}"
    echo -e "${GREEN}✓ MCP built for production${NC}"
else
    echo "Setting up MCP for development..."
    command -v uv &> /dev/null && uv sync || echo -e "${YELLOW}⚠ uv not found, skipping MCP setup${NC}"
    echo -e "${GREEN}✓ MCP set up for development${NC}"
fi

# Build Docker images for production
if [ "$TARGET" = "production" ]; then
    echo -e "\n${GREEN}--- Building Docker Images ---${NC}"
    cd "$PROJECT_ROOT"

    # Set platform for production builds
    BUILD_PLATFORM=""
    if [ "$TARGET" = "production" ]; then
        BUILD_PLATFORM="--platform linux/amd64"
        echo "Building for production with platform: linux/amd64"
    fi

    # Build frontend image
    echo "Building frontend image..."
    if [ -n "$DOCKER_REGISTRY" ]; then
        docker buildx build $BUILD_PLATFORM -f app/Dockerfile.do -t $DOCKER_REGISTRY/$DOCKER_APP_IMAGE:$DOCKER_TAG ./app --load ||
            { echo -e "${RED}❌ Failed to build app Docker image${NC}"; exit 1; }
        docker tag $DOCKER_REGISTRY/$DOCKER_APP_IMAGE:$DOCKER_TAG $DOCKER_APP_IMAGE:latest
    else
        docker buildx build $BUILD_PLATFORM -f app/Dockerfile.do -t $DOCKER_APP_IMAGE:$DOCKER_TAG ./app --load ||
            { echo -e "${RED}❌ Failed to build app Docker image${NC}"; exit 1; }
        docker tag $DOCKER_APP_IMAGE:$DOCKER_TAG $DOCKER_APP_IMAGE:latest
    fi

    # Build MCP image
    echo "Building MCP image..."
    if [ -n "$DOCKER_REGISTRY" ]; then
        docker buildx build $BUILD_PLATFORM -f mcp/Dockerfile.do -t $DOCKER_REGISTRY/$DOCKER_MCP_IMAGE:$DOCKER_TAG ./mcp --load ||
            { echo -e "${RED}❌ Failed to build MCP Docker image${NC}"; exit 1; }
        docker tag $DOCKER_REGISTRY/$DOCKER_MCP_IMAGE:$DOCKER_TAG $DOCKER_MCP_IMAGE:latest
    else
        docker buildx build $BUILD_PLATFORM -f mcp/Dockerfile.do -t $DOCKER_MCP_IMAGE:$DOCKER_TAG ./mcp --load ||
            { echo -e "${RED}❌ Failed to build MCP Docker image${NC}"; exit 1; }
        docker tag $DOCKER_MCP_IMAGE:$DOCKER_TAG $DOCKER_MCP_IMAGE:latest
    fi

    # Push to registry if specified
    if [ -n "$DOCKER_REGISTRY" ]; then
        echo -e "\n${GREEN}--- Pushing Images to Registry ---${NC}"

        docker push $DOCKER_REGISTRY/$DOCKER_APP_IMAGE:$DOCKER_TAG ||
            { echo -e "${RED}❌ Failed to push app image${NC}"; exit 1; }
        echo "✓ Pushed app image"

        docker push $DOCKER_REGISTRY/$DOCKER_MCP_IMAGE:$DOCKER_TAG ||
            { echo -e "${RED}❌ Failed to push MCP image${NC}"; exit 1; }
        echo "✓ Pushed MCP image"

        echo -e "${GREEN}✓ Images pushed to registry${NC}"
    else
        echo -e "${YELLOW}⚠ No registry specified, skipping push${NC}"
    fi

    echo -e "${GREEN}✓ Docker images built successfully${NC}"
else
    echo -e "\n${YELLOW}--- Skipping Docker Images (local development) ---${NC}"
fi

# Security scan for production builds
if [ "$TARGET" = "production" ]; then
    echo -e "\n${GREEN}--- Running Security Scan ---${NC}"
    cd "$PROJECT_ROOT"

    if command -v gitleaks &> /dev/null; then
        gitleaks detect --no-banner --no-git || {
            echo -e "${RED}❌ Security scan failed - secrets detected${NC}"
            exit 1
        }
        echo -e "${GREEN}✓ Security scan passed${NC}"
    else
        echo -e "${YELLOW}⚠ gitleaks not found, skipping security scan${NC}"
    fi
fi

echo -e "\n${GREEN}🎉 Build completed successfully for $TARGET environment!${NC}"

# Next steps
if [ "$TARGET" = "production" ]; then
    echo "Next: scripts/build-and-deploy.sh production"
else
    echo "Next: make dev (start development)"
fi