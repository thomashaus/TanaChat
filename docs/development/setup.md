# Development Setup Guide

This guide covers setting up a complete development environment for TanaChat, including all services (API, Web, MCP) and local infrastructure.

## Prerequisites

- **Docker & Docker Compose**: For running local services and LocalStack.
- **Python 3.12+**: For API and CLI tools (`uv` recommended).
- **Node.js 18+**: For the web frontend.
- **Make**: For running build automation commands.

## 🚀 Quick Start

The fastest way to get started is using the included `Makefile`.

### 1. Clone and Setup

```bash
git clone https://github.com/thomashaus/TanaChat.git
cd TanaChat

# Run automated setup (installs dependencies)
make setup
```

### 2. Configure Environment

Copy the example environment file and configure your keys.

```bash
cp .env.example .env.local
# Edit .env.local with your TANA_API_KEY and other settings
```

### 3. Start Development Services

**Option A: Automated Build & Deploy (Recommended)**

```bash
# Build and run everything locally with validation
./scripts/build-and-deploy.sh local
```

**Option B: Using Make Commands**

```bash
# Starts Web, API, MCP, and LocalStack (S3)
make dev
```

**Option C: Individual Services**

```bash
# Build and deploy individual services
./scripts/build.sh local
./scripts/deploy.sh local

# Or use make commands
make dev-app    # Frontend (localhost:5173)
make dev-api    # API (localhost:8000)
make dev-mcp    # MCP (localhost:8001)
```

## 📦 LocalStack (S3) Setup

We use LocalStack to emulate AWS S3 storage locally.

1. **Start LocalStack**: `docker-compose -f local/docker-compose.yml up -d`
2. **Initialize Bucket**:
   ```bash
   ./local/setup-localstack.sh
   ```

This creates a `tanachat-local` bucket accessible at `http://localhost:4566`.

## 🛠 Common Commands

### Build & Deploy Scripts
```bash
# Complete build and deploy pipeline
./scripts/build-and-deploy.sh [local|production]

# Individual operations
./scripts/build.sh [local|production]
./scripts/deploy.sh [local|production]
```

### Traditional Make Commands
| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make lint` | Lint code (Python & TS) |
| `make format` | Format code |
| `make build` | Build production images |
| `make dev` | Start all development services |

## Troubleshooting

- **Port Conflicts**: Ensure ports 8000 (API), 5173 (Web), and 4566 (LocalStack) are free.
- **Dependencies**: Run `make setup` again if you encounter missing package errors.
- **LocalStack**: If S3 fails, restart the container: `docker-compose -f local/docker-compose.yml restart localstack`
