#!/bin/bash

# Tana Import Workflow Script
# Complete workflow for importing and managing Tana workspace exports

set -e  # Exit on any error

echo "🚀 Starting Tana Import Workflow"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required tools exist
if [ ! -f "./bin/tana-importjson" ]; then
    echo -e "${RED}❌ Error: tana-importjson not found in ./bin/${NC}"
    echo "Please run 'make setup' first to install the tools."
    exit 1
fi

if [ ! -f "./bin/tana-keytags" ]; then
    echo -e "${RED}❌ Error: tana-keytags not found in ./bin/${NC}"
    echo "Please run 'make setup' first to install the tools."
    exit 1
fi

# Step 1: Check for import files
echo -e "\n${BLUE}📁 Step 1: Checking for Tana export files${NC}"
IMPORT_DIR="./files/import"

if [ ! -d "$IMPORT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Import directory not found. Creating...${NC}"
    mkdir -p "$IMPORT_DIR"
    echo -e "${YELLOW}📝 Please place your Tana JSON export files in $IMPORT_DIR${NC}"
    echo -e "${YELLOW}   and run this script again.${NC}"
    exit 1
fi

# Count JSON files in import directory
IMPORT_FILES=($(find "$IMPORT_DIR" -name "*.json" 2>/dev/null))
IMPORT_COUNT=${#IMPORT_FILES[@]}

if [ $IMPORT_COUNT -eq 0 ]; then
    echo -e "${RED}❌ No JSON files found in $IMPORT_DIR${NC}"
    echo -e "${YELLOW}📝 Please place your Tana JSON export files in $IMPORT_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found $IMPORT_COUNT Tana export file(s)${NC}"

# Step 2: Run the import
echo -e "\n${BLUE}📥 Step 2: Importing Tana data${NC}"
./bin/tana-importjson

# Step 3: Validate keytags
echo -e "\n${BLUE}🔑 Step 3: Validating KeyTags${NC}"
./bin/tana-keytags validate

# Step 4: Show keytags status
echo -e "\n${BLUE}📋 Step 4: Current KeyTags status${NC}"
./bin/tana-keytags list

# Step 5: Suggest next steps
echo -e "\n${BLUE}💡 Step 5: Next Steps${NC}"
echo "Your Tana workspace has been imported successfully!"
echo ""
echo "📁 Export structure:"
echo "   ./files/export/           - Generated markdown files"
echo "   ./files/export/SuperTags.md    - All supertags analysis"
echo "   ./files/export/import-summary.md - Import statistics"
echo "   ./files/export/*/        - Directory per supertag"
echo ""
echo "🔧 KeyTags management:"
echo "   ./bin/tana-keytags add --from-export    - Add missing supertags"
echo "   ./bin/tana-keytags remove 'tag-name'   - Remove specific keytag"
echo "   ./bin/tana-keytags validate             - Check consistency"
echo ""
echo "🔍 Data exploration:"
echo "   ./bin/tana-find --export path/to/file.json 'project' - Find project nodes"
echo "   ./bin/tana-analyze path/to/file.json   - Analyze workspace"
echo "   ./bin/tana-tags path/to/file.json     - Analyze supertags"
echo ""
echo "📤 Posting to Tana:"
echo "   ./bin/tana-post 'Content here' -n 'INBOX' - Post to Tana"
echo ""

# Step 6: Show import summary if it exists
SUMMARY_FILE="./files/export/import-summary.md"
if [ -f "$SUMMARY_FILE" ]; then
    echo -e "${BLUE}📊 Import Summary Preview:${NC}"
    echo "----------------------------------------"
    head -20 "$SUMMARY_FILE"
    echo "..."
    echo ""
    echo "Full summary available at: $SUMMARY_FILE"
fi

echo -e "${GREEN}✅ Tana Import Workflow completed successfully!${NC}"