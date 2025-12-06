# TanaChat API

FastAPI backend for TanaChat.ai with authentication, file management, and Tana workspace integration.

## Features

- **Authentication**: JWT-based user authentication and authorization
- **File Management**: Secure file upload and download with S3 storage integration
- **Tana Integration**: API endpoints for Tana workspace import, export, and analysis
- **User Management**: Multi-user support with data isolation
- **Health Monitoring**: Health check endpoints for monitoring

## API Endpoints

- `/api/health` - Health check
- `/api/auth/login` - User authentication
- `/api/tana/upload` - Tana file upload
- `/api/tana/files` - File management
- `/api/spaces/*` - S3 storage integration

## Development

### Setup

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

### Environment Variables

See `.env.example` for required environment variables:

- `TANA_API_KEY` - Tana API key
- `S3_ACCESS_KEY` - S3 storage access key
- `S3_SECRET_KEY` - S3 storage secret key
- `S3_REGION` - S3 storage region
- `S3_BUCKET` - S3 storage bucket name
- `SECRET_KEY` - JWT secret key

## API Documentation

When running locally, visit:
- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## License

MIT License - see LICENSE file in root directory.