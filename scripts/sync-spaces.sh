#!/bin/bash
set -e

echo "☁️  Syncing with S3 storage..."

# Load environment
if [ -f .env.local ]; then
    export $(grep -v '^#' .env.local | xargs)
fi

# Check required vars
if [ -z "$S3_ACCESS_KEY" ] || [ -z "$S3_SECRET_KEY" ]; then
    echo "❌ S3_ACCESS_KEY and S3_SECRET_KEY required in .env.local"
    exit 1
fi

# Configure AWS CLI for S3
export AWS_ACCESS_KEY_ID="$S3_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$S3_SECRET_KEY"

ENDPOINT="${S3_ENDPOINT:-https://s3.amazonaws.com}"
BUCKET="${S3_BUCKET:-tanachat}"

echo "📋 Listing bucket contents..."
aws s3 ls "s3://$BUCKET/" --endpoint-url "$ENDPOINT"

echo ""
echo "✅ Sync complete!"
echo ""
echo "Useful commands:"
echo "  List:   aws s3 ls s3://$BUCKET/ --endpoint-url $ENDPOINT"
echo "  Upload: aws s3 cp file.txt s3://$BUCKET/path/ --endpoint-url $ENDPOINT"
echo "  Download: aws s3 cp s3://$BUCKET/path/file.txt . --endpoint-url $ENDPOINT"
