"""
KeyTags Manager - Core business logic for managing supertag metadata

This module contains the core functionality for managing KeyTags,
which control which supertags get their own directories during import.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from .colors import Colors


class KeyTagsManager:
    """Core KeyTags management functionality"""

    def __init__(self, files_dir: Path = None):
        """Initialize with custom files directory"""
        self.files_dir = files_dir or Path("./files")
        self.metadata_dir = self.files_dir / "metadata"
        self.keytags_file = self.metadata_dir / "keytags.json"

        # Ensure metadata directory exists
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def load_keytags(self) -> Dict[str, Any]:
        """Load keytags.json file"""
        if not self.keytags_file.exists():
            Colors.error(f"KeyTags file not found: {self.keytags_file}")
            Colors.info("Please run tana-importjson first to create the keytags.json file")
            return {}

        try:
            with open(self.keytags_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            Colors.error(f"Invalid JSON in keytags file: {e}")
            return {}
        except Exception as e:
            Colors.error(f"Error loading keytags file: {e}")
            return {}

    def save_keytags(self, keytags_data: Dict[str, Any], import_file: str = None) -> bool:
        """Save keytags.json file with tracking metadata"""
        try:
            # Add tracking metadata
            keytags_data['updated_on'] = datetime.now().isoformat()
            if import_file:
                # If import_file is a filename, try to read the footer from SuperTags.md
                if import_file == "SuperTags.md":
                    import_file = self.get_footer_from_supertags_md()
                keytags_data['import_file'] = import_file

            with open(self.keytags_file, 'w', encoding='utf-8') as f:
                json.dump(keytags_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Colors.error(f"Error saving keytags file: {e}")
            return False

    def get_footer_from_supertags_md(self) -> str:
        """Extract the footer text from SuperTags.md"""
        try:
            supertags_file = self.files_dir / "export" / "SuperTags.md"
            if not supertags_file.exists():
                return "SuperTags.md"

            with open(supertags_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Find the footer line (starts with --- then contains *Imported from*)
            for i, line in enumerate(lines):
                if line.strip() == "---":
                    # Look for the footer line after the ---
                    if i + 1 < len(lines):
                        footer_line = lines[i + 1].strip()
                        if footer_line.startswith("*Imported from"):
                            return footer_line

            return "SuperTags.md"
        except Exception as e:
            Colors.error(f"Error reading footer from SuperTags.md: {e}")
            return "SuperTags.md"

    def load_supertags_from_export(self, export_dir: Path) -> Dict[str, Dict[str, Any]]:
        """Load supertags from SuperTags.md"""
        supertags_file = export_dir / "SuperTags.md"

        if not supertags_file.exists():
            Colors.error(f"SuperTags.md not found: {supertags_file}")
            Colors.info("Please run tana-importjson first to create the SuperTags.md file")
            return {}

        supertags = {}

        try:
            with open(supertags_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Parse the markdown table
            in_table = False
            for line in lines:
                line = line.strip()
                if '| Supertag Name | Node ID | Usage Count |' in line:
                    in_table = True
                    continue
                if in_table and line.startswith('|---'):
                    continue
                if in_table and line.startswith('|'):
                    parts = [p.strip() for p in line.split('|')[1:-1]]  # Skip empty first/last
                    if len(parts) >= 3:
                        name = parts[0]
                        node_id = parts[1].strip('`')  # Remove backticks
                        if name and node_id and name != 'Supertag Name':
                            supertags[name] = {
                                'name': name,
                                'node_id': node_id,
                                'usage_count': parts[2] if len(parts) > 2 else '0'
                            }
                elif in_table and not line.startswith('|'):
                    break

        except Exception as e:
            Colors.error(f"Error parsing SuperTags.md: {e}")
            return {}

        return supertags

    def add_specific_keytags(self, tag_names: List[str], export_dir: Path = None) -> Tuple[bool, Dict[str, Any]]:
        """Add specific supertags by name from SuperTags.md export"""
        # Load current keytags and export supertags
        current_keytags = self.load_keytags()
        export_dir = export_dir or self.files_dir / "export"
        available_tags = self.load_supertags_from_export(export_dir)

        if not available_tags:
            return False, {'message': 'No supertags found in export file', 'added_count': 0}

        tags_to_add = {}
        found_tags = []
        not_found_tags = []

        for tag_name in tag_names:
            tag_name_lower = tag_name.lower()
            found_match = False

            # Look for exact or case-insensitive match
            for available_name, tag_data in available_tags.items():
                if (available_name.lower() == tag_name_lower or
                    tag_data.get('name', '').lower() == tag_name_lower):

                    tag_id = tag_data['node_id']
                    if tag_id not in current_keytags['supertags']['user_defined']:
                        tags_to_add[tag_id] = {
                            'name': tag_data['name'],
                            'node_id': tag_id,
                            'source_node': None,
                            'description': '',
                            'created': int(time.time() * 1000),
                            'source_file': 'SuperTags.md'
                        }
                        found_tags.append(tag_data['name'])
                    else:
                        found_tags.append(f"{tag_data['name']} (already exists)")
                    found_match = True
                    break

            if not found_match:
                not_found_tags.append(tag_name)

        if not tags_to_add:
            message = f"No new keytags to add. Found: {', '.join(found_tags) if found_tags else 'None'}"
            if not_found_tags:
                message += f". Not found: {', '.join(not_found_tags)}"
            return True, {'message': message, 'added_count': 0, 'found_tags': found_tags, 'not_found_tags': not_found_tags}

        # Add to keytags
        current_keytags['supertags']['user_defined'].update(tags_to_add)
        system_tags = len(current_keytags['supertags'].get('system', {}))
        current_keytags['total_supertags'] = len(current_keytags['supertags']['user_defined']) + system_tags
        current_keytags['created_at'] = datetime.now().isoformat()

        # Save updated keytags
        if self.save_keytags(current_keytags, "SuperTags.md"):
            message = f"Added {len(tags_to_add)} new keytags: {', '.join(tags_to_add[t_id]['name'] for t_id in tags_to_add)}"
            if not_found_tags:
                message += f". Not found: {', '.join(not_found_tags)}"
            return True, {
                'message': message,
                'added_count': len(tags_to_add),
                'added_tags': tags_to_add,
                'found_tags': found_tags,
                'not_found_tags': not_found_tags
            }
        else:
            return False, {'message': 'Failed to save updated keytags', 'added_count': 0}

    def add_from_export(self, export_dir: Path = None) -> Tuple[bool, Dict[str, Any]]:
        """Add all supertags from SuperTags.md export"""
        export_dir = export_dir or self.files_dir / "export"

        # Load current keytags and export supertags
        current_keytags = self.load_keytags()
        available_tags = self.load_supertags_from_export(export_dir)

        if not available_tags:
            return False, {'message': 'No supertags found in export file', 'added_count': 0}

        # Get current user-defined tags
        current_user_tags = current_keytags.get('supertags', {}).get('user_defined', {})

        # Find tags to add (not already in keytags)
        tags_to_add = {}
        for name, tag_data in available_tags.items():
            # Check if this tag is already in keytags by name
            already_exists = any(
                existing_data.get('name') == name
                for existing_data in current_user_tags.values()
            )
            if not already_exists:
                tags_to_add[tag_data['node_id']] = {
                    'name': name,
                    'node_id': tag_data['node_id'],
                    'source_node': None,
                    'description': '',
                    'created': datetime.now().timestamp() * 1000,  # Tana uses milliseconds
                    'source_file': 'SuperTags.md'
                }

        if not tags_to_add:
            return True, {'message': 'All available supertags are already in keytags', 'added_count': 0}

        # Add to keytags
        current_keytags['supertags']['user_defined'].update(tags_to_add)
        system_tags = len(current_keytags['supertags'].get('system', {}))
        current_keytags['total_supertags'] = len(current_keytags['supertags']['user_defined']) + system_tags
        current_keytags['created_at'] = datetime.now().isoformat()

        # Save updated keytags
        if self.save_keytags(current_keytags, "SuperTags.md"):
            return True, {
                'message': f'Added {len(tags_to_add)} new keytags',
                'added_count': len(tags_to_add),
                'added_tags': tags_to_add
            }
        else:
            return False, {'message': 'Failed to save updated keytags', 'added_count': 0}

    def remove_keytag(self, tag_name: str) -> Tuple[bool, str]:
        """Remove a specific keytag by name"""
        keytags_data = self.load_keytags()
        user_defined = keytags_data.get('supertags', {}).get('user_defined', {})

        if not user_defined:
            return False, "No user-defined keytags to remove"

        # Find the tag to remove
        tag_to_remove = None
        tag_id_to_remove = None

        for tag_id, tag_data in user_defined.items():
            if tag_data.get('name') == tag_name:
                tag_to_remove = tag_data
                tag_id_to_remove = tag_id
                break

        if not tag_to_remove:
            return False, f"KeyTag '{tag_name}' not found"

        # Remove the tag
        del keytags_data['supertags']['user_defined'][tag_id_to_remove]
        keytags_data['total_supertags'] = len(keytags_data['supertags']['user_defined']) + len(keytags_data['supertags']['system'])
        keytags_data['created_at'] = datetime.now().isoformat()

        # Save updated keytags
        if self.save_keytags(keytags_data, "SuperTags.md"):
            return True, f"Removed keytag '{tag_name}'"
        else:
            return False, "Failed to save updated keytags"

    def validate_against_export(self, export_dir: Path = None) -> Dict[str, Any]:
        """Validate keytags against SuperTags.md"""
        export_dir = export_dir or self.files_dir / "export"

        # Load keytags and export supertags
        keytags_data = self.load_keytags()
        export_tags = self.load_supertags_from_export(export_dir)

        if not keytags_data:
            return {
                'valid': False,
                'error': 'No keytags data found'
            }

        if not export_tags:
            return {
                'valid': False,
                'error': 'No export supertags found'
            }

        # Extract keytag names
        keytag_names = set()
        for tag_data in keytags_data.get('supertags', {}).get('user_defined', {}).values():
            keytag_names.add(tag_data.get('name', ''))

        export_names = set(export_tags.keys())

        # Find issues
        missing_in_keytags = export_names - keytag_names
        extra_in_keytags = keytag_names - export_names
        common = keytag_names & export_names

        issues = 0
        if missing_in_keytags:
            issues += 1
        if extra_in_keytags:
            issues += 1

        return {
            'valid': issues == 0,
            'keytags_count': len(keytag_names),
            'export_count': len(export_names),
            'common_count': len(common),
            'missing_in_keytags': list(missing_in_keytags),
            'extra_in_keytags': list(extra_in_keytags),
            'common': list(common),
            'issues': issues,
            'missing_details': {
                'count': len(missing_in_keytags),
                'tags': [
                    {'name': name, 'node_id': export_tags[name]['node_id']}
                    for name in missing_in_keytags
                ]
            } if missing_in_keytags else None,
            'suggestions': self._get_validation_suggestions(missing_in_keytags, extra_in_keytags)
        }

    def _get_validation_suggestions(self, missing: set, extra: set) -> List[str]:
        """Get suggestions for validation issues"""
        suggestions = []

        if missing:
            suggestions.append(f"Run: tana-keytags add --from-export to add {len(missing)} missing supertags")

        if extra:
            suggestions.append(f"Remove extra supertags with: tana-keytags remove")

        return suggestions

    def list_keytags(self) -> Dict[str, Any]:
        """Get formatted list of current keytags"""
        keytags_data = self.load_keytags()

        if not keytags_data:
            return {
                'exists': False,
                'error': 'No keytags file found'
            }

        user_defined = keytags_data.get('supertags', {}).get('user_defined', {})
        system = keytags_data.get('supertags', {}).get('system', {})

        return {
            'exists': True,
            'file_info': {
                'path': str(self.keytags_file),
                'created_at': keytags_data.get('created_at', 'Unknown'),
                'source_file': keytags_data.get('source_file', 'Unknown')
            },
            'user_defined': user_defined,
            'system': system,
            'counts': {
                'total': keytags_data.get('total_supertags', 0),
                'user_defined': len(user_defined),
                'system': len(system)
            }
        }

    def get_interactive_remove_options(self) -> List[Tuple[str, str]]:
        """Get list of keytags for interactive removal"""
        keytags_data = self.load_keytags()
        user_defined = keytags_data.get('supertags', {}).get('user_defined', {})

        options = []
        for tag_id, tag_data in user_defined.items():
            name = tag_data.get('name', 'Unknown')
            options.append((tag_id, name))

        return options

    def create_sample_keytags(self, export_file: str = "sample-export.json") -> bool:
        """Create a sample keytags.json file for testing"""
        sample_data = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "source_file": export_file,
            "total_supertags": 3,
            "supertags": {
                "user_defined": {
                    "XP0quB9qcpnO": {
                        "name": "project",
                        "node_id": "XP0quB9qcpnO",
                        "source_node": None,
                        "description": "Project management and planning",
                        "created": int(datetime.now().timestamp() * 1000),
                        "owner_id": "sample-owner",
                        "meta_node_id": "sv2Lk2Rpl5J_",
                        "source_file": export_file
                    },
                    "o6SogPA3v4oc": {
                        "name": "spark note",
                        "node_id": "o6SogPA3v4oc",
                        "source_node": None,
                        "description": "Quick insights and ideas",
                        "created": int(datetime.now().timestamp() * 1000),
                        "owner_id": "sample-owner",
                        "meta_node_id": "LHOOJUvJYhTS",
                        "source_file": export_file
                    },
                    "crqjNErByssm": {
                        "name": "note",
                        "node_id": "crqjNErByssm",
                        "source_node": None,
                        "description": "General notes and information",
                        "created": int(datetime.now().timestamp() * 1000),
                        "owner_id": "sample-owner",
                        "meta_node_id": "qAXQ4JzIPLri",
                        "source_file": export_file
                    }
                },
                "system": {}
            }
        }

        return self.save_keytags(sample_data)