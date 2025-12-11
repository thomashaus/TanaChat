# TanaChat API Documentation - Complete Reference

## Overview
TanaChat provides a comprehensive API suite for accessing and modifying Tana workspace data through JSON exports. All APIs work with dynamic supertags and support real-time change detection.

## 🔐 Authentication
All API endpoints require a Bearer token for authentication:
```http
Authorization: Bearer YOUR_API_TOKEN
```

Get your API token from the user management system or use the `/api/auth/login` endpoint.

---

## 📊 **Complete API Reference**

### **1. Supertag Management APIs**

#### **GET /api/v1/supertags/list** - supertag-list()
Returns all supertags and their node IDs by parsing Tana JSON exports.

**Request:**
```http
GET /api/v1/supertags/list
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "success": true,
  "data": {
    "supertags": [
      {
        "name": "project",
        "node_id": "XP0quB9qcpnO",
        "usage_count": 42,
        "description": "Project management and planning",
        "created": "2025-01-01T00:00:00Z",
        "fields": [
          {"name": "status", "type": "select"},
          {"name": "deadline", "type": "date"}
        ]
      }
    ],
    "total_count": 1,
    "last_updated": "2025-01-01T00:00:00Z",
    "source_file": "/files/export/tana-export.json"
  },
  "metadata": {
    "user": "username",
    "timestamp": "2025-01-01T00:00:00Z"
  }
}
```

**MCP Tool Usage:**
```bash
{
  "method": "tools/call",
  "params": {
    "name": "supertag_list",
    "arguments": {
      "include_usage_count": true,
      "include_fields": false
    }
  }
}
```

---

#### **GET /api/v1/supertags/changes** - supertag_changes()
Check for changes in supertags since last check (handles dynamic supertags).

**Request:**
```http
GET /api/v1/supertags/changes?since_timestamp=2025-01-01T00:00:00Z&include_usage_changes=true
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "success": true,
  "data": {
    "has_changes": true,
    "changes": {
      "added": [
        {
          "name": "ai-research",
          "node_id": "XP1abC9qcpnO",
          "usage_count": 3
        }
      ],
      "removed": [],
      "modified": [],
      "usage_changes": [
        {
          "node_id": "XP0quB9qcpnO",
          "name": "project",
          "previous_usage": 42,
          "current_usage": 48
        }
      ]
    },
    "previous_count": 12,
    "current_count": 13,
    "last_checked": "2025-01-01T00:00:00Z"
  },
  "metadata": {
    "note": "Dynamic supertags detected - consider regular change checks"
  }
}
```

**MCP Tool Usage:**
```bash
{
  "method": "tools/call",
  "params": {
    "name": "supertag_changes",
    "arguments": {
      "include_usage_changes": true
    }
  }
}
```

---

### **2. Node Management APIs**

#### **GET /api/v1/nodes/{node_id}** - node_read(nodeid)
Read a Tana node and return as markdown.

**Request:**
```http
GET /api/v1/nodes/XP0quB9qcpnO?include_children=true&format=markdown
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "success": true,
  "data": {
    "node_id": "XP0quB9qcpnO",
    "name": "Project Launch",
    "content": "# Project Launch\n\n## 🏷️ Supertags\n- **project**\n\n## 📝 Content\nLaunch the new product initiative with comprehensive planning...\n\n## ℹ️ Metadata\n**Created:** 2025-01-01T00:00:00Z | **Modified:** 2025-01-02T00:00:00Z",
    "supertags": ["project"],
    "metadata": {
      "created": "2025-01-01T00:00:00Z",
      "modified": "2025-01-02T00:00:00Z",
      "parent_id": null
    }
  },
  "metadata": {
    "user": "username",
    "timestamp": "2025-01-01T00:00:00Z",
    "format": "markdown",
    "include_children": true
  }
}
```

**MCP Tool Usage:**
```bash
{
  "method": "tools/call",
  "params": {
    "name": "node_read",
    "arguments": {
      "node_id": "XP0quB9qcpnO",
      "include_children": true,
      "format": "markdown"
    }
  }
}
```

---

#### **GET /api/v1/nodes/by-supertag/{supertag}** - node_list(supertag)
List all nodes that have a specific supertag, including inheritance support.

**Request:**
```http
GET /api/v1/nodes/by-supertag/project?include_inherited=true&limit=10&sort_by=created&order=desc
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "success": true,
  "data": {
    "supertag": "project",
    "supertag_id": "XP0quB9qcpnO",
    "nodes": [
      {
        "node_id": "XP0quB9qcpnO",
        "name": "Project Launch",
        "content_preview": "Launch the new product initiative with...",
        "created": "2025-01-01T00:00:00Z",
        "modified": "2025-01-02T00:00:00Z",
        "supertags": ["project"]
      }
    ],
    "total_count": 1,
    "included_inherited_tags": []
  },
  "metadata": {
    "user": "username",
    "timestamp": "2025-01-01T00:00:00Z",
    "query_options": {
      "include_inherited": true,
      "limit": 10,
      "sort_by": "created",
      "order": "desc"
    }
  }
}
```

**MCP Tool Usage:**
```bash
{
  "method": "tools/call",
  "params": {
    "name": "node_list",
    "arguments": {
      "supertag": "project",
      "include_inherited": true,
      "limit": 10,
      "sort_by": "created",
      "order": "desc",
      "force_refresh": false
    }
  }
}
```

---

#### **POST /api/v1/nodes/{node_id}/append** - node_append(nodeid, markdown)
Append markdown content to a Tana node (write operation with automatic backups).

**Request:**
```http
POST /api/v1/nodes/XP0quB9qcpnO/append
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "content": "## Update\nAdded new requirements section after planning phase.",
  "position": "after_section",
  "section": "Planning",
  "create_backup": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "node_id": "XP0quB9qcpnO",
    "previous_version": "2025-01-02T00:00:00Z",
    "new_version": "2025-01-02T01:30:00Z",
    "backup_created": true,
    "backup_path": "/files/backups/XP0quB9qcpnO_20250102_013000.md",
    "content_preview": "# Project Launch\n\n## Description\nLaunch the new product initiative\n\n## Planning\nInitial planning phase completed\n\n## Update\nAdded new requirements section after planning phase.",
    "modification_info": {
      "position": "after_section",
      "section": "Planning",
      "content_length": 85
    }
  },
  "metadata": {
    "user": "username",
    "timestamp": "2025-01-02T01:30:00Z",
    "operation": "append",
    "note": "Changes saved to JSON file. Import into Tana to see changes."
  }
}
```

**MCP Tool Usage:**
```bash
{
  "method": "tools/call",
  "params": {
    "name": "node_append",
    "arguments": {
      "node_id": "XP0quB9qcpnO",
      "content": "## Update\nAdded new requirements section.",
      "position": "end",
      "create_backup": true
    }
  }
}
```

---

## 🔄 **Dynamic Supertags Handling**

### **Change Detection**
The APIs automatically handle the dynamic nature of Tana supertags:

- **Real-time Updates**: 60-second cache TTL (configurable)
- **Change Tracking**: Detects added, removed, modified supertags
- **Usage Monitoring**: Tracks changes in supertag usage counts
- **Force Refresh**: Bypass cache with `force_refresh=true` parameter

### **Cache Management**
```http
# Force fresh data (bypass cache)
GET /api/v1/supertags/list?force_refresh=true

# Short TTL for dynamic data
# Default: 60 seconds, configurable per request
```

### **Backup System**
All write operations create automatic backups:

1. **Node Backups**: Individual node markdown backups in `/files/backups/`
2. **JSON Backups**: Full JSON file backups before modifications
3. **Timestamp Tracking**: Precise modification timestamps
4. **Metadata Preservation**: Complete node metadata in backups

---

## 🛠️ **Advanced Features**

### **Content Positioning**
The `node_append` API supports precise content positioning:

| Position | Description | Example |
|----------|-------------|---------|
| `start` | Insert at beginning of node | Top of meeting notes |
| `end` | Append to end (default) | Add new action items |
| `before_section` | Insert before specific section | Before deadline section |
| `after_section` | Insert after specific section | After planning section |

### **Inheritance Support**
Supertag inheritance is automatically resolved:

```json
{
  "included_inherited_tags": ["readwise", "spark note"],
  "inheritance_chain": ["book note", "spark note", "readwise"]
}
```

### **Error Handling**
All APIs return consistent error responses:

```json
{
  "success": false,
  "error": {
    "code": "NODE_NOT_FOUND",
    "message": "Node with ID 'invalid_id' not found",
    "details": {
      "node_id": "invalid_id",
      "suggestion": "Use supertag_list() to see available nodes"
    }
  }
}
```

---

## 📝 **Usage Examples**

### **Complete Workflow Example**

1. **List all supertags:**
   ```bash
   curl -H "Authorization: Bearer TOKEN" \
     http://localhost:8000/api/v1/supertags/list
   ```

2. **Find project nodes:**
   ```bash
   curl -H "Authorization: Bearer TOKEN" \
     "http://localhost:8000/api/v1/nodes/by-supertag/project"
   ```

3. **Read specific node:**
   ```bash
   curl -H "Authorization: Bearer TOKEN" \
     http://localhost:8000/api/v1/nodes/XP0quB9qcpnO
   ```

4. **Append content to node:**
   ```bash
   curl -X POST -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"content": "## Action Items\n- Review requirements"}' \
     http://localhost:8000/api/v1/nodes/XP0quB9qcpnO/append
   ```

5. **Check for changes:**
   ```bash
   curl -H "Authorization: Bearer TOKEN" \
     "http://localhost:8000/api/v1/supertags/changes?include_usage_changes=true"
   ```

### **MCP Integration (Claude Desktop/ChatGPT)**

All APIs are available as MCP tools with the same functionality:

```bash
# Start TanaChat MCP server
./mcp/start.sh

# Connect Claude Desktop or ChatGPT
# Tools automatically available: supertag_list, node_read, node_list, node_append, supertag_changes
```

---

## 🔧 **Configuration**

### **File Structure**
```
files/
├── metadata/
│   └── keytags.json
├── export/
│   └── tana-export.json (source of truth)
├── backups/
│   ├── {node_id}_{timestamp}.md (node backups)
│   └── export.backup_{timestamp}.json (file backups)
└── users/
    └── {username}/ (user-specific data)
```

### **Environment Variables**
```bash
# API Configuration
API_URL=http://localhost:8000
CACHE_TTL=60

# File paths
EXPORT_DIR=./files/export
BACKUP_DIR=./files/backups

# Security
JWT_SECRET_KEY=your-secret-key
BACKUP_ENABLED=true
```

---

## 🧪 **Testing**

### **API Testing**
```bash
# Test health
curl http://localhost:8000/health

# Test authentication
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/auth/me

# Test supertag API
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/supertags/list
```

### **MCP Testing**
```bash
# Start MCP server
cd mcp && python src/main.py

# Test with MCP client
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "supertag_list",
    "arguments": {}
  }
}
```

---

## 📈 **Performance Considerations**

### **Caching Strategy**
- **Supertag List**: 60-second TTL for dynamic data
- **Node Content**: 30-second TTL for frequently accessed nodes
- **Change Detection**: Immediate cache invalidation on modifications

### **Large Dataset Handling**
- **Pagination**: Built-in support for large result sets
- **Lazy Loading**: Load JSON data on-demand
- **Memory Management**: Efficient JSON parsing with streaming

### **Backup Optimization**
- **Incremental Backups**: Only backup modified nodes
- **Compression**: Compress old backups after 30 days
- **Cleanup**: Automatic cleanup of backups older than 90 days

---

## 🔒 **Security Features**

### **Authentication**
- **Bearer Tokens**: Secure API key authentication
- **User Isolation**: Each user has isolated file directories
- **Session Management**: Configurable token expiration

### **Data Protection**
- **Automatic Backups**: Prevent data loss during modifications
- **Validation**: Input sanitization and validation
- **Audit Logging**: Comprehensive operation logging

### **Rate Limiting**
- **API Limits**: Configurable per-user rate limits
- **Bulk Operations**: Optimized for batch processing
- **Error Recovery**: Graceful degradation under load

---

## 🆕 **Future Enhancements**

### **Planned Features**
1. **Real-time Sync**: WebSocket-based real-time updates
2. **Webhook Support**: Event-driven notifications
3. **Advanced Search**: Full-text search across nodes
4. **Batch Operations**: Bulk node modifications
5. **Version Control**: Git-style versioning for nodes

### **Integration Possibilities**
- **External APIs**: Connect with project management tools
- **Automation**: IFTTT/Zapier integration
- **Analytics**: Usage statistics and insights
- **Collaboration**: Multi-user workspace sharing

---

This API provides comprehensive access to Tana workspace data with robust error handling, backup systems, and full support for the dynamic nature of Tana supertags.