# CLI Tools Overview

The `bin` directory contains Python-based command-line tools for direct interaction with Tana workspaces and data.

## Core Tools

### Data Management
- **`tanachat-importjson`**: Import Tana JSON exports and convert to various formats
- **`tanachat-convert`**: Convert between Markdown and Tana paste formats
- **`tanachat-find`**: Search for specific nodes and content
- **`tanachat-analyze`**: Analyze workspace structure and content

### Workspace Management
- **`tanachat-createuser`**: Create and manage user accounts
- **`tanachat-login`**: Authenticate with Tana API
- **`tanachat-post`**: Post content to Tana via API
- **`tanachat-sync-spaces`**: Synchronize Tana spaces
- **`tanachat-setup-spaces`**: Configure space settings

### Content Tools
- **`tanachat-keytags`**: Manage supertag metadata and categorization
- **`tanachat-tags`**: Work with node tags and taxonomy
- **`tanachat-obsidian`**: Export/import data with Obsidian format

## Usage

### Make tools executable:
```bash
chmod +x bin/tanachat-*
```

### Run any tool:
```bash
./bin/tanachat-importjson --help
./bin/tanachat-find --query "search term"
./bin/tanachat-convert --input.md --output.txt
```

### Common workflow:
```bash
# Authenticate
./bin/tanachat-login

# Import Tana export
./bin/tanachat-importjson input.json --output workspace.md

# Search content
./bin/tanachat-find --search "important topic"

# Sync with remote space
./bin/tanachat-sync-spaces --space-id "your-space-id"
```

## Integration with AI

These CLI tools provide the same functionality as the [MCP Tools](../mcp/tools.md) but can be used in scripts and automation workflows or when AI integration is not needed.
