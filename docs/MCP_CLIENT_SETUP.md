# MCP Client Setup Guide

This guide shows how to connect TanaChat MCP server to various AI clients including Claude Desktop, Claude Code, and ChatGPT.

## 🚀 Quick Start

**Server URL**: `https://mcp.tanachat.ai`
**MCP Endpoint**: `https://mcp.tanachat.ai/mcp`

## 📋 Available Tools

The TanaChat MCP server provides these tools:

- **`check_auth_status`** - Verify Tana API connection
- **`list_spaces_files`** - List files in DigitalOcean Spaces storage
- **`validate_tana_file`** - Validate Tana JSON file format

---

## 🖥️ Claude Desktop Setup

### Method 1: Direct Connection

1. **Open Claude Desktop Settings**:
   - Click on Claude Desktop → Settings → Developer

2. **Edit MCP Configuration**:
   ```json
   {
     "mcpServers": {
       "tanachat": {
         "command": "node",
         "args": ["-e", "require('https').createServer((req, res) => { if (req.url === '/') { res.writeHead(200, {'Content-Type': 'application/json'}); res.end(JSON.stringify({jsonrpc: '2.0', id: 1, method: 'initialize', params: {protocolVersion: '2024-11-05', capabilities: {tools: {}}, serverInfo: {name: 'tanachat', version: '0.1.0'}}})); } }).listen(0, () => console.log(JSON.stringify({port: this.address().port})))"],
         "env": {
           "TANACHAT_MCP_URL": "https://mcp.tanachat.ai/mcp"
         }
       }
     }
   }
   ```

### Method 2: Using MCP Bridge (Recommended)

1. **Install MCP Bridge**:
   ```bash
   npm install -g @modelcontextprotocol/bridge
   ```

2. **Create bridge configuration**:
   ```yaml
   # ~/.config/claude-desktop/mcp-servers.yaml
   servers:
     tanachat:
       url: https://mcp.tanachat.ai/mcp
       headers:
         Content-Type: "application/json"
   ```

3. **Add to Claude Desktop**:
   ```json
   {
     "mcpServers": {
       "tanachat": {
         "command": "mcp-bridge",
         "args": ["--config", "~/.config/claude-desktop/mcp-servers.yaml"]
       }
     }
   }
   ```

### Method 3: Local Proxy

1. **Create proxy script** (`tanachat-proxy.js`):
   ```javascript
   const https = require('https');
   const { spawn } = require('child_process');

   const options = {
     hostname: 'mcp.tanachat.ai',
     port: 443,
     path: '/mcp',
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     }
   };

   process.stdin.on('data', (data) => {
     const req = https.request(options, (res) => {
       res.on('data', (chunk) => {
         process.stdout.write(chunk);
       });
     });

     req.write(data);
     req.end();
   });
   ```

2. **Add to Claude Desktop**:
   ```json
   {
     "mcpServers": {
       "tanachat": {
         "command": "node",
         "args": ["/path/to/tanachat-proxy.js"]
       }
     }
   }
   ```

---

## 💻 Claude Code Setup

### Method 1: Direct HTTP Connection

1. **Create MCP client script** (`tanachat-mcp.js`):
   ```javascript
   const https = require('https');

   class TanaChatMCPClient {
     constructor() {
       this.serverUrl = 'https://mcp.tanachat.ai/mcp';
       this.requestId = 1;
     }

     async initialize() {
       return this.sendRequest({
         jsonrpc: '2.0',
         id: this.requestId++,
         method: 'initialize',
         params: {
           protocolVersion: '2024-11-05',
           capabilities: { tools: {} },
           clientInfo: { name: 'claude-code', version: '1.0' }
         }
       });
     }

     async listTools() {
       return this.sendRequest({
         jsonrpc: '2.0',
         id: this.requestId++,
         method: 'tools/list'
       });
     }

     async callTool(name, args = {}) {
       return this.sendRequest({
         jsonrpc: '2.0',
         id: this.requestId++,
         method: 'tools/call',
         params: { name, arguments: args }
       });
     }

     async sendRequest(request) {
       return new Promise((resolve, reject) => {
         const data = JSON.stringify(request);
         const options = {
           hostname: 'mcp.tanachat.ai',
           port: 443,
           path: '/mcp',
           method: 'POST',
           headers: {
             'Content-Type': 'application/json',
             'Content-Length': data.length
           }
         };

         const req = https.request(options, (res) => {
           let responseData = '';
           res.on('data', (chunk) => responseData += chunk);
           res.on('end', () => {
             try {
               resolve(JSON.parse(responseData));
             } catch (error) {
               reject(error);
             }
           });
         });

         req.on('error', reject);
         req.write(data);
         req.end();
       });
     }
   }

   module.exports = TanaChatMCPClient;
   ```

2. **Use in Claude Code**:
   ```javascript
   // In your Claude Code session
   const TanaChatMCPClient = require('./tanachat-mcp.js');
   const client = new TanaChatMCPClient();

   // Initialize connection
   await client.initialize();

   // List available tools
   const tools = await client.listTools();
   console.log('Available tools:', tools.result.tools);

   // Call a tool
   const result = await client.callTool('check_auth_status');
   console.log('Auth status:', result.result);
   ```

### Method 2: MCP Server Integration

1. **Add to Claude Code settings** (`~/.claude/config.json`):
   ```json
   {
     "mcpServers": {
       "tanachat": {
         "url": "https://mcp.tanachat.ai/mcp",
         "description": "TanaChat MCP Server for workspace management"
       }
     }
   }
   ```

2. **Restart Claude Code** to load the MCP server.

---

## 🤖 ChatGPT Setup

### Method 1: Custom Actions

1. **Create OpenAPI specification** (`tanachat-openapi.json`):
   ```json
   {
     "openapi": "3.0.0",
     "info": {
       "title": "TanaChat MCP Server",
       "version": "1.0.0",
       "description": "AI-powered Tana workspace management"
     },
     "servers": [
       {
         "url": "https://mcp.tanachat.ai",
         "description": "Production server"
       }
     ],
     "paths": {
       "/api/v1/tools": {
         "get": {
           "summary": "List available MCP tools",
           "operationId": "listTools",
           "responses": {
             "200": {
               "description": "List of available tools",
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "properties": {
                       "tools": {
                         "type": "array",
                         "items": {
                           "type": "object",
                           "properties": {
                             "name": {"type": "string"},
                             "description": {"type": "string"},
                             "parameters": {"type": "object"}
                           }
                         }
                       }
                     }
                   }
                 }
               }
             }
           }
         }
       }
     }
   }
   ```

2. **Add Custom Action to ChatGPT**:
   - Go to ChatGPT → Settings → Custom Actions
   - Import the OpenAPI specification
   - Set authentication to "None"

### Method 2: API Integration

1. **Create plugin manifest** (`plugin.json`):
   ```json
   {
     "schema_version": "1.0",
     "name_for_model": "tanachat_mcp",
     "name_for_human": "TanaChat MCP",
     "description_for_model": "Connect to Tana workspace for data management and analysis",
     "description_for_human": "Manage and analyze your Tana workspace with AI assistance",
     "api": {
       "type": "openapi",
       "url": "https://mcp.tanachat.ai/openapi.json"
     },
     "auth": {
       "type": "none"
     }
   }
   ```

2. **Host the manifest** and register with ChatGPT.

---

## 🔧 Testing Your Connection

### Test MCP Protocol

```bash
# Test initialization
curl -X POST https://mcp.tanachat.ai/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {"tools": {}},
      "clientInfo": {"name": "test", "version": "1.0"}
    }
  }'

# Test tool listing
curl -X POST https://mcp.tanachat.ai/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  }'

# Test tool call
curl -X POST https://mcp.tanachat.ai/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "check_auth_status",
      "arguments": {}
    }
  }'
```

### Test REST API

```bash
# Health check
curl https://mcp.tanachat.ai/health

# API tools
curl https://mcp.tanachat.ai/api/v1/tools

# API documentation
open https://mcp.tanachat.ai/docs
```

---

## 🛠 Usage Examples

### Claude Desktop

```
@tanachat Check my Tana API connection status
@tanachat List all files in my DigitalOcean Spaces
@tanachat Validate this Tana export file: [paste JSON content]
```

### Claude Code

```javascript
// Check authentication
const authStatus = await client.callTool('check_auth_status');
console.log('Tana API Status:', authStatus.result);

// List files in Spaces
const files = await client.callTool('list_spaces_files', {
  bucket: 'tanachat',
  prefix: 'exports/'
});
console.log('Files:', files.result);

// Validate Tana file
const validation = await client.callTool('validate_tana_file', {
  content: tanaJsonContent
});
console.log('Validation:', validation.result);
```

### ChatGPT

```
Use the TanaChat MCP tool to:
1. Check if my Tana API key is working
2. List all exported files in my storage
3. Validate this Tana workspace export format
```

---

## 🔒 Authentication Setup

The MCP server requires these environment variables to be configured:

```bash
# Tana Integration
TANA_API_KEY=your_tana_api_key_here

# DigitalOcean Spaces (if using file storage)
S3_ACCESS_KEY=your_spaces_access_key
S3_SECRET_KEY=your_spaces_secret_key
S3_BUCKET=tanachat
S3_REGION=nyc3
S3_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

**Note**: For the public MCP server at `mcp.tanachat.ai`, these are already configured.

---

## 🚨 Troubleshooting

### Connection Issues

1. **Verify server is accessible**:
   ```bash
   curl https://mcp.tanachat.ai/health
   ```

2. **Check MCP protocol version**: Ensure client supports `2024-11-05`

3. **Verify JSON format**: MCP requires strict JSON formatting

### Authentication Issues

1. **Check Tana API key**: Ensure it's valid and has necessary permissions
2. **Verify Spaces credentials**: Check S3 access keys are correct
3. **Test local setup**: Run local MCP server to debug

### Client-Specific Issues

- **Claude Desktop**: Check Developer settings are enabled
- **Claude Code**: Verify MCP server configuration file
- **ChatGPT**: Ensure Custom Actions API specification is valid

---

## 📚 Additional Resources

- **Tana API Documentation**: https://tana.inc/docs
- **MCP Protocol Specification**: https://modelcontextprotocol.io
- **Claude Desktop Developer Guide**: https://docs.anthropic.com/claude/docs/overview
- **DigitalOcean Spaces API**: https://docs.digitalocean.com/products/spaces

---

## 🆘 Support

If you encounter issues:

1. **Check server status**: https://mcp.tanachat.ai/health
2. **Review API docs**: https://mcp.tanachat.ai/docs
3. **Test with curl**: Use the testing examples above
4. **File an issue**: https://github.com/thomashaus/TanaChat/issues