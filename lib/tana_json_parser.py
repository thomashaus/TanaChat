"""
Tana JSON Parser - Enhanced TanaImporter with JSON parsing capabilities

This module extends the TanaImporter to parse actual Tana JSON exports
and extract supertag and node information dynamically.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .colors import Colors
from .keytags_manager import KeyTagsManager


class TanaJSONParser:
    """Enhanced Tana JSON parsing capabilities"""

    def __init__(self, files_dir: Path = None):
        """Initialize with custom files directory"""
        self.files_dir = files_dir or Path("./files")
        self.metadata_dir = self.files_dir / "metadata"
        self.export_dir = self.files_dir / "export"
        self.keytags_manager = KeyTagsManager(self.files_dir)

        # Cache parsed data
        self._cached_data = None
        self._cache_timestamp = None

    def get_fresh_data(self, force_refresh: bool = False, cache_ttl: int = 60) -> Dict[str, Any]:
        """Get fresh or cached Tana JSON data with dynamic supertag awareness"""
        now = datetime.now()

        # Check if cache is valid (shorter TTL for dynamic data)
        if (not force_refresh and
            self._cached_data and
            self._cache_timestamp and
            (now - self._cache_timestamp).seconds < cache_ttl):
            return self._cached_data

        # Parse fresh data
        self._cached_data = self.parse_tana_json()
        self._cache_timestamp = now
        return self._cached_data

    def check_for_changes(self, previous_data: Dict = None) -> Dict[str, Any]:
        """Check if supertags or nodes have changed since last parse"""
        current_data = self.get_fresh_data(force_refresh=True)

        if not previous_data:
            return {
                "has_changes": True,
                "changes": {"initial_load": True},
                "previous_count": 0,
                "current_count": len(current_data.get("supertags", []))
            }

        previous_supertags = {s["node_id"]: s for s in previous_data.get("supertags", [])}
        current_supertags = {s["node_id"]: s for s in current_data.get("supertags", [])}

        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "usage_changes": []
        }

        # Check for added supertags
        for node_id, supertag in current_supertags.items():
            if node_id not in previous_supertags:
                changes["added"].append(supertag)

        # Check for removed supertags
        for node_id, supertag in previous_supertags.items():
            if node_id not in current_supertags:
                changes["removed"].append(supertag)

        # Check for modified supertags
        for node_id, current_supertag in current_supertags.items():
            if node_id in previous_supertags:
                previous = previous_supertags[node_id]

                # Check for meaningful changes (excluding usage count)
                if (current_supertag["name"] != previous["name"] or
                    current_supertag.get("description") != previous.get("description") or
                    len(current_supertag.get("fields", [])) != len(previous.get("fields", []))):
                    changes["modified"].append({
                        "node_id": node_id,
                        "previous": previous,
                        "current": current_supertag
                    })

                # Track usage count changes separately
                if (current_supertag.get("usage_count", 0) !=
                    previous.get("usage_count", 0)):
                    changes["usage_changes"].append({
                        "node_id": node_id,
                        "name": current_supertag["name"],
                        "previous_usage": previous.get("usage_count", 0),
                        "current_usage": current_supertag.get("usage_count", 0)
                    })

        has_changes = bool(any(changes[key] for key in ["added", "removed", "modified"]))

        return {
            "has_changes": has_changes,
            "changes": changes,
            "previous_count": len(previous_supertags),
            "current_count": len(current_supertags),
            "last_checked": datetime.now().isoformat()
        }

    def parse_tana_json(self, file_path: str = None) -> Dict[str, Any]:
        """Parse Tana JSON export file and return structured data"""
        if not file_path:
            # Look for Tana JSON export file
            possible_files = [
                self.export_dir / "tana-export.json",
                self.export_dir / "export.json",
                self.files_dir / "tana-export.json"
            ]

            file_path = None
            for possible_file in possible_files:
                if possible_file.exists():
                    file_path = str(possible_file)
                    break

            if not file_path:
                return {
                    "supertags": [],
                    "nodes": [],
                    "raw_data": {},
                    "error": "No Tana JSON export file found"
                }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tana_data = json.load(f)

            # Extract supertags
            supertags = self.extract_supertags_from_json(tana_data)

            # Create node index
            node_index = self.create_node_index(tana_data)

            return {
                "supertags": supertags,
                "nodes": node_index,
                "raw_data": tana_data,
                "source_file": file_path,
                "parsed_at": datetime.now().isoformat()
            }

        except Exception as e:
            Colors.error(f"Error parsing Tana JSON: {e}")
            return {
                "supertags": [],
                "nodes": [],
                "raw_data": {},
                "error": str(e)
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
                    "created": self.format_timestamp(node.get("created")),
                    "node_data": node
                }
                supertags.append(supertag_info)

        return supertags

    def create_node_index(self, tana_data: Dict) -> Dict[str, Dict]:
        """Create an index of all nodes for quick lookup"""
        node_index = {}

        for node in self.traverse_nodes(tana_data):
            node_id = node.get("uid", "")
            if node_id:
                node_index[node_id] = {
                    "name": node.get("name", ""),
                    "content": self.extract_content(node),
                    "supertags": self.extract_node_supertags(node),
                    "created": self.format_timestamp(node.get("created")),
                    "modified": self.format_timestamp(node.get("edited")),
                    "parent_id": self.extract_parent_id(node),
                    "children": node.get("children", []),
                    "raw_data": node
                }

        return node_index

    def traverse_nodes(self, tana_data: Dict, nodes: List = None) -> List[Dict]:
        """Recursively traverse all nodes in Tana JSON"""
        if nodes is None:
            nodes = []

        # Handle different Tana export formats
        if "nodes" in tana_data:
            # Format with explicit nodes array
            for node in tana_data["nodes"]:
                nodes.append(node)
                if "children" in node:
                    self.traverse_nodes({"nodes": node["children"]}, nodes)
        elif isinstance(tana_data, list):
            # Format with direct array of nodes
            for node in tana_data:
                nodes.append(node)
                if "children" in node:
                    self.traverse_nodes(node["children"], nodes)
        else:
            # Single node format
            nodes.append(tana_data)
            if "children" in tana_data:
                self.traverse_nodes(tana_data["children"], nodes)

        return nodes

    def is_supertag(self, node: Dict) -> bool:
        """Check if a node is a supertag"""
        # Look for supertag indicators
        return (
            node.get("type") == "supertag" or
            "supertag" in node.get("name", "").lower() or
            any(field.get("type") == "supertag" for field in node.get("fields", [])) or
            node.get("uid", "").startswith("supertag_")
        )

    def extract_description(self, node: Dict) -> str:
        """Extract description from node"""
        # Look for description in different possible locations
        description = ""

        if "description" in node:
            description = node["description"]
        elif "notes" in node:
            description = node["notes"]
        elif "children" in node:
            # Look for a description field in children
            for child in node["children"]:
                if child.get("name", "").lower() in ["description", "desc", "about"]:
                    description = self.extract_content(child)
                    break

        return description

    def extract_fields(self, node: Dict) -> List[Dict]:
        """Extract field definitions from supertag"""
        fields = []

        if "fields" in node:
            for field in node["fields"]:
                fields.append({
                    "name": field.get("name", ""),
                    "type": field.get("type", "text"),
                    "required": field.get("required", False),
                    "default": field.get("default", "")
                })

        return fields

    def extract_content(self, node: Dict) -> str:
        """Extract text content from node"""
        content_parts = []

        if "content" in node:
            content_parts.append(node["content"])

        if "children" in node:
            for child in node["children"]:
                if not self.is_supertag(child):
                    child_content = self.extract_content(child)
                    if child_content:
                        content_parts.append(child_content)

        return "\n".join(content_parts)

    def extract_node_supertags(self, node: Dict) -> List[str]:
        """Extract supertags applied to a node"""
        supertags = []

        if "supertags" in node:
            supertags.extend(node["supertags"])

        if "tags" in node:
            supertags.extend(node["tags"])

        return list(set(supertags))  # Remove duplicates

    def extract_parent_id(self, node: Dict) -> Optional[str]:
        """Extract parent node ID"""
        # This depends on the Tana JSON structure
        return node.get("parentId") or node.get("parent_id")

    def count_supertag_usage(self, supertag_id: str, tana_data: Dict) -> int:
        """Count how many nodes use this supertag"""
        count = 0

        for node in self.traverse_nodes(tana_data):
            if supertag_id in self.extract_node_supertags(node):
                count += 1

        return count

    def format_timestamp(self, timestamp: Any) -> str:
        """Format Tana timestamp to ISO format"""
        if not timestamp:
            return ""

        if isinstance(timestamp, str):
            return timestamp

        if isinstance(timestamp, (int, float)):
            # Handle Unix timestamp (milliseconds)
            return datetime.fromtimestamp(timestamp / 1000).isoformat()

        return str(timestamp)

    def find_node_by_id(self, node_id: str, tana_data: Dict = None) -> Optional[Dict]:
        """Find node by ID in Tana JSON structure"""
        if not tana_data:
            data = self.get_fresh_data()
            node_index = data.get("nodes", {})
            return node_index.get(node_id)

        for node in self.traverse_nodes(tana_data):
            if node.get("uid") == node_id:
                return node

        return None

    def list_nodes_by_supertag(self, supertag_name: str, options: Dict = None) -> Dict:
        """List all nodes with specified supertag, including inheritance"""
        if options is None:
            options = {}

        data = self.get_fresh_data()
        nodes = data.get("nodes", {})
        supertags = data.get("supertags", [])

        # Find the supertag ID
        supertag_id = None
        for supertag in supertags:
            if supertag["name"].lower() == supertag_name.lower():
                supertag_id = supertag["node_id"]
                break

        if not supertag_id:
            return {
                "success": False,
                "error": f"Supertag '{supertag_name}' not found"
            }

        # Get inheritance chain
        include_inherited = options.get("include_inherited", True)
        target_supertags = [supertag_id]

        if include_inherited:
            # TODO: Implement inheritance resolution from keytags
            pass

        # Filter nodes by supertag
        matching_nodes = []
        for node_id, node_info in nodes.items():
            node_supertags = set(node_info.get("supertags", []))
            if any(supertag in node_supertags for supertag in target_supertags):
                matching_nodes.append({
                    "node_id": node_id,
                    "name": node_info["name"],
                    "content_preview": (node_info["content"][:100] + "...") if len(node_info["content"]) > 100 else node_info["content"],
                    "created": node_info["created"],
                    "modified": node_info["modified"],
                    "supertags": node_info["supertags"]
                })

        # Sort results
        sort_by = options.get("sort_by", "name")
        reverse = options.get("order", "desc").lower() == "desc"
        matching_nodes.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)

        return {
            "success": True,
            "data": {
                "supertag": supertag_name,
                "supertag_id": supertag_id,
                "nodes": matching_nodes,
                "total_count": len(matching_nodes)
            }
        }

    def read_node_markdown(self, node_id: str, include_children: bool = False) -> Dict:
        """Read node content and convert to markdown"""
        data = self.get_fresh_data()
        nodes = data.get("nodes", {})

        node_info = nodes.get(node_id)
        if not node_info:
            return {
                "success": False,
                "error": f"Node '{node_id}' not found"
            }

        # Convert to markdown
        markdown_content = self.convert_node_to_markdown(node_info, include_children)

        return {
            "success": True,
            "data": {
                "node_id": node_id,
                "name": node_info["name"],
                "content": markdown_content,
                "supertags": node_info["supertags"],
                "metadata": {
                    "created": node_info["created"],
                    "modified": node_info["modified"],
                    "parent_id": node_info.get("parent_id")
                }
            }
        }

    def convert_node_to_markdown(self, node_info: Dict, include_children: bool = False) -> str:
        """Convert node data to markdown format"""
        content_parts = []

        # Title
        content_parts.append(f"# {node_info['name']}")
        content_parts.append("")

        # Supertags
        if node_info.get("supertags"):
            content_parts.append("## 🏷️ Supertags")
            for supertag in node_info["supertags"]:
                content_parts.append(f"- {supertag}")
            content_parts.append("")

        # Content
        if node_info.get("content"):
            content_parts.append("## 📝 Content")
            content_parts.append(node_info["content"])
            content_parts.append("")

        # Metadata
        metadata = []
        if node_info.get("created"):
            metadata.append(f"**Created:** {node_info['created']}")
        if node_info.get("modified"):
            metadata.append(f"**Modified:** {node_info['modified']}")

        if metadata:
            content_parts.append("## ℹ️ Metadata")
            content_parts.append(" | ".join(metadata))
            content_parts.append("")

        return "\n".join(content_parts)

    def get_supertag_list(self) -> Dict:
        """Get all supertags from Tana JSON"""
        data = self.get_fresh_data()
        supertags = data.get("supertags", [])

        return {
            "success": True,
            "data": {
                "supertags": supertags,
                "total_count": len(supertags),
                "last_updated": data.get("parsed_at"),
                "source_file": data.get("source_file")
            }
        }

    def append_to_node(self, node_id: str, content: str, options: Dict = None) -> Dict:
        """Append markdown content to a specific node in Tana JSON"""
        if options is None:
            options = {}

        try:
            # Get fresh data
            data = self.get_fresh_data(force_refresh=True)
            raw_data = data.get("raw_data", {})

            if not raw_data:
                return {
                    "success": False,
                    "error": "No Tana JSON data available"
                }

            # Find the node
            node_data = self.find_node_by_id(node_id, raw_data)
            if not node_data:
                return {
                    "success": False,
                    "error": f"Node '{node_id}' not found"
                }

            # Create backup before modification
            backup_result = self.create_node_backup(node_id, node_data)
            if not backup_result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to create backup: {backup_result['error']}"
                }

            # Append content based on options
            position = options.get("position", "end")
            section = options.get("section")
            create_backup = options.get("create_backup", True)

            # Convert node to JSON structure for modification
            modified_node = self.modify_node_content(node_data, content, position, section)

            # Update the node in the JSON structure
            update_result = self.update_node_in_json(node_id, modified_node, raw_data)
            if not update_result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to update node: {update_result['error']}"
                }

            # Save the modified JSON
            save_result = self.save_modified_json(raw_data, data.get("source_file"))
            if not save_result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to save changes: {save_result['error']}"
                }

            # Clear cache to force refresh
            self._cached_data = None
            self._cache_timestamp = None

            # Return success with metadata
            return {
                "success": True,
                "data": {
                    "node_id": node_id,
                    "previous_version": backup_result.get("timestamp"),
                    "new_version": datetime.now().isoformat(),
                    "backup_created": backup_result["success"],
                    "backup_path": backup_result.get("backup_path"),
                    "content_preview": self.generate_content_preview(modified_node),
                    "modification_info": {
                        "position": position,
                        "section": section,
                        "content_length": len(content)
                    }
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error appending to node: {str(e)}"
            }

    def create_node_backup(self, node_id: str, node_data: Dict) -> Dict:
        """Create a backup of the node before modification"""
        try:
            # Create backups directory if it doesn't exist
            backups_dir = self.files_dir / "backups"
            backups_dir.mkdir(parents=True, exist_ok=True)

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{node_id}_{timestamp}.md"
            backup_path = backups_dir / backup_filename

            # Convert node to markdown for backup
            markdown_content = self.convert_node_to_markdown({
                "name": node_data.get("name", ""),
                "content": self.extract_content(node_data),
                "supertags": self.extract_node_supertags(node_data),
                "created": self.format_timestamp(node_data.get("created")),
                "modified": self.format_timestamp(node_data.get("edited"))
            }, include_children=False)

            # Add backup metadata
            backup_header = f"""---
backup_timestamp: {datetime.now().isoformat()}
node_id: {node_id}
node_name: {node_data.get('name', 'Unknown')}
operation: pre-modification-backup
original_uid: {node_data.get('uid', 'unknown')}
---

"""

            # Write backup file
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_header + markdown_content)

            return {
                "success": True,
                "backup_path": str(backup_path),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def modify_node_content(self, node_data: Dict, content: str, position: str, section: str = None) -> Dict:
        """Modify node content by appending new content"""
        import copy

        # Create a deep copy to avoid modifying original
        modified_node = copy.deepcopy(node_data)

        # Extract current content
        current_content = self.extract_content(node_data)

        # Format new content for appending
        new_content = f"\n\n{content}" if current_content else content

        # Handle different positions
        if position == "start":
            modified_content = content + (f"\n\n{current_content}" if current_content else "")
        elif position == "end":
            modified_content = current_content + new_content
        elif position == "before_section" and section:
            # Find section and insert before it
            modified_content = self.insert_before_section(current_content, section, content)
        elif position == "after_section" and section:
            # Find section and insert after it
            modified_content = self.insert_after_section(current_content, section, content)
        else:
            # Default to end
            modified_content = current_content + new_content

        # Update the node's content
        if "content" in modified_node:
            modified_node["content"] = modified_content
        else:
            # If no content field, add one
            modified_node["content"] = modified_content

        # Update modified timestamp
        modified_node["edited"] = int(datetime.now().timestamp() * 1000)

        return modified_node

    def insert_before_section(self, content: str, section: str, new_content: str) -> str:
        """Insert content before a specific section"""
        lines = content.split('\n')
        section_pattern = f"## {section}"  # Assuming markdown sections

        for i, line in enumerate(lines):
            if line.strip() == section_pattern or section.lower() in line.lower():
                # Insert before this line
                lines.insert(i, f"\n{new_content}")
                break

        return '\n'.join(lines)

    def insert_after_section(self, content: str, section: str, new_content: str) -> str:
        """Insert content after a specific section"""
        lines = content.split('\n')
        section_pattern = f"## {section}"

        for i, line in enumerate(lines):
            if line.strip() == section_pattern or section.lower() in line.lower():
                # Find the end of this section (next ## or end of content)
                insert_pos = i + 1
                while (insert_pos < len(lines) and
                       not lines[insert_pos].strip().startswith("##") and
                       lines[insert_pos].strip()):
                    insert_pos += 1

                lines.insert(insert_pos, f"\n{new_content}")
                break

        return '\n'.join(lines)

    def update_node_in_json(self, node_id: str, modified_node: Dict, json_data: Dict) -> Dict:
        """Update a node in the JSON structure"""
        def find_and_update(nodes):
            for i, node in enumerate(nodes):
                if node.get("uid") == node_id:
                    nodes[i] = modified_node
                    return True
                # Recurse into children
                if "children" in node and isinstance(node["children"], list):
                    if find_and_update(node["children"]):
                        return True
            return False

        # Handle different JSON structures
        if "nodes" in json_data:
            if find_and_update(json_data["nodes"]):
                return {"success": True}
        elif isinstance(json_data, list):
            if find_and_update(json_data):
                return {"success": True}
        else:
            # Single node structure
            if json_data.get("uid") == node_id:
                # Update the entire structure
                json_data.update(modified_node)
                return {"success": True}

        return {
            "success": False,
            "error": f"Node '{node_id}' not found in JSON structure"
        }

    def save_modified_json(self, json_data: Dict, source_file: str) -> Dict:
        """Save the modified JSON back to the source file"""
        try:
            if not source_file:
                return {
                    "success": False,
                    "error": "No source file path available"
                }

            # Create backup of original file
            original_path = Path(source_file)
            backup_path = original_path.with_suffix(f".backup_{int(datetime.now().timestamp())}.json")

            if original_path.exists():
                import shutil
                shutil.copy2(original_path, backup_path)

            # Write modified JSON
            with open(source_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "backup_path": str(backup_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def generate_content_preview(self, node_data: Dict, max_length: int = 200) -> str:
        """Generate a preview of the node content"""
        content = self.extract_content(node_data)
        if len(content) <= max_length:
            return content
        else:
            return content[:max_length] + "..."