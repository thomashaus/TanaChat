#!/bin/bash
# Build and deploy TanaChat to target environment
#
# Usage: scripts/build-and-deploy.sh [local|production]
#   local: Build and run locally with docker-compose
#   production: Build, push to registry, and deploy to DigitalOcean
#
# Requirements:
#   local: Docker, docker-compose, Node.js, Python 3.12+
#   production: Docker, doctl, PROD_TOKEN, PROD_REGISTRY_NAME

set -e
TARGET=${1:-local}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment variables from .env or .env.local
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

if [ -f "$PROJECT_ROOT/.env.local" ]; then
    set -a
    source "$PROJECT_ROOT/.env.local"
    set +a
fi

# Load production-specific environment variables for production target
if [ "$TARGET" = "production" ] && [ -f "$PROJECT_ROOT/.do/env.local" ]; then
    set -a
    source "$PROJECT_ROOT/.do/env.local"
    set +a
    echo "✓ Loaded production environment from .do/env.local"
fi

# Configuration defaults
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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print step headers
print_step() {
    echo -e "\n${BLUE}=== Step $1: $2 ===${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print info
print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

echo -e "${CYAN}🚀 TanaChat.ai Build & Deploy Pipeline${NC}"
echo -e "${CYAN}Target: $TARGET environment${NC}"
echo -e "${CYAN}Timestamp: $(date)${NC}"

# Step 1: Cleanup previous builds and containers
print_step "1" "Cleanup Target Environment"

if [ "$TARGET" = "production" ]; then
    # Remove build artifacts
    [ -d "$PROJECT_ROOT/app/dist" ] && rm -rf "$PROJECT_ROOT/app/dist"
    print_success "Cleaned frontend build artifacts"

    # Remove old Docker images
    docker images $DOCKER_APP_IMAGE | grep -v REPOSITORY | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
    docker images $DOCKER_MCP_IMAGE | grep -v REPOSITORY | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
    print_success "Cleaned up old Docker images"
else
    # Stop local containers
    cd "$PROJECT_ROOT"
    [ -f "local/docker-compose.yml" ] && docker-compose -f local/docker-compose.yml down --remove-orphans 2>/dev/null || true
    print_success "Stopped local containers"

    # Remove build artifacts
    [ -d "$PROJECT_ROOT/app/dist" ] && rm -rf "$PROJECT_ROOT/app/dist"
    print_success "Cleaned frontend build artifacts"
fi

print_success "Step 1 completed: Target cleaned up"

# Step 2: Validate tools and environment
print_step "2" "Readiness Check and Environment Validation"

# Check required tools
command -v node >/dev/null 2>&1 || { print_error "Node.js required. Install from https://nodejs.org"; exit 1; }
command -v python3 >/dev/null 2>&1 || { print_error "Python 3.12+ required"; exit 1; }
command -v docker >/dev/null 2>&1 || { print_error "Docker required"; exit 1; }
print_success "Required tools are available"

# Environment-specific validation
if [ "$TARGET" = "production" ]; then
    # Check required production variables
    MISSING_VARS=""
    [ -z "$PROD_TOKEN" ] && MISSING_VARS="$MISSING_VARS PROD_TOKEN"
    [ -z "$PROD_REGISTRY_NAME" ] && MISSING_VARS="$MISSING_VARS PROD_REGISTRY_NAME"

    [ -n "$MISSING_VARS" ] && {
        print_error "Missing production environment variables:$MISSING_VARS"
        echo "Set these in your environment or .do/env.local file"
        exit 1
    }

    # Validate DigitalOcean access
    command -v doctl >/dev/null 2>&1 || { print_error "doctl required for production deployment"; exit 1; }
    doctl account get >/dev/null 2>&1 || { print_error "DigitalOcean authentication failed. Run 'doctl auth init'"; exit 1; }
    [ -d "$PROJECT_ROOT/.do" ] || { print_error ".do directory not found. Required for production deployment."; exit 1; }

    print_success "DigitalOcean authentication verified"
else
    # Validate local deployment requirements
    command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1 || {
        print_error "docker-compose required for local deployment"
        exit 1
    }
    [ -f "$PROJECT_ROOT/local/docker-compose.yml" ] || { print_error "local/docker-compose.yml not found"; exit 1; }
fi

print_success "Step 2 completed: Environment ready and validated"

# Step 3: Build components and Docker images
print_step "3" "Build Images for $TARGET Environment"

cd "$PROJECT_ROOT"
[ -f "scripts/build.sh" ] || { print_error "build.sh not found in scripts directory"; exit 1; }
./scripts/build.sh "$TARGET" || { print_error "Build script failed"; exit 1; }
print_success "Build script completed successfully"

print_success "Step 3 completed: Images built for $TARGET environment"

# Step 4: Deploy to target environment
print_step "4" "Deploy to $TARGET Environment"

cd "$PROJECT_ROOT"
if [ "$TARGET" = "production" ]; then
    # Use .do/deploy.sh for production deployment
    [ -f ".do/deploy.sh" ] || { print_error ".do/deploy.sh not found"; exit 1; }
    cd .do
    ./deploy.sh production || { print_error "Production deploy script failed"; exit 1; }
    cd ..
    print_success "Production deploy script completed successfully"
else
    # Use scripts/deploy.sh for local deployment
    [ -f "scripts/deploy.sh" ] || { print_error "deploy.sh not found in scripts directory"; exit 1; }
    ./scripts/deploy.sh "$TARGET" || { print_error "Deploy script failed"; exit 1; }
    print_success "Deploy script completed successfully"
fi

print_success "Step 4 completed: Deployed to $TARGET environment"

# Step 5: Validate deployment and test services
print_step "5" "Deployment Validation and Testing"

if [ "$TARGET" = "production" ]; then
    # Production deployment validation
    if command -v doctl >/dev/null 2>&1; then
        cd "$PROJECT_ROOT/.do"
        APP_ID=$(doctl apps list --format Name,ID | grep "$APP_NAME" | awk '{print $2}' | head -1)

        if [ -n "$APP_ID" ]; then
            echo "Checking deployment status..."
            sleep 30  # Allow deployment to start

            # Monitor deployment status (wait up to 10 minutes)
            for i in {1..20}; do
                STATUS=$(doctl apps get-deployment "$APP_ID" --format State | tail -1)
                echo "Deployment status: $STATUS"

                [ "$STATUS" = "ACTIVE" ] && { print_success "Deployment is active and healthy"; break; }
                [ "$STATUS" = "FAILED" ] && {
                    print_error "Deployment failed"
                    doctl apps get-deployment "$APP_ID" --format Progress,Cause
                    exit 1
                }
                sleep 30
            done

            # Test production URL
            APP_URL=$(doctl apps get "$APP_ID" --format URL | tail -1)
            [ -n "$APP_URL" ] && {
                print_info "Production URL: $APP_URL"
                curl -s -f "$APP_URL" >/dev/null 2>&1 && print_success "Production endpoint is responding" || print_warning "Production endpoint not yet ready"
            }
        else
            print_warning "Could not find app ID for status checking"
        fi
    fi
else
    # Local deployment validation
    cd "$PROJECT_ROOT"
    echo "Waiting for services to start..."
    sleep 15

    # Test frontend
    curl -s -f http://localhost:$LOCAL_FRONTEND_PORT >/dev/null 2>&1 &&
        print_success "Frontend is running on http://localhost:$LOCAL_FRONTEND_PORT" ||
        print_warning "Frontend not yet ready"

    # Test MCP API
    curl -s -f http://localhost:$LOCAL_API_PORT/health >/dev/null 2>&1 &&
        print_success "MCP API is running on http://localhost:$LOCAL_API_PORT" ||
        curl -s -f http://localhost:$LOCAL_API_PORT >/dev/null 2>&1 &&
        print_success "MCP API is running on http://localhost:$LOCAL_API_PORT" ||
        print_warning "MCP API not yet ready"

    # Check LocalStack
    docker ps | grep -q "localstack/localstack" &&
        print_success "LocalStack is running" ||
        print_warning "LocalStack not detected"
fi

# Run deployment tests
[ -f "scripts/test.sh" ] && {
    echo "Running deployment tests..."
    # Export environment variables for test script
    export LOCAL_FRONTEND_PORT LOCAL_API_PORT
    export PROD_TOKEN PROD_REGISTRY_NAME
    if [ "$TARGET" = "production" ] && [ -f ".do/env.local" ]; then
        export $(grep -v '^#' .do/env.local | xargs)
    fi
    ./scripts/test.sh "$TARGET" && print_success "Deployment tests passed" || print_warning "Deployment tests had issues"
} || print_warning "No test script found, skipping automated tests"

print_success "Step 5 completed: Deployment validated and tested"

# Final summary
echo -e "\n${CYAN}🎉 Build & Deploy Pipeline Completed${NC}"
echo -e "${CYAN}Target: $TARGET | Completed: $(date)${NC}"

if [ "$TARGET" = "production" ]; then
    echo -e "\n${GREEN}Production Deployment Summary:${NC}"
    echo "  - Deployed to DigitalOcean App Platform"
    echo "  - Images built and pushed to container registry"
    echo "  - Monitor at: https://cloud.digitalocean.com/apps"
    [ -n "$APP_URL" ] && echo "  - Live URL: $APP_URL"
else
    echo -e "\n${GREEN}Local Deployment Summary:${NC}"
    echo "  - Frontend: http://localhost:$LOCAL_FRONTEND_PORT"
    echo "  - MCP API: http://localhost:$LOCAL_API_PORT (docs: /docs)"
    echo "  - LocalStack: http://localhost:4566"
    echo "  - Stop: docker-compose -f local/docker-compose.yml down"
fi