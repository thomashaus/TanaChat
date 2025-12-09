# API Overview

TanaChat provides both an MCP (Model Context Protocol) server for AI integration and a minimal HTTP API for essential operations.

## Services

### MCP Server (Primary)
The main interface for AI assistant integration.

- **Production**: `https://mcp.tanachat.ai`
- **Local**: `http://localhost:8000`
- **MCP Endpoint**: `https://mcp.tanachat.ai/mcp`

See [MCP Setup](../mcp/setup.md) for integration details.

### HTTP API (Minimal)
Essential web API for user management and health checks.

- **Production**: `https://mcp.tanachat.ai`
- **Local**: `http://localhost:8000`

## Available Endpoints

### Health & Status
- `GET /health`: Server health check
- `GET /`: Server status page

### User Management
- `POST /api/auth/login`: User authentication
- `POST /api/auth/create`: Create new user account
- `GET /api/auth/status`: Check authentication status

### MCP Integration
- `POST /mcp`: Model Context Protocol endpoint for AI assistants

## Authentication

The HTTP API uses JWT tokens for authentication:

```bash
# Get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/auth/status
```

## Development

The API uses FastAPI and supports:
- Interactive docs at `/docs` (local)
- OpenAPI schema at `/openapi.json`
- CORS for frontend integration

For full functionality, use the MCP server interface rather than direct HTTP API calls.
