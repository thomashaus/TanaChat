#!/usr/bin/env python3
"""
Tana JSON Outline Generator

Analyzes a Tana JSON export and displays a hierarchical outline.
Shows nodes up to specified depth (default: 2).

Usage:
    python3 tana_outline.py [json_file] [--depth N] [--workspace-id ID]
"""

import json
import argparse
from typing import Dict, List, Set, Optional
from collections import defaultdict

class TanaOutlineGenerator:
    def __init__(self, json_data: Dict, max_depth: int = 2, workspace_id: str = None, start_node: str = None):
        self.data = json_data
        self.max_depth = max_depth
        self.workspace_id = workspace_id
        self.start_node = start_node
        self.docs = {doc['id']: doc for doc in self.data.get('docs', [])}
        self.root_nodes = []
        self.processed_nodes = set()

    def identify_root_nodes(self) -> List[str]:
        """Identify root nodes using multiple strategies"""
        root_candidates = set()

        # Strategy 1: Nodes with no parentId
        for doc in self.docs.values():
            if not doc.get('parentId'):
                root_candidates.add(doc['id'])

        # Strategy 2: If workspace specified, find nodes expanded in that workspace
        if self.workspace_id and 'workspaces' in self.data:
            workspaces = self.data['workspaces']
            if self.workspace_id in workspaces:
                try:
                    workspace_info = json.loads(workspaces[self.workspace_id])
                    expanded_nodes = workspace_info.get('expanded', [])

                    # Extract node IDs from expanded paths
                    for expanded_path in expanded_nodes:
                        parts = expanded_path.split('+')
                        if len(parts) >= 2:  # workspace + root-tab + node-id
                            node_id = parts[-1]
                            if node_id in self.docs:
                                root_candidates.add(node_id)
                except json.JSONDecodeError:
                    pass

        # Strategy 3: Filter out system nodes
        user_root_nodes = []
        for node_id in root_candidates:
            if not node_id.startswith('SYS_'):
                user_root_nodes.append(node_id)

        # Strategy 4: Prioritize specific node types
        prioritized = []
        other = []

        for node_id in user_root_nodes:
            doc = self.docs.get(node_id, {})
            doc_type = doc.get('props', {}).get('_docType', '')
            name = doc.get('props', {}).get('name', '')

            # Prioritize organizational nodes
            if (doc_type in ['home', 'search'] or
                name in ['Home', 'Areas', 'Projects', 'Vision', 'Calendar', 'Tasks', 'Library', 'Resources'] or
                'Hub' in name):
                prioritized.append(node_id)
            else:
                other.append(node_id)

        self.root_nodes = prioritized + other
        return self.root_nodes

    def get_node_info(self, node_id: str) -> Dict:
        """Get formatted node information"""
        doc = self.docs.get(node_id, {})
        if not doc:
            return {'name': 'Unknown', 'type': 'unknown', 'id': node_id}

        props = doc.get('props', {})
        return {
            'name': props.get('name', 'Unnamed'),
            'type': props.get('_docType', 'unknown'),
            'id': node_id,
            'description': props.get('description', ''),
            'created': props.get('created'),
            'has_meta': '_metaNodeId' in props,
            'has_owner': '_ownerId' in props
        }

    def get_children(self, node_id: str) -> List[str]:
        """Get direct children of a node"""
        children = []
        for doc_id, doc in self.docs.items():
            if doc.get('parentId') == node_id:
                children.append(doc_id)

        # Sort by creation time if available
        def sort_key(doc_id):
            doc = self.docs.get(doc_id, {})
            created = doc.get('props', {}).get('created', 0)
            return created if created else 0

        children.sort(key=sort_key)
        return children

    def print_outline(self):
        """Print the hierarchical outline"""
        print("=" * 80)
        print("🏗️  TANA OUTLINE ANALYSIS")
        print("=" * 80)

        # Show workspace info
        if 'currentWorkspaceId' in self.data:
            print(f"Workspace ID: {self.data['currentWorkspaceId']}")

        total_nodes = len(self.docs)
        system_nodes = len([doc_id for doc_id in self.docs.keys() if doc_id.startswith('SYS_')])
        user_nodes = total_nodes - system_nodes

        print(f"Total nodes: {total_nodes:,}")
        print(f"System nodes: {system_nodes:,}")
        print(f"User nodes: {user_nodes:,}")
        print(f"Max depth: {self.max_depth}")

        # Show start node info if specified
        if self.start_node:
            print(f"Start node: {self.start_node}")
        print()

        # If start node is specified, show only that node and its children
        if self.start_node:
            if self.start_node in self.docs:
                info = self.get_node_info(self.start_node)
                print(f"🎯 STARTING NODE: {info['name']} ({info['type']})")
                print("-" * 50)
                print(f"🔗 ID: {self.start_node}")

                if info['description']:
                    desc = info['description'][:80] + '...' if len(info['description']) > 80 else info['description']
                    print(f"📝 {desc}")

                print()
                self._print_children(self.start_node, depth=1)
            else:
                print(f"❌ Start node '{self.start_node}' not found")
            return

        # Otherwise, identify and display root nodes
        root_nodes = self.identify_root_nodes()

        print(f"📑 ROOT NODES ({len(root_nodes)}):")
        print("-" * 50)

        if not root_nodes:
            print("No root nodes found")
            return

        # Display each root node and its children
        for i, root_id in enumerate(root_nodes[:20], 1):  # Limit to first 20 roots
            info = self.get_node_info(root_id)
            print(f"{i:2d}. {info['name']} ({info['type']})")

            if info['description']:
                desc = info['description'][:80] + '...' if len(info['description']) > 80 else info['description']
                print(f"     📝 {desc}")

            print(f"     🔗 ID: {root_id}")

            # Show children up to max_depth
            self._print_children(root_id, depth=1)
            print()

        if len(root_nodes) > 20:
            print(f"... and {len(root_nodes) - 20} more root nodes")

    def _print_children(self, node_id: str, depth: int):
        """Recursively print children with depth limiting"""
        if depth > self.max_depth:
            return

        children = self.get_children(node_id)
        if not children:
            return

        # Limit children shown per node to prevent overwhelming output
        max_children = 10
        shown_children = children[:max_children]
        remaining = len(children) - max_children

        for i, child_id in enumerate(shown_children):
            info = self.get_node_info(child_id)
            indent = "    " * depth

            # Node type icons
            icon = "📄"
            if info['type'] == 'search':
                icon = "🔍"
            elif info['type'] == 'home':
                icon = "🏠"
            elif info['type'] == 'tagDef':
                icon = "🏷️"
            elif info['has_meta']:
                icon = "⚙️"

            print(f"{indent}{'├─' if i < len(shown_children) - 1 or remaining > 0 else '└─'} {icon} {info['name']}")

            # Show additional info for important nodes
            if depth == 1 and info['description']:
                desc = info['description'][:60] + '...' if len(info['description']) > 60 else info['description']
                print(f"{indent}    │  📝 {desc}")

            # Recursively show children
            self._print_children(child_id, depth + 1)

        if remaining > 0:
            indent = "    " * depth
            print(f"{indent}└─ ... and {remaining} more children")

    def print_home_children_list(self, max_depth: int = 1):
        """Print just the specified node and its children names"""
        # Use custom start node if specified, otherwise find Home node
        start_node_id = None
        start_node_name = None

        if self.start_node:
            start_node_id = self.start_node
            if start_node_id in self.docs:
                start_node_name = self.docs[start_node_id].get('props', {}).get('name', 'Unknown')
            else:
                print(f"❌ Start node '{start_node_id}' not found")
                return
        else:
            # Find the Home node (usually has docType 'home' or name 'Home')
            for doc_id, doc in self.docs.items():
                if not doc.get('parentId'):
                    props = doc.get('props', {})
                    doc_type = props.get('_docType', '')
                    name = props.get('name', '')
                    if doc_type == 'home' or name.lower() == 'home':
                        start_node_id = doc_id
                        start_node_name = name
                        break

        if not start_node_id:
            print("❌ Start node not found")
            return

        # Get start node info
        start_info = self.get_node_info(start_node_id)
        print(f"🎯 {start_info['name']}")

        # If using Home node, find children by ownership pattern
        if not self.start_node:
            # Find Home children by looking for root nodes owned by Home
            home_children = []
            for doc_id, doc in self.docs.items():
                if not doc.get('parentId'):  # Root nodes only
                    props = doc.get('props', {})
                    owner_id = props.get('_ownerId')
                    if owner_id == start_node_id:
                        name = props.get('name', 'Unnamed')
                        home_children.append((doc_id, name))

            # Sort by creation time
            home_children.sort(key=lambda x: self.docs.get(x[0], {}).get('props', {}).get('created', 0))

            # Print Home children with optional depth
            if home_children:
                for child_id, name in home_children:
                    print(f"  └─ {name}")
                    # Show children of children if max_depth > 1
                    if max_depth > 1:
                        self._print_children_simple(child_id, depth=2, max_depth=max_depth)
            else:
                print("  └─ No children found")
        else:
            # For custom start nodes, use regular parent-child relationships
            children = self.get_children(start_node_id)
            if children:
                for child_id in children:
                    child_info = self.get_node_info(child_id)
                    print(f"  └─ {child_info['name']}")
                    # Show children of children if max_depth > 1
                    if max_depth > 1:
                        self._print_children_simple(child_id, depth=2, max_depth=max_depth)
            else:
                print("  └─ No children found")

    def _print_children_simple(self, node_id: str, depth: int, max_depth: int):
        """Simple version of _print_children for --list option"""
        if depth > max_depth:
            return

        children = self.get_children(node_id)
        if not children:
            return

        # Limit children shown per node
        max_children = 10
        shown_children = children[:max_children]
        remaining = len(children) - max_children

        for i, child_id in enumerate(shown_children):
            info = self.get_node_info(child_id)
            indent = "    " * depth

            print(f"{indent}{'├─' if i < len(shown_children) - 1 or remaining > 0 else '└─'} {info['name']}")

            # Recursively show children
            self._print_children_simple(child_id, depth + 1, max_depth)

        if remaining > 0:
            indent = "    " * depth
            print(f"{indent}└─ ... and {remaining} more")

    def print_statistics(self):
        """Print detailed statistics about the outline"""
        print("\n" + "=" * 80)
        print("📊 OUTLINE STATISTICS")
        print("=" * 80)

        # Node type distribution
        type_counts = defaultdict(int)
        for doc in self.docs.values():
            doc_type = doc.get('props', {}).get('_docType', 'unknown')
            type_counts[doc_type] += 1

        print("Node Type Distribution:")
        for doc_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {doc_type:20}: {count:6,}")

        # Tree depth statistics
        print(f"\nTree Statistics:")
        print(f"  Max display depth: {self.max_depth}")
        print(f"  Root nodes found: {len(self.root_nodes)}")

        # Calculate actual tree depth
        max_actual_depth = 0
        for root_id in self.root_nodes[:10]:  # Sample first 10 roots
            depth = self._calculate_depth(root_id, 0)
            max_actual_depth = max(max_actual_depth, depth)

        print(f"  Sample max actual depth: {max_actual_depth}")

    def _calculate_depth(self, node_id: str, current_depth: int) -> int:
        """Calculate the maximum depth from a given node"""
        if node_id in self.processed_nodes or current_depth > 50:  # Prevent infinite loops
            return current_depth

        self.processed_nodes.add(node_id)

        children = self.get_children(node_id)
        if not children:
            return current_depth

        max_child_depth = current_depth
        for child_id in children:
            child_depth = self._calculate_depth(child_id, current_depth + 1)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth


def main():
    parser = argparse.ArgumentParser(description='Generate outline from Tana JSON export')
    parser.add_argument('json_file', help='Path to Tana JSON export file')
    parser.add_argument('--depth', '-d', type=int, default=2,
                       help='Maximum depth to display (default: 2)')
    parser.add_argument('--workspace-id', '-w', type=str,
                       help='Workspace ID to filter nodes (optional)')
    parser.add_argument('--stats', '-s', action='store_true',
                       help='Show detailed statistics')
    parser.add_argument('--list', '-l', action='store_true',
                       help='Just list Home node and children names')
    parser.add_argument('--count', '-n', type=int, default=1,
                       help='Number of layers to show with --list (default: 1)')
    parser.add_argument('--start', type=str,
                       help='Starting node ID instead of Home node')

    args = parser.parse_args()

    try:
        # Load JSON data
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Generate outline
        generator = TanaOutlineGenerator(data, args.depth, args.workspace_id, args.start)

        if args.list:
            generator.print_home_children_list(args.count)
        else:
            generator.print_outline()

            if args.stats:
                generator.print_statistics()

    except FileNotFoundError:
        print(f"❌ Error: File '{args.json_file}' not found")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())