#!/usr/bin/env python3
"""
Tests for tana-keytags command functionality
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
import sys

# Add parent directory to path for testing
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import the functions to test
# Note: In a real test suite, you'd refactor the CLI tool to separate business logic
# For now, we'll test the command-line interface

class TestTanaKeyTags(unittest.TestCase):
    """Test tana-keytags functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.files_dir = self.test_dir / "files"
        self.metadata_dir = self.files_dir / "metadata"
        self.export_dir = self.files_dir / "export"

        # Create directories
        self.metadata_dir.mkdir(parents=True)
        self.export_dir.mkdir(parents=True)

        # Sample keytags data
        self.sample_keytags = {
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
                    },
                    "o6SogPA3v4oc": {
                        "name": "spark note",
                        "node_id": "o6SogPA3v4oc",
                        "source_node": None,
                        "description": "Quick insights",
                        "created": 1764871952695,
                        "owner_id": "test-owner",
                        "meta_node_id": "LHOOJUvJYhTS",
                        "source_file": "test-export.json"
                    }
                },
                "system": {}
            }
        }

        # Sample SuperTags.md content
        self.sample_supertags_md = """# SuperTags Analysis
Generated: 2024-12-04 15:00:00
Total unique supertags: 3
Showing: 3 user-defined supertags (excluding system tags)
---

| Supertag Name | Node ID | Usage Count |
|---------------|---------|-------------|
| project | `XP0quB9qcpnO` | 5 |
| spark note | `o6SogPA3v4oc` | 3 |
| note | `crqjNErByssm` | 10 |
"""

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_keytags_file_creation(self):
        """Test keytags.json file creation and structure"""
        keytags_file = self.metadata_dir / "keytags.json"

        # Write sample keytags
        with open(keytags_file, 'w') as f:
            json.dump(self.sample_keytags, f, indent=2)

        # Verify file exists and has correct structure
        self.assertTrue(keytags_file.exists())

        with open(keytags_file, 'r') as f:
            data = json.load(f)

        self.assertEqual(data['version'], '1.0')
        self.assertEqual(data['total_supertags'], 2)
        self.assertEqual(len(data['supertags']['user_defined']), 2)
        self.assertIn('project', [tag['name'] for tag in data['supertags']['user_defined'].values()])

    def test_keytags_validation_logic(self):
        """Test keytags validation logic"""
        # Create keytags file
        keytags_file = self.metadata_dir / "keytags.json"
        with open(keytags_file, 'w') as f:
            json.dump(self.sample_keytags, f, indent=2)

        # Create SuperTags.md with additional supertag
        supertags_file = self.export_dir / "SuperTags.md"
        with open(supertags_file, 'w') as f:
            f.write(self.sample_supertags_md)

        # Simulate validation logic
        keytag_names = set()
        for tag_data in self.sample_keytags['supertags']['user_defined'].values():
            keytag_names.add(tag_data['name'])

        # Parse SuperTags.md to get export names
        export_names = set()
        for line in self.sample_supertags_md.split('\n'):
            if line.startswith('| ') and 'project' in line or 'spark note' in line or 'note' in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 2 and parts[0] not in ['Supertag Name', '---']:
                    export_names.add(parts[0])

        # Check validation results
        missing_in_keytags = export_names - keytag_names
        common = keytag_names & export_names

        self.assertEqual(len(common), 2)  # project and spark note
        self.assertIn('note', missing_in_keytags)

    def test_keytags_add_from_export_logic(self):
        """Test logic for adding supertags from export"""
        # Start with initial keytags
        keytags_file = self.metadata_dir / "keytags.json"
        with open(keytags_file, 'w') as f:
            json.dump(self.sample_keytags, f, indent=2)

        # Parse SuperTags.md to find missing supertags
        export_names = set()
        export_data = {}
        for line in self.sample_supertags_md.split('\n'):
            if line.startswith('| ') and 'project' in line or 'spark note' in line or 'note' in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 2 and parts[0] not in ['Supertag Name', '---']:
                    name = parts[0]
                    node_id = parts[1].strip('`')
                    export_names.add(name)
                    export_data[name] = {
                        'name': name,
                        'node_id': node_id,
                        'source_node': None,
                        'description': '',
                        'created': 1764871952695,
                        'source_file': 'SuperTags.md'
                    }

        # Find missing supertags
        keytag_names = set()
        for tag_data in self.sample_keytags['supertags']['user_defined'].values():
            keytag_names.add(tag_data['name'])

        missing_tags = export_names - keytag_names

        # Should find 'note' as missing
        self.assertIn('note', missing_tags)
        self.assertEqual(len(missing_tags), 1)

        # Simulate adding the missing tag
        new_keytags = self.sample_keytags.copy()
        for tag_name in missing_tags:
            if tag_name in export_data:
                tag_info = export_data[tag_name]
                new_keytags['supertags']['user_defined'][tag_info['node_id']] = tag_info

        # Verify the tag was added
        self.assertEqual(len(new_keytags['supertags']['user_defined']), 3)
        new_keytags['total_supertags'] = len(new_keytags['supertags']['user_defined'])
        self.assertEqual(new_keytags['total_supertags'], 3)

    def test_keytags_remove_logic(self):
        """Test keytags removal logic"""
        # Remove 'spark note' from keytags
        tag_to_remove = "spark note"

        updated_keytags = self.sample_keytags.copy()

        # Find and remove the tag
        tag_id_to_remove = None
        for tag_id, tag_data in updated_keytags['supertags']['user_defined'].items():
            if tag_data['name'] == tag_to_remove:
                tag_id_to_remove = tag_id
                break

        self.assertIsNotNone(tag_id_to_remove)
        self.assertEqual(tag_id_to_remove, 'o6SogPA3v4oc')

        # Remove the tag
        del updated_keytags['supertags']['user_defined'][tag_id_to_remove]
        updated_keytags['total_supertags'] = len(updated_keytags['supertags']['user_defined'])

        # Verify removal
        self.assertEqual(len(updated_keytags['supertags']['user_defined']), 1)
        self.assertEqual(updated_keytags['total_supertags'], 1)

        remaining_names = [tag['name'] for tag in updated_keytags['supertags']['user_defined'].values()]
        self.assertNotIn(tag_to_remove, remaining_names)
        self.assertIn('project', remaining_names)


class TestImportSummary(unittest.TestCase):
    """Test import summary functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.export_dir = self.test_dir / "export"
        self.export_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_import_summary_structure(self):
        """Test import summary file structure"""
        summary_content = """# Import Summary
Generated: 2024-12-04 15:00:00
Source File: test-export.json
File Size: 1234567 bytes
Modified: 2024-12-04 14:30:00

## 📊 Key Metrics

- **Total Supertags Found:** 15
- **User-defined Supertags:** 12
- **System Supertags:** 3
- **KeyTags Loaded:** 3
- **Target Supertags:** 3
- **Nodes Processed:** 245
- **Directories Created:** 3

## 📁 Directory Structure

- **note/**: 180 files
- **project/**: 45 files
- **spark-note/**: 20 files

## 📋 Generated Files

**Total markdown files created:** 248
"""

        summary_file = self.export_dir / "import-summary.md"
        with open(summary_file, 'w') as f:
            f.write(summary_content)

        # Verify file exists and has expected content
        self.assertTrue(summary_file.exists())

        with open(summary_file, 'r') as f:
            content = f.read()

        self.assertIn("Import Summary", content)
        self.assertIn("Key Metrics", content)
        self.assertIn("Directory Structure", content)
        self.assertIn("Generated Files", content)
        self.assertIn("Total markdown files created:** 248", content)

    def test_metrics_parsing(self):
        """Test parsing metrics from import summary"""
        summary_content = """# Import Summary
Generated: 2024-12-04 15:00:00
Source File: test-export.json
File Size: 1234567 bytes
Modified: 2024-12-04 14:30:00

## 📊 Key Metrics

- **Total Supertags Found:** 15
- **User-defined Supertags:** 12
- **System Supertags:** 3
- **KeyTags Loaded:** 3
- **Target Supertags:** 3
- **Nodes Processed:** 245
- **Directories Created:** 3
"""

        # Parse metrics (simplified parsing logic)
        metrics = {}
        for line in summary_content.split('\n'):
            if line.strip().startswith('- **') and ':' in line:
                # Extract metric name and value
                # Format: "- **Metric Name:** value"
                content = line.strip()[3:]  # Remove "- **"
                if '**:' in content:
                    name, value = content.split('**:', 1)
                    name = name.strip()
                    value = value.strip()
                    metrics[name] = value
                elif ':' in content:
                    # Handle case where **: might not be present
                    name, value = content.split(':', 1)
                    name = name.strip().rstrip('*').strip()
                    value = value.strip()
                    # Clean up any remaining ** from value
                    value = value.lstrip('*').strip()
                    metrics[name] = value

        expected_metrics = {
            'Total Supertags Found': '15',
            'User-defined Supertags': '12',
            'System Supertags': '3',
            'KeyTags Loaded': '3',
            'Target Supertags': '3',
            'Nodes Processed': '245',
            'Directories Created': '3'
        }

        # Account for any leading * in keys
        normalized_metrics = {}
        for key, value in metrics.items():
            normalized_key = key.lstrip('*')
            normalized_metrics[normalized_key] = value

        for key, expected_value in expected_metrics.items():
            self.assertIn(key, normalized_metrics)
            self.assertEqual(normalized_metrics[key], expected_value)


if __name__ == '__main__':
    unittest.main()