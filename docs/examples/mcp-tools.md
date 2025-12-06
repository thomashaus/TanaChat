# MCP Tools Guide

This guide demonstrates how to use the TanaChat.ai MCP tools with Claude Desktop and ChatGPT.

## Setup

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tanachat": {
      "command": "uv",
      "args": [
        "--cwd", "/path/to/TanaChat.ai/mcp",
        "run", "python", "-m", "src.server"
      ],
      "env": {
        "TANACHAT_API_URL": "http://localhost:8000",
        "TANACHAT_API_TOKEN": "your-jwt-token"
      }
    }
  }
}
```

### ChatGPT

The MCP server is accessible through the Model Context Protocol. Configure your client to connect to:
- **Endpoint**: `stdio` (for local usage)
- **Command**: `uv run python -m src.server` (from mcp directory)

## Available Tools

### Core Tana Operations

#### validate_tana_file
Validate a Tana Intermediate Format (TIF) file.

```
Usage: validate_tana_file(file_path)

Example:
"Please validate the file samples/tana/imports/valid/minimal.json"
```

Response:
```json
{
  "valid": true,
  "version": "TanaIntermediateFile V0.1",
  "node_count": 1,
  "summary": {
    "leaf_nodes": 1,
    "top_level_nodes": 1
  }
}
```

#### import_tana_file
Import and parse a Tana file into memory.

```
Usage: import_tana_file(file_path, format="auto")

Example:
"Import the Tana file at samples/tana/imports/valid/with-supertags.json"
```

#### export_tana_file
Export a Tana document to different formats.

```
Usage: export_tana_file(document, format, output_path)

Formats: tif, json, markdown, obsidian

Example:
"Export the current document to Obsidian format in /tmp/export/"
```

#### find_tana_nodes
Search for nodes matching criteria.

```
Usage: find_tana_nodes(query, filters)

Example queries:
- "Find all nodes with todo state 'done'"
- "Search for nodes containing 'design'"
- "Get all nodes with supertag 'Project'"
- "Find all calendar nodes from this week"
```

#### analyze_tana_document
Generate statistics and insights about a Tana document.

```
Usage: analyze_tana_document(document_or_path)

Returns:
- Node counts by type
- Supertag usage statistics
- Calendar events summary
- Task completion rates
- Content analysis
```

### User Management

#### authenticate_user
Authenticate with the TanaChat.ai API.

```
Usage: authenticate_user(username, password)

Example:
"Please authenticate as user john_doe with password ********"
```

#### get_user_files
List user's uploaded Tana files.

```
Usage: get_user_files()

Example:
"Show me all my uploaded Tana files"
```

#### upload_tana_file
Upload a Tana file to user's space.

```
Usage: upload_tana_file(file_path, description)

Example:
"Upload samples/tana/imports/valid/full-workspace.json with description 'My workspace backup'"
```

## Example Workflows

### 1. Validate and Analyze a Tana File

**User**: "Please validate and analyze my Tana file"

```
[Assistant uses tools]
1. validate_tana_file("path/to/file.json")
2. analyze_tana_document("path/to/file.json")
```

**Result**: The assistant provides validation results, statistics, and insights about the document structure.

### 2. Find and Export Tasks

**User**: "Export all my completed tasks to Markdown"

```
[Assistant workflow]
1. find_tana_nodes(query="todo_state=done")
2. export_tana_file(results, format="markdown", output_path="/tmp/tasks.md")
```

### 3. Daily Review Workflow

**User**: "Show me my daily meeting notes and action items"

```
[Assistant workflow]
1. find_tana_nodes(query="type=calendar AND date=today")
2. For each meeting node:
   - Extract attendees
   - List action items
   - Summarize key points
```

### 4. Project Status Report

**User**: "Generate a status report for the Website Redesign project"

```
[Assistant workflow]
1. find_tana_nodes(query="supertag=Project AND name='Website Redesign'")
2. find_tana_nodes(query="parent='Website Redesign' AND todo_state=todo")
3. find_tana_nodes(query="parent='Website Redesign' AND todo_state=done")
4. analyze_tana_document() to get statistics
5. Compile into a readable report
```

## Configuration

### Environment Variables

- `TANACHAT_API_URL`: API endpoint (default: http://localhost:8000)
- `TANACHAT_API_TOKEN`: JWT token for authentication
- `TANACHAT_DEBUG`: Enable debug logging (default: false)

### Custom Tool Behavior

The MCP server can be configured by creating `mcp/config.json`:

```json
{
  "cache_enabled": true,
  "cache_ttl": 3600,
  "max_file_size": 10485760,
  "allowed_formats": ["tif", "json", "markdown"],
  "default_export_format": "tif"
}
```

## Error Handling

Common errors and solutions:

### File Not Found
```
Error: File not found: /path/to/file.json
Solution: Check the file path and ensure it exists
```

### Invalid Tana Format
```
Error: Invalid Tana file format
Solution: Run validate_tana_file first to check for errors
```

### Authentication Required
```
Error: Authentication required
Solution: Run authenticate_user with valid credentials
```

### Rate Limit Exceeded
```
Error: Rate limit exceeded
Solution: Wait a moment before making more requests
```

## Advanced Usage

### Batch Operations

Process multiple files:

```
"Validate all Tana files in the samples/tana/imports/valid directory"
```

The assistant will:
1. List all .json files in the directory
2. Validate each file
3. Provide a summary report

### Custom Queries

Complex search queries:

```
"Find all high-priority tasks due this week in projects tagged as 'Active'"
```

This translates to:
- `todo_state=todo`
- `priority=high`
- `due_date<=7_days`
- `supertag=Active`

### Integration with Other Tools

Combine with external services:

```
"Upload my validated Tana file to Spaces and get the public URL"
```

The assistant will:
1. Validate the file
2. Upload via API
3. Return the access URL

## Tips for Effective Use

1. **Start with validation**: Always validate files before processing
2. **Use specific queries**: Be precise when searching for nodes
3. **Export regularly**: Save important results to external files
4. **Check authentication**: Ensure you're authenticated before file operations
5. **Use descriptive names**: Name your files clearly for easier reference

## Troubleshooting

### MCP Server Not Responding

1. Check if the server is running:
   ```bash
   cd mcp && uv run python -m src.server
   ```

2. Verify configuration in your client

3. Check environment variables are set correctly

### Authentication Issues

1. Verify your username and password
2. Check if your token has expired
3. Re-authenticate with `authenticate_user`

### File Access Issues

1. Ensure file paths are correct
2. Check file permissions
3. Verify file format is supported

## Sample Scripts

Create reusuable workflows:

```python
# daily_review.py
# Run with MCP tool: execute_script("daily_review.py")

# Find today's meetings
meetings = find_tana_nodes("type=calendar AND date=today")

# Process each meeting
for meeting in meetings:
    print(f"Meeting: {meeting['name']}")
    actions = find_tana_nodes(f"parent='{meeting['uid']}' AND type=task")
    if actions:
        print("  Action Items:")
        for action in actions:
            print(f"  - {action['name']}")
```