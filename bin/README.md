# Tana Command Line Tools

Command-line utilities for working with Tana files and TanaChat.ai.

## Available Tools

### User Management

- **`tana-createuser`** - Create a new TanaChat.ai user
- **`tana-login`** - Authenticate and get JWT token

### Tana File Operations

- **`tana-importjson`** - Import Tana JSON files and generate markdown exports
- **`tana-update-keytags`** - Create keytags.json metadata file with supertags and node IDs
- **`tana-find`** - Search Tana imports for nodes
- **`tana-analyze`** - Analyze Tana workspace statistics
- **tana-convert** - Convert Markdown to Tana paste format
- **tana-tags** - Manage and analyze tags
- **tana-post** - Post content to external platforms

## Usage Examples

### Import Tana JSON

```bash
# Interactive mode - lists all files and lets you choose
./bin/tana-importjson

# Import specific file directly
./bin/tana-importjson --file workspace-export.json

# Import without clearing export directory
./bin/tana-importjson --file workspace-export.json --no-clear
```

### Update KeyTags Metadata

```bash
# Analyze latest import file
./bin/tana-update-keytags

# Scan all import files
./bin/tana-update-keytags --scan-all

# Include system supertags
./bin/tana-update-keytags --include-system

# Dry run to preview
./bin/tana-update-keytags --dry-run
```

### Create a User

```bash
# Interactive mode
./bin/tana-createuser

# Non-interactive mode
./bin/tana-createuser --name "John Doe" --username john --email john@example.com

# From config file
./bin/tana-createuser --config user.json
```

### Login

```bash
# Interactive password prompt
./bin/tana-login john

# Use stored token
./bin/tana-login --show-token john

# Validate token only
./bin/tana-login --validate-only --token xyz
```

### Find Nodes

```bash
# List supertags
./bin/tana-find --list

# Find by supertag
./bin/tana-find "Project"

# Search by keyword
./bin/tana-find --search "design"

# Use specific export file
./bin/tana-find --export my-export.json "Task"
```

## Shared Library

All tools use the shared library in `./lib` for:

- **Consistent behavior** across CLI and API
- **Centralized business logic**
- **Unified file paths** (defaults to `./files`)
- **Common utilities** (colors, error handling)

## File Paths

- **Local Data**: `./files/` (default)
  - Exports: `./files/exports/`
  - Imports: `./files/imports/`
  - User data: `./files/metadata/`

- **Configuration**: Override with `--files-dir` option

## Authentication

1. Create user with `tana-createuser`
2. Login with `tana-login` to get JWT token
3. Use token for API requests: `Authorization: Bearer <token>`
4. Use token for MCP server configuration

## Environment Variables

- `TANACHAT_FILES_DIR`: Override default files directory
- `TANACHAT_DEBUG`: Enable debug output