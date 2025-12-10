# TanaChat Command Line Tools

Enhanced command-line utilities for comprehensive Tana workspace management, import/export, and analysis.

## 🚀 Enhanced Import & Export Tools

### Tana Import System
- **`tanachat-importjson`** - **Enhanced** - Import Tana JSON exports with metanode detection, complete formatting preservation, and smart folder organization
- **`tanachat-obsidian`** - **Completely rewritten** - Create comprehensive Obsidian vaults from Tana data (4,080+ user nodes, diary consolidation, YAML frontmatter)

### Content & Analysis Tools
- **`tanachat-keytags`** - Enhanced supertag management with comprehensive productivity supertag support (15+ types)
- **tanachat-outline`** - Generate hierarchical outlines from Tana JSON exports
- **tanachat-find`** - Advanced search across Tana imports with metadata filtering
- **tanachat-analyze`** - Complete workspace analysis with detailed statistics
- **tanachat-tags`** - Comprehensive tag and taxonomy management
- **tanachat-convert`** - Convert between Markdown and Tana paste formats

### User Management
- **`tanachat-createuser`** - Create new TanaChat.ai users
- **tanachat-login`** - Authenticate with Tana API and get JWT token

### Workspace Integration
- **tanachat-post`** - Post content to external platforms
- **tanachat-sync-spaces`** - Synchronize Tana spaces
- `tanachat-setup-spaces` - Configure workspace and space settings

## 🔥 Key Enhancements

### Metanode Hierarchy Detection
- Automatically discovers all user supertags (177+ found in typical workspaces)
- Smart mapping through Tana's internal metanode structure
- Preserves rich formatting and content relationships

### Complete Formatting Preservation
- Maintains bold, italics, links, HTML spans
- Preserves Tana's native content structure
- Creates Obsidian-compatible markdown with proper linking

### Smart Organization
- **Diary Consolidation**: Day/Week/Month/Year unified into diary folder
- **Dynamic Folders**: Creates folders based on actual supertag usage
- **Node ID Filenames**: Unique identification using `G4pITdVwJ2Be.md` format
- **User Content Only**: Excludes all system nodes and internal structures

## Usage Examples

### Enhanced Import & Export
```bash
# Import with complete formatting preservation
./bin/tanachat-importjson -f private.json

# Create comprehensive Obsidian vault
./bin/tanachat-obsidian -f private.json

# Manage enhanced supertags
./bin/tanachat-keytags --list
./bin/tanachat-keytags --add "project" --node-id "G4pITdVwJ2Be"
```

### Advanced Analysis
```bash
# Complete workspace analysis
./bin/tanachat-analyze -f private.json

# Advanced search with metadata
./bin/tanachat-find --query "important" --supertag "project"

# Generate structured outlines
./bin/tanachat-outline --node-id "G4pITdVwJ2Be" --format tree
```

### User Management
```bash
# Create and authenticate users
./bin/tanachat-createuser --username "newuser"
./bin/tanachat-login

# Manage workspace access
./bin/tanachat-sync-spaces --list
./bin/tanachat-setup-spaces --auto-config
```

## Quick Start

1. **Make tools executable:**
```bash
chmod +x bin/tanachat-*
```

2. **Test with sample data:**
```bash
# Test enhanced import
./bin/tanachat-importjson -f your-tana-export.json

# Create Obsidian vault
./bin/tanachat-obsidian -f your-tana-export.json
```

3. **Analyze results:**
```bash
# Check import summary
cat files/export/import-summary.md

# Browse Obsidian vault
open files/export/obsidian
```

## Integration Options

### MCP Tools
All CLI functionality is also available through Model Context Protocol (MCP) tools:
- Direct integration with AI assistants (Claude Desktop, Cursor)
- Real-time content analysis and manipulation
- Natural language workspace management

### Automation
- Scriptable interfaces for batch operations
- JSON output for integration with other tools
- Error handling and progress reporting
- Security validation with gitleaks integration

## Requirements

### Python Environment
- Python 3.12+ (recommended)
- Standard library modules only for enhanced import system
- No additional dependencies required for core functionality

### Optional Dependencies
- `uv` (for development and building)
- Docker (for containerized deployment)
- DigitalOcean CLI (for production deployment)

## Security

All tools include comprehensive security measures:
- **Input Validation**: Protects against malformed inputs
- **Permission Checking**: Verifies file and directory access
- **Gitleaks Integration**: Scans for hardcoded secrets (production mode)
- **Environment Isolation**: Safe execution contexts

## Support

- **Documentation**: [docs/](../docs/) for comprehensive guides
- **GitHub**: Issues and feature requests at [thomhas/TanaChat](https://github.com/thomhaus/TanaChat)
- **Community**: Discord and community forums for user discussions