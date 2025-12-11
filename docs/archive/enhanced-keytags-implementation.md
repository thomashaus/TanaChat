# TanaChat Enhanced KeyTags Implementation Plan

## Overview
Implement enhanced KeyTags functionality with support for:
1. API-to-supertag mapping
2. Directory-based organization with multi-supertag support
3. Supertag inheritance handling
4. MCP integration
5. Template system

## Key Features

### 1. Supertag Inheritance Support
```python
class KeyTagsManager:
    def get_inheritance_chain(self, supertag_name: str) -> List[str]:
        """Get the full inheritance chain for a supertag"""

    def resolve_directory_mapping(self, supertag_name: str) -> str:
        """Resolve directory mapping considering inheritance"""

    def get_all_supertags_in_directory(self, directory_name: str) -> List[str]:
        """Get all supertags (including inherited) that map to a directory"""
```

### 2. API Mapping System
```python
class APIMapper:
    def map_api_to_supertags(self, api_endpoint: str, supertags: List[str]):
        """Map an API endpoint to specific supertags"""

    def get_apis_for_supertag(self, supertag_name: str) -> List[Dict]:
        """Get all APIs mapped to a supertag (including inherited)"""

    def discover_apis_from_tana(self, tana_data: Dict) -> List[Dict]:
        """Discover API definitions from Tana export"""
```

### 3. Directory Management
```python
class DirectoryManager:
    def create_directory(self, name: str, supertags: List[str], template: str = None):
        """Create directory configuration with supertag mappings"""

    def add_supertags_to_directory(self, directory: str, supertags: List[str]):
        """Add supertags to existing directory"""

    def validate_directory_consistency(self) -> List[str]:
        """Check for conflicts in directory mappings"""
```

### 4. Enhanced Schema Design
```json
{
  "version": "2.0",
  "inheritance": {
    "day": ["diary"],
    "week": ["diary", "day"],
    "month": ["diary", "week", "day"],
    "quarter": ["diary", "month", "week", "day"],
    "year": ["diary", "quarter", "month", "week", "day"],
    "spark note": ["readwise"],
    "book note": ["readwise", "spark note"],
    "article": ["readwise", "spark note"],
    "tweet": ["readwise", "spark note"]
  },
  "directories": {
    "diary": {
      "description": "Time-based diary entries with inheritance",
      "primary_supertags": ["diary"],
      "inherited_supertags": ["day", "week", "month", "quarter", "year"],
      "template": "diary-entry",
      "inheritance_rules": {
        "children_inherit_parent_fields": true,
        "merge_inherited_templates": true
      },
      "created_at": "2025-01-01T00:00:00Z"
    },
    "readwise": {
      "description": "Readwise imports and highlights",
      "primary_supertags": ["readwise"],
      "inherited_supertags": ["spark note", "book note", "article", "tweet"],
      "template": "readwise-import",
      "inheritance_rules": {
        "children_inherit_parent_fields": true,
        "merge_inherited_templates": true,
        "auto_categorize": true
      },
      "created_at": "2025-01-01T00:00:00Z"
    }
  },
  "apis": {
    "diary_search": {
      "endpoint": "/api/diary/search",
      "method": "GET",
      "mapped_supertags": ["diary"],
      "inherited_supertags": ["day", "week", "month", "quarter", "year"],
      "directory": "diary",
      "description": "Search diary entries across all time periods"
    },
    "readwise_import": {
      "endpoint": "/api/readwise/import",
      "method": "POST",
      "mapped_supertags": ["readwise"],
      "inherited_supertags": ["spark note", "book note", "article", "tweet"],
      "directory": "readwise",
      "description": "Import Readwise highlights and notes",
      "parameters": {
        "source": ["book", "article", "tweet", "pdf"],
        "auto_categorize": true,
        "inherit_fields": true
      }
    },
    "spark_note_search": {
      "endpoint": "/api/spark-notes/search",
      "method": "GET",
      "mapped_supertags": ["spark note"],
      "inherited_supertags": ["readwise", "book note", "article", "tweet"],
      "directory": "readwise",
      "description": "Search spark notes including all Readwise content"
    }
  },
  "supertags": {
    "user_defined": { ... },
    "system": { ... }
  }
}
```

## Implementation Steps

### Phase 1: Core Infrastructure
1. **Extend KeyTagsManager with inheritance support**
   - Add inheritance chain resolution
   - Implement directory mapping with inheritance
   - Support for conflict detection

2. **Create API mapping system**
   - APIMapper class for API-to-supertag mapping
   - API discovery from Tana exports
   - Integration with existing keytags system

3. **Implement Directory Manager**
   - Directory creation and management
   - Multi-supertag directory support
   - Template system integration

### Phase 2: CLI Enhancement
4. **Update tanachat-keytags CLI**
   ```bash
   # Inheritance management
   tana-keytags inheritance show day
   tana-keytags inheritance add week day
   tana-keytags inheritance validate

   # Directory management
   tana-keytags directory create diary --supertags diary,day,week,month,quarter,year
   tana-keytags directory add-inheritance diary day week month
   tana-keytags directory show diary

   # API mapping
   tana-keytags api map diary_search /api/diary/search --directory diary
   tana-keytags api list --directory diary
   tana-keytags api discover --from-export
   ```

### Phase 3: Import/Export Enhancement
5. **Enhance TanaImporter for inheritance**
   - Process supertag inheritance during import
   - Create directory structures based on inheritance rules
   - Generate appropriate index files for inheritance hierarchies

6. **MCP Integration**
   - Add inheritance-aware tools
   - API mapping operations via MCP
   - Directory management through MCP

### Phase 4: Advanced Features
7. **Template System with Inheritance**
   - Template inheritance based on supertag hierarchy
   - Field merging and override rules
   - Conditional template sections

8. **Conflict Resolution System**
   - Handle conflicting directory mappings
   - Inheritance loop detection
   - User choice for conflict resolution

## Key Considerations

### Real-World Example: Readwise → Spark Note Inheritance

The Readwise use case is perfect for demonstrating inheritance benefits:

```json
{
  "inheritance": {
    "spark note": ["readwise"],
    "book note": ["readwise", "spark note"],
    "article": ["readwise", "spark note"],
    "tweet": ["readwise", "spark note"]
  },
  "directories": {
    "readwise": {
      "primary_supertags": ["readwise"],
      "inherited_supertags": ["spark note", "book note", "article", "tweet"],
      "description": "All Readwise content organized in one place"
    }
  }
}
```

**Benefits:**
- All Readwise content (books, articles, tweets) automatically goes to `/readwise/` directory
- `spark note` inherits Readwise's fields (source URL, highlights, tags)
- `book note` gets both Readwise and spark note fields
- API calls to any inherited supertag work across the entire Readwise directory

**Example CLI Operations:**
```bash
# Map readwise API - automatically covers all inherited supertags
tana-keytags api map readwise_import /api/readwise/import --directory readwise

# Spark notes search will work across all Readwise content
tana-keytags api map spark_note_search /api/spark-notes/search --directory readwise

# Add inheritance relationship
tana-keytags inheritance add "spark note" readwise
```

### 1. Inheritance Chain Resolution
```python
def resolve_inheritance_chain(self, supertag: str, visited: set = None) -> List[str]:
    """Resolve full inheritance chain with cycle detection"""
    if visited is None:
        visited = set()

    if supertag in visited:
        raise ValueError(f"Circular inheritance detected: {supertag}")

    visited.add(supertag)
    chain = [supertag]

    # Get direct parents from inheritance map
    parents = self.inheritance_map.get(supertag, [])
    for parent in parents:
        chain.extend(self.resolve_inheritance_chain(parent, visited.copy()))

    return chain
```

### 2. Directory Mapping with Inheritance
```python
def resolve_directory_for_supertag(self, supertag: str) -> str:
    """Resolve directory mapping considering inheritance"""
    # First check direct mapping
    if supertag in self.supertag_to_directory:
        return self.supertag_to_directory[supertag]

    # Check inheritance chain
    inheritance_chain = self.resolve_inheritance_chain(supertag)
    for ancestor in inheritance_chain[1:]:  # Skip self
        if ancestor in self.supertag_to_directory:
            return self.supertag_to_directory[ancestor]

    return None  # No directory mapping found
```

### 3. Conflict Detection
```python
def detect_inheritance_conflicts(self) -> List[Dict]:
    """Detect conflicts in inheritance and directory mappings"""
    conflicts = []

    # Check for circular inheritance
    for supertag in self.inheritance_map:
        try:
            self.resolve_inheritance_chain(supertag)
        except ValueError as e:
            conflicts.append({
                "type": "circular_inheritance",
                "supertag": supertag,
                "message": str(e)
            })

    # Check for conflicting directory mappings
    directory_supertags = {}
    for supertag, directory in self.supertag_to_directory.items():
        if directory in directory_supertags:
            conflicts.append({
                "type": "conflicting_directory_mapping",
                "directory": directory,
                "supertags": [directory_supertags[directory], supertag]
            })

    return conflicts
```

## Testing Strategy

### 1. Inheritance Testing
- Test complex inheritance chains
- Validate circular inheritance detection
- Test inheritance resolution with multiple levels

### 2. Directory Mapping Testing
- Test multi-supertag directories
- Validate inheritance-based directory resolution
- Test conflict detection and resolution

### 3. API Integration Testing
- Test API-to-supertag mapping
- Validate API discovery from exports
- Test MCP integration with inheritance

## Benefits

1. **Better Organization**: Hierarchical organization of related supertags
2. **Reduced Duplication**: Inherited properties reduce configuration duplication
3. **API Integration**: Seamless mapping between APIs and supertag hierarchies
4. **Flexibility**: Support for complex relationships and configurations
5. **Maintainability**: Clear inheritance patterns make systems easier to understand

## Migration Path

1. **Backward Compatibility**: Existing keytags.json files continue to work
2. **Gradual Migration**: Users can add inheritance and directory features incrementally
3. **Migration Tools**: CLI commands to help migrate existing configurations
4. **Documentation**: Comprehensive guides for new features

This implementation plan addresses the critical requirement for supertag inheritance while providing a robust foundation for API mapping and directory organization.