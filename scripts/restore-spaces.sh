#!/bin/bash
# Restore script for TanaChat data from DigitalOcean Spaces backup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
S3_BUCKET=${S3_BUCKET:-"tanachat"}
S3_REGION=${S3_REGION:-"nyc3"}
S3_ENDPOINT=${S3_ENDPOINT:-"https://nyc3.digitaloceanspaces.com"}

# Function to show usage
show_usage() {
    echo -e "${BLUE}Usage:${NC} $0 [backup_id]"
    echo -e "\n${BLUE}Examples:${NC}"
    echo "  $0                           # Interactive restore (shows available backups)"
    echo "  $0 20241205_143022          # Restore specific backup"
    echo "  $0 latest                    # Restore latest backup"
}

# Function to list available backups
list_backups() {
    echo -e "\n${YELLOW}Available Backups:${NC}"
    aws --endpoint-url="$S3_ENDPOINT" s3 ls "s3://$S3_BUCKET/backups/" | \
        awk '{print $2}' | \
        sed 's/\///' | \
        sort -r
}

# Function to restore from backup
restore_backup() {
    local backup_id=$1
    local backup_prefix="backups/$backup_id"

    echo -e "\n${YELLOW}Restoring from backup: $backup_id${NC}"
    echo -e "Location: s3://$S3_BUCKET/$backup_prefix"

    # Download manifest
    echo -n "  Downloading manifest... "
    MANIFEST="/tmp/manifest_$backup_id.json"
    aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$backup_prefix/manifest.json" "$MANIFEST" --quiet
    echo -e "${GREEN}✓${NC}"

    # Show what will be restored
    echo -e "\n${YELLOW}This backup contains:${NC}"
    jq -r '.files | to_entries[] | "  • \(.key)"' "$MANIFEST"

    # Ask for confirmation
    echo -e "\n${RED}WARNING: This will overwrite existing data!${NC}"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Restore cancelled."
        exit 0
    fi

    # Create temp directory
    TEMP_DIR="/tmp/restore_$backup_id"
    mkdir -p "$TEMP_DIR"

    # Restore metadata files
    echo -e "\n${YELLOW}Restoring metadata...${NC}"

    # Restore users.json
    if jq -e '.files["User metadata"]' "$MANIFEST" &>/dev/null; then
        users_file=$(jq -r '.files["User metadata"]' "$MANIFEST")
        echo -n "  Restoring user metadata... "
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$backup_prefix/$users_file" "$TEMP_DIR/users.json" --quiet
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "$TEMP_DIR/users.json" "s3://$S3_BUCKET/metadata/users.json" --quiet
        echo -e "${GREEN}✓${NC}"
    fi

    # Restore keytags.json
    if jq -e '.files["Keytags metadata"]' "$MANIFEST" &>/dev/null; then
        keytags_file=$(jq -r '.files["Keytags metadata"]' "$MANIFEST")
        echo -n "  Restoring keytags metadata... "
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$backup_prefix/$keytags_file" "$TEMP_DIR/keytags.json" --quiet
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "$TEMP_DIR/keytags.json" "s3://$S3_BUCKET/metadata/keytags.json" --quiet
        echo -e "${GREEN}✓${NC}"
    fi

    # Restore user files
    if jq -e '.files["User files"]' "$MANIFEST" &>/dev/null; then
        files_archive=$(jq -r '.files["User files"]' "$MANIFEST")
        echo -n "  Restoring user files... "

        # Download and extract
        aws --endpoint-url="$S3_ENDPOINT" s3 cp "s3://$S3_BUCKET/$backup_prefix/$files_archive" "$TEMP_DIR/files.tar.gz" --quiet
        mkdir -p "$TEMP_DIR/files"
        tar -xzf "$TEMP_DIR/files.tar.gz" -C "$TEMP_DIR/files"

        # Upload back to Spaces
        aws --endpoint-url="$S3_ENDPOINT" s3 sync "$TEMP_DIR/files/" "s3://$S3_BUCKET/files/" --delete --quiet

        echo -e "${GREEN}✓${NC}"
    fi

    # Cleanup
    rm -rf "$TEMP_DIR" "$MANIFEST"

    echo -e "\n${GREEN}✅ Restore completed successfully!${NC}"
    echo -e "\n${YELLOW}Note: If you have a running TanaChat instance, you may need to restart it to pick up the restored data.${NC}"
}

# Main execution
if [ $# -eq 0 ]; then
    # Interactive mode
    echo -e "${BLUE}TanaChat Restore Tool${NC}"
    echo

    list_backups

    echo
    read -p "Enter backup ID to restore (or 'latest'): " backup_id

    if [ -z "$backup_id" ]; then
        echo -e "${RED}No backup selected.${NC}"
        exit 1
    fi
else
    backup_id=$1
fi

# Handle special case
if [ "$backup_id" = "latest" ]; then
    backup_id=$(aws --endpoint-url="$S3_ENDPOINT" s3 ls "s3://$S3_BUCKET/backups/" | \
                awk '{print $2}' | \
                sed 's/\///' | \
                sort -r | \
                head -n1)

    if [ -z "$backup_id" ]; then
        echo -e "${RED}No backups found.${NC}"
        exit 1
    fi

    echo -e "${BLUE}Selected latest backup: $backup_id${NC}"
fi

# Validate backup exists
if ! aws --endpoint-url="$S3_ENDPOINT" s3 ls "s3://$S3_BUCKET/backups/$backup_id" &>/dev/null; then
    echo -e "${RED}Backup '$backup_id' not found.${NC}"
    echo
    list_backups
    exit 1
fi

# Restore the backup
restore_backup "$backup_id"