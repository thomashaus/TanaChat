# tanachat-outline - Tana JSON Outline Generator

## Overview

`tanachat-outline` is a command-line tool that analyzes Tana JSON exports and generates hierarchical outlines with various display options. It's part of the TanaChat CLI tool suite and provides detailed insights into your Tana workspace structure.

## Features

- **Hierarchical Display**: Show nodes in a tree structure with configurable depth
- **Smart Root Detection**: Automatically identifies and prioritizes organizational nodes
- **Workspace Filtering**: Filter nodes by specific workspace ID
- **Statistics**: Generate detailed statistics about your Tana workspace
- **Multiple Output Formats**: Choose between detailed outline or simple list format
- **Interactive Selection**: Browse and select from available JSON files
- **Color-Coded Output**: Uses ANSI colors for better readability

## Installation

The script is included in the TanaChat project. Ensure you have the project set up:

```bash
# Clone the repository
git clone https://github.com/thomashaus/TanaChat.git
cd TanaChat

# Run setup
make setup

# The script will be available in bin/tanachat-outline
```

## Usage

### Basic Usage

```bash
# Interactive file selection
tanachat-outline

# Analyze specific file
tanachat-outline export.json

# Show 3 levels deep
tanachat-outline --depth 3 export.json

# Filter by workspace
tanachat-outline --workspace-id abc123 export.json

# Show statistics
tanachat-outline --stats export.json

# Simple list format
tanachat-outline --list export.json

# Start from specific node
tanachat-outline --start node123 export.json
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--depth` | `-d` | Maximum depth to display | 2 |
| `--workspace-id` | `-w` | Workspace ID to filter nodes | None |
| `--stats` | `-s` | Show detailed statistics | False |
| `--list` | `-l` | Simple list format (Home node only) | False |
| `--count` | `-n` | Number of layers with --list | 1 |
| `--start` | | Starting node ID | Home node |

### Examples

#### 1. Quick Overview
```bash
tanachat-outline my-export.json
```
Shows a 2-level deep outline of all root nodes.

#### 2. Deep Analysis
```bash
tanachat-outline --depth 5 --stats my-export.json
```
Shows 5 levels deep followed by detailed statistics.

#### 3. Workspace-Specific View
```bash
tanachat-outline --workspace-id "ws_abc123" --depth 3 my-export.json
```
Shows only nodes from the specified workspace.

#### 4. Simple Navigation
```bash
tanachat-outline --list --count 2 my-export.json
```
Shows Home node and its direct children, plus one more level.

#### 5. Node-Centric View
```bash
tanachat-outline --start "node_xyz789" --depth 4 my-export.json
```
Starts the outline from a specific node and shows 4 levels deep.

## Output Formats

### Standard Outline Format

The default output provides:
- Header with analysis information
- Root nodes with type indicators
- Hierarchical tree structure with Unicode characters
- Node icons based on type (📄, 🔍, 🏠, 🏷️, ⚙️)
- Descriptions for important nodes
- Limits to prevent overwhelming output

Example:
```
================================================================================
🏗️  TANA OUTLINE ANALYSIS
================================================================================
Workspace ID: ws_abc123
Total nodes: 15,432
System nodes: 234
User nodes: 15,198
Max depth: 2

📑 ROOT NODES (3):
--------------------------------------------------
 1. Home (home)
     🔗 ID: node_abc123
     ├─ 🔍 Areas
     ├─ 🔍 Projects
     └─ 🔍 Calendar

 2. Daily Notes (node)
     🔗 ID: node_def456
     └─ 📄 2024-01-15
```

### List Format

The `--list` option provides a simplified view:
- Shows Home node and its children
- Minimal formatting
- Easy to parse programmatically

Example:
```
🎯 Home
  └─ Areas
  └─ Projects
  └─ Calendar
  └─ Daily Notes
      └─ 2024-01-15
      └─ 2024-01-14
```

### Statistics Format

The `--stats` option adds detailed statistics:
- Node type distribution
- Tree depth information
- Workspace details
- Sample metrics

Example:
```
================================================================================
📊 OUTLINE STATISTICS
================================================================================
Node Type Distribution:
  node               : 12,345
  search             :   234
  home               :     1
  tagDef             :    45

Tree Statistics:
  Max display depth: 2
  Root nodes found: 3
  Max actual depth: 8

Workspace Information:
  ws_abc123: 1234 characters
  ws_def456: 567 characters
```

## Node Type Icons

The tool uses specific icons for different node types:

| Icon | Node Type | Description |
|------|-----------|-------------|
| 📄 | Default | Standard node |
| 🔍 | Search | Search/smart view |
| 🏠 | Home | Home node |
| 🏷️ | TagDef | Tag definition |
| ⚙️ | Meta | Node with metadata |

## Root Node Detection

The tool uses multiple strategies to identify root nodes:

1. **Parent-less nodes**: Nodes without a parentId
2. **Workspace expansion**: Nodes expanded in specific workspaces
3. **System filtering**: Excludes system nodes (prefixed with SYS_)
4. **Prioritization**: Prioritizes organizational nodes like Home, Areas, Projects

Prioritized node types:
- `home` or nodes named "Home"
- `search` nodes
- Nodes with names: Areas, Projects, Vision, Calendar, Tasks, Library, Resources
- Nodes containing "Hub" in the name

## Integration with TanaChat

`tanachat-outline` integrates seamlessly with the TanaChat ecosystem:

### File Locations
- Looks for JSON files in `files/import/` directory
- Works with files generated by other TanaChat tools
- Uses the same directory structure as `tanachat-importjson`

### Shared Libraries
- Uses `TanaIO` for file management
- Leverages `Colors` for consistent output formatting
- Integrates with `TanaParser` for robust JSON parsing

### API Compatibility
- Works with JSON exports from Tana API
- Compatible with files generated by MCP server tools
- Supports workspace-aware analysis

## Performance Considerations

### Large Files
- Limits output to prevent terminal overflow
- Shows first 20 root nodes by default
- Limits children per node to 10 (with "N more" indicator)
- Uses caching for repeated operations

### Memory Usage
- Builds an in-memory index for fast lookups
- Processes JSON using Python's built-in json module
- Implements lazy evaluation for expensive operations

## Error Handling

The tool provides clear error messages for:
- Missing or invalid JSON files
- Malformed JSON data
- File permission issues
- Missing command-line arguments

Example error outputs:
```bash
❌ File not found: export.json
❌ Invalid JSON format: Expecting ',' delimiter: line 123 column 45
❌ Error: Permission denied: /path/to/file.json
```

## Troubleshooting

### Common Issues

1. **"No JSON files found"**
   - Ensure files are in `files/import/` directory
   - Check file extensions are `.json`
   - Verify file permissions

2. **"Invalid JSON format"**
   - Validate JSON with a linter
   - Check for truncated downloads
   - Ensure proper UTF-8 encoding

3. **"Start node not found"**
   - Verify node ID exists in the export
   - Use quotes around node IDs with special characters
   - Try without specifying a start node

4. **Performance issues**
   - Reduce `--depth` parameter
   - Use `--list` for simpler output
   - Process large files in chunks

### Debug Tips

1. **Check file structure**:
   ```bash
   head -20 export.json | jq .
   ```

2. **Validate JSON**:
   ```bash
   python3 -m json.tool export.json > /dev/null
   ```

3. **Preview statistics**:
   ```bash
   tanachat-outline --depth 1 --stats export.json
   ```

## Development

### Code Structure

- `TanaOutlineGenerator`: Main class for outline generation
- `TanaParser`: Utility class for JSON parsing and analysis
- `TanaIO`: File management and directory operations
- `Colors`: Terminal color formatting

### Extending the Tool

To add new features:

1. **Add output formats**: Extend the `print_*` methods
2. **New filtering options**: Add parameters to `identify_root_nodes`
3. **Additional statistics**: Enhance the `print_statistics` method
4. **Custom node icons**: Update the `_print_children` method

### Testing

Run tests with:
```bash
# Test with sample data
tanachat-outline --depth 1 tests/sample.json

# Validate error handling
tanachat-outline non-existent.json

# Test all options
tanachat-outline --depth 3 --stats --list tests/sample.json
```

## Contributing

1. Follow the existing code style (PEP 8)
2. Add comprehensive docstrings
3. Include error handling for new features
4. Test with various Tana export formats
5. Update documentation for new features

## Related Tools

- `tanachat-importjson`: Import and convert Tana JSON files
- `tanachat-find`: Search within Tana exports
- `tanachat-tags`: Analyze tag usage
- `tanachat-post`: Post content to Tana via API

## License

Part of the TanaChat project, licensed under the MIT License.