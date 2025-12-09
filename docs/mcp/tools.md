# MCP Tools Reference

The TanaChat MCP server provides the following tools for AI assistants.

## Available Tools

### `check_auth_status`
Verifies the connection to the Tana API using the configured API key.

### `list_storage_files`
Lists files stored in the configured S3 compatible storage bucket.

- **Arguments**:
    - `prefix` (string, optional): Filter files by prefix.

### `validate_tana_file`
Validates a Tana JSON export file against the Tana Intermediate Format specification.

- **Arguments**:
    - `content` (string): The JSON content of the Tana export.

## Usage Examples

**User**: "Check if my Tana connection is working."
**model**: Calls `check_auth_status()`

**User**: "What files do I have in my 'exports' folder?"
**model**: Calls `list_storage_files(prefix="exports/")`
