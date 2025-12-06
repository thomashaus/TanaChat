#!/bin/bash
# Backup script for TanaChat data from DigitalOcean Spaces

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${PROJECT_ROOT}/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
S3_BUCKET=${S3_BUCKET:-"tanachat"}
S3_REGION=${S3_REGION:-"nyc3"}
S3_ENDPOINT=${S3_ENDPOINT:-"https://nyc3.digitaloceanspaces.com"}

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo -e "${GREEN}🔄 Starting TanaChat Backup from Spaces${NC}"
echo -e "Timestamp: $TIMESTAMP"
echo -e "Bucket: $S3_BUCKET"
echo -e "Endpoint: $S3_ENDPOINT"

# Check dependencies
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI not found. Please install it to use S3 backup.${NC}"
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo -e "${RED}Error: AWS credentials not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.${NC}"
    exit 1
fi

# Create backup prefix in Spaces
BACKUP_PREFIX="backups/$TIMESTAMP"
BACKUP_MANIFEST="$BACKUP_DIR/manifest_$TIMESTAMP.json"

echo -e "\n${YELLOW}Backing up from DigitalOcean Spaces...${NC}"

# Initialize manifest
cat > "$BACKUP_MANIFEST" <<EOF
{
    "timestamp": "$TIMESTAMP",
    "bucket": "$S3_BUCKET",
    "endpoint": "$S3_ENDPOINT",
    "files": {},
    "checksums": {}
}
EOF

# Function to backup and add to manifest
backup_file() {
    local source=$1
    local dest=$2
    local description=$3

    if aws --endpoint-url="$S3_ENDPOINT" s3 ls "s3://$S3_BUCKET/$source" &>/dev/null; then
        echo -n "  Backing up $description... "

        # Copy to local backup dir
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$source" "$BACKUP_DIR/$dest" --quiet

        # Copy to backup location in Spaces
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$source" "s3://$S3_BUCKET/$BACKUP_PREFIX/$dest" --quiet

        # Get checksum
        local checksum=$(sha256sum "$BACKUP_DIR/$dest" | cut -d' ' -f1)

        # Update manifest
        jq --arg key "$description" --arg file "$dest" --arg sum "$checksum" \
            '.files[$key] = $file | .checksums[$file] = $sum' \
            "$BACKUP_MANIFEST" > "${BACKUP_MANIFEST}.tmp" && mv "${BACKUP_MANIFEST}.tmp" "$BACKUP_MANIFEST"

        echo -e "${GREEN}✓${NC}"
    else
        echo -e "  ${YELLOW}Skipping $description (not found)${NC}"
    fi
}

# Backup metadata files
backup_file "metadata/users.json" "users.json" "User metadata"
backup_file "metadata/keytags.json" "keytags.json" "Keytags metadata"

# Backup all user files (create a tarball)
echo -n "  Backing up user files... "
FILE_BACKUP="$BACKUP_DIR/files_$TIMESTAMP.tar.gz"
TEMP_FILES_DIR="$BACKUP_DIR/temp_files_$TIMESTAMP"

# Create temp directory and download all files
mkdir -p "$TEMP_FILES_DIR"
aws --endpoint-url="$S3_ENDPOINT" s3 sync "s3://$S3_BUCKET/files/" "$TEMP_FILES_DIR/" --exclude "metadata/*" --quiet 2>/dev/null || true

if [ "$(ls -A "$TEMP_FILES_DIR" 2>/dev/null)" ]; then
    # Create tarball
    tar -czf "$FILE_BACKUP" -C "$TEMP_FILES_DIR" .

    # Upload tarball to backup location
    aws --endpoint-url="$S3_ENDPOINT" s3 cp "$FILE_BACKUP" "s3://$S3_BUCKET/$BACKUP_PREFIX/files.tar.gz" --quiet

    # Add to manifest
    checksum=$(sha256sum "$FILE_BACKUP" | cut -d' ' -f1)
    jq --arg key "User files" --arg file "files.tar.gz" --arg sum "$checksum" \
        '.files[$key] = $file | .checksums[$file] = $sum' \
        "$BACKUP_MANIFEST" > "${BACKUP_MANIFEST}.tmp" && mv "${BACKUP_MANIFEST}.tmp" "$BACKUP_MANIFEST"

    # Clean up
    rm -rf "$TEMP_FILES_DIR"

    echo -e "${GREEN}✓${NC}"
else
    rm -rf "$TEMP_FILES_DIR"
    echo -e "  ${YELLOW}No user files found${NC}"
fi

# Upload manifest to backup location
echo -n "  Uploading backup manifest... "
aws --endpoint-url="$S3_ENDPOINT" s3 cp "$BACKUP_MANIFEST" "s3://$S3_BUCKET/$BACKUP_PREFIX/manifest.json" --quiet
echo -e "${GREEN}✓${NC}"

# Show backup summary
echo -e "\n${GREEN}✅ Backup completed successfully!${NC}"
echo -e "Backup location: s3://$S3_BUCKET/$BACKUP_PREFIX/"
echo -e "Local backup: $BACKUP_DIR"
echo -e "Backup ID: $TIMESTAMP"

# Show what was backed up
echo -e "\n${YELLOW}Backup Contents:${NC}"
jq -r '.files | to_entries[] | "  • \(.key): \(.value)"' "$BACKUP_MANIFEST"

# Cleanup old backups (keep last 10)
echo -e "\n${YELLOW}Cleaning up old backups (keeping last 10)...${NC}"
aws --endpoint-url="$S3_ENDPOINT" s3 ls "s3://$S3_BUCKET/backups/" | \
    awk '{print $2}' | \
    sort -r | \
    tail -n +11 | \
    while read -r backup; do
        if [ -n "$backup" ]; then
            echo -n "  Removing $backup... "
            aws --endpoint-url="$S3_ENDPOINT" s3 rb "s3://$S3_BUCKET/backups/$backup" --force --quiet
            echo -e "${GREEN}✓${NC}"
        fi
    done