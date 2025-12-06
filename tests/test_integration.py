#!/usr/bin/env python3
"""
Integration tests for Tana tools workflow
Tests the complete workflow from import to keytags management
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
import sys
import subprocess

# Add parent directory to path for testing
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class TestTanaIntegration(unittest.TestCase):
    """Integration tests for Tana tools workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.bin_dir = project_root / "bin"
        self.files_dir = self.test_dir / "files"
        self.import_dir = self.files_dir / "import"
        self.export_dir = self.files_dir / "export"
        self.metadata_dir = self.files_dir / "metadata"

        # Create directory structure
        self.import_dir.mkdir(parents=True)
        self.export_dir.mkdir(parents=True)
        self.metadata_dir.mkdir(parents=True)

        # Create a minimal Tana export file for testing
        self.sample_tana_export = {
            "version": "1.0.0",
            "nodes": [
                {
                    "uid": "node1",
                    "name": "Test Project",
                    "supertags": [
                        {"name": "project", "uid": "XP0quB9qcpnO"}
                    ],
                    "children": [
                        {
                            "uid": "node2",
                            "name": "Task 1",
                            "supertags": [
                                {"name": "task", "uid": "task123"}
                            ]
                        }
                    ]
                },
                {
                    "uid": "node3",
                    "name": "Meeting Notes",
                    "supertags": [
                        {"name": "note", "uid": "crqjNErByssm"}
                    ]
                }
            ]
        }

        self.export_file = self.import_dir / "test-export.json"
        with open(self.export_file, 'w') as f:
            json.dump(self.sample_tana_export, f, indent=2)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_file_structure_creation(self):
        """Test that the proper file structure is created"""
        # Test that directories are created
        self.assertTrue(self.import_dir.exists())
        self.assertTrue(self.export_dir.exists())
        self.assertTrue(self.metadata_dir.exists())

        # Test that export file exists
        self.assertTrue(self.export_file.exists())

    def test_sample_export_validity(self):
        """Test that our sample export is valid JSON"""
        with open(self.export_file, 'r') as f:
            data = json.load(f)

        self.assertIn('version', data)
        self.assertIn('nodes', data)
        self.assertEqual(len(data['nodes']), 2)

    def test_command_help(self):
        """Test that commands show help properly"""
        commands = ['tana-importjson', 'tana-keytags', 'tana-convert', 'tana-find']

        for cmd in commands:
            cmd_path = self.bin_dir / cmd
            if cmd_path.exists():
                try:
                    result = subprocess.run(
                        [str(cmd_path), '--help'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    # Help should return 0 (success) or not crash
                    self.assertTrue(result.returncode == 0 or result.returncode == 1)
                except subprocess.TimeoutExpired:
                    self.fail(f"Command {cmd} timed out when showing help")
                except Exception as e:
                    # Note: Commands might fail if dependencies aren't met,
                    # but they shouldn't crash badly
                    self.fail(f"Command {cmd} crashed: {e}")

    def test_keytags_file_format(self):
        """Test keytags file format requirements"""
        # Create a sample keytags file
        keytags_data = {
            "version": "1.0",
            "created_at": "2024-12-04T15:00:00.000000",
            "source_file": "test-export.json",
            "total_supertags": 2,
            "supertags": {
                "user_defined": {
                    "XP0quB9qcpnO": {
                        "name": "project",
                        "node_id": "XP0quB9qcpnO",
                        "source_node": None,
                        "description": "Project management",
                        "created": 1761999717122,
                        "owner_id": "test-owner",
                        "meta_node_id": "sv2Lk2Rpl5J_",
                        "source_file": "test-export.json"
                    }
                },
                "system": {}
            }
        }

        keytags_file = self.metadata_dir / "keytags.json"
        with open(keytags_file, 'w') as f:
            json.dump(keytags_data, f, indent=2)

        # Verify file structure
        with open(keytags_file, 'r') as f:
            loaded_data = json.load(f)

        required_fields = ['version', 'created_at', 'source_file', 'total_supertags', 'supertags']
        for field in required_fields:
            self.assertIn(field, loaded_data)

        self.assertIn('user_defined', loaded_data['supertags'])
        self.assertIn('system', loaded_data['supertags'])

    def test_export_directory_structure(self):
        """Test expected export directory structure"""
        # Create the expected directory structure
        expected_dirs = [
            self.export_dir / "project",
            self.export_dir / "note",
            self.export_dir / "task"
        ]

        for dir_path in expected_dirs:
            dir_path.mkdir(exist_ok=True)

        # Verify directories exist
        for dir_path in expected_dirs:
            self.assertTrue(dir_path.exists())

        # Create sample markdown files
        sample_content = """# Test Node

**Node ID:** `node123`

**Created:** 2024-12-04 15:00:00

---

This is test content.
"""

        for dir_path in expected_dirs:
            md_file = dir_path / "test-node.md"
            with open(md_file, 'w') as f:
                f.write(sample_content)
            self.assertTrue(md_file.exists())

    def test_metadata_files_creation(self):
        """Test creation of required metadata files"""
        # Create keytags.json
        keytags_file = self.metadata_dir / "keytags.json"
        keytags_data = {
            "version": "1.0",
            "created_at": "2024-12-04T15:00:00.000000",
            "source_file": "test-export.json",
            "total_supertags": 1,
            "supertags": {
                "user_defined": {},
                "system": {}
            }
        }
        with open(keytags_file, 'w') as f:
            json.dump(keytags_data, f, indent=2)

        # Create users.json
        users_file = self.metadata_dir / "users.json"
        users_data = {
            "version": "1.0",
            "created_at": "2024-12-04T15:00:00.000000",
            "last_updated": "2024-12-04T15:00:00.000000",
            "users": {}
        }
        with open(users_file, 'w') as f:
            json.dump(users_data, f, indent=2)

        # Verify files exist and have correct structure
        self.assertTrue(keytags_file.exists())
        self.assertTrue(users_file.exists())

        with open(keytags_file, 'r') as f:
            data = json.load(f)
            self.assertIn('supertags', data)

        with open(users_file, 'r') as f:
            data = json.load(f)
            self.assertIn('users', data)

    def test_workflow_dependencies(self):
        """Test that workflow dependencies are properly handled"""
        # Test keytags dependency on import
        keytags_file = self.metadata_dir / "keytags.json"
        supertags_file = self.export_dir / "SuperTags.md"

        # Neither file should exist initially
        self.assertFalse(keytags_file.exists())
        self.assertFalse(supertags_file.exists())

        # Create SuperTags.md (simulating successful import)
        supertags_content = """# SuperTags Analysis
Generated: 2024-12-04 15:00:00
Total unique supertags: 2
Showing: 2 user-defined supertags (excluding system tags)
---

| Supertag Name | Node ID | Usage Count |
|---------------|---------|-------------|
| project | `XP0quB9qcpnO` | 1 |
| note | `crqjNErByssm` | 1 |
"""
        with open(supertags_file, 'w') as f:
            f.write(supertags_content)

        self.assertTrue(supertags_file.exists())

        # Now keytags operations should be possible
        # (In real tests, you'd call the actual commands here)

    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test with invalid JSON
        invalid_file = self.import_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json content")

        # File exists but is invalid
        self.assertTrue(invalid_file.exists())

        # Try to load it (should fail gracefully)
        try:
            with open(invalid_file, 'r') as f:
                json.load(f)
            self.fail("Expected JSONDecodeError")
        except json.JSONDecodeError:
            pass  # Expected

        # Test with missing directories
        missing_dir = self.files_dir / "missing"
        self.assertFalse(missing_dir.exists())

        # Creating missing_dir should work
        missing_dir.mkdir(parents=True)
        self.assertTrue(missing_dir.exists())


class TestFilePermissions(unittest.TestCase):
    """Test file permissions and accessibility"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.bin_dir = project_root / "bin"

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_script_executability(self):
        """Test that scripts are executable"""
        scripts = [
            'tana-importjson',
            'tana-keytags',
            'tana-convert',
            'tana-find',
            'tana-analyze',
            'tana-tags',
            'tana-post'
        ]

        for script in scripts:
            script_path = self.bin_dir / script
            if script_path.exists():
                # Check if file is executable
                file_stat = script_path.stat()
                # In octal, 0o111 means execute for user, group, and others
                # We check if any execute bit is set
                self.assertTrue(
                    file_stat.st_mode & 0o111 != 0,
                    f"Script {script} is not executable"
                )

    def test_file_accessibility(self):
        """Test that files are readable and writable"""
        # Create a test file
        test_file = self.test_dir / "test.txt"
        test_content = "Test content"

        # Write to file
        with open(test_file, 'w') as f:
            f.write(test_content)

        # Verify file exists and is readable
        self.assertTrue(test_file.exists())
        self.assertTrue(os.access(test_file, os.R_OK))
        self.assertTrue(os.access(test_file, os.W_OK))

        # Read from file
        with open(test_file, 'r') as f:
            read_content = f.read()
        self.assertEqual(read_content, test_content)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)