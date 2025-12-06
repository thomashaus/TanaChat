# Local Development Configuration

This directory contains Docker Compose files for local development.

## Files

- **local-docker-app.yml**: Docker Compose for the React web application
- **local-docker-mcp.yml**: Docker Compose for the MCP server

## Usage

### Start the Web App
```bash
cd local
docker-compose -f local-docker-app.yml up -d
```

### Start the MCP Server
```bash
cd local
docker-compose -f local-docker-mcp.yml up -d
```

### Stop Services
```bash
cd local
docker-compose -f local-docker-app.yml down
docker-compose -f local-docker-mcp.yml down
```

## URLs

- Web App: http://localhost:5173
- MCP Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Environment

All services are configured for local development with:
- localhost URLs
- Development environment variables
- Volume mounts for live coding