"""
Workspace-based KeyTags Manager

Manages KeyTags files per workspace ID instead of global keytags.
Each workspace gets its own {workspace_id}-keytags.json file.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from .colors import Colors


class WorkspaceKeyTagsManager:
    """Workspace-specific KeyTags management"""

    def __init__(self, files_dir: Path = None):
        """Initialize with custom files directory"""
        self.files_dir = files_dir or Path("./files")
        self.metadata_dir = self.files_dir / "metadata"

    def get_workspace_id_from_json(self, json_file_path: Path) -> Optional[str]:
        """Extract workspace ID from Tana JSON export"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                tana_data = json.load(f)

            # Look for workspace ID in metadata section
            if isinstance(tana_data, dict):
                # Check various possible locations for workspace ID
                metadata = tana_data.get("metadata", {})
                workspace_id = (
                    metadata.get("workspace_id") or
                    metadata.get("workspaceId") or
                    tana_data.get("workspace_id") or
                    tana_data.get("workspaceId") or
                    # Look in nodes for workspace info
                    self._extract_workspace_id_from_nodes(tana_data.get("nodes", []))
                )

                if workspace_id:
                    return str(workspace_id)

            return None

        except Exception as e:
            Colors.error(f"Error reading JSON file {json_file_path}: {e}")
            return None

    def _extract_workspace_id_from_nodes(self, nodes: List[Dict]) -> Optional[str]:
        """Extract workspace ID from node data"""
        for node in nodes:
            if isinstance(node, dict):
                # Check various fields that might contain workspace info
                workspace_fields = [
                    "workspace_id",
                    "workspaceId",
                    "workspace",
                    "space_id",
                    "spaceId"
                ]

                for field in workspace_fields:
                    if field in node and node[field]:
                        return str(node[field])

                # Recursively check children
                if "children" in node and isinstance(node["children"], list):
                    result = self._extract_workspace_id_from_nodes(node["children"])
                    if result:
                        return result

        return None

    def get_keytags_file_path(self, workspace_id: str) -> Path:
        """Get the keytags file path for a specific workspace"""
        return self.metadata_dir / f"{workspace_id}-keytags.json"

    def load_keytags(self, workspace_id: str) -> Dict[str, Any]:
        """Load keytags file for specific workspace"""
        keytags_file = self.get_keytags_file_path(workspace_id)

        if not keytags_file.exists():
            Colors.info(f"KeyTags file not found for workspace '{workspace_id}': {keytags_file}")
            Colors.info("Creating starter KeyTags file...")
            return self.create_starter_keytags_file(workspace_id)

        try:
            with open(keytags_file, 'r', encoding='utf-8') as f:
                keytags_data = json.load(f)

            # Verify workspace ID matches
            if keytags_data.get("workspace_id") != workspace_id:
                Colors.warning(f"Workspace ID mismatch in keytags file. Expected: {workspace_id}, Found: {keytags_data.get('workspace_id')}")
                # Update the workspace ID
                keytags_data["workspace_id"] = workspace_id
                self.save_keytags(workspace_id, keytags_data)

            return keytags_data

        except json.JSONDecodeError as e:
            Colors.error(f"Invalid JSON in keytags file: {e}")
            Colors.info("Creating new starter KeyTags file...")
            return self.create_starter_keytags_file(workspace_id)
        except Exception as e:
            Colors.error(f"Error loading keytags file: {e}")
            return self.create_starter_keytags_file(workspace_id)

    def create_starter_keytags_file(self, workspace_id: str) -> Dict[str, Any]:
        """Create a starter keytags file for a new workspace"""
        starter_data = {
            "version": "2.0",
            "workspace_id": workspace_id,
            "created_at": datetime.now().isoformat(),
            "source_file": None,  # Will be set when import happens
            "total_supertags": 0,
            "last_import": None,
            "inheritance": {},
            "directories": {},
            "apis": {},
            "supertags": {
                "user_defined": {},
                "system": {}
            }
        }

        # Save the starter file
        if self.save_keytags(workspace_id, starter_data):
            Colors.success(f"Created starter KeyTags file for workspace: {workspace_id}")
        else:
            Colors.error(f"Failed to create starter KeyTags file for workspace: {workspace_id}")

        return starter_data

    def save_keytags(self, workspace_id: str, keytags_data: Dict[str, Any],
                    import_file: str = None) -> bool:
        """Save keytags file for specific workspace"""
        try:
            # Ensure workspace ID is set
            keytags_data["workspace_id"] = workspace_id

            # Add tracking metadata
            keytags_data['updated_on'] = datetime.now().isoformat()
            if import_file:
                keytags_data['last_import'] = import_file
                keytags_data['source_file'] = import_file

            # Ensure metadata directory exists
            self.metadata_dir.mkdir(parents=True, exist_ok=True)

            keytags_file = self.get_keytags_file_path(workspace_id)

            with open(keytags_file, 'w', encoding='utf-8') as f:
                json.dump(keytags_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            Colors.error(f"Error saving keytags file: {e}")
            return False

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """List all available workspaces"""
        workspaces = []

        if not self.metadata_dir.exists():
            return workspaces

        for keytags_file in self.metadata_dir.glob("*-keytags.json"):
            try:
                with open(keytags_file, 'r', encoding='utf-8') as f:
                    keytags_data = json.load(f)

                workspace_id = keytags_file.stem.replace("-keytags", "")
                workspaces.append({
                    "workspace_id": workspace_id,
                    "workspace_name": keytags_data.get("workspace_name", workspace_id),
                    "file_path": str(keytags_file),
                    "created_at": keytags_data.get("created_at"),
                    "total_supertags": keytags_data.get("total_supertags", 0),
                    "last_import": keytags_data.get("last_import"),
                    "source_file": keytags_data.get("source_file")
                })

            except Exception as e:
                Colors.error(f"Error reading workspace keytags {keytags_file}: {e}")

        return workspaces

    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete a workspace's keytags file"""
        try:
            keytags_file = self.get_keytags_file_path(workspace_id)

            if keytags_file.exists():
                keytags_file.unlink()
                Colors.success(f"Deleted workspace keytags file: {workspace_id}")
                return True
            else:
                Colors.warning(f"Workspace keytags file not found: {workspace_id}")
                return False

        except Exception as e:
            Colors.error(f"Error deleting workspace keytags file: {e}")
            return False

    def migrate_from_global_keytags(self, global_keytags_file: Path = None) -> bool:
        """Migrate from global keytags.json to workspace-based system"""
        if not global_keytags_file:
            global_keytags_file = self.files_dir / "metadata" / "keytags.json"

        if not global_keytags_file.exists():
            Colors.info("No global keytags.json file found. No migration needed.")
            return True

        try:
            with open(global_keytags_file, 'r', encoding='utf-8') as f:
                global_data = json.load(f)

            # Create a default workspace for the global data
            default_workspace_id = "default_workspace"
            workspace_data = {
                "version": "2.0",
                "workspace_id": default_workspace_id,
                "workspace_name": "Migrated Workspace",
                "created_at": global_data.get("created_at", datetime.now().isoformat()),
                "source_file": global_data.get("source_file"),
                "total_supertags": global_data.get("total_supertags", 0),
                "updated_on": global_data.get("updated_on"),
                "last_import": global_data.get("import_file"),
                "supertags": global_data.get("supertags", {}),
                # New v2.0 features
                "inheritance": {},
                "directories": {},
                "apis": {}
            }

            # Save as workspace-specific file
            if self.save_keytags(default_workspace_id, workspace_data):
                Colors.success(f"Migrated global keytags to workspace: {default_workspace_id}")

                # Backup the original file
                backup_file = global_keytags_file.with_suffix(".backup.json")
                global_keytags_file.rename(backup_file)
                Colors.info(f"Original keytags.json backed up to: {backup_file}")

                return True
            else:
                Colors.error("Failed to save migrated workspace data")
                return False

        except Exception as e:
            Colors.error(f"Error migrating global keytags: {e}")
            return False

    def get_workspace_stats(self, workspace_id: str) -> Dict[str, Any]:
        """Get statistics for a specific workspace"""
        keytags_data = self.load_keytags(workspace_id)

        return {
            "workspace_id": workspace_id,
            "total_supertags": keytags_data.get("total_supertags", 0),
            "user_defined_count": len(keytags_data.get("supertags", {}).get("user_defined", {})),
            "system_count": len(keytags_data.get("supertags", {}).get("system", {})),
            "inheritance_count": len(keytags_data.get("inheritance", {})),
            "directory_count": len(keytags_data.get("directories", {})),
            "api_count": len(keytags_data.get("apis", {})),
            "created_at": keytags_data.get("created_at"),
            "updated_at": keytags_data.get("updated_on"),
            "last_import": keytags_data.get("last_import"),
            "source_file": keytags_data.get("source_file"),
            "version": keytags_data.get("version", "1.0")
        }