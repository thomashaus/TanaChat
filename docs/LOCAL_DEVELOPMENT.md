# Local Development with LocalStack

This guide covers setting up and using LocalStack for local TanaChat development with S3-compatible storage.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12+
- Node.js 18+
- AWS CLI (optional, for manual S3 operations)

### 1. Start Local Development Stack

```bash
# Start all services including LocalStack
docker-compose -f local/docker-compose.yml up -d

# Check all containers are running
docker ps | grep tanachat
```

This starts:
- **tanachat-app**: React frontend (http://localhost:5173)
- **tanachat-mcp**: MCP + API server (http://localhost:8000)
- **tanachat-localstack**: S3-compatible storage (http://localhost:4566)

### 2. Setup LocalStack S3 Storage

```bash
# Run the automated setup script
./local/setup-localstack.sh
```

Or manually:

```bash
# Create bucket
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3 mb s3://tanachat-local --region us-east-1

# Create metadata structure
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3api put-object \
  --bucket tanachat-local --key "metadata/" --content-length 0
```

### 3. Verify Setup

```bash
# Test LocalStack health
curl http://localhost:4566/_localstack/health

# Test MCP server health
curl http://localhost:8000/health

# Test MCP integration with LocalStack
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_auth_status","arguments":{}}}'

# Test API documentation
open http://localhost:8000/docs
```

## 📁 LocalStack Configuration

### Environment Variables

The MCP server uses these LocalStack-specific environment variables:

```bash
S3_ENDPOINT=http://localstack:4566
S3_ACCESS_KEY=test
S3_SECRET_KEY=test
S3_BUCKET=tanachat-local
```

### Bucket Structure

```
tanachat-local/
├── metadata/
│   ├── users.json          # User registry
│   └── config.json         # App configuration
├── users/                  # User-specific data
│   └── [username]/
└── import/                 # Tana import files
```

## 🛠 Development Workflow

### 1. Local Development

```bash
# Start services
docker-compose -f local/docker-compose.yml up -d

# View logs
docker-compose -f local/docker-compose.yml logs -f

# Stop services
docker-compose -f local/docker-compose.yml down
```

### 2. Create Test Users

```bash
# Interactive user creation
./bin/tanachat-createuser

# Non-interactive with test data
./bin/tanachat-createuser \
  --name "Test User" \
  --username test \
  --email test@example.com \
  --tana-key test-key \
  --non-interactive
```

### 3. Test S3 Operations

```bash
# List buckets
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3 ls

# List bucket contents
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3 ls s3://tanachat-local/ --recursive

# Upload a file
echo "test data" > /tmp/test.txt
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
  aws --endpoint-url=http://localhost:4566 s3 cp /tmp/test.txt s3://tanachat-local/test.txt
```

## 🔧 Troubleshooting

### LocalStack Issues

**Port Already in Use**
```bash
# Kill process on port 4566
lsof -ti:4566 | xargs kill -9
```

**Container Not Starting**
```bash
# Check logs
docker logs tanachat-localstack

# Recreate container
docker-compose -f local/docker-compose.yml down
docker-compose -f local/docker-compose.yml up -d localstack
```

**S3 Connection Errors**
```bash
# Verify LocalStack is running
curl http://localhost:4566/_localstack/health

# Check network connectivity
docker network ls | grep tanachat
docker network inspect local_tanachat
```

### MCP Server Issues

**Authentication Errors**
```bash
# Check environment variables
docker exec tanachat-mcp env | grep -E "(S3_|BUCKET)"

# Restart MCP service
docker restart tanachat-mcp

# Check MCP logs
docker logs tanachat-mcp | tail -20
```

**Tools Not Working**
```bash
# Test MCP connection
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Test specific tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"check_auth_status","arguments":{}}}'
```

## 🧪 Testing

### Run Local Tests

```bash
# Test all local services
python tests/test-all-local.py

# Test specific components
python tests/local/test_mcp.py
python tests/local/test_api.py
python tests/local/test_www.py
```

### Manual Testing Checklist

- [ ] LocalStack S3 service running
- [ ] MCP server healthy on port 8000
- [ ] React app loads on port 5173
- [ ] MCP tools respond correctly
- [ ] User creation works
- [ ] S3 bucket accessible
- [ ] API documentation loads

## 📊 Monitoring

### Container Health

```bash
# Check all containers
docker ps

# Container resource usage
docker stats

# Container logs
docker-compose -f local/docker-compose.yml logs -f tanachat-mcp
```

### LocalStack Monitoring

```bash
# LocalStack health
curl http://localhost:4566/_localstack/health

# S3 service status
curl http://localhost:4566/_localstack/health | jq '.services.s3'
```

### Application Monitoring

```bash
# MCP server metrics
curl http://localhost:8000/metrics

# Application logs
docker logs tanachat-mcp | grep -E "(ERROR|WARN|INFO)"
```

## 🔄 Reset Local Environment

```bash
# Stop and remove containers
docker-compose -f local/docker-compose.yml down -v

# Remove LocalStack data
rm -rf local/tmp/localstack-data/

# Recreate bucket structure
./local/setup-localstack.sh

# Restart services
docker-compose -f local/docker-compose.yml up -d
```

## 🚀 Production Differences

| Feature | Local (LocalStack) | Production |
|---------|-------------------|------------|
| S3 Endpoint | `http://localstack:4566` | `https://nyc3.digitaloceanspaces.com` |
| Bucket Name | `tanachat-local` | `tanachat` |
| Access Keys | `test/test` | Real DO Spaces keys |
| Domain | `localhost:*` | `*.tanachat.ai` |
| TLS | HTTP only | HTTPS enforced |

## 📚 Additional Resources

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [AWS S3 CLI Commands](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)