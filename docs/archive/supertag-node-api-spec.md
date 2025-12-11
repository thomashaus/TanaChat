# TanaChat Supertag & Node API Specification

## Overview
New API endpoints to provide direct access to Tana workspace supertags and nodes through TanaChat, enabling seamless integration with external applications and workflows.

## API Endpoints

### 1. GET /api/v1/supertags/list - supertag-list()
**Description**: Returns all supertags and their node IDs from the Tana workspace

**Request**:
```http
GET /api/v1/supertags/list
Authorization: Bearer <api_token>
```

**Response**:
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
        "fields": ["status", "deadline", "priority"],
        "inheritance_chain": []
      },
      {
        "name": "spark note",
        "node_id": "o6SogPA3v4oc",
        "usage_count": 156,
        "description": "Quick insights and ideas",
        "created": "2025-01-01T00:00:00Z",
        "fields": ["source", "tags"],
        "inheritance_chain": ["readwise"]
      }
    ],
    "total_count": 2,
    "last_updated": "2025-01-01T00:00:00Z"
  },
  "metadata": {
    "source": "keytags.json",
    "workspace_id": "workspace_123"
  }
}
```

### 2. GET /api/v1/nodes/{node_id} - node-read(nodeid)
**Description**: Returns markdown representation of a specific node

**Request**:
```http
GET /api/v1/nodes/XP0quB9qcpnO
Authorization: Bearer <api_token>
```

**Query Parameters**:
- `include_children` (boolean, default: false) - Include child nodes
- `format` (string, default: "markdown") - Response format: "markdown", "json"
- `depth` (integer, default: 1) - Maximum depth for child nodes

**Response**:
```json
{
  "success": true,
  "data": {
    "node_id": "XP0quB9qcpnO",
    "name": "Project Launch",
    "content": "# Project Launch\n\n## Description\nLaunch the new product initiative\n\n## Status\n🔄 In Progress\n\n**Created:** 2025-01-01\n**Modified:** 2025-01-02",
    "supertags": ["project"],
    "metadata": {
      "created": "2025-01-01T00:00:00Z",
      "modified": "2025-01-02T00:00:00Z",
      "node_id": "XP0quB9qcpnO",
      "parent_id": null
    },
    "children": [
      {
        "node_id": "child123",
        "name": "Tasks",
        "content": "## Tasks\n- [ ] Design mockups\n- [ ] Write documentation"
      }
    ]
  }
}
```

### 3. POST /api/v1/nodes/{node_id}/append - node-append(nodeid, markdown)
**Description**: Appends markdown content to a specific node

**Request**:
```http
POST /api/v1/nodes/XP0quB9qcpnO/append
Authorization: Bearer <api_token>
Content-Type: application/json

{
  "content": "## Update\nAdded new requirements section.",
  "position": "end",  // "start" | "end" | "before_section" | "after_section"
  "section": null,    // Section name for position targeting
  "create_backup": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "node_id": "XP0quB9qcpnO",
    "previous_version": "2025-01-02T00:00:00Z",
    "new_version": "2025-01-02T01:00:00Z",
    "backup_created": true,
    "backup_path": "/files/backups/XP0quB9qcpnO_2025-01-02T00:00:00Z.md",
    "content_preview": "# Project Launch\n\n## Description\n...\n## Update\nAdded new requirements section."
  },
  "metadata": {
    "modified_at": "2025-01-02T01:00:00Z",
    "content_length": 1250,
    "lines_added": 3
  }
}
```

### 4. GET /api/v1/nodes/by-supertag/{supertag} - node-list(supertag)
**Description**: Returns all nodes that have the specified supertag

**Request**:
```http
GET /api/v1/nodes/by-supertag/project
Authorization: Bearer <api_token>
```

**Query Parameters**:
- `include_inherited` (boolean, default: true) - Include nodes from inherited supertags
- `limit` (integer, default: 50) - Maximum number of results
- `offset` (integer, default: 0) - Pagination offset
- `sort_by` (string, default: "name") - Sort field: "name", "created", "modified"
- `order` (string, default: "asc") - Sort order: "asc", "desc"

**Response**:
```json
{
  "success": true,
  "data": {
    "supertag": "project",
    "supertag_info": {
      "name": "project",
      "node_id": "XP0quB9qcpnO",
      "description": "Project management and planning"
    },
    "nodes": [
      {
        "node_id": "XP0quB9qcpnO",
        "name": "Project Launch",
        "description": "Launch the new product initiative",
        "created": "2025-01-01T00:00:00Z",
        "modified": "2025-01-02T00:00:00Z",
        "child_count": 5,
        "content_preview": "Launch the new product initiative with..."
      },
      {
        "node_id": "ABC123DEF456",
        "name": "Website Redesign",
        "description": "Complete overhaul of company website",
        "created": "2025-01-03T00:00:00Z",
        "modified": "2025-01-04T00:00:00Z",
        "child_count": 8,
        "content_preview": "Redesign the company website to improve..."
      }
    ],
    "pagination": {
      "total_count": 2,
      "limit": 50,
      "offset": 0,
      "has_more": false
    },
    "included_inherited_tags": []
  }
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "code": "NODE_NOT_FOUND",
    "message": "Node with ID 'XP0quB9qcpnO' not found",
    "details": {
      "node_id": "XP0quB9qcpnO",
      "suggestion": "Check if the node ID is correct or use supertag-list() to see available nodes"
    }
  },
  "metadata": {
    "timestamp": "2025-01-01T00:00:00Z",
    "request_id": "req_123456789"
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `SUPERTAG_NOT_FOUND` | 404 | Supertag not found |
| `NODE_NOT_FOUND` | 404 | Node ID not found |
| `INVALID_NODE_ID` | 400 | Invalid node ID format |
| `INVALID_CONTENT` | 400 | Invalid markdown content |
| `APPEND_FAILED` | 500 | Failed to append content |
| `BACKUP_FAILED` | 500 | Failed to create backup |
| `UNAUTHORIZED` | 401 | Invalid or missing API token |
| `RATE_LIMITED` | 429 | Too many requests |

## Integration with KeyTags System

### API-to-Supertag Mapping
```json
{
  "apis": {
    "supertag_management": {
      "supertag_list": {
        "endpoint": "/api/v1/supertags/list",
        "method": "GET",
        "mapped_supertags": ["system", "admin"],
        "directory": "system",
        "description": "List all supertags in workspace"
      },
      "node_operations": {
        "endpoints": [
          "/api/v1/nodes/{node_id}",
          "/api/v1/nodes/{node_id}/append",
          "/api/v1/nodes/by-supertag/{supertag}"
        ],
        "method": ["GET", "POST"],
        "mapped_supertags": ["api", "integration"],
        "directory": "api",
        "description": "Node read, append, and list operations"
      }
    }
  }
}
```

### Directory Structure
```
files/
├── metadata/
│   ├── keytags.json (includes API mappings)
│   └── node_index.json (node to file mappings)
├── backups/ (automatic backups before modifications)
│   └── {node_id}_{timestamp}.md
└── export/
    ├── {supertag}/ (existing structure)
    │   ├── {node_id}.md
    │   └── {supertag}.md
    └── api-generated/ (API-sourced content)
        └── auto-generated/
```

## Implementation Requirements

### 1. Enhanced TanaImporter with JSON Parsing
```python
class TanaImporter:
    def get_supertag_list(self) -> List[Dict]:
        """Parse Tana JSON export and extract all supertags with their node IDs"""

    def read_node_markdown(self, node_id: str, include_children: bool = False) -> Dict:
        """Parse Tana JSON and find node by ID, convert to markdown"""

    def append_to_node(self, node_id: str, content: str, options: Dict = None) -> Dict:
        """Parse Tana JSON, locate node, and append content in JSON format"""

    def list_nodes_by_supertag(self, supertag: str, options: Dict = None) -> Dict:
        """Parse Tana JSON and find all nodes with specified supertag, including inheritance"""

    def parse_tana_json(self, file_path: str = None) -> Dict:
        """Load and parse Tana JSON export file"""

    def find_node_by_id(self, node_id: str, tana_data: Dict) -> Dict:
        """Recursively search for node by ID in Tana JSON structure"""

    def extract_node_content(self, node_data: Dict) -> str:
        """Extract content from Tana node and convert to markdown"""

    def update_node_content(self, node_id: str, new_content: str, tana_data: Dict) -> Dict:
        """Update node content in Tana JSON structure"""
```

### 2. JSON Parsing Strategy

The APIs will parse the actual Tana JSON export to extract live data:

```python
def parse_tana_export(self, file_path: str = None) -> Dict:
    """Parse Tana JSON export file and return structured data"""
    if not file_path:
        file_path = self.files_dir / "export" / "tana-export.json"

    with open(file_path, 'r', encoding='utf-8') as f:
        tana_data = json.load(f)

    # Extract supertags
    supertags = self.extract_supertags_from_json(tana_data)

    # Create node index
    node_index = self.create_node_index(tana_data)

    return {
        "supertags": supertags,
        "nodes": node_index,
        "raw_data": tana_data
    }

def extract_supertags_from_json(self, tana_data: Dict) -> List[Dict]:
    """Extract all supertags from Tana JSON"""
    supertags = []

    # Look for nodes with supertag definitions
    for node in self.traverse_nodes(tana_data):
        if self.is_supertag(node):
            supertag_info = {
                "name": node.get("name", ""),
                "node_id": node.get("uid", ""),
                "description": self.extract_description(node),
                "fields": self.extract_fields(node),
                "usage_count": self.count_supertag_usage(node.get("uid", ""), tana_data),
                "created": node.get("created", ""),
                "children": node.get("children", [])
            }
            supertags.append(supertag_info)

    return supertags
```

### 2. New API Controllers
```python
# mcp/src/main.py additions
@app.get("/api/v1/supertags/list", tags=["Supertags"])
async def supertag_list(user: dict = Depends(get_current_user)):

@app.get("/api/v1/nodes/{node_id}", tags=["Nodes"])
async def node_read(node_id: str, user: dict = Depends(get_current_user)):

@app.post("/api/v1/nodes/{node_id}/append", tags=["Nodes"])
async def node_append(node_id: str, request: AppendRequest, user: dict = Depends(get_current_user)):

@app.get("/api/v1/nodes/by-supertag/{supertag}", tags=["Nodes"])
async def node_list(supertag: str, user: dict = Depends(get_current_user)):
```

### 3. MCP Tools
```python
# New MCP tools for supertag/node operations
{
  "supertag_list": {
    "description": "List all supertags and their node IDs",
    "parameters": {}
  },
  "node_read": {
    "description": "Read a node as markdown",
    "parameters": {"node_id": "string"}
  },
  "node_append": {
    "description": "Append markdown to a node",
    "parameters": {"node_id": "string", "content": "string"}
  },
  "node_list": {
    "description": "List nodes by supertag",
    "parameters": {"supertag": "string"}
  }
}
```

## Use Cases

1. **External Integration**: Connect TanaChat with other tools and services
2. **Automation**: Automate node updates based on external triggers
3. **Reporting**: Generate reports from Tana workspace data
4. **Backup/Sync**: Sync Tana content with external systems
5. **Content Management**: Programmatic content creation and updates

## Security Considerations

1. **Authentication**: All endpoints require valid API token
2. **Authorization**: User-specific node access controls
3. **Rate Limiting**: Prevent API abuse
4. **Backup Creation**: Automatic backups before modifications
5. **Content Validation**: Validate markdown content
6. **Audit Logging**: Log all modifications for compliance

## Testing Strategy

1. **Unit Tests**: Test each API endpoint independently
2. **Integration Tests**: Test with real Tana workspace data
3. **Security Tests**: Test authentication and authorization
4. **Performance Tests**: Test with large datasets
5. **Backup Tests**: Verify backup creation and restoration