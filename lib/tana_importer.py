"""
Tana Importer - Core business logic for importing Tana JSON exports

This module contains the core functionality for importing Tana JSON exports
and converting them to organized markdown files with directory structure.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

from .tana_io import TanaIO
from .colors import Colors


def add_markdown_footer(content: List[str], source_file: Path = None) -> List[str]:
    """Add footer with import filename and date/time to markdown content"""
    if source_file and source_file.exists():
        # Get file modification time
        mod_time = datetime.fromtimestamp(source_file.stat().st_mtime)
        footer = f"\n\n---\n*Imported from {source_file.name} -- {mod_time.strftime('%Y-%m-%d %H:%M:%S')}*"
        content.append(footer)
    return content


class TanaImporter:
    """Core Tana import functionality"""

    def __init__(self, files_dir: Path = None):
        """Initialize with custom files directory"""
        self.tana_io = TanaIO(files_dir)

    def extract_all_supertags(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all supertags and count occurrences"""
        supertags = {}

        # Handle different Tana JSON formats
        nodes = data.get('nodes', data.get('docs', []))

        def extract_and_count(items):
            for item in items:
                if not isinstance(item, dict):
                    continue

                # Handle Tagr format supertag definitions
                props = item.get('props', {})
                if props.get('_docType') == 'tagDef':
                    tag_id = item.get('id', '')
                    tag_name = props.get('name', '')

                    if tag_id and tag_name:
                        if tag_id not in supertags:
                            supertags[tag_id] = {
                                'name': tag_name,
                                'count': 0
                            }
                        # Don't increment count for definitions, only for usage

                # Handle supertags array (Tana Intermediate Format)
                elif 'supertags' in item:
                    for supertag in item.get('supertags', []):
                        if isinstance(supertag, dict):
                            tag_id = supertag.get('uid', supertag.get('id', ''))
                            tag_name = supertag.get('name', '')

                            if tag_id and tag_name:
                                if tag_id not in supertags:
                                    supertags[tag_id] = {
                                        'name': tag_name,
                                        'count': 0
                                    }
                                supertags[tag_id]['count'] += 1

                # Recursively process children
                children = item.get('children', [])
                if children:
                    extract_and_count(children)

        # Start extraction
        extract_and_count(nodes)

        return supertags

    def create_supertags_md(self, supertags: Dict[str, Any], export_dir: Path, source_file: Path = None) -> None:
        """Create SuperTags.md with all supertags and usage counts"""
        # Filter out system supertags
        user_defined = {
            tag_id: tag_data for tag_id, tag_data in supertags.items()
            if not tag_id.startswith('SYS_')
        }

        content = [
            "# SuperTags Analysis",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total unique supertags: {len(supertags)}",
            f"Showing: {len(user_defined)} user-defined supertags (excluding system tags)",
            "---",
            "",
            "| Supertag Name | Node ID | Usage Count |",
            "|---------------|---------|-------------|"
        ]

        # Sort by count descending
        sorted_supertags = sorted(
            user_defined.items(),
            key=lambda x: x[1].get('count', 0),
            reverse=True
        )

        for tag_id, tag_data in sorted_supertags:
            name = tag_data.get('name', 'Unknown')
            count = tag_data.get('count', 0)
            content.append(f"| {name} | `{tag_id}` [(tana)](https://app.tana.inc?nodeid={tag_id}) | {count} |")

        content = add_markdown_footer(content, source_file)

        supertags_file = export_dir / "SuperTags.md"
        with open(supertags_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

    def find_home_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Find the home/root node in the Tana data"""
        docs = data.get('docs', [])

        # Look for nodes with specific patterns
        for doc in docs:
            if not isinstance(doc, dict):
                continue

            # Check for home-like patterns
            name = doc.get('name', '').lower()
            if any(pattern in name for pattern in ['home', 'root', 'main', 'start']):
                return doc

        # Return first doc as fallback
        if docs and isinstance(docs[0], dict):
            return docs[0]

        return {}

    def create_home_md(self, home_node: Dict[str, Any], export_dir: Path, source_file: Path = None) -> None:
        """Create Home.md with home node information"""
        name = home_node.get('name', 'Home')
        node_id = home_node.get('id', home_node.get('uid', 'unknown'))

        content = [
            f"# {name}",
            "",
            f"**Node ID:** `{node_id}` [(tana)](https://app.tana.inc?nodeid={node_id})",
            ""
        ]

        # Add description if available
        description = home_node.get('description', '')
        if description:
            content.extend([
                f"**Description:** {description}",
                ""
            ])

        # Add metadata
        created = home_node.get('created')
        if created:
            content.extend([
                f"**Created:** {datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d %H:%M:%S')}",
                ""
            ])

        content = add_markdown_footer(content, source_file)

        home_file = export_dir / "Home.md"
        with open(home_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

    def load_keytags(self, files_dir: Path) -> Dict[str, Any]:
        """Load keytags.json file"""
        keytags_file = files_dir / "metadata" / "keytags.json"

        if not keytags_file.exists():
            Colors.error(f"KeyTags file not found: {keytags_file}")
            Colors.info("Please run tana-keytags setup first to create the keytags.json file")
            return {}

        try:
            with open(keytags_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            Colors.error(f"Invalid JSON in keytags file: {e}")
            return {}
        except Exception as e:
            Colors.error(f"Error loading keytags file: {e}")
            return {}

    def extract_nodes_by_supertag(self, data: Dict[str, Any], keytags_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all nodes grouped by their supertags"""
        nodes_by_supertag = {}

        # Get target supertags from keytags
        target_supertags = {}
        for tag_data in keytags_data.get('supertags', {}).get('user_defined', {}).values():
            tag_name = tag_data.get('name', '')
            if tag_name:
                target_supertags[tag_name] = tag_data.get('node_id', '')

        # Handle different Tana JSON formats
        docs = data.get('docs', data.get('nodes', []))

        # Build a mapping of meta node IDs to supertag names
        # This is needed because Tana uses _metaNodeId to reference supertag definitions
        # through a metanode hierarchy: Node -> metanode -> tuple -> supertag
        meta_node_to_supertag = {}

        # Create efficient lookup
        doc_lookup = {doc.get('id'): doc for doc in docs}

        # Build target supertag ID set
        target_supertag_ids = set(target_supertags.values())

        print(f"  Building metanode mappings for {len(target_supertag_ids)} target supertags...")

        # Now trace the metanode hierarchy efficiently
        for doc in docs:
            if not doc.get('children'):
                continue

            doc_id = doc.get('id')
            children = doc.get('children', [])

            # Check if this document has a structure we care about
            for child_id in children:
                child_doc = doc_lookup.get(child_id)
                if not child_doc or not child_doc.get('children'):
                    continue

                child_children = child_doc.get('children', [])
                for grandchild_id in child_children:
                    if grandchild_id in target_supertag_ids:
                        # Found mapping!
                        for supertag_name, supertag_id in target_supertags.items():
                            if grandchild_id == supertag_id:
                                meta_node_to_supertag[doc_id] = supertag_name
                                break

        def traverse_nodes(items, parent_path=None):
            for item in items:
                if not isinstance(item, dict):
                    continue

                props = item.get('props', {})

                # Skip supertag definition nodes themselves
                if props.get('_docType') == 'tagDef':
                    continue

                # Check if this node has any target supertags via _metaNodeId
                meta_node_id = props.get('_metaNodeId')
                if meta_node_id and meta_node_id in meta_node_to_supertag:
                    supertag_name = meta_node_to_supertag[meta_node_id]

                    # Filter out supertag definition nodes
                    # These have names like "Field defaults for Everything tagged #X"
                    # and are not actual content nodes
                    node_name = props.get('name', '')
                    if not node_name.startswith('Field defaults for'):
                        if supertag_name not in nodes_by_supertag:
                            nodes_by_supertag[supertag_name] = []

                        nodes_by_supertag[supertag_name].append({
                            'name': node_name or 'Untitled',
                            'node_id': item.get('id', item.get('uid', 'unknown')),
                            'description': props.get('description', ''),
                            'created': props.get('created'),
                            'children': item.get('children', []),
                            'path': parent_path
                        })

                # Also check for direct supertag references (legacy format)
                node_supertags = item.get('supertags', [])
                for supertag in node_supertags:
                    if isinstance(supertag, dict):
                        supertag_id = supertag.get('id', supertag.get('uid', ''))
                        supertag_name = supertag.get('name', '')

                        # Check if this matches any of our target supertags
                        for target_name, target_id in target_supertags.items():
                            if (supertag_id == target_id or
                                supertag_name.lower() == target_name.lower()):

                                # Filter out supertag definition nodes
                                node_name = props.get('name', '')
                                if not node_name.startswith('Field defaults for'):
                                    if target_name not in nodes_by_supertag:
                                        nodes_by_supertag[target_name] = []

                                    nodes_by_supertag[target_name].append({
                                        'name': node_name or 'Untitled',
                                        'node_id': item.get('id', item.get('uid', 'unknown')),
                                        'description': props.get('description', ''),
                                        'created': props.get('created'),
                                        'children': item.get('children', []),
                                        'path': parent_path
                                    })

                # Recursively process children
                children = item.get('children', [])
                if children:
                    current_name = props.get('name', 'Untitled')
                    current_path = f"{parent_path} / {current_name}" if parent_path else current_name
                    traverse_nodes(children, current_path)

        # Start traversal
        traverse_nodes(docs)

        return nodes_by_supertag

    def format_node_content(self, node_info: Dict[str, Any]) -> str:
        """Format node content as markdown"""
        content = []

        # Node name (title)
        node_name = node_info.get('name', 'Untitled')
        content.append(f"# {node_name}")

        # Node metadata
        node_id = node_info.get('node_id', 'unknown')
        content.append(f"**Node ID:** `{node_id}`")

        # Description
        description = node_info.get('description', '')
        if description and description.strip():
            content.append(f"**Description:** {description}")

        # Created date
        created = node_info.get('created')
        if created:
            if isinstance(created, str):
                # ISO format string
                content.append(f"**Created:** {created}")
            else:
                # Timestamp in milliseconds
                created_date = datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d %H:%M:%S')
                content.append(f"**Created:** {created_date}")

        # Path
        path = node_info.get('path', '')
        if path:
            content.append(f"**Path:** {path}")

        content.append("---")
        content.append("")

        # Children and subnodes as structured data
        children = node_info.get('children', [])
        if children:
            content.append("## 📋 Content & Subnodes")
            content.extend(self.format_children_as_data(children))

        return '\n'.join(content)

    def format_children_as_data(self, children: List[Any], level: int = 0) -> List[str]:
        """Format child nodes as structured data in markdown"""
        content = []

        for child in children:
            if isinstance(child, str):
                # This is a reference to another node
                content.append(f"- **Reference:** `{child}`")
                continue

            if isinstance(child, dict):
                child_name = child.get('name', 'Untitled')
                child_id = child.get('id', child.get('uid', 'unknown'))
                child_desc = child.get('description', '')
                child_created = child.get('created')

                # Create structured data block for each child
                content.append(f"### {child_name}")
                content.append(f"```yaml")
                content.append(f"name: {child_name}")
                content.append(f"node_id: {child_id}")

                if child_desc:
                    content.append(f"description: {child_desc}")

                if child_created:
                    if isinstance(child_created, str):
                        content.append(f"created: {child_created}")
                    else:
                        created_date = datetime.fromtimestamp(child_created/1000).strftime('%Y-%m-%d %H:%M:%S')
                        content.append(f"created: {created_date}")

                # Check for additional properties
                props = child.get('props', {})
                if props:
                    content.append("properties:")
                    for key, value in props.items():
                        if key not in ['name', 'description', 'created']:
                            content.append(f"  {key}: {value}")

                content.append("```")
                content.append("")

                # Recursively process children
                child_children = child.get('children', [])
                if child_children:
                    content.extend(self.format_children_as_data(child_children, level + 1))

        return content

    def format_children(self, children: List[Any], level: int = 0) -> List[str]:
        """Format child nodes as markdown (legacy method)"""
        content = []

        for child in children:
            if isinstance(child, str):
                # This is a reference to another node
                content.append(f"{'  ' * level}  - Referenced node: `{child}`")
                continue

            if isinstance(child, dict):
                child_name = child.get('name', 'Untitled')
                child_id = child.get('id', child.get('uid', 'unknown'))

                content.append(f"{'  ' * (level + 1)}- **{child_name}** (`{child_id}`)")

                # Add description if available
                child_desc = child.get('description', '')
                if child_desc and child_desc.strip():
                    content.append(f"{'  ' * (level + 2)}- {child_desc}")

                # Recursively process children
                child_children = child.get('children', [])
                if child_children:
                    content.extend(self.format_children(child_children, level + 2))

        return content

    def create_supertag_directories(self, nodes_by_supertag: Dict[str, List[Dict[str, Any]]], export_dir: Path, data: Dict[str, Any] = None) -> int:
        """Create directories and markdown files for each supertag with index + individual node files"""
        total_files_created = 0

        # Create doc_lookup for efficient child content resolution
        doc_lookup = {}
        if data:
            docs = data.get('docs', data.get('nodes', []))
            doc_lookup = {doc.get('id'): doc for doc in docs}

        for supertag_name, nodes in nodes_by_supertag.items():
            if not nodes:
                continue

            # Create directory (replace spaces with hyphens and lowercase)
            dir_name = supertag_name.replace(' ', '-').lower()
            supertag_dir = export_dir / dir_name
            supertag_dir.mkdir(parents=True, exist_ok=True)

            Colors.info(f"📁 Creating {len(nodes)} files in '{supertag_name}' directory")

            # First, create all individual node files using node ID as filename
            node_files = {}
            for node_info in nodes:
                node_id = node_info.get('node_id', 'unknown')
                filename = f"{node_id}.md"
                file_path = supertag_dir / filename

                # Format content with the new structure
                markdown_content = self.format_node_content_new(node_info, supertag_name, doc_lookup)

                # Write individual node file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                node_files[node_id] = {
                    'name': node_info.get('name', 'Untitled'),
                    'filename': filename,
                    'created': node_info.get('created'),
                    'description': node_info.get('description', '')
                }
                total_files_created += 1

            # Create index file for the supertag
            index_content = self.create_supertag_index(supertag_name, node_files)
            index_path = supertag_dir / f"{supertag_name.replace(' ', '-').lower()}.md"

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)

            total_files_created += 1
            Colors.success(f"✅ Created {len(nodes) + 1} files in '{supertag_name}' directory")

        return total_files_created

    def create_supertag_index(self, supertag_name: str, node_files: Dict[str, Dict[str, Any]]) -> str:
        """Create an index file for a supertag with links to all node files"""
        content = []
        content.append(f"# {supertag_name.title()}")
        content.append(f"")
        content.append(f"**Total nodes:** {len(node_files)}")
        content.append("")
        content.append("## 📋 All Nodes")
        content.append("")

        # Sort nodes by name
        sorted_nodes = sorted(node_files.items(), key=lambda x: x[1]['name'].lower())

        for node_id, node_info in sorted_nodes:
            name = node_info['name']
            filename = node_info['filename']
            description = node_info.get('description', '')
            created = node_info.get('created')

            # Create Obsidian-style link
            content.append(f"- [[{filename}|{name}]]")

            # Add description if available
            if description and description.strip():
                content.append(f"  - {description}")

            # Add created date if available
            if created:
                if isinstance(created, str):
                    content.append(f"  - **Created:** {created}")
                else:
                    created_date = datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d')
                    content.append(f"  - **Created:** {created_date}")

            content.append("")

        return '\n'.join(content)

    def format_node_content_new(self, node_info: Dict[str, Any], supertag_name: str, doc_lookup: Dict[str, Any] = None) -> str:
        """Format node content as markdown with the new structure, preserving formatting"""
        content = []

        # Node name (title) - this is the main heading
        node_name = node_info.get('name', 'Untitled')
        content.append(f"# {node_name}")
        content.append("")

        # Supertags section
        content.append(f"## 🏷️ Supertags")
        content.append(f"- **{supertag_name.title()}**")
        content.append("")

        # Children section - preserve formatting and content
        children = node_info.get('children', [])
        if children:
            content.append("## 📋 Children")
            content.append("")

            # We need to get the full child data to preserve content
            for child_id in children:
                child_content = self.get_child_content(child_id, node_info.get('node_id'), doc_lookup)
                if child_content:
                    content.append(child_content)

            content.append("")

        # Node metadata (collapsible)
        content.append("## 📝 Node Details")
        content.append(f"**Node ID:** `{node_info.get('node_id', 'unknown')}`")

        # Created date
        created = node_info.get('created')
        if created:
            if isinstance(created, str):
                content.append(f"**Created:** {created}")
            else:
                created_date = datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d %H:%M:%S')
                content.append(f"**Created:** {created_date}")

        # Description
        description = node_info.get('description', '')
        if description and description.strip():
            content.append(f"**Description:** {description}")

        # Path
        path = node_info.get('path', '')
        if path:
            content.append(f"**Path:** {path}")

        return '\n'.join(content)

    def get_child_content(self, child_id: str, parent_node_id: str, doc_lookup: Dict[str, Any] = None) -> str:
        """Get child content preserving formatting, returning markdown"""
        if not doc_lookup:
            # Fallback if no doc lookup available
            return f"- [[{child_id}.md]]"

        child_doc = doc_lookup.get(child_id)
        if not child_doc:
            # Child not found in lookup, treat as reference
            return f"- [[{child_id}.md]]"

        props = child_doc.get('props', {})

        # Check if this is a named node (regular Tana node)
        child_name = props.get('name')
        if child_name and child_name.strip():
            # Create Obsidian-style link with display name
            return f"- [[{child_id}.md|{child_name}]]"

        # If no name, this might be content-only. Check for actual content fields
        content_fields = ['description', 'content', 'text']
        for field in content_fields:
            if field in props and props[field]:
                content = props[field]
                if isinstance(content, str) and content.strip():
                    # Return the content as-is to preserve formatting
                    # Add some spacing to make it look better
                    if not content.startswith(('\n', '\r')):
                        return f"- {content}"
                    else:
                        # If content starts with newlines, preserve structure
                        lines = content.strip().split('\n')
                        if len(lines) == 1:
                            return f"- {lines[0]}"
                        else:
                            # Multi-line content - format properly
                            result = [f"- {lines[0]}"]
                            for line in lines[1:]:
                                result.append(f"  {line}")
                            return '\n'.join(result)

        # If no explicit content fields, check for other metadata that might be content
        # Look for fields that could contain rich text
        for key, value in props.items():
            if key not in ['created', '_ownerId', '_flags', '_metaNodeId', '_docType', '_sourceId']:
                if isinstance(value, str) and value.strip() and len(value) > 20:
                    # This looks like content rather than metadata
                    return f"- {value}"

        # Last resort - create a generic reference
        return f"- [[{child_id}.md|Child Node]]"

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility"""
        import re

        # Replace problematic characters with underscores or remove them
        # Keep letters, numbers, spaces, hyphens, underscores, and parentheses
        sanitized = re.sub(r'[^\w\s\-\(\)]', '', filename)

        # Replace multiple spaces with single space
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()

        # Replace spaces with hyphens for markdown convention
        sanitized = sanitized.replace(' ', '-')

        # Ensure it's not empty
        if not sanitized:
            sanitized = 'unnamed-node'

        # Limit length to avoid filesystem issues (excluding .md extension)
        max_length = 80
        if len(sanitized) > max_length and sanitized.endswith('.md'):
            sanitized = sanitized[:max_length-3] + '.md'
        elif len(sanitized) > max_length:
            sanitized = sanitized[:max_length-3] + '...'

        # Add .md extension
        if not sanitized.endswith('.md'):
            sanitized += '.md'

        return sanitized

    def create_import_summary(self, import_file: Path, supertags: List[Dict[str, Any]], keytags_data: Dict[str, Any],
                             nodes_by_supertag: Dict[str, List[Dict[str, Any]]], total_markdown_files: int,
                             export_dir: Path, issues: List[Dict[str, Any]] = None) -> Path:
        """Create import-summary.md with detailed metrics and issues"""

        # Convert supertags to list format
        if isinstance(supertags, dict):
            supertag_list = list(supertags.values())
        else:
            supertag_list = supertags

        summary = [
            "# Import Summary",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Source File: {import_file.name}",
            f"File Size: {import_file.stat().st_size:,} bytes",
            f"Modified: {datetime.fromtimestamp(import_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 📊 Key Metrics",
            "",
            f"- **Total Supertags Found:** {len(supertag_list)}",
            f"- **User-defined Supertags:** {len([s for s in supertag_list if not s.get('name', '').startswith('SYS_')])}",
            f"- **System Supertags:** {len([s for s in supertag_list if s.get('name', '').startswith('SYS_')])}",
            f"- **KeyTags Loaded:** {keytags_data.get('total_supertags', 0)}",
            f"- **Target Supertags:** {len(keytags_data.get('supertags', {}).get('user_defined', {}))}",
            f"- **Nodes Processed:** {total_markdown_files}",
            f"- **Directories Created:** {len(nodes_by_supertag)}",
            "",
            "## 📁 Directory Structure",
            ""
        ]

        # Add directory details
        if nodes_by_supertag:
            for supertag_name in sorted(nodes_by_supertag.keys()):
                node_count = len(nodes_by_supertag[supertag_name])
                dir_name = supertag_name.replace(' ', '-').lower()
                summary.append(f"- **{dir_name}/**: {node_count} files")

            summary.append("")

        # Add KeyTags details
        summary.extend([
            "## 🏷️ KeyTags Processed",
            ""
        ])

        user_defined = keytags_data.get('supertags', {}).get('user_defined', {})
        if user_defined:
            summary.append("| Supertag Name | Node ID | Files Created |")
            summary.append("|---------------|---------|---------------|")

            for tag_id, tag_data in user_defined.items():
                tag_name = tag_data.get('name', 'Unknown')
                files_created = len(nodes_by_supertag.get(tag_name, []))
                summary.append(f"| {tag_name} | `{tag_id}` [(tana)](https://app.tana.inc?nodeid={tag_id}) | {files_created} |")

            summary.append("")

        # Add issues if any
        if issues:
            summary.extend([
                "## ⚠️ Issues and Warnings",
                ""
            ])

            for issue in issues:
                severity = issue.get('severity', 'INFO')
                icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}.get(severity, "•")
                summary.append(f"- {icon} **{severity}:** {issue.get('message', 'Unknown issue')}")
                if issue.get('details'):
                    summary.append(f"  - *{issue['details']}*")

            summary.append("")

        # Add next steps
        summary.extend([
            "## 🎯 Next Steps",
            "",
            "1. Review the generated markdown files in each supertag directory",
            "2. Check for any nodes that may need manual cleanup",
            "3. Verify that Node IDs are correctly preserved",
            "4. Consider updating any cross-references between nodes",
            "",
            "## 📋 Generated Files",
            "",
            f"- **SuperTags.md**: Complete analysis of all {len(supertag_list)} supertags found",
            f"- **Home.md**: Home node information",
            f"- **import-summary.md**: This summary file",
            "",
            f"**Total markdown files created:** {total_markdown_files + 3}",
            ""
        ])

        # Write summary to file
        summary_file = export_dir / "import-summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary))

        return summary_file

    def import_file(self, import_file: Path, clear_export: bool = True) -> Dict[str, Any]:
        """Import a Tana JSON file and return summary"""
        # Validate and load Tana JSON
        data = self.tana_io.load_tana_file(import_file)

        # Clear export directory if requested
        if clear_export and self.tana_io.export_dir.exists():
            import shutil
            shutil.rmtree(self.tana_io.export_dir)
        self.tana_io.export_dir.mkdir(parents=True, exist_ok=True)

        # Extract and process supertags
        supertags = self.extract_all_supertags(data)

        # Load keytags and process nodes by supertag
        keytags_data = self.load_keytags(self.tana_io.files_dir)
        nodes_by_supertag = self.extract_nodes_by_supertag(data, keytags_data)

        # Create directory structure
        total_markdown_files = self.create_supertag_directories(nodes_by_supertag, self.tana_io.export_dir, data)

        # Only create metadata files if there's actual content to export
        has_content = total_markdown_files > 0 or len(supertags) > 0

        if has_content:
            self.create_supertags_md(supertags, self.tana_io.export_dir, import_file)

            # Find and create home node
            home_node = self.find_home_node(data)
            self.create_home_md(home_node, self.tana_io.export_dir, import_file)
        else:
            # No content to export, remove the export directory completely
            import shutil
            if self.tana_io.export_dir.exists():
                shutil.rmtree(self.tana_io.export_dir)

        # Collect issues
        issues = []
        target_supertags = set(keytags_data.get('supertags', {}).get('user_defined', {}).keys())
        found_supertags = set(nodes_by_supertag.keys())
        missing_supertags = target_supertags - found_supertags

        if missing_supertags:
            issues.append({
                'severity': 'WARNING',
                'message': f'{len(missing_supertags)} target supertags had no nodes',
                'details': f'Missing: {", ".join(sorted(missing_supertags))}'
            })

        # Create import summary only if there's content or the export directory exists
        summary_file = None
        if has_content or self.tana_io.export_dir.exists():
            summary_file = self.create_import_summary(
                import_file, supertags, keytags_data, nodes_by_supertag,
                total_markdown_files, self.tana_io.export_dir, issues
            )

        return {
            'success': True,
            'import_file': import_file,
            'supertags_found': len(supertags),
            'keytags_loaded': keytags_data.get('total_supertags', 0),
            'nodes_processed': total_markdown_files,
            'directories_created': len(nodes_by_supertag),
            'issues': issues,
            'summary_file': summary_file,
            'nodes_by_supertag': nodes_by_supertag,
            'export_dir_exists': self.tana_io.export_dir.exists()
        }