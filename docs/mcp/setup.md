# MCP Client Setup

This guide details how to connect the TanaChat MCP server to AI clients like Claude Desktop.

## Quick Start

- **Server URL**: `https://mcp.tanachat.ai`
- **MCP Endpoint**: `https://mcp.tanachat.ai/mcp`

## Claude Desktop Configuration

Add the following to your `claude_desktop_config.json`:

### Method 1: Docker (Recommended for Local)

```json
{
  "mcpServers": {
    "tanachat": {
      "command": "docker",
      "args": ["exec", "-i", "tanachat-mcp", "python", "src/main.py"]
    }
  }
}
```

### Method 2: Direct URL (For Production)

Requires `@modelcontextprotocol/bridge`.

```json
{
  "mcpServers": {
    "tanachat": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/bridge", "https://mcp.tanachat.ai/mcp"]
    }
  }
}
```

## Environment Variables

Ensure the MCP server has access to:

- `TANA_API_KEY`: For interacting with Tana.
- `S3_ACCESS_KEY` / `S3_SECRET_KEY`: For file operations.

## Testing Connection

```bash
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```
