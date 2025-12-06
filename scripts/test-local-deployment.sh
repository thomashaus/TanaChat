#!/bin/bash
# Test local DigitalOcean-style deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Local Deployment Test${NC}"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

# Build and start services
echo -e "\n${YELLOW}Building Docker images...${NC}"
cd "$PROJECT_ROOT"

# Build app image
echo -n "  Building app image... "
docker build -f app/Dockerfile.do -t tanachat-app:test ./app
echo -e "${GREEN}✓${NC}"

# Build API image
echo -n "  Building API image... "
docker build -t tanachat-api:test ./api
echo -e "${GREEN}✓${NC}"

# Build MCP image
echo -n "  Building MCP image... "
docker build -f mcp/Dockerfile.do -t tanachat-mcp:test ./mcp
echo -e "${GREEN}✓${NC}"

# Start services
echo -e "\n${YELLOW}Starting services...${NC}"
docker-compose -f docker-compose.do.yml up -d

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"

wait_for_service() {
    local service_name=$1
    local health_url=$2
    local max_attempts=30
    local attempt=1

    echo -n "  Waiting for $service_name... "
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$health_url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC}"
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
        echo -n "."
    done

    echo -e "${RED}✗${NC}"
    return 1
}

# Check health endpoints
wait_for_service "Frontend" "http://localhost:5173"
wait_for_service "API" "http://localhost:8000/api/health"
wait_for_service "MCP" "http://localhost:8001/health"

# Run integration tests
echo -e "\n${YELLOW}Running integration tests...${NC}"

# Test API health
echo -n "  Testing API health... "
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
fi

# Test S3 connectivity
echo -n "  Testing S3 connectivity... "
if aws --endpoint-url=http://localhost:4566 s3 ls s3://tanachat-test &>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠ (Will be created on first use)${NC}"
fi

# Show service URLs
echo -e "\n${GREEN}🎉 Services are running!${NC}"
echo -e "\nService URLs:"
echo -e "  • Frontend: ${BLUE}http://localhost:5173${NC}"
echo -e "  • API: ${BLUE}http://localhost:8000${NC}"
echo -e "  • API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  • MCP Server: ${BLUE}http://localhost:8001${NC}"
echo -e "  • LocalStack S3: ${BLUE}http://localhost:4566${NC}"

# Show useful commands
echo -e "\n${YELLOW}Useful Commands:${NC}"
echo -e "  • View logs: docker-compose -f docker-compose.do.yml logs -f"
echo -e "  • Stop services: docker-compose -f docker-compose.do.yml down"
echo -e "  • List S3 buckets: aws --endpoint-url=http://localhost:4566 s3 ls"
echo -e "  • Test API: curl http://localhost:8000/api/health"

# Ask if user wants to open browser
echo -e "\n${YELLOW}Would you like to open the application in your browser? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open http://localhost:5173
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5173
    fi
fi

echo -e "\n${GREEN}Test deployment complete!${NC}"