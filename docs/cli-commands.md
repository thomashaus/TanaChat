# TanaChat CLI Commands Documentation

## 📋 Overview

TanaChat provides simple, powerful CLI tools for managing Tana workspace data. All commands support workspace-based organization.

## 🏢 Workspace Management

### **New: Workspace-Based KeyTags**

TanaChat now supports multiple workspaces with automatic workspace detection:

```bash
# List all workspaces
tanachat-keytags workspaces

# Create new workspace
tanachat-keytags create my_workspace

# Switch to workspace
tanachat-keytags use my_workspace

# Delete workspace
tanachat-keytags delete old_workspace
```

## 🚀 Core CLI Commands

### **1. tanachat-importjson** - Import Tana Data

**Purpose**: Import Tana JSON exports and generate markdown files.

```bash
# Interactive import (shows available files)
tanachat-importjson

# Import specific file
tanachat-importjson --file my-export.json

# Custom files directory
tanachat-importjson --files-dir /path/to/files

# Import without clearing export directory
tanachat-importjson --no-clear
```

**What it does**:
- ✅ Validates JSON file
- ✅ Detects workspace ID automatically
- ✅ Creates `{workspace_id}-keytags.json` if needed
- ✅ Generates SuperTags.md, Home.md
- ✅ Creates directory structure for supertags
- ✅ Migrates legacy keytags.json to workspace system

### **2. tanachat-keytags** - Manage KeyTags

**Purpose**: Manage supertags that get their own directories.

```bash
# List current keytags
tanachat-keytags list

# Add all supertags from export
tanachat-keytags add --from-export

# Add specific supertags
tanachat-keytags add project task documentation

# Remove specific keytag
tanachat-keytags remove --name project

# Interactive removal
tanachat-keytags remove

# Validate against current export
tanachat-keytags validate
```

### **3. tanachat-find** - Search Nodes

**Purpose**: Find nodes by supertag or content.

```bash
# Find all project nodes
tanachat-find project

# Custom files directory
tanachat-find --files-dir /path/to/files task

# Search by content
tanachat-find "meeting notes"
```

### **4. tanachat-outline** - Generate Outlines

**Purpose**: Generate hierarchical outlines from Tana data.

```bash
# Generate outline from export file
tanachat-outline export.json

# Limit depth
tanachat-outline export.json --depth 3

# Show statistics
tanachat-outline export.json --stats

# List top-level nodes
tanachat-outline export.json --list --count 20
```

### **5. tanachat-convert** - Convert Formats

**Purpose**: Convert Tana data to different formats.

```bash
# Convert to markdown
tanachat-convert export.json markdown

# Custom output directory
tanachat-convert export.json markdown --output /path/to/output

# Convert to JSON
tanachat-convert export.json json --output clean.json
```

### **6. tanachat-obsidian** - Generate Obsidian Vault

**Purpose**: Generate Obsidian-compatible files.

```bash
# Generate Obsidian vault
tanachat-obsidian export.json

# Custom vault directory
tanachat-obsidian export.json --output /path/to/vault

# Include frontmatter
tanachat-obsidian export.json --frontmatter
```

## 🔧 Common Workflows

### **New Workspace Setup**
```bash
# 1. Create workspace
tanachat-keytags create my_project_workspace

# 2. Import Tana data
tanachat-importjson --file my-project-export.json

# 3. Add keytags from export
tanachat-keytags add --from-export

# 4. Validate setup
tanachat-keytags validate
```

### **Switch Between Workspaces**
```bash
# List available workspaces
tanachat-keytags workspaces

# Switch to specific workspace
tanachat-keytags use my_project_workspace

# Verify active workspace
tanachat-keytags list
```

### **Search and Generate**
```bash
# Find project nodes
tanachat-find project

# Generate outline for current workspace
tanachat-outline files/export.json

# Generate Obsidian vault
tanachat-obsidian files/export.json
```

## 📁 File Structure

```
files/
├── metadata/
│   ├── {workspace_id}-keytags.json    # Workspace-specific keytags
│   └── keytags.backup.json            # Legacy backup
├── export/
│   └── {workspace_id}/                # Workspace exports
├── import/                            # JSON files to import
└── backups/                           # Auto-generated backups
```

## 🚨 Important Notes

1. **Auto Workspace Detection**: Import automatically detects workspace ID from JSON
2. **Migration**: Legacy `keytags.json` automatically migrates to `default_workspace-keytags.json`
3. **Backup System**: All operations create automatic backups
4. **File Organization**: Each workspace gets isolated files and directories

## 🔍 Help Commands

Each command has built-in help:

```bash
tanachat-importjson --help
tanachat-keytags --help
tanachat-find --help
tanachat-outline --help
tanachat-convert --help
tanachat-obsidian --help
```

## 🎯 Quick Start

```bash
# 1. Import your Tana export
tanachat-importjson --file your-export.json

# 2. Add keytags (supertags you want directories for)
tanachat-keytags add --from-export

# 3. Find your content
tanachat-find project

# 4. Generate outputs
tanachat-outline files/export.json
tanachat-obsidian files/export.json
```

That's it! Simple, powerful Tana data management. 🎉