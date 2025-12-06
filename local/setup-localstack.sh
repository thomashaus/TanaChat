#!/bin/bash
# LocalStack Setup Script for TanaChat Development

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 TanaChat LocalStack Setup${NC}"
echo -e "Date: $(date)"
echo -e "$(printf '─%.0s' {1..50})"

# Configuration
BUCKET_NAME="tanachat-local"
ENDPOINT_URL="http://localhost:4566"
REGION="us-east-1"

echo -e "${BLUE}Configuration:${NC}"
echo -e "  • Bucket: $BUCKET_NAME"
echo -e "  • Endpoint: $ENDPOINT_URL"
echo -e "  • Region: $REGION"

# Check if LocalStack is running
echo -e "\n${YELLOW}Checking LocalStack status...${NC}"
if ! curl -s "$ENDPOINT_URL/_localstack/health" | grep -q '"s3": "running"'; then
    echo -e "❌ LocalStack S3 service is not running"
    echo -e "Please start LocalStack with: docker-compose -f local/docker-compose.yml up -d"
    exit 1
fi

echo -e "${GREEN}✓ LocalStack S3 is running${NC}"

# Create S3 bucket
echo -e "\n${YELLOW}Creating S3 bucket...${NC}"
if AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 ls | grep -q "$BUCKET_NAME"; then
    echo -e "${GREEN}✓ Bucket $BUCKET_NAME already exists${NC}"
else
    AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    echo -e "${GREEN}✓ Created bucket $BUCKET_NAME${NC}"
fi

# Create metadata directory structure
echo -e "\n${YELLOW}Creating metadata structure...${NC}"

# Create initial users.json
USERS_JSON='{"users": [], "version": "1.0", "created": "'$(date -Iseconds)'", "description": "TanaChat users metadata"}'
echo "$USERS_JSON" > /tmp/users.json
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 cp /tmp/users.json "s3://$BUCKET_NAME/metadata/users.json"

# Create initial config.json
CONFIG_JSON='{"app": {"name": "TanaChat", "version": "0.1.0", "environment": "local"}, "features": {"mcp": true, "api": true, "auth": false}, "storage": {"type": "s3", "endpoint": "'$ENDPOINT_URL'", "bucket": "'$BUCKET_NAME'"}}'
echo "$CONFIG_JSON" > /tmp/config.json
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 cp /tmp/config.json "s3://$BUCKET_NAME/metadata/config.json"

# Create user directories structure
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3api put-object --bucket "$BUCKET_NAME" --key "users/" --content-length 0
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3api put-object --bucket "$BUCKET_NAME" --key "import/" --content-length 0

echo -e "${GREEN}✓ Created metadata structure${NC}"

# Verify setup
echo -e "\n${YELLOW}Verifying setup...${NC}"
echo -e "Buckets:"
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 ls

echo -e "\nBucket contents:"
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url="$ENDPOINT_URL" s3 ls "s3://$BUCKET_NAME/" --recursive

echo -e "\n${GREEN}🎉 LocalStack setup complete!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo -e "1. Test MCP server: curl -X POST http://localhost:8000/mcp -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"check_auth_status\",\"arguments\":{}}}'"
echo -e "2. Create a user: ./bin/tanachat-createuser --name 'Test User' --username test"
echo -e "3. Test S3 access: AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test aws --endpoint-url=$ENDPOINT_URL s3 ls s3://$BUCKET_NAME"

# Cleanup temp files
rm -f /tmp/users.json /tmp/config.json