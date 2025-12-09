#!/bin/bash
# Validate all sample files against their schemas

set -e

# Usage: scripts/validate-samples.sh [local|production]
TARGET=${1:-local}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SAMPLES_DIR="$PROJECT_ROOT/samples"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed${NC}"
    echo "Install jq: brew install jq (macOS) or apt-get install jq (Ubuntu)"
    exit 1
fi

# Check if ajv-cli is available (for JSON schema validation)
if ! command -v ajv &> /dev/null; then
    echo -e "${YELLOW}Warning: ajv-cli not found, JSON schema validation will be skipped${NC}"
    echo "Install with: npm install -g ajv-cli"
fi

echo "🔍 Validating sample files for $TARGET environment..."

# Validate JSON syntax
echo -e "\n${GREEN}--- JSON Syntax Validation ---${NC}"

errors=0

# Function to validate JSON file
validate_json() {
    local file="$1"
    echo -n "  $file ... "

    if jq empty "$file" 2>/dev/null; then
        echo -e "${GREEN}✓ Valid JSON${NC}"
        return 0
    else
        echo -e "${RED}✗ Invalid JSON${NC}"
        jq empty "$file" 2>&1 | head -n 5
        ((errors++))
        return 1
    fi
}

# Validate all JSON files
find "$SAMPLES_DIR" -name "*.json" -type f | while read -r file; do
    validate_json "$file"
done

# Validate against schema if ajv is available
if command -v ajv &> /dev/null; then
    echo -e "\n${GREEN}--- Schema Validation ---${NC}"

    schema_file="$SAMPLES_DIR/tana/schemas/tana-intermediate-format.schema.json"

    if [ -f "$schema_file" ]; then
        echo -n "  Validating TIF files against schema ... "

        # Validate all valid TIF files
        valid_files=$(find "$SAMPLES_DIR/tana/imports/valid" -name "*.json" -type f)
        if [ -n "$valid_files" ]; then
            if echo "$valid_files" | xargs ajv validate -s "$schema_file" --all-errors 2>/dev/null; then
                echo -e "${GREEN}✓ All valid files pass schema validation${NC}"
            else
                echo -e "${RED}✗ Schema validation failed${NC}"
                ((errors++))
            fi
        fi

        # Check that invalid files fail validation
        echo -n "  Checking invalid files fail validation ... "
        invalid_files=$(find "$SAMPLES_DIR/tana/imports/invalid" -name "*.json" -type f)
        if [ -n "$invalid_files" ]; then
            if echo "$invalid_files" | xargs ajv validate -s "$schema_file" 2>/dev/null; then
                echo -e "${YELLOW}⚠ Some invalid files passed validation (might be expected)${NC}"
            else
                echo -e "${GREEN}✓ Invalid files properly fail validation${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}⚠ Schema file not found: $schema_file${NC}"
    fi
fi

# Check file sizes
echo -e "\n${GREEN}--- File Size Check ---${NC}"

large_files=$(find "$SAMPLES_DIR" -name "*.json" -type f -exec wc -c {} + | awk '$1 > 1048576 {print $2}')
if [ -n "$large_files" ]; then
    echo -e "${YELLOW}⚠ Large files found (>1MB):${NC}"
    echo "$large_files" | while read -r file; do
        size=$(wc -c < "$file")
        echo "  $file: $((size / 1024))KB"
    done
else
    echo -e "${GREEN}✓ All files under 1MB${NC}"
fi

# Check for required fields in TIF files
echo -e "\n${GREEN}--- TIF Structure Check ---${NC}"

check_tif_structure() {
    local file="$1"
    echo -n "  $file ... "

    # Check required top-level fields
    if ! jq -e '.version' "$file" &>/dev/null; then
        echo -e "${RED}✗ Missing 'version' field${NC}"
        ((errors++))
        return 1
    fi

    if ! jq -e '.nodes' "$file" &>/dev/null; then
        echo -e "${RED}✗ Missing 'nodes' field${NC}"
        ((errors++))
        return 1
    fi

    # Check if nodes array is empty for valid files
    if [[ "$file" == *"/valid/"* ]]; then
        node_count=$(jq '.nodes | length' "$file" 2>/dev/null || echo "0")
        if [ "$node_count" -eq 0 ]; then
            echo -e "${RED}✗ No nodes in valid file${NC}"
            ((errors++))
            return 1
        fi
    fi

    echo -e "${GREEN}✓ Structure OK${NC}"
    return 0
}

# Check structure of all TIF files
find "$SAMPLES_DIR/tana" -name "*.json" -type f | while read -r file; do
    check_tif_structure "$file"
done

# Summary
echo -e "\n${GREEN}--- Validation Summary ---${NC}"

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $errors validation error(s)${NC}"
    exit 1
fi