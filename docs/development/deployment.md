# Deployment Guide

TanaChat provides automated deployment scripts for both local development and production environments.

## Quick Start

### Local Development
```bash
# Build and run everything locally
./scripts/build-and-deploy.sh local
```

### Production Deployment
```bash
# Build, push to registry, and deploy to DigitalOcean
./scripts/build-and-deploy.sh production
```

## Environment Variables

### Production
Required environment variables for production deployment:
- `PROD_TOKEN`: DigitalOcean API token
- `PROD_REGISTRY_NAME`: Container registry URL (e.g., `registry.digitalocean.com/tanachat`)

### Common
- `DOCKER_APP_IMAGE`: Frontend image name (default: `tanachat-app`)
- `DOCKER_MCP_IMAGE`: MCP image name (default: `tanachat-mcp`)
- `DOCKER_TAG`: Image tag (default: `latest`)
- `APP_NAME`: Application name (default: `tanachat`)

## Individual Script Usage

### Build Script
Build components and Docker images:
```bash
./scripts/build.sh [local|production]
```

- **local**: Builds frontend and sets up MCP for development
- **production**: Builds frontend, MCP, Docker images, and pushes to registry

### Deploy Script
Deploy to target environment:
```bash
./scripts/deploy.sh [local|production]
```

- **local**: Starts services with docker-compose
- **production**: Deploys to DigitalOcean App Platform

## Manual Docker Deployment

For custom deployment environments:

### Build Images
```bash
# Frontend
docker build -f app/Dockerfile.do -t tanachat-app ./app

# Backend / MCP
docker build -f mcp/Dockerfile.do -t tanachat-mcp ./mcp
```

### Environment Variables
Key variables for container deployment:
- `TANA_API_KEY`: Tana API access token
- `S3_ENDPOINT`: S3-compatible storage endpoint
- `S3_ACCESS_KEY` / `S3_SECRET_KEY`: Storage credentials
- `S3_BUCKET`: Storage bucket name

For complete configuration, see [Configuration Guide](configuration.md).
