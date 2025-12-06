#!/bin/bash
# Seed LocalStack with sample Tana files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SAMPLES_DIR="$PROJECT_ROOT/samples"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🌱 Seeding LocalStack with sample files..."

# Check if LocalStack is running
if ! docker ps | grep -q "localstack/localstack"; then
    echo -e "${YELLOW}Warning: LocalStack not running. Start it with:${NC}"
    echo "  docker-compose up -d localstack"
    echo "  Or run: make dev"
    exit 1
fi

# Wait for LocalStack to be ready
echo -n "  Waiting for LocalStack to be ready ..."
for i in {1..30}; do
    if aws --endpoint-url=http://localhost:4566 s3 ls &>/dev/null; then
        echo -e " ${GREEN}✓${NC}"
        break
    fi
    sleep 1
    echo -n "."
done

# Create buckets if they don't exist
BUCKETS=("tanachat" "tanachat-tana-files" "tanachat-uploads")

for bucket in "${BUCKETS[@]}"; do
    echo -n "  Creating bucket $bucket ... "
    if aws --endpoint-url=http://localhost:4566 s3 ls "s3://$bucket" &>/dev/null; then
        echo -e "${YELLOW}Already exists${NC}"
    else
        aws --endpoint-url=http://localhost:4566 s3 mb "s3://$bucket" &>/dev/null
        echo -e "${GREEN}Created${NC}"
    fi
done

# Upload sample Tana files
echo -e "\n${GREEN}--- Uploading Sample Tana Files ---${NC}"

upload_samples() {
    local source_dir="$1"
    local target_prefix="$2"

    if [ ! -d "$source_dir" ]; then
        return
    fi

    echo "  Uploading from $source_dir to s3://tanachat-tana-files/$target_prefix"

    find "$source_dir" -name "*.json" -type f | while read -r file; do
        relative_path="${file#$source_dir/}"
        target_key="$target_prefix/$relative_path"

        echo -n "    $relative_path ... "
        if aws --endpoint-url=http://localhost:4566 s3 cp "$file" "s3://tanachat-tana-files/$target_key" &>/dev/null; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
        fi
    done
}

# Upload valid samples
upload_samples "$SAMPLES_DIR/tana/imports/valid" "samples/valid"

# Upload invalid samples
upload_samples "$SAMPLES_DIR/tana/imports/invalid" "samples/invalid"

# Upload export examples
upload_samples "$SAMPLES_DIR/tana/exports" "samples/exports"

# Create a sample metadata file
echo -e "\n${GREEN}--- Creating Sample Metadata ---${NC}"

metadata=$(cat <<EOF
{
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "description": "Sample Tana files for testing and documentation",
  "samples": {
    "valid": [
      "minimal.json - Smallest valid TIF file",
      "with-supertags.json - Example with supertags",
      "with-fields.json - Example with fields",
      "full-workspace.json - Complete workspace example"
    ],
    "invalid": [
      "missing-version.json - Missing version field",
      "wrong-version.json - Unsupported version",
      "empty-nodes.json - Empty nodes array",
      "missing-uid.json - Node without UID",
      "not-json.txt - Invalid JSON format"
    ]
  },
  "usage": "Use these files with the API endpoint: POST /api/tana/validate"
}
EOF
)

echo "$metadata" > /tmp/sample-metadata.json
aws --endpoint-url=http://localhost:4566 s3 cp /tmp/sample-metadata.json "s3://tanachat-tana-files/samples/metadata.json" &>/dev/null
echo -e "  ${GREEN}✓ Created metadata.json${NC}"

# List uploaded files
echo -e "\n${GREEN}--- Uploaded Files ---${NC}"
aws --endpoint-url=http://localhost:4566 s3 ls --recursive "s3://tanachat-tana-files/samples/" | while read -r line; do
    echo "  $line"
done

# Generate test commands
echo -e "\n${GREEN}--- Test Commands ---${NC}"
echo "  # Test validation with minimal sample"
echo "  curl -X POST http://localhost:8000/api/tana/validate \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d @samples/tana/imports/valid/minimal.json"
echo ""
echo "  # Download sample from LocalStack"
echo "  aws --endpoint-url=http://localhost:4566 s3 cp s3://tanachat-tana-files/samples/valid/minimal.json -"
echo ""
echo "  # List all samples"
echo "  aws --endpoint-url=http://localhost:4566 s3 ls s3://tanachat-tana-files/samples/"

echo -e "\n${GREEN}✓ Seeding complete!${NC}"