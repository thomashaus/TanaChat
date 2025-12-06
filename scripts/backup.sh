#!/bin/bash
# Backup script for TanaChat data

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

echo -e "${GREEN}🔄 Starting TanaChat Backup${NC}"
echo -e "Timestamp: $TIMESTAMP"

# Function to backup to local
backup_local() {
    echo -e "\n${YELLOW}Creating local backups...${NC}"

    # Backup files directory
    if [ -d "$PROJECT_ROOT/files" ]; then
        echo -n "  Backing up files directory... "
        tar -czf "$BACKUP_DIR/files_$TIMESTAMP.tar.gz" -C "$PROJECT_ROOT" files/
        echo -e "${GREEN}✓${NC}"
    fi

    # Backup metadata
    if [ -d "$PROJECT_ROOT/files/metadata" ]; then
        echo -n "  Backing up metadata... "
        tar -czf "$BACKUP_DIR/metadata_$TIMESTAMP.tar.gz" -C "$PROJECT_ROOT/files" metadata/
        echo -e "${GREEN}✓${NC}"
    fi

    # Backup config files
    echo -n "  Backing up configuration... "
    tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
        -C "$PROJECT_ROOT" \
        .env.example \
        docker-compose*.yml \
        *.yaml \
        *.yml \
        api/pyproject.toml \
        app/package.json \
        mcp/pyproject.toml
    echo -e "${GREEN}✓${NC}"

    # Create backup manifest
    cat > "$BACKUP_DIR/manifest_$TIMESTAMP.json" <<EOF
{
    "timestamp": "$TIMESTAMP",
    "files": {
        "files": "files_$TIMESTAMP.tar.gz",
        "metadata": "metadata_$TIMESTAMP.tar.gz",
        "config": "config_$TIMESTAMP.tar.gz"
    },
    "checksums": {
EOF

    # Add checksums
    for file in "$BACKUP_DIR"/*_$TIMESTAMP.tar.gz; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            checksum=$(sha256sum "$file" | cut -d' ' -f1)
            echo "        \"$filename\": \"$checksum\"," >> "$BACKUP_DIR/manifest_$TIMESTAMP.json"
        fi
    done

    # Close JSON
    sed -i '$ s/,$//' "$BACKUP_DIR/manifest_$TIMESTAMP.json"
    echo "    }" >> "$BACKUP_DIR/manifest_$TIMESTAMP.json"
    echo "}" >> "$BACKUP_DIR/manifest_$TIMESTAMP.json"

    echo -e "  ${GREEN}Manifest created${NC}"
}

# Function to backup to S3/DigitalOcean Spaces
backup_s3() {
    if ! command -v aws &> /dev/null; then
        echo -e "${YELLOW}Warning: AWS CLI not found, skipping S3 backup${NC}"
        return
    fi

    echo -e "\n${YELLOW}Creating S3 backup...${NC}"

    # Create backup bucket in S3
    BACKUP_PREFIX="backups/$TIMESTAMP"

    # Upload all backup files
    for file in "$BACKUP_DIR"/*_$TIMESTAMP.*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo -n "  Uploading $filename... "
            aws --endpoint-url="$S3_ENDPOINT" s3 cp "$file" "s3://$S3_BUCKET/$BACKUP_PREFIX/$filename"
            echo -e "${GREEN}✓${NC}"
        fi
    done

    echo -e "  ${GREEN}S3 backup complete${NC}"
}

# Function to cleanup old backups
cleanup_old_backups() {
    echo -e "\n${YELLOW}Cleaning up old local backups...${NC}"

    # Keep last 10 backups
    cd "$BACKUP_DIR"
    ls -t files_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm
    ls -t metadata_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm
    ls -t config_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm
    ls -t manifest_*.json 2>/dev/null | tail -n +11 | xargs -r rm

    echo -e "  ${GREEN}Old backups cleaned${NC}"
}

# Main execution
backup_local

# S3 backup if configured
if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    backup_s3
else
    echo -e "\n${YELLOW}S3 credentials not configured, skipping cloud backup${NC}"
fi

# Cleanup old backups
cleanup_old_backups

echo -e "\n${GREEN}✅ Backup completed successfully!${NC}"
echo -e "Backup location: $BACKUP_DIR"
echo -e "Backup ID: $TIMESTAMP"

# Show backup summary
echo -e "\n${YELLOW}Backup Summary:${NC}"
echo -e "  Files: $(ls -1 "$BACKUP_DIR"/*_$TIMESTAMP.tar.gz 2>/dev/null | wc -l) archives"
if [ -f "$BACKUP_DIR/manifest_$TIMESTAMP.json" ]; then
    echo -e "  Manifest: $BACKUP_DIR/manifest_$TIMESTAMP.json"
fi
echo -e "  Total size: $(du -sh "$BACKUP_DIR"/*_$TIMESTAMP.* 2>/dev/null | cut -f1 | paste -sd+ | bc)B"