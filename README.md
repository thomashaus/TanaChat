# TanaChat.ai

**AI-powered platform with MCP server, API, and web interface for Tana workspace management and analysis.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18](https://img.shields.io/badge/node.js-18-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.x-blue.svg)](https://www.typescriptlang.org/)

## 🎯 What is TanaChat.ai?

TanaChat.ai is a comprehensive AI-powered platform for **Tana workspace management** that provides multiple interfaces for working with Tana data:

- **CLI Tools** for power users and automation
- **REST API** for programmatic access
- **Web Interface** for casual users
- **MCP Server** for AI assistant integration

### Key Capabilities

✅ **AI Chat Interface**: Simulate conversations with your Tana workspace
✅ **Import & Export**: Convert Tana JSON exports to organized markdown
✅ **Content Analysis**: Deep analysis of workspace structure and patterns
✅ **API Integration**: Post content directly to Tana nodes
✅ **User Management**: Secure authentication with data isolation
✅ **Cloud Storage**: S3/Spaces storage integration

## 🏗 Architecture

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + MCP Protocol + Python 3.12 + Pydantic (single unified service)
- **CLI Tools**: Click + Python 3.12
- **Database**: PostgreSQL (production) / SQLite (development)
- **Storage**: DigitalOcean Spaces (S3 compatible)
- **Authentication**: JWT tokens
- **Deployment**: Docker + DigitalOcean App Platform

### Simplified Service Architecture
- **2 Services Only**: Frontend (React) + Backend (MCP Server with FastAPI)
- **Unified Backend**: MCP server provides both REST API and MCP protocol
- **Independent Scaling**: Each service can be scaled and deployed separately
- **Clean Separation**: Frontend focuses on UI, Backend handles all business logic

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**: [Install Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Install Node.js](https://nodejs.org/)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **DigitalOcean Account**: [Create account](https://www.digitalocean.com/)
- **Tana API Key**: Get from [Tana Settings](https://tana.inc/)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/thomashaus/TanaChat.git
cd TanaChat

# Run the automated setup
make setup

# Manual setup (if make fails):
# Install Python dependencies
cd api && pip install -e . && cd ..
cd mcp && pip install -e . && cd ..

# Install Node.js dependencies
cd app && npm install && cd ..

# Install CLI tools in development mode
pip install -e .
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your credentials
nano .env.local  # or your preferred editor
```

**Required Environment Variables:**

```bash
# Tana Integration
TANA_API_KEY=your_tana_api_key_here

# Database
DATABASE_URL=sqlite:///./tanachat.db  # Development
# DATABASE_URL=postgresql://user:pass@host:port/dbname  # Production

# Storage (DigitalOcean Spaces or S3)
S3_ACCESS_KEY=your_spaces_access_key
S3_SECRET_KEY=your_spaces_secret_key
S3_BUCKET=tanachat
S3_REGION=nyc3
S3_ENDPOINT=https://nyc3.digitaloceanspaces.com

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here
API_SECRET_KEY=your_api_secret_key_here

# Frontend
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Services

```bash
# Option 1: Docker Local Development (Recommended)
docker-compose -f local/docker-compose.yml up -d

# Option 2: Native Development
make dev

# Or start individual services:
make dev-app    # Frontend only (http://localhost:5173)
make dev-api    # API only (http://localhost:8000)
make dev-mcp    # MCP server only (http://localhost:8001)
```

### 4. Setup LocalStack for Docker Development

If using Docker Compose, setup LocalStack S3 storage:

```bash
# Automated setup
./local/setup-localstack.sh

# Or manual setup
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3 mb s3://tanachat-local
```

### 5. Verify Setup

Once running, visit:
- **Web Interface**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/health
- **MCP Health**: http://localhost:8000/health
- **LocalStack Health**: http://localhost:4566/_localstack/health

## 🛠 Development Guide

### Project Structure

```
TanaChat/
├── app/                    # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── pages/          # Page components
│   │   └── utils/          # Utility functions
│   ├── Dockerfile.do       # Production Dockerfile
│   └── package.json
├── api/                    # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   └── Dockerfile
├── mcp/                    # MCP Server
│   ├── src/
│   │   ├── tools/          # MCP tools
│   │   └── main.py         # Server entry point
│   └── Dockerfile.do
├── bin/                    # CLI tools
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── .do/                    # Deployment configs (git-ignored)
└── docker-compose.yml      # Local development
```

### Development Commands

```bash
# Setup
make setup              # Install all dependencies
make clean              # Clean build artifacts

# Development
make dev                # Start all services
make dev-app            # Frontend development server
make dev-api            # API development server
make dev-mcp            # MCP server development

# Testing
make test               # Run all tests
make test-api           # API tests only
make test-mcp           # MCP tests only
make test-app           # Frontend tests only
make coverage           # Generate coverage report

# Code Quality
make lint               # Lint all code
make lint-api           # Lint Python code
make lint-app           # Lint TypeScript code
make format             # Format all code

# Building
make build              # Build for production
make build-app          # Build frontend
make build-api          # Build API
make build-mcp          # Build MCP server

# Database
make db-init            # Initialize database
make db-migrate         # Run migrations
make db-reset           # Reset database

# Deployment
make deploy             # Deploy to production
make deploy-staging     # Deploy to staging
```

### Working with the MCP Server

The MCP (Model Context Protocol) server provides tools for AI assistants:

```bash
# Test MCP server
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# Call a tool
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "check_auth_status",
      "arguments": {}
    }
  }'
```

Available MCP tools:
- `check_auth_status` - Verify Tana API connection
- `list_spaces_files` - List files in storage
- `validate_tana_file` - Validate Tana file format

### API Development

The FastAPI backend provides REST endpoints:

```bash
# View API documentation
open http://localhost:8000/docs

# Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/auth/status

# Run with auto-reload
cd api && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

The React frontend uses Vite for fast development:

```bash
# Start development server
cd app && npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

## 📦 Docker Development

### Local Development with Docker

```bash
# Start all services with LocalStack
docker-compose -f local/docker-compose.yml up -d

# View logs
docker-compose -f local/docker-compose.yml logs -f

# Stop services
docker-compose -f local/docker-compose.yml down

# Rebuild specific service
docker-compose -f local/docker-compose.yml up -d --build tanachat-mcp

# Setup LocalStack S3 storage
./local/setup-localstack.sh

# Check container status
docker ps | grep tanachat
```

**Services Started:**
- **tanachat-app**: React frontend (http://localhost:5173)
- **tanachat-mcp**: MCP + API server (http://localhost:8000)
- **tanachat-localstack**: S3-compatible storage (http://localhost:4566)

### Production Docker Images

```bash
# Build production images
docker build -f app/Dockerfile.do -t tanachat-app:latest ./app
docker build -f mcp/Dockerfile.do -t tanachat-mcp:latest ./mcp

# Run with Docker
docker run -p 5173:80 tanachat-app:latest
docker run -p 8001:8000 tanachat-mcp:latest
```

## 🚀 Deployment

### DigitalOcean App Platform (Recommended)

1. **Set up Environment:**
   ```bash
   cd .do
   cp env.example env.local
   # Edit env.local with your credentials
   ```

2. **Deploy using CLI:**
   ```bash
   # Install doctl
   curl -sL https://github.com/digitalocean/doctl/releases/latest/download/doctl-$(uname -s)-$(uname -m).tar.gz | tar xz
   sudo mv doctl /usr/local/bin/

   # Authenticate
   doctl auth init

   # Deploy
   doctl apps create --spec appspec.yaml
   ```

3. **Configure Environment Variables:**
   - Set up secrets in App Platform console
   - Configure domains and networking

4. **Monitor Deployment:**
   ```bash
   # Check deployment status
   doctl apps list
   doctl apps list-deployments <app-id>
   ```

### Environment Variables for Production

```bash
# Required
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/dbname
TANA_API_KEY=your_tana_api_key
S3_ACCESS_KEY=your_spaces_access_key
S3_SECRET_KEY=your_spaces_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
API_SECRET_KEY=your_api_secret_key

# Frontend
VITE_API_URL=https://your-api-domain.com
VITE_CDN_URL=https://your-cdn-domain.com

# Optional
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=info
```

## 🔧 Configuration

### Tana Integration

1. **Get API Key:**
   - Go to [Tana Settings](https://tana.inc/settings)
   - Navigate to Developer Options
   - Generate API key

2. **Configure Connection:**
   ```python
   # In your environment
   TANA_API_KEY=your_api_key

   # Test connection
   curl -X POST http://localhost:8001/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "check_auth_status"}}'
   ```

### DigitalOcean Spaces Setup

1. **Create Spaces Bucket:**
   - Go to DigitalOcean Control Panel
   - Create Spaces bucket
   - Note bucket name and region

2. **Generate Access Keys:**
   - Go to Settings → Developer → Spaces access keys
   - Create new access key
   - Save access key and secret

3. **Configure CORS:**
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
       "AllowedOrigins": ["https://yourdomain.com"],
       "MaxAgeSeconds": 3000
     }
   ]
   ```

## 🧪 Testing

```bash
# All tests
make test

# Specific test suites
make test-api      # Backend tests
make test-mcp      # MCP server tests
make test-app      # Frontend tests
make test-integration  # Integration tests

# Coverage report
make coverage

# Specific test file
pytest tests/test_api.py
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process on port
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

**2. Python Dependencies**
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall dependencies
pip install -e . --force-reinstall
```

**3. Node.js Dependencies**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**4. Database Issues**
```bash
# Reset database
make db-reset

# Check connection
python -c "from src.database import engine; print(engine.url)"
```

**5. Docker Issues**
```bash
# Clean Docker system
docker system prune -a
docker volume prune

# Rebuild containers
docker-compose build --no-cache
```

## 📚 API Reference

### REST API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/status` - Check authentication status

#### Tana Integration
- `POST /api/tana/upload` - Upload Tana export
- `GET /api/tana/nodes` - List nodes
- `POST /api/tana/nodes` - Create node
- `GET /api/tana/search` - Search nodes

#### File Management
- `GET /api/files` - List files
- `POST /api/files/upload` - Upload file
- `DELETE /api/files/{file_id}` - Delete file

### MCP Tools

- `check_auth_status` - Verify Tana API connection
- `list_spaces_files` - List files in DigitalOcean Spaces
- `validate_tana_file` - Validate Tana JSON format

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes**: Commit with descriptive messages
4. **Add tests**: Ensure test coverage
5. **Run linting**: `make lint`
6. **Submit PR**: With clear description

### Code Standards

- **Python**: Follow PEP 8, use black for formatting
- **TypeScript**: Use ESLint + Prettier configuration
- **Commits**: Use conventional commit messages
- **Tests**: Maintain >80% coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- **[Local Development Guide](docs/LOCAL_DEVELOPMENT.md)** - Complete LocalStack setup and troubleshooting
- **[MCP Client Setup](docs/MCP_CLIENT_SETUP.md)** - Configure Claude Desktop, Claude Code, and ChatGPT

## 🔗 Links

- **Live Demo**: https://tanachat.ai
- **API Documentation**: https://mcp.tanachat.ai/docs
- **MCP Server**: https://mcp.tanachat.ai
- **Issues**: https://github.com/thomashaus/TanaChat/issues
- **Discussions**: https://github.com/thomashaus/TanaChat/discussions

## 🙏 Acknowledgments

- [Tana](https://tana.inc/) for the amazing note-taking platform
- [FastAPI](https://fastapi.tiangolo.com/) for the modern Python web framework
- [React](https://reactjs.org/) for the user interface library
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework