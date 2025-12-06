# Samples Directory

This directory contains sample files for documentation, manual testing, and development purposes.

## Structure

```
samples/
├── tana/                      # Tana Intermediate Format (TIF) samples
│   ├── imports/               # Sample TIF files for import testing
│   │   ├── valid/            # Valid TIF files
│   │   └── invalid/          # Invalid TIF files (error testing)
│   ├── exports/              # Export format examples
│   └── schemas/              # JSON schemas for validation
├── users/                    # User data samples
│   ├── requests/             # API request examples
│   └── responses/            # API response examples
├── api/                      # API-specific samples
│   ├── requests/             # API request payloads
│   └── responses/            # API response examples
└── scripts/                  # Sample management scripts
```

## Usage

### Manual Testing
```bash
# Test API with sample data
curl -X POST http://localhost:8000/api/tana/validate \
  -H "Content-Type: application/json" \
  -d @samples/tana/imports/valid/minimal.json

# Test MCP tool with sample
mcp call validate_tana_file samples/tana/imports/valid/minimal.json
```

### Development
```bash
# Load samples into LocalStack
./scripts/seed-samples.sh

# Generate additional samples
python scripts/generate-samples.py

# Validate all samples
./scripts/validate-samples.sh
```

### Documentation
Samples are referenced in:
- [API Usage Examples](../docs/examples/api-usage.md)
- [MCP Tools Guide](../docs/examples/mcp-tools.md)
- [Tana Tools Documentation](../docs/tana-tools.md)

## File Descriptions

### Tana Import Samples

#### Valid Files
- `minimal.json` - Smallest valid TIF file
- `with-supertags.json` - Example with supertags
- `with-fields.json` - Example with custom fields
- `full-workspace.json` - Complete workspace example
- `large-export.json` - Large file for performance testing

#### Invalid Files
- `missing-version.json` - Missing version field
- `wrong-version.json` - Unsupported version
- `empty-nodes.json` - Empty nodes array
- `missing-uid.json` - Node without UID
- `not-json.txt` - Invalid JSON format
- `too-large.json` - Exceeds size limit

### API Samples

#### Requests
- `register.json` - User registration payload
- `login.json` - User login payload
- `upload-tana.json` - Tana file upload request

#### Responses
- `register-success.json` - Successful registration
- `register-error-exists.json` - User already exists
- `upload-success.json` - File upload success
- `validation-error.json` - Validation failure

## Generation

Samples can be generated programmatically:
```bash
# Generate test data
python scripts/generate-samples.py --type tana --count 100
python scripts/generate-samples.py --type users --count 10
```

See [scripts/generate-samples.py](../scripts/generate-samples.py) for details.