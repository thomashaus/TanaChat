# Environment Variables Guide

This guide explains how to configure TanaChat using environment variables. All URLs, tokens, and sensitive configuration should use environment variables instead of hardcoded values.

## Quick Start

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Fill in your actual values in `.env`

3. For production, ensure these are set in your deployment environment

## Required Environment Variables

### API Server URLs
- `LOCAL_API_URL` - Local API server URL (default: http://localhost:8000)
- `LOCAL_MCP_URL` - Local MCP server URL (default: http://localhost:8000)
- `LOCAL_APP_URL` - Local app URL (default: http://localhost:3000)
- `PROD_API_URL` - Production API server URL (default: https://api.tanachat.ai)
- `PROD_MCP_URL` - Production MCP server URL (default: https://mcp.tanachat.ai)
- `PROD_APP_URL` - Production app URL (default: https://tanachat.ai)
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated or *)
- `API_SECRET_KEY` - Secret key for JWT tokens

### DigitalOcean Spaces
- `SPACES_ACCESS_KEY` - DigitalOcean Spaces access key
- `SPACES_SECRET_KEY` - DigitalOcean Spaces secret key
- `SPACES_BUCKET` - Spaces bucket name (default: tanachat)
- `SPACES_REGION` - Spaces region (default: nyc3)
- `SPACES_ENDPOINT` - Spaces endpoint URL

### Tana Integration
- `TANA_API_KEY` - Your Tana API key

## Environment Variable Naming Convention

### URLs
- Local development: `LOCAL_*_URL`
- Production: `PRODUCTION_*_URL`
- API base: `API_BASE_URL` or `API_URL`

### Tokens and Keys
- `*_TOKEN` - Authentication tokens
- `*_KEY` - API keys or secret keys
- `*_SECRET` - Secret values

### Regional Configuration
- `*_REGION` - AWS/Spaces regions
- `*_ENDPOINT` - Service endpoints
- `*_BUCKET` - Storage bucket names

## Usage Examples

### In Python Code
```python
import os

# Get API URL with fallback
api_url = os.getenv("API_BASE_URL", "http://localhost:8000")

# Get Spaces configuration
spaces_key = os.getenv("SPACES_ACCESS_KEY")
spaces_secret = os.getenv("SPACES_SECRET_KEY")

# Must have environment variables
required_token = os.environ["TANA_API_KEY"]  # Raises exception if not set
```

### In React/Vite Frontend
```javascript
// Vite automatically makes VITE_* variables available
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// During build, these get replaced with actual values
const cdnUrl = import.meta.env.VITE_CDN_URL;
```

### In Tests
```python
# Tests should use environment variables for all external URLs
api_url = os.getenv("API_BASE_URL", "http://localhost:8000")
frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
production_url = os.getenv("PRODUCTION_API_URL", "https://mcp.tanachat.ai")
```

### In Shell Scripts
```bash
#!/bin/bash
# Use environment variables for all external services
API_URL="${API_BASE_URL:-http://localhost:8000}"
SPACES_ENDPOINT="${SPACES_ENDPOINT:-https://nyc3.digitaloceanspaces.com}"
```

## Environment Files

### `.env` (Local Development)
For local development. Never commit this file.

### `.env.example` (Template)
Committed to git. Shows all available environment variables.

### `.env.test` (Testing)
For test configurations.

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use different values for each environment** - dev, staging, production
3. **Rotate keys regularly** - Especially for production
4. **Use secure storage** - Docker secrets, Kubernetes secrets, or cloud KMS
5. **Least privilege principle** - Only grant necessary permissions

## Environment Variables by Component

### Backend (FastAPI/MCP Server)
```bash
API_BASE_URL=http://localhost:8000
TANA_API_KEY=your_tana_key
SPACES_ACCESS_KEY=your_spaces_key
SPACES_SECRET_KEY=your_spaces_secret
SPACES_BUCKET=tanachat
SPACES_REGION=nyc3
SPACES_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

### Frontend (React/Vite)
```bash
VITE_API_URL=http://localhost:8000
VITE_CDN_URL=https://cdn.tanachat.ai
```

### Tests
```bash
API_BASE_URL=http://localhost:8000
FRONTEND_BASE_URL=http://localhost:5173
PRODUCTION_API_URL=https://mcp.tanachat.ai
PRODUCTION_FRONTEND_URL=https://tanachat.ai
TEST_TIMEOUT=30
```

### Deployment
```bash
DO_TOKEN=dop_v1_your_token
API_BASE_URL=https://mcp.tanachat.ai
PRODUCTION_FRONTEND_URL=https://tanachat.ai
```

## Validation

Before deployment, verify all required variables are set:

```python
import os

required_vars = [
    "TANA_API_KEY",
    "SPACES_ACCESS_KEY",
    "SPACES_SECRET_KEY"
]

missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing required environment variables: {missing}")
```

## Debugging

### Check Current Environment
```bash
# Show all environment variables
env | grep -E "(API_|SPACES_|TANA_|VITE_)"

# Show specific variable
echo $API_BASE_URL
```

### Test Configuration
```python
import os
from src.config import settings

print(f"API URL: {settings.api_url}")
print(f"Spaces bucket: {settings.s3_bucket}")
print(f"Tana API configured: {bool(settings.tana_api_key)}")
```

## Common Issues

### Hardcoded URLs in Code
Symptom: Application works locally but fails in production
Solution: Replace hardcoded URLs with environment variables

### Missing Environment Variables
Symptom: KeyError or missing values
Solution: Set all required variables in deployment environment

### Default Values
Symptom: Wrong environment being used
Solution: Ensure correct `.env` file or environment variables are set