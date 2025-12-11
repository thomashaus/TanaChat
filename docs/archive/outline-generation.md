# TanaChat Outline Generator Specification

**Status**: ✅ Implemented
**Version**: 1.0
**Created**: 2025-12-10
**Updated**: 2025-12-10

## Overview

The TanaChat Outline Generator provides hierarchical outline generation from Tana JSON exports across multiple interfaces (CLI, MCP, REST API, and Web UI). This specification defines the requirements, implementation details, and API contracts for this feature.

## Requirements

### Functional Requirements

1. **Parse Tana JSON exports** and extract hierarchical node structure
2. **Generate hierarchical outlines** with configurable depth (1-10 levels)
3. **Support multiple output formats**: Outline view and List view
4. **Workspace filtering** by workspace ID for multi-workspace exports
5. **Custom starting points** by node ID instead of root nodes
6. **Include statistics** about node types, depth, and workspace structure
7. **File upload support** for direct JSON file processing
8. **Real-time validation** of JSON content before processing

### Non-Functional Requirements

1. **Performance**: Handle exports with up to 50,000 nodes efficiently
2. **Security**: Validate all input JSON to prevent injection attacks
3. **Usability**: Provide intuitive interfaces across all platforms
4. **Consistency**: Same behavior and output across CLI, MCP, REST, and Web
5. **Documentation**: Clear usage instructions and examples

## Architecture

### Core Components

```
┌─────────────────────┐
│   TanaOutlineGenerator   │  (bin/tanachat-outline)
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│      TanaParser      │  (lib/tana_parser.py)
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   Shared Logic      │  (Core algorithms)
└─────────────────────┘
```

### Interfaces

1. **CLI Tool**: `bin/tanachat-outline`
2. **MCP Server**: Tool `generate_outline` at `/mcp`
3. **REST API**: Endpoints at `/api/v1/outline/*`
4. **Web UI**: React component at `/outline`

## API Contracts

### CLI Interface

```bash
tanachat-outline [options] [json_file]

Options:
  --depth, -d N          Maximum depth to display (default: 2)
  --workspace-id, -w ID  Workspace ID to filter nodes
  --stats, -s            Show detailed statistics
  --list, -l             Simple list format
  --count, -n N         Layers with --list (default: 1)
  --start ID            Starting node ID
```

### MCP Server

**Tool Name**: `generate_outline`

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "content": {"type": "string", "description": "Tana JSON export content"},
    "max_depth": {"type": "integer", "default": 2, "description": "Maximum depth to display"},
    "workspace_id": {"type": "string", "description": "Workspace ID to filter nodes"},
    "start_node": {"type": "string", "description": "Starting node ID"},
    "format": {"type": "string", "enum": ["outline", "list"], "default": "outline"},
    "include_stats": {"type": "boolean", "default": false}
  },
  "required": ["content"]
}
```

**Response**:
```json
{
  "content": [
    {
      "type": "text",
      "text": "🏗️ TANA OUTLINE GENERATION\n\n[hierarchical outline text]"
    }
  ]
}
```

### REST API

#### POST /api/v1/outline/generate

**Request Body**:
```typescript
interface OutlineRequest {
  content: string;
  max_depth: number;
  workspace_id?: string;
  start_node?: string;
  format: 'outline' | 'list';
  include_stats: boolean;
}
```

**Response**:
```json
{
  "success": true,
  "outline": "hierarchical outline text...",
  "metadata": {
    "max_depth": 2,
    "workspace_id": "ws_123",
    "format": "outline",
    "include_stats": true,
    "total_nodes": 15432
  }
}
```

#### POST /api/v1/outline/validate

**Request Body**:
```json
{
  "content": "Tana JSON content..."
}
```

**Response**:
```json
{
  "valid": true,
  "message": "Valid Tana JSON format",
  "stats": {
    "total_nodes": 15432,
    "root_nodes": 3,
    "has_workspaces": true,
    "workspace_count": 2
  }
}
```

### Web Interface

**Route**: `/outline`

**Features**:
- File upload with drag-and-drop
- Real-time JSON validation
- Configuration options
- Live preview
- Download functionality
- Responsive design

## Data Models

### Tana JSON Structure

```json
{
  "currentWorkspaceId": "ws_abc123",
  "docs": [
    {
      "id": "node_123",
      "parentId": "node_456",
      "props": {
        "name": "Node Name",
        "_docType": "node",
        "description": "Optional description",
        "created": 1703123456789
      }
    }
  ],
  "workspaces": {
    "ws_abc123": "{\"expanded\":[\"ws_abc123+root-tab+node_789\"]}"
  }
}
```

### Node Information

```typescript
interface NodeInfo {
  name: string;
  type: string;
  id: string;
  description: string;
  created: number | null;
  has_meta: boolean;
  has_owner: boolean;
}
```

## Implementation Details

### Core Algorithm

1. **Parse JSON**: Validate and parse Tana JSON export
2. **Build Index**: Create node index for efficient lookup
3. **Identify Roots**: Find root nodes using multiple strategies
4. **Generate Hierarchy**: Build tree structure with depth limiting
5. **Format Output**: Apply format-specific rendering
6. **Add Statistics**: Generate metadata if requested

### Root Node Detection

1. **Strategy 1**: Nodes without `parentId`
2. **Strategy 2**: Nodes expanded in specified workspace
3. **Strategy 3**: Filter out system nodes (SYS_ prefix)
4. **Strategy 4**: Prioritize organizational nodes

### Performance Optimizations

1. **Node Indexing**: O(1) node lookup by ID
2. **Children Caching**: Cache child relationships
3. **Output Limiting**: Limit displayed nodes to prevent overflow
4. **Lazy Evaluation**: Calculate statistics only when needed

## Error Handling

### Validation Errors

- **Invalid JSON**: Return descriptive error with line/column
- **Missing Fields**: Specify required JSON structure
- **File Errors**: Handle missing/invalid files gracefully

### Runtime Errors

- **Memory Limits**: Handle large exports gracefully
- **Timeout**: Prevent infinite loops in circular references
- **Permission Errors**: Handle file access issues

## Security Considerations

### Input Validation

1. **JSON Structure**: Validate against expected schema
2. **Size Limits**: Limit input size to prevent DoS
3. **Content Sanitization**: Escape output appropriately

### Output Sanitization

1. **Text Encoding**: Ensure proper UTF-8 handling
2. **XSS Prevention**: Escape HTML in web interface
3. **Path Traversal**: Validate file paths and IDs

## Testing Strategy

### Unit Tests

- **TanaParser**: JSON parsing and node analysis
- **TanaOutlineGenerator**: Outline generation logic
- **Validation**: Input validation functions

### Integration Tests

- **CLI Tool**: Command-line interface testing
- **MCP Server**: Tool call/response validation
- **REST API**: Endpoint testing with various inputs
- **Web UI**: Component testing with user interactions

### Performance Tests

- **Large Exports**: Test with 10K+ nodes
- **Memory Usage**: Monitor memory consumption
- **Response Time**: Ensure <2s for typical exports

## Deployment

### Environment Variables

```bash
# No specific environment variables required
# Uses standard TanaChat configuration
```

### Dependencies

- **Python 3.12+**: For CLI and MCP server
- **Node.js 18+**: For web interface
- **FastAPI**: REST API server
- **React**: Web frontend

## Monitoring

### Metrics

- **Usage**: Number of outlines generated per day
- **Performance**: Average processing time
- **Errors**: Validation failure rate
- **Size**: Average export size processed

### Logging

- **INFO**: Successful outline generation
- **WARN**: Large exports or near limits
- **ERROR**: Validation failures and exceptions

## Future Enhancements

### Version 2.0 Features

1. **Real-time Collaboration**: Multiple users editing outlines
2. **Export Formats**: PDF, Markdown, HTML exports
3. **Custom Templates**: User-defined outline templates
4. **Advanced Filtering**: Tag-based and date-based filtering
5. **API Rate Limiting**: Prevent abuse of endpoints

### Potential Integrations

1. **Tana API Integration**: Direct API calls to Tana
2. **Cloud Storage**: Integration with S3, Google Drive
3. **Search Integration**: Full-text search within outlines
4. **Analytics**: Usage analytics and user behavior tracking

## Related Specifications

- [Tana JSON Export Format](./tana-json-format.md)
- [MCP Server Architecture](./mcp-server.md)
- [REST API Guidelines](./rest-api.md)
- [Web UI Components](./web-components.md)

## Implementation Checklist

- [x] CLI tool implementation
- [x] MCP server integration
- [x] REST API endpoints
- [x] Web UI component
- [x] Input validation
- [x] Error handling
- [x] Documentation
- [x] Security review
- [x] Performance optimization
- [x] Testing coverage

## Support

For issues or questions regarding this specification:
- Create an issue in the TanaChat repository
- Contact the development team
- Check the troubleshooting guide in the main documentation