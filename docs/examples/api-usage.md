# API Usage Examples

This document provides examples of how to use the TanaChat.ai API with sample data.

## Authentication

All API endpoints (except `/health` and `/register`) require authentication.

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d @samples/api/requests/register.json
```

Response:
```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "created_at": "2024-01-23T17:30:00.000Z"
}
```

### Login to get token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d @samples/api/requests/login.json
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

### Using the token

```bash
TOKEN="YOUR_JWT_TOKEN"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/health
```

## Tana File Operations

### Validate a Tana file

```bash
# Valid file
curl -X POST http://localhost:8000/api/tana/validate \
  -H "Content-Type: application/json" \
  -d @samples/tana/imports/valid/minimal.json

# Invalid file (will return errors)
curl -X POST http://localhost:8000/api/tana/validate \
  -H "Content-Type: application/json" \
  -d @samples/tana/imports/invalid/missing-version.json
```

Valid file response:
```json
{
  "valid": true,
  "version": "TanaIntermediateFile V0.1",
  "node_count": 1,
  "supertags": [],
  "summary": {
    "leaf_nodes": 1,
    "total_nodes": 1
  }
}
```

Invalid file response:
```json
{
  "valid": false,
  "error": "Tana validation error",
  "details": "Missing required field: version"
}
```

### Upload a Tana file

```bash
curl -X POST http://localhost:8000/api/tana/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@samples/tana/imports/valid/with-supertags.json" \
  -F "description=Sample file with supertags"
```

Response:
```json
{
  "success": true,
  "file_id": "tana_file_20240123_173045_abc123",
  "original_filename": "with-supertags.json",
  "size": 1245,
  "stored_at": "spaces://tanachat/tana-files/...",
  "validation": {
    "valid": true,
    "version": "TanaIntermediateFile V0.1",
    "node_count": 3,
    "supertags": ["Project", "Task", "Active"]
  }
}
```

### List uploaded files

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tana/files
```

### Download a file

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tana/files/tana_file_20240123_173045_abc123 \
  -o downloaded_file.json
```

## Advanced Queries

### Find nodes by type

```bash
curl -X POST http://localhost:8000/api/tana/find \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "tana_file_20240123_173045_abc123",
    "query": {
      "type": "node",
      "todo_state": "todo"
    }
  }'
```

### Search by content

```bash
curl -X POST http://localhost:8000/api/tana/search \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "tana_file_20240123_173045_abc123",
    "text": "design"
  }'
```

## Error Handling

### Common error responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 413 Payload Too Large
```json
{
  "detail": "File too large. Maximum size is 10MB"
}
```

## Using with HTTPie (easier than curl)

```bash
# Install HTTPie
pip install httpie

# Examples with httpie
http POST localhost:8000/api/tana/validate < samples/tana/imports/valid/minimal.json

http --auth bearer:$TOKEN POST localhost:8000/api/tana/upload \
  file@samples/tana/imports/valid/with-supertags.json \
  description="Sample upload"
```

## Testing with Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "john_doe", "password": "SecureP@ssw0rd123!"}
)
token = response.json()["access_token"]

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Validate file
with open("samples/tana/imports/valid/minimal.json") as f:
    file_content = f.read()

response = requests.post(
    f"{BASE_URL}/api/tana/validate",
    headers=headers,
    data=file_content
)

print(response.json())
```

## Rate Limits

The API implements rate limiting:
- **Validation endpoint**: 100 requests per minute
- **Upload endpoint**: 10 requests per minute
- **Other endpoints**: 1000 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1642972800
```