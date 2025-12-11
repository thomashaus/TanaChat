"""
Tana Parser - Parse and analyze Tana JSON exports

This module provides utilities for parsing and analyzing Tana JSON export files.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime


class TanaParser:
    """
    Parser for Tana JSON export files.

    Provides methods to extract and analyze node hierarchy, relationships,
    and metadata from Tana JSON exports.
    """

    def __init__(self, json_data: Dict):
        """
        Initialize the parser with JSON data.

        Args:
            json_data: Parsed Tana JSON data
        """
        self.data = json_data
        self.docs = {doc['id']: doc for doc in self.data.get('docs', [])}
        self.nodes_index = self._build_nodes_index()
        self.children_cache = {}

    def _build_nodes_index(self) -> Dict[str, Dict]:
        """
        Build a comprehensive index of all nodes for fast lookup.

        Returns:
            Dictionary mapping node IDs to their data
        """
        index = {}
        for doc_id, doc in self.docs.items():
            index[doc_id] = {
                'id': doc_id,
                'props': doc.get('props', {}),
                'parentId': doc.get('parentId'),
                'children': []
            }
        return index

    def get_node(self, node_id: str) -> Optional[Dict]:
        """
        Get node data by ID.

        Args:
            node_id: ID of the node

        Returns:
            Node data dictionary or None if not found
        """
        return self.nodes_index.get(node_id)

    def get_node_name(self, node_id: str) -> str:
        """
        Get the name of a node.

        Args:
            node_id: ID of the node

        Returns:
            Node name or 'Unnamed' if not found
        """
        node = self.get_node(node_id)
        if node:
            return node['props'].get('name', 'Unnamed')
        return 'Unknown'

    def get_node_type(self, node_id: str) -> str:
        """
        Get the type of a node.

        Args:
            node_id: ID of the node

        Returns:
            Node type or 'unknown' if not found
        """
        node = self.get_node(node_id)
        if node:
            return node['props'].get('_docType', 'unknown')
        return 'unknown'

    def get_children(self, node_id: str) -> List[str]:
        """
        Get direct children of a node.

        Args:
            node_id: ID of the parent node

        Returns:
            List of child node IDs
        """
        if node_id in self.children_cache:
            return self.children_cache[node_id]

        children = []
        for doc_id, doc in self.docs.items():
            if doc.get('parentId') == node_id:
                children.append(doc_id)

        # Sort by creation time if available
        def sort_key(child_id):
            child = self.get_node(child_id)
            if child:
                created = child['props'].get('created', 0)
                return created if created else 0
            return 0

        children.sort(key=sort_key)
        self.children_cache[node_id] = children
        return children

    def get_parent(self, node_id: str) -> Optional[str]:
        """
        Get the parent of a node.

        Args:
            node_id: ID of the child node

        Returns:
            Parent node ID or None if no parent
        """
        node = self.get_node(node_id)
        if node:
            return node.get('parentId')
        return None

    def get_path(self, node_id: str) -> List[str]:
        """
        Get the full path from root to a node.

        Args:
            node_id: ID of the target node

        Returns:
            List of node IDs from root to target
        """
        path = []
        current = node_id

        while current and current not in path:  # Prevent infinite loops
            path.append(current)
            current = self.get_parent(current)

        return list(reversed(path))

    def get_path_names(self, node_id: str) -> List[str]:
        """
        Get the full path names from root to a node.

        Args:
            node_id: ID of the target node

        Returns:
            List of node names from root to target
        """
        path_ids = self.get_path(node_id)
        return [self.get_node_name(node_id) for node_id in path_ids]

    def is_root_node(self, node_id: str) -> bool:
        """
        Check if a node is a root node (has no parent).

        Args:
            node_id: ID of the node to check

        Returns:
            True if the node is a root node
        """
        node = self.get_node(node_id)
        if node:
            return not node.get('parentId')
        return False

    def is_system_node(self, node_id: str) -> bool:
        """
        Check if a node is a system node.

        Args:
            node_id: ID of the node to check

        Returns:
            True if the node is a system node
        """
        return node_id.startswith('SYS_') if node_id else False

    def get_root_nodes(self) -> List[str]:
        """
        Get all root nodes (nodes with no parent).

        Returns:
            List of root node IDs
        """
        roots = []
        for node_id in self.nodes_index:
            if self.is_root_node(node_id) and not self.is_system_node(node_id):
                roots.append(node_id)
        return roots

    def count_descendants(self, node_id: str) -> int:
        """
        Count all descendants of a node.

        Args:
            node_id: ID of the node

        Returns:
            Number of descendants
        """
        count = 0
        children = self.get_children(node_id)

        for child_id in children:
            count += 1
            count += self.count_descendants(child_id)

        return count

    def get_tree_depth(self, node_id: str) -> int:
        """
        Get the maximum depth of the tree rooted at a node.

        Args:
            node_id: ID of the root node

        Returns:
            Maximum depth (0 for leaf nodes)
        """
        children = self.get_children(node_id)
        if not children:
            return 0

        max_child_depth = 0
        for child_id in children:
            child_depth = self.get_tree_depth(child_id)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth + 1

    def search_nodes(self, query: str, search_type: str = 'name') -> List[str]:
        """
        Search for nodes based on various criteria.

        Args:
            query: Search query
            search_type: Type of search ('name', 'description', 'type', 'all')

        Returns:
            List of matching node IDs
        """
        matches = []
        query_lower = query.lower()

        for node_id, node in self.nodes_index.items():
            props = node['props']

            if search_type in ['name', 'all']:
                name = props.get('name', '').lower()
                if query_lower in name:
                    matches.append(node_id)
                    continue

            if search_type in ['description', 'all']:
                description = props.get('description', '').lower()
                if query_lower in description:
                    matches.append(node_id)
                    continue

            if search_type in ['type', 'all']:
                node_type = props.get('_docType', '').lower()
                if query_lower in node_type:
                    matches.append(node_id)
                    continue

        return matches

    def get_nodes_by_type(self, node_type: str) -> List[str]:
        """
        Get all nodes of a specific type.

        Args:
            node_type: Type of nodes to find

        Returns:
            List of node IDs matching the type
        """
        matches = []
        for node_id, node in self.nodes_index.items():
            if node['props'].get('_docType') == node_type:
                matches.append(node_id)
        return matches

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the parsed data.

        Returns:
            Dictionary with various statistics
        """
        stats = {
            'total_nodes': len(self.nodes_index),
            'root_nodes': len(self.get_root_nodes()),
            'system_nodes': 0,
            'user_nodes': 0,
            'node_types': defaultdict(int),
            'max_depth': 0,
            'nodes_with_children': 0,
            'leaf_nodes': 0
        }

        # Count node types and system vs user nodes
        for node_id, node in self.nodes_index.items():
            if self.is_system_node(node_id):
                stats['system_nodes'] += 1
            else:
                stats['user_nodes'] += 1

            node_type = node['props'].get('_docType', 'unknown')
            stats['node_types'][node_type] += 1

        # Calculate tree depth and count nodes with children
        for root_id in self.get_root_nodes()[:10]:  # Sample first 10 roots for performance
            depth = self.get_tree_depth(root_id)
            stats['max_depth'] = max(stats['max_depth'], depth)

        # Count nodes with children vs leaf nodes
        for node_id in self.nodes_index:
            children = self.get_children(node_id)
            if children:
                stats['nodes_with_children'] += 1
            else:
                stats['leaf_nodes'] += 1

        return dict(stats)

    def validate_structure(self) -> List[str]:
        """
        Validate the structure of the Tana JSON data.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required top-level fields
        if 'docs' not in self.data:
            errors.append("Missing 'docs' field in JSON data")
            return errors

        docs = self.data['docs']
        if not isinstance(docs, list):
            errors.append("'docs' field must be a list")
            return errors

        # Check each document
        required_doc_fields = ['id']
        for i, doc in enumerate(docs):
            if not isinstance(doc, dict):
                errors.append(f"Document {i} is not an object")
                continue

            for field in required_doc_fields:
                if field not in doc:
                    errors.append(f"Document {i} missing required field: {field}")

            # Validate document structure
            if 'props' in doc and not isinstance(doc['props'], dict):
                errors.append(f"Document {i} 'props' field is not an object")

            # Check for circular references
            if 'parentId' in doc:
                parent_id = doc['parentId']
                if parent_id == doc.get('id'):
                    errors.append(f"Document {i} has itself as parent")

        return errors

    def export_summary(self) -> Dict[str, Any]:
        """
        Export a summary of the parsed data.

        Returns:
            Dictionary with summary information
        """
        stats = self.get_statistics()

        # Get workspace information
        workspace_info = {}
        if 'workspaces' in self.data:
            for ws_id, ws_data in self.data['workspaces'].items():
                try:
                    if ws_data:
                        workspace_parsed = json.loads(ws_data) if isinstance(ws_data, str) else ws_data
                        workspace_info[ws_id] = {
                            'size': len(str(ws_data)),
                            'expanded_nodes': len(workspace_parsed.get('expanded', []))
                        }
                    else:
                        workspace_info[ws_id] = {'size': 0, 'expanded_nodes': 0}
                except (json.JSONDecodeError, TypeError):
                    workspace_info[ws_id] = {'size': len(str(ws_data)), 'expanded_nodes': 0}

        # Get recent nodes
        recent_nodes = []
        for node_id, node in list(self.nodes_index.items())[:10]:
            created = node['props'].get('created')
            if created:
                try:
                    # Handle different timestamp formats
                    if isinstance(created, (int, float)):
                        created_dt = datetime.fromtimestamp(created / 1000 if created > 1e10 else created)
                    else:
                        created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    recent_nodes.append({
                        'id': node_id,
                        'name': self.get_node_name(node_id),
                        'created': created_dt.isoformat()
                    })
                except (ValueError, TypeError):
                    pass

        return {
            'statistics': stats,
            'workspace_info': workspace_info,
            'current_workspace': self.data.get('currentWorkspaceId'),
            'recent_nodes': recent_nodes[:5],  # Top 5 recent nodes
            'export_timestamp': datetime.now().isoformat()
        }