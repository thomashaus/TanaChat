#!/bin/bash
# Deploy TanaChat to target environment
#
# Usage: scripts/deploy.sh [local|production]
#   local: Start services with docker-compose for development
#   production: Deploy to DigitalOcean App Platform using .do configurations
#
# Production deployment requires:
#   - .do/ directory with deployment configurations
#   - doctl authenticated with DigitalOcean
#   - Images already built and pushed to registry
#
# Local deployment requires:
#   - docker-compose or docker compose
#   - local/docker-compose.yml configuration

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

# Configuration
DOCKER_APP_IMAGE=${DOCKER_APP_IMAGE:-tanachat-app}
DOCKER_MCP_IMAGE=${DOCKER_MCP_IMAGE:-tanachat-mcp}
DOCKER_TAG=${DOCKER_TAG:-latest}
APP_NAME=${APP_NAME:-tanachat}
PROD_REGISTRY_NAME=${PROD_REGISTRY_NAME:-""}
LOCAL_FRONTEND_PORT=${LOCAL_FRONTEND_PORT:-5173}
LOCAL_API_PORT=${LOCAL_API_PORT:-8000}

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Deploying TanaChat to $TARGET environment...${NC}"

# Validate required tools
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker required${NC}"; exit 1; }
[ "$TARGET" = "production" ] && {
    command -v doctl >/dev/null 2>&1 || { echo -e "${RED}❌ doctl required for production${NC}"; exit 1; }
}

# Deploy based on target environment
if [ "$TARGET" = "production" ]; then
    echo -e "\n${GREEN}--- Production Deployment ---${NC}"

    # Validate DigitalOcean access and configuration
    doctl auth init 2>/dev/null || { echo -e "${RED}❌ DigitalOcean authentication failed. Run 'doctl auth init'${NC}"; exit 1; }
    [ -f "$PROJECT_ROOT/.do/appspec.yaml" ] || { echo -e "${RED}❌ .do/appspec.yaml not found${NC}"; exit 1; }

    cd "$PROJECT_ROOT/.do"

    # Build and push images (if needed)
    [ -f "./build-images.sh" ] && {
        echo "Building and pushing images..."
        ./build-images.sh
        echo -e "${GREEN}✓ Images built and pushed${NC}"
    }

    # Deploy to DigitalOcean App Platform
    echo "Deploying to DigitalOcean App Platform..."
    if [ -f "./deploy.sh" ]; then
        ./deploy.sh production
    else
        # Direct deployment via doctl
        APP_ID=$(doctl apps list --format Name,ID | grep "$APP_NAME" | awk '{print $2}' | head -1)
        [ -n "$APP_ID" ] && doctl apps create-deployment --wait "$APP_ID" || {
            echo -e "${YELLOW}⚠ Auto-deployment failed, deploy via DigitalOcean console${NC}"
        }
    fi

    echo -e "${GREEN}✓ Deployment initiated${NC}"

    # Check deployment status
    echo -e "\n${BLUE}--- Deployment Status ---${NC}"
    sleep 30
    [ -f "./status.sh" ] && ./status.sh || echo -e "${YELLOW}⚠ Check deployment at: https://cloud.digitalocean.com/apps${NC}"

else
    echo -e "\n${GREEN}--- Local Development Deployment ---${NC}"
    cd "$PROJECT_ROOT"

    # Validate docker-compose
    command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1 || {
        echo -e "${RED}❌ docker-compose required${NC}"
        exit 1
    }
    [ -f "local/docker-compose.yml" ] || { echo -e "${RED}❌ local/docker-compose.yml not found${NC}"; exit 1; }

    # Stop existing containers
    docker-compose -f local/docker-compose.yml down --remove-orphans 2>/dev/null || true

    # Start local services
    echo "Starting local containers..."
    docker-compose -f local/docker-compose.yml up --build -d
    echo -e "${GREEN}✓ Local deployment completed${NC}"

    # Display service information
    echo -e "\n${BLUE}--- Local Services ---${NC}"
    echo "🌐 Frontend: http://localhost:$LOCAL_FRONTEND_PORT"
    echo "🔧 MCP API: http://localhost:$LOCAL_API_PORT"
    echo "🗄️  LocalStack: http://localhost:4566"

    # Wait and check service health
    echo -e "\n${YELLOW}--- Checking Service Health ---${NC}"
    sleep 10

    curl -s http://localhost:$LOCAL_API_PORT/health >/dev/null 2>&1 &&
        echo -e "${GREEN}✓ MCP API is healthy${NC}" ||
        echo -e "${YELLOW}⚠ MCP API not yet ready${NC}"

    curl -s http://localhost:$LOCAL_FRONTEND_PORT >/dev/null 2>&1 &&
        echo -e "${GREEN}✓ Frontend is healthy${NC}" ||
        echo -e "${YELLOW}⚠ Frontend not yet ready${NC}"
fi

echo -e "\n${GREEN}🎉 Deployment completed for $TARGET environment!${NC}"

# Environment-specific notes
if [ "$TARGET" = "production" ]; then
    echo "Production deployment:"
    echo "  - Monitor: https://cloud.digitalocean.com/apps"
    echo "  - Check logs in DigitalOcean console"
    echo "  - Update DNS if needed"
else
    echo "Local deployment:"
    echo "  - Frontend: http://localhost:$LOCAL_FRONTEND_PORT"
    echo "  - API docs: http://localhost:$LOCAL_API_PORT/docs"
    echo "  - Stop: docker-compose -f local/docker-compose.yml down"
fi