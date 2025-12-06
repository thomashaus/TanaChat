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

        def traverse_nodes(items, parent_path=None):
            for item in items:
                if not isinstance(item, dict):
                    continue

                # Check if this node has any target supertags
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
                                # These have names like "Field defaults for Everything tagged #X"
                                # and are not actual content nodes
                                node_name = item.get('name', '')
                                if not node_name.startswith('Field defaults for'):
                                    if target_name not in nodes_by_supertag:
                                        nodes_by_supertag[target_name] = []

                                    nodes_by_supertag[target_name].append({
                                        'name': item.get('name', 'Untitled'),
                                        'node_id': item.get('id', item.get('uid', 'unknown')),
                                        'description': item.get('description', ''),
                                        'created': item.get('created'),
                                        'children': item.get('children', []),
                                        'path': parent_path
                                    })

                # Recursively process children
                children = item.get('children', [])
                if children:
                    current_name = item.get('name', 'Untitled')
                    current_path = f"{parent_path} / {current_name}" if parent_path else current_name
                    traverse_nodes(children, current_path)

        # Start traversal
        traverse_nodes(docs)

        return nodes_by_supertag

    def format_node_content(self, node_info: Dict[str, Any]) -> str:
        """Format node content as markdown"""
        content = []

        # Node name
        node_name = node_info.get('name', 'Untitled')
        content.append(f"# {node_name}\n")

        # Node ID
        node_id = node_info.get('node_id', 'unknown')
        content.append(f"**Node ID:** `{node_id}`\n")

        # Description
        description = node_info.get('description', '')
        if description and description.strip():
            content.append(f"**Description:** {description}\n")

        # Created date
        created = node_info.get('created')
        if created:
            if isinstance(created, str):
                # ISO format string
                content.append(f"**Created:** {created}\n")
            else:
                # Timestamp in milliseconds
                created_date = datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d %H:%M:%S')
                content.append(f"**Created:** {created_date}\n")

        # Path
        path = node_info.get('path', '')
        if path:
            content.append(f"**Path:** {path}\n")

        content.append("---")

        # Children
        children = node_info.get('children', [])
        if children:
            content.extend(self.format_children(children))

        return '\n'.join(content)

    def format_children(self, children: List[Any], level: int = 0) -> List[str]:
        """Format child nodes as markdown"""
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

    def create_supertag_directories(self, nodes_by_supertag: Dict[str, List[Dict[str, Any]]], export_dir: Path) -> int:
        """Create directories and markdown files for each supertag"""
        total_files_created = 0

        for supertag_name, nodes in nodes_by_supertag.items():
            if not nodes:
                continue

            # Create directory (replace spaces with hyphens and lowercase)
            dir_name = supertag_name.replace(' ', '-').lower()
            supertag_dir = export_dir / dir_name
            supertag_dir.mkdir(parents=True, exist_ok=True)

            Colors.info(f"📁 Creating {len(nodes)} files in '{supertag_name}' directory")

            # Create markdown file for each node
            for node_info in nodes:
                # Use node ID as filename to ensure uniqueness
                node_id = str(node_info['node_id'])
                filename = f"{node_id}.md"
                file_path = supertag_dir / filename

                # Format content
                markdown_content = self.format_node_content(node_info)

                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                total_files_created += 1

            Colors.success(f"✅ Created {len(nodes)} files in '{supertag_name}' directory")

        return total_files_created

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
        total_markdown_files = self.create_supertag_directories(nodes_by_supertag, self.tana_io.export_dir)

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