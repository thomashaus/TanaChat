# Tana Tools

Portable Python scripts for analyzing and converting Tana workspace data.

## Overview

These tools work with any Tana workspace export and require no specific configuration. They are designed to be portable and shareable across different projects.

## 🚀 Available Tools

| Tool | Purpose | Features | Dependencies |
|------|---------|----------|
| **`tana-importjson`** | Import Tana JSON exports to markdown | ✅ Directory structure, ✅ Import summary | Requires valid import |
| **`tana-keytags`** | Manage supertag metadata | ✅ List/Add/Remove/Validate keytags | Requires completed import |
| **`tana-convert`** | Convert markdown to Tana format | ✅ Self-contained |
| **`tana-find`** | Find nodes by supertag/keyword | ✅ Self-contained |
| **`tana-analyze`** | Analyze workspace structure | ✅ Self-contained |
| **`tana-tags`** | Analyze supertag usage | ✅ Self-contained |
| **`tana-post`** | Post content to Tana nodes | 🔑 API token required |

## 📋 Quick Reference

```bash
# Import Tana JSON exports to markdown
tana-importjson                              # Interactive mode
tana-importjson --file export.json          # Import specific file
tana-importjson --no-clear                   # Keep existing files

# Manage supertag metadata
tana-keytags list                            # List current keytags
tana-keytags add --from-export              # Add missing supertags
tana-keytags remove "project"                # Remove specific keytag
tana-keytags validate                        # Validate against export

# Convert markdown to Tana format
tana-convert notes.md                    # Display output
tana-convert notes.md | pbcopy           # Copy to clipboard
tana-convert --demo                         # Show demo

# Find nodes in Tana export
tana-find --exports                        # List available exports
tana-find --export file.json "Atomic Note"    # Find by supertag
tana-find --export file.json --search "project"   # Find by keyword

# Analyze Tana workspace
tana-analyze --exports                    # List available exports
tana-analyze export.json                  # Analyze specific export
tana-analyze --detailed                   # Detailed analysis

# Analyze supertags
tana-tags --exports                       # List available exports
tana-tags export.json                     # Analyze supertags in export
tana-tags export.json --verbose           # Show node examples
tana-tags --count                         # Count unique supertags only

# Post content to Tana
tana-post "Meeting notes" -n "INBOX"      # Quick post
tana-post -f notes.md -n "INBOX"          # Post file content
tana-post -f notes.md -n "node_id" --supertag "Meeting"  # With supertag
tana-post "Task completed" -n "INBOX" --dry-run  # Preview only
```

## 🛠 Installation

### Prerequisites
- Python 3.6+ (pre-installed on most systems)
- Tana export file (JSON format)
- No external dependencies required

### Setup
1. Clone the repository:
```bash
git clone https://github.com/your-repo/TanaChat.ai
cd TanaChat.ai
```

2. Make scripts executable:
```bash
chmod +x bin/tana-*
```

3. Verify installation:
```bash
bin/tana-convert --demo
```

## 📖 Usage

### tana-importjson

Import Tana JSON exports and generate organized markdown files with directory structure.

**Important**: This tool creates a complete markdown export system and should be run first before using other tools that depend on the import structure.

```bash
# Interactive mode - select from available exports
tana-importjson

# Import specific file
tana-importjson --file workspace-export.json

# Keep existing export files (no confirmation)
tana-importjson --no-clear

# Custom files directory
tana-importjson --files-dir /path/to/files
```

**What it creates:**

1. **SuperTags.md** - Complete analysis of all supertags found in the export
2. **Home.md** - Home/root node information
3. **import-summary.md** - Detailed metrics and validation report
4. **Directory structure** - Organized markdown files by supertag:
   ```
   files/export/
   ├── SuperTags.md           # All supertags with usage counts
   ├── Home.md               # Home node information
   ├── import-summary.md     # Import metrics and issues
   ├── project/              # All nodes with #project supertag
   ├── note/                 # All nodes with #note supertag
   ├── atomic-note/          # All nodes with #atomic-note supertag
   └── spark-note/           # All nodes with #spark-note supertag
   ```

**Generated Files Format:**
Each markdown file contains:
- Node name as H1 header
- Node ID for reference
- Creation date and metadata
- Formatted content hierarchy

**KeyTags Integration:**
The tool automatically reads from `files/metadata/keytags.json` to determine which supertags should have their own directories. This allows you to selectively export only the supertags you're interested in.

**Example Output:**
```
🚀 Tana JSON Importer
Import directory: files/import
Export directory: files/export

📁 Available Tana JSON files:
   1. workspace-export.json
      Size: 2.1 MB | Modified: 2024-12-04 14:30

✅ Import completed successfully!

📊 Summary:
  Source file: workspace-export.json
  File size: 2,147,483,648 bytes
  Supertags found: 42
  KeyTags loaded: 4
  Nodes processed: 287
  Files created: SuperTags.md, Home.md, import-summary.md, 287 markdown files

📁 Created directories:
  📂 project/ (45 files)
  📂 note/ (198 files)
  📂 atomic-note/ (32 files)
  📂 spark-note/ (12 files)

📄 Import summary created: import-summary.md
```

### tana-keytags

Manage supertag metadata for selective exports. This tool controls which supertags get their own directories during import.

**Prerequisites**: Must run `tana-importjson` first to create the required files.

```bash
# List current keytags
tana-keytags list

# Add all supertags from export
tana-keytags add --from-export

# Remove specific keytag
tana-keytags remove --name "project"

# Interactive removal
tana-keytags remove

# Validate keytags against export
tana-keytags validate

# Custom files directory
tana-keytags list --files-dir /path/to/files
```

**Subcommands:**

#### `list`
Shows current keytags with their metadata in a formatted table.

```
🔑 Current KeyTags
File: files/metadata/keytags.json
Last updated: 2024-12-04T14:29:05.357312
Source: workspace-export.json

📋 User-defined KeyTags (4):
Name                 Node ID         Description
------------------------------------------------------------
project              XP0quB9qcpnO
spark note           o6SogPA3v4oc
atomic note          5c2Ri811If-D
note                 crqjNErByssm
```

#### `add --from-export`
Automatically adds all supertags from the SuperTags.md export file that aren't already in keytags.

```
📥 Loading supertags from export...
Found 42 supertags in SuperTags.md
Adding 7 new keytags:
  • collection (a3tQo07Akrs6)
  • context (0-b71otJrlg0)
  • document (cZCWBcfIJpgB)
  • goals (3VoZuQu0SCIL)
  • role (jOQ78NaOth9I)
  • task (NXkC0h-qPRS3)
  • vision (56J56YWSM7BA)

Add these keytags? [y/N]: y
✅ Added 7 keytags
```

#### `remove`
Remove supertags from keytags either interactively or by name.

```bash
# Remove specific keytag
tana-keytags remove --name "goals"

# Interactive selection
tana-keytags remove
```

#### `validate`
Compare keytags against the current SuperTags.md export and identify discrepancies.

```
🔍 Validating KeyTags...

📊 Validation Results:
  KeyTags: 10 supertags
  Export: 11 supertags
  Common: 10 supertags

⚠️  Supertags in export but not in KeyTags (1):
  • goals (3VoZuQu0SCIL)
⚠️  Found 1 validation issues

💡 Suggestions:
  • Run: tana-keytags add --from-export to add missing supertags
```

**KeyTags File Structure:**
The `files/metadata/keytags.json` file contains:
- Version and metadata
- User-defined supertags with their node IDs
- Source file tracking
- Creation timestamps

### tana-convert

Converts markdown files to Tana-compatible hierarchical format that can be pasted directly into Tana.

```bash
# Basic conversion
tana-convert notes.md

# Convert and copy to clipboard (macOS)
tana-convert notes.md | pbcopy

# Save to file
tana-convert notes.md -o output.txt

# Add supertag to first heading
tana-convert meeting.md --supertag "Meeting"

# Preserve markdown formatting
tana-convert notes.md --preserve-emphasis

# Show conversion statistics
tana-convert notes.md --stats
```

**Sample Input (Markdown):**
```markdown
# Project Planning

## Tasks
- Design system
- [x] Write docs
- [ ] Test features

### Status
Ready to start
```

**Sample Output (Tana Format):**
```
- Tasks
    - Design system
    - ☑ Write docs
    - ☐ Test features
  - Status
      Ready to start
```

### tana-find

Search for nodes in Tana exports by supertag or keyword.

```bash
# List all available exports
tana-find --exports

# Find by supertag
tana-find --export file.json "Atomic Note"

# Find by keyword search
tana-find --export file.json --search "project"

# Limit results
tana-find --export file.json "Meeting" -l 10

# Different output formats
tana-find --export file.json "Atomic Note" --format json
tana-find --export file.json --search "note" --format simple
```

**Output Options:**
- `table` (default): Formatted table with details
- `simple`: Just node names
- `json`: JSON format for automation

### tana-analyze

Provides comprehensive analysis of Tana workspace structure and content patterns.

```bash
# Analyze latest export
tana-analyze

# Analyze specific export
tana-analyze export.json

# Show available exports
tana-analyze --exports

# Detailed analysis
tana-analyze export.json --detailed

# Content pattern analysis
tana-analyze export.json --patterns
```

**Analysis Report Includes:**
- Basic statistics (nodes, descriptions, children)
- Supertag usage and frequency
- Content patterns (headings, lists, links, tasks)
- Node types and structures
- Date ranges and modification trends

### tana-tags

Analyzes supertag usage patterns in your Tana workspace without requiring any external scripts.

```bash
# Analyze latest export
tana-tags

# Analyze specific export
tana-tags export.json

# Show available exports
tana-tags --exports

# Verbose output with node examples
tana-tags export.json --verbose

# Count only unique supertags
tana-tags --count

# Sort by name instead of count
tana-tags export.json --sort name
```

**Features:**
- Automatic supertag categorization (time-based vs content-based)
- Node examples for each supertag
- Usage frequency analysis
- File statistics and metadata

**Output Categories:**
- **Time-based**: Day, Week, Month, Quarter, Year, Journal
- **Content-based**: Notes, Ideas, Meeting, Project
- **Other**: Custom or uncategorized supertags

### tana-post

Posts formatted content directly to Tana nodes using the Tana Input API.

```bash
# Quick post to INBOX
tana-post "Meeting notes discussed project timeline" -n "INBOX"

# Post file content
tana-post -f meeting-notes.md -n "INBOX"

# Post with supertag
tana-post -f meeting-notes.md -n "node_id" --supertag "Meeting"

# Preview without posting
tana-post "Task completed" -n "INBOX" --dry-run

# Post with custom formatting
tana-post -f notes.md -n "INBOX" --preserve-emphasis --bullet "•"
```

**Configuration:**
Set up your Tana API token using one of these methods:

1. **Environment Variable** (recommended):
```bash
export TANA_API_TOKEN="your_token_here"
```

2. **Config File**:
```bash
echo '{"api_token": "your_token_here"}' > tana-config.json
```

**Get your API token:**
1. Open Tana (desktop or web)
2. Go to **Settings** → **API**
3. Click **Create Token**
4. Copy the token and configure it above

**Common Target Nodes:**
- `INBOX` - Your main Tana inbox
- `SCHEMA/INBOX` - Schema definitions inbox
- Any node ID from your workspace

## 📁 Export Files

Tana exports are JSON files created from your Tana workspace:

### How to Export from Tana
1. Open Tana (desktop or web)
2. Go to **Settings** (⚙️ icon)
3. Click **Export**
4. Select **JSON** format
5. Choose your desired export options
6. Save the file

### Export File Locations
The tools automatically search in these directories:
- `./Tana/Exports/`
- `../Tana/Exports/`
- `./exports/`
- `../exports/`

### Export File Naming
Common patterns:
- `Tana Data YYYY-MM-DD.json`
- `workspace-export.json`
- `V3G_abc123@timestamp.json`

## 🔧 Advanced Usage

### Integration with Other Tools

**With vim/neovim:**
```bash
:w !tana-convert -n "INBOX" --supertag "Note"
```

**With obsidian:**
```markdown
!tana-convert % | pbcopy
```

**With Alfred/Raycast:**
```bash
# Create workflow to convert markdown to Tana format
tana-convert "{query}" | pbcopy
```

### Automation Examples

**Batch conversion:**
```bash
for file in *.md; do
    tana-convert "$file" -o "${file%.tana}"
done
```

**Integration with git hooks:**
```bash
# Pre-commit hook to format meeting notes
#!/bin/bash
if [[ $1 == *.md ]]; then
    tana-convert "$1" | pbcopy
    echo "Converted $1 to Tana format and copied to clipboard"
fi
```

## 🎯 Use Cases

### 1. Content Migration
- Convert meeting notes from other formats to Tana
- Migrate markdown knowledge bases to Tana
- Archive content in Tana-compatible format

### 2. Content Discovery
- Find all nodes related to specific projects
- Search for tasks and action items
- Analyze content patterns in your workspace

### 3. Workspace Analysis
- Understand your Tana usage patterns
- Identify most used supertags
- Track content growth over time

### 4. Content Organization
- Structure information hierarchically
- Tag and categorize content
- Prepare content for sharing

## 🔍 Troubleshooting

### Common Issues

**"No Tana export files found"**
```bash
# Check for exports in common locations
tana-find --exports

# Manually specify the export file path
tana-find --export /path/to/export.json
```

**"Invalid JSON in export file"**
- Ensure the export was created properly from Tana
- Check if the file is corrupted or incomplete
- Try re-exporting from Tana

**"Tana API token not found"** (tana-post only)
```bash
# Set environment variable
export TANA_API_TOKEN="your_token_here"

# Or create config file
echo '{"api_token": "your_token_here"}' > tana-config.json
```

**"Authentication failed"** (tana-post only)
- Verify your API token is correct
- Check if the token has expired
- Ensure the token has write permissions

**"Target node not found"** (tana-post only)
- Verify the node ID or name is correct
- Use "INBOX" for testing
- Check node ID format in your Tana workspace

**"Permission denied"**
```bash
# Make scripts executable
chmod +x bin/tana-*
```

### Getting Help

Each script includes comprehensive help:
```bash
tana-importjson --help
tana-keytags --help
tana-convert --help
tana-find --help
tana-analyze --help
```

## 📊 Performance

| Tool | Large Exports (100K+ nodes) | Small Exports (<1K nodes) |
|------|--------------------------|-----------------------|
| tana-importjson | ~5-15 seconds | ~1-3 seconds |
| tana-keytags | ~0.1 seconds | ~0.05 seconds |
| tana-analyze | ~2-5 seconds | ~0.5 seconds |
| tana-find | ~1-2 seconds | ~0.2 seconds |
| tana-tags | ~2-3 seconds | ~0.3 seconds |
| tana-post | ~0.1 seconds + API | ~0.05 seconds + API |
| tana-convert | ~0.1 seconds | ~0.05 seconds |

## 🤝 Contributing

These tools are designed to be simple and portable. When contributing:

1. Keep dependencies minimal (Python standard library only)
2. Maintain compatibility with Python 3.6+
3. Include comprehensive help documentation
4. Test with various export file formats
5. Follow the existing code style and structure

## 📄 License

These tools are part of the TanaChat.ai project and are open source. See the main project license for details.

## 🆘 Support

For issues, questions, or feature requests:

1. Check the help documentation first
2. Test with a small export file first
3. Include export file details when reporting issues
4. Provide example input and expected output

---

**Last Updated**: December 2024
**Tools**: 7 portable Python utilities
**Status**: ✅ Working and tested