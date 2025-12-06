#!/bin/bash

# Tana KeyTags Management Script
# Demonstration of keytags management workflow

set -e

echo "🔑 Tana KeyTags Management Demo"
echo "==============================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check prerequisites
if [ ! -f "./bin/tana-keytags" ]; then
    echo -e "${RED}❌ tana-keytags not found. Run 'make setup' first.${NC}"
    exit 1
fi

if [ ! -f "./files/metadata/keytags.json" ]; then
    echo -e "${YELLOW}⚠️  No keytags.json found. Running import first...${NC}"
    if [ ! -f "./files/export/SuperTags.md" ]; then
        echo -e "${RED}❌ No export found. Please run tana-importjson first.${NC}"
        exit 1
    fi
fi

echo -e "\n${BLUE}1. Current KeyTags Status${NC}"
./bin/tana-keytags list

echo -e "\n${BLUE}2. Validating KeyTags against export${NC}"
./bin/tana-keytags validate

echo -e "\n${BLUE}3. Adding missing supertags from export${NC}"
echo "This will add all supertags from SuperTags.md that aren't in keytags..."
echo "y" | ./bin/tana-keytags add --from-export

echo -e "\n${BLUE}4. Updated KeyTags Status${NC}"
./bin/tana-keytags list

echo -e "\n${BLUE}5. Re-validating after additions${NC}"
./bin/tana-keytags validate

echo -e "\n${GREEN}✅ KeyTags management demo completed!${NC}"
echo ""
echo "KeyTags commands you can use:"
echo "  ./bin/tana-keytags list                    - Show all keytags"
echo "  ./bin/tana-keytags add --from-export       - Add missing tags"
echo "  ./bin/tana-keytags remove 'tag-name'      - Remove specific tag"
echo "  ./bin/tana-keytags validate               - Check consistency"
echo ""
echo "Files:"
echo "  ./files/metadata/keytags.json             - KeyTags configuration"
echo "  ./files/export/SuperTags.md               - All supertags from export"