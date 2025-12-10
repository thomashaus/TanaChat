# CLI Tools Overview

The `bin` directory contains Python-based command-line tools for direct interaction with Tana workspaces and data management.

## 🚀 Enhanced Import & Export Tools

### Tana Import System
- **`tanachat-importjson`**: **Enhanced** - Import Tana JSON exports with smart supertag detection and markdown preservation
- **`tanachat-obsidian`**: **Completely rewritten** - Export Tana data to enhanced Obsidian vaults (4,080+ user nodes, smart folder organization)

### Content & Workspace Tools
- **`tanachat-keytags`**: Manage supertag metadata and categorization (supports 15+ productivity supertags)
- **`tanachat-tags`**: Work with node tags and taxonomy
- **`tanachat-outline`**: Generate structured outlines from Tana content
- **`tanachat-find`**: Search for specific nodes and content
- **`tanachat-analyze`**: Analyze workspace structure and content

### User & Space Management
- **`tanachat-createuser`**: Create and manage user accounts
- **`tanachat-login`**: Authenticate with Tana API
- **`tanachat-post`**: Post content to Tana via API
- **`tanachat-sync-spaces`**: Synchronize Tana spaces
- **`tanachat-setup-spaces`**: Configure space settings
- **`tanachat-convert`**: Convert between Markdown and Tana paste formats

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

### Enhanced Workflows

#### Tana Import & Obsidian Export
```bash
# Import Tana JSON with full formatting preservation
./bin/tanachat-importjson -f private.json

# Create comprehensive Obsidian vault (all user content)
./bin/tanachat-obsidian -f private.json

# Manage supertags for targeted imports
./bin/tanachat-keytags --list
./bin/tanachat-keytags --add "project" --node-id "G4pITdVwJ2Be"
```

#### Content Analysis & Search
```bash
# Analyze workspace structure
./bin/tanachat-analyze -f private.json

# Search across all content
./bin/tanachat-find --query "important topic"

# Generate outlines from content
./bin/tanachat-outline --node-id "G4pITdVwJ2Be" --format markdown
```

#### User & Space Management
```bash
# Authenticate and manage users
./bin/tanachat-login
./bin/tanachat-createuser --username "newuser"

# Sync and configure spaces
./bin/tanachat-sync-spaces --space-id "your-space-id"
./bin/tanachat-setup-spaces --auto-config
```

## 🔥 New Features & Enhancements

### Enhanced Import System (`tanachat-importjson`)
- **Metanode Hierarchy Detection**: Automatically discovers all supertags using proven metanode tracing
- **Complete Formatting Preservation**: Maintains bold, italics, links, HTML spans, and rich content
- **Smart Node ID Filenames**: Uses `G4pITdVwJ2Be.md` format for unique identification
- **Supertag Indexing**: Creates comprehensive index files with Obsidian-style links
- **Dynamic Supertag Discovery**: Finds all user supertags, not just configured KeyTags

### Enhanced Obsidian Export (`tanachat-obsidian`)
- **Complete User Content Export**: Processes 4,080+ user nodes (vs 1,191 KeyTags only)
- **Smart Diary Consolidation**: Day/Week/Month/Year all grouped into unified diary folder
- **Dynamic Folder Organization**: Creates folders based on actual supertag usage
- **YAML Frontmatter**: Proper Obsidian metadata with dates, tags, and classification
- **Time-Based Naming**: `2025-12-10.md`, `2025-W50.md`, `2025-December.md` formats
- **System Content Filtering**: Excludes all SYS_* nodes, tag definitions, and meta nodes

## Integration with AI

These CLI tools provide the same functionality as the [MCP Tools](../mcp/tools.md) but can be used in scripts and automation workflows or when AI integration is not needed.
