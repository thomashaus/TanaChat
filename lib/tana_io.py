"""Tana file I/O operations"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from .colors import Colors

# Default paths
DEFAULT_FILES_DIR = Path("./files")
DEFAULT_EXPORT_DIR = DEFAULT_FILES_DIR / "export"  # For markdown exports
DEFAULT_IMPORT_DIR = DEFAULT_FILES_DIR / "import"  # For Tana JSON imports


class TanaIO:
    """Handle Tana file input/output operations"""

    def __init__(self, files_dir: Optional[Path] = None):
        """Initialize with custom files directory"""
        self.files_dir = files_dir or DEFAULT_FILES_DIR
        self.export_dir = self.files_dir / "export"  # For markdown exports
        self.import_dir = self.files_dir / "import"  # For Tana JSON imports

        # Ensure directories exist
        for dir_path in [self.files_dir, self.export_dir, self.import_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def find_latest_import(self, pattern: str = "*.json") -> Path:
        """Find the most recent Tana import file"""
        imports = list(self.import_dir.glob(pattern))

        if not imports:
            Colors.error(f"No Tana import files found in {self.import_dir}")

        latest = max(imports, key=lambda f: f.stat().st_mtime)
        return latest

    def load_tana_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a Tana JSON file"""
        if not file_path.exists():
            Colors.error(f"Tana file not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            Colors.error(f"Invalid JSON in file {file_path}: {e}")
        except Exception as e:
            Colors.error(f"Error reading file {file_path}: {e}")

    def save_tana_file(self, data: Dict[str, Any], file_path: Path) -> None:
        """Save data to a Tana JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            Colors.error(f"Error saving file {file_path}: {e}")

    def validate_tana_structure(self, data: Dict[str, Any]) -> bool:
        """Basic validation of Tana file structure"""
        if not isinstance(data, dict):
            return False

        # Check for TIF format
        if 'version' in data and 'nodes' in data:
            return True

        # Check for export format
        if 'docs' in data:
            return True

        return False

    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get file information"""
        stat = file_path.stat()
        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'is_tana': file_path.suffix.lower() == '.json'
        }

    def list_files(self, directory: Optional[Path] = None, pattern: str = "*.json") -> List[Dict[str, Any]]:
        """List files in directory with info"""
        dir_path = directory or self.import_dir
        files = []

        for file_path in dir_path.glob(pattern):
            files.append(self.get_file_info(file_path))

        return sorted(files, key=lambda x: x['modified'], reverse=True)

    def search_files(self, keyword: str, directories: Optional[List[Path]] = None) -> List[Dict[str, Any]]:
        """Search for files containing keyword"""
        dirs = directories or [self.import_dir]
        matches = []

        for dir_path in dirs:
            if not dir_path.exists():
                continue

            for file_path in dir_path.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            file_info = self.get_file_info(file_path)
                            file_info['matches'] = content.lower().count(keyword.lower())
                            matches.append(file_info)
                except:
                    continue

        return sorted(matches, key=lambda x: x['matches'], reverse=True)

    def backup_file(self, file_path: Path, backup_dir: Optional[Path] = None) -> Path:
        """Create a backup of a file"""
        if backup_dir is None:
            backup_dir = self.files_dir / "backups"

        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name

        import shutil
        shutil.copy2(file_path, backup_path)

        return backup_path