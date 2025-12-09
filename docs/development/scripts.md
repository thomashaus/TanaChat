# Build & Deploy Scripts

TanaChat provides comprehensive automation scripts for building and deploying applications across different environments.

## Script Overview

### Main Scripts

| Script | Purpose | Environment |
|--------|---------|-------------|
| `build-and-deploy.sh` | Complete build and deploy pipeline | local, production |
| `build.sh` | Build components and Docker images | local, production |
| `deploy.sh` | Deploy to target environment | local, production |

### Utility Scripts

| Script | Purpose |
|--------|---------|
| `setup.sh` | Install project dependencies |
| `test.sh` | Run test suites |
| `seed-samples.sh` | Load sample data |
| `validate-samples.sh` | Validate sample data integrity |

## Usage

### Complete Pipeline
```bash
# Local development with validation
./scripts/build-and-deploy.sh local

# Production deployment with registry push
./scripts/build-and-deploy.sh production
```

### Individual Operations
```bash
# Build only (no deployment)
./scripts/build.sh production

# Deploy only (assumes images built)
./scripts/deploy.sh production
```

## Environment Variables

### Required for Production
- `PROD_TOKEN`: DigitalOcean API token
- `PROD_REGISTRY_NAME`: Container registry URL

### Optional Configuration
- `DOCKER_APP_IMAGE`: Frontend image name (default: `tanachat-app`)
- `DOCKER_MCP_IMAGE`: MCP image name (default: `tanachat-mcp`)
- `DOCKER_TAG`: Image tag (default: `latest`)
- `APP_NAME`: Application name (default: `tanachat`)

## Script Flow

### build-and-deploy.sh
1. **Cleanup**: Remove old containers and build artifacts
2. **Validate**: Check required tools and environment variables
3. **Build**: Execute build script for target environment
4. **Deploy**: Execute deploy script for target environment
5. **Test**: Run deployment validation and tests

### build.sh
1. **Frontend**: Build React application (development or production)
2. **MCP**: Install Python dependencies and build API
3. **Docker**: Build container images (production only)
4. **Registry**: Push images to registry (production only)
5. **Security**: Run gitleaks security scan (production only)

### deploy.sh
- **Local**: Start services with docker-compose
- **Production**: Deploy to DigitalOcean App Platform

## Error Handling

All scripts include:
- Input validation with clear error messages
- Exit on error (`set -e`)
- Progress indicators and colored output
- Rollback information for failed deployments

## Requirements

### Local Development
- Docker & docker-compose
- Node.js 18+
- Python 3.12+
- uv (Python package manager)

### Production Deployment
- All local requirements
- DigitalOcean CLI (`doctl`)
- Container registry access
- Authenticated DigitalOcean account