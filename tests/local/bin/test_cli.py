#!/usr/bin/env python3
"""
Local CLI Tools Tests

Tests the command-line interface tools locally.
"""

import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

class CLITester:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.bin_dir = self.project_root / "bin"
        self.results = []

    def test(self, name: str, test_func):
        """Run a test and record results"""
        print(f"🧪 Testing {name}...")
        try:
            result = test_func()
            self.results.append({
                "name": name,
                "status": "PASS",
                "result": result
            })
            print(f"✅ {name} - PASS")
            return True
        except Exception as e:
            self.results.append({
                "name": name,
                "status": "FAIL",
                "error": str(e)
            })
            print(f"❌ {name} - FAIL: {e}")
            return False

    def run_command(self, cmd: List[str], input_data: str = None, timeout: int = 30) -> Dict[str, Any]:
        """Run a command and return result"""
        try:
            result = subprocess.run(
                cmd,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=self.project_root
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out",
                "success": False
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }

    def test_cli_tools_exist(self):
        """Test if CLI tool files exist"""
        tools = []
        for tool_file in self.bin_dir.glob("tanachat-*"):
            if tool_file.is_file():
                tools.append(tool_file.name)

        if not tools:
            raise ValueError("No CLI tools found in bin directory")

        return {
            "tools_found": tools,
            "tool_count": len(tools)
        }

    def test_tanachat_help(self):
        """Test tanachat main command help"""
        cmd = ["python", "-m", "tanachat", "--help"]
        result = self.run_command(cmd)

        if not result["success"]:
            raise ValueError(f"Help command failed: {result['stderr']}")

        return {
            "has_usage": "usage:" in result["stdout"].lower(),
            "has_commands": "--help" in result["stdout"],
            "output_length": len(result["stdout"])
        }

    def test_tanachat_version(self):
        """Test tanachat version command"""
        cmd = ["python", "-m", "tanachat", "--version"]
        result = self.run_command(cmd)

        if not result["success"]:
            # Try alternative version flag
            cmd = ["python", "-m", "tanachat", "version"]
            result = self.run_command(cmd)

        return {
            "success": result["success"],
            "version_output": result["stdout"].strip(),
            "has_version_number": bool(result["stdout"].strip() and result["stdout"].strip() != "")
        }

    def test_tanachat_createuser(self):
        """Test tanachat-createuser tool"""
        tool_path = self.bin_dir / "tanachat-createuser"
        if not tool_path.exists():
            # Try as module
            cmd = ["python", "-m", "tanachat.cli.createuser", "--help"]
        else:
            cmd = ["python", str(tool_path), "--help"]

        result = self.run_command(cmd)

        return {
            "tool_exists": tool_path.exists() or result["success"],
            "help_available": result["success"],
            "has_usage": "usage:" in result["stdout"].lower() if result["success"] else False
        }

    def test_tanachat_login(self):
        """Test tanachat-login tool"""
        tool_path = self.bin_dir / "tanachat-login"
        if not tool_path.exists():
            # Try as module
            cmd = ["python", "-m", "tanachat.cli.login", "--help"]
        else:
            cmd = ["python", str(tool_path), "--help"]

        result = self.run_command(cmd)

        return {
            "tool_exists": tool_path.exists() or result["success"],
            "help_available": result["success"],
            "has_usage": "usage:" in result["stdout"].lower() if result["success"] else False
        }

    def test_tanachat_importjson(self):
        """Test tanachat-importjson tool"""
        tool_path = self.bin_dir / "tanachat-importjson"

        # Create sample JSON file for testing
        sample_data = {
            "version": "1.0",
            "nodes": [
                {
                    "uid": "test-node-1",
                    "name": "Test Node",
                    "type": "node",
                    "children": []
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_data, f)
            sample_file = f.name

        try:
            if tool_path.exists():
                cmd = ["python", str(tool_path), "--help"]
                result = self.run_command(cmd)

                # If help works, try with sample file
                if result["success"]:
                    cmd = ["python", str(tool_path), sample_file, "--dry-run"]
                    result = self.run_command(cmd)
            else:
                # Try as module
                cmd = ["python", "-m", "tanachat.cli.importjson", "--help"]
                result = self.run_command(cmd)

            return {
                "tool_exists": tool_path.exists() or result["success"],
                "help_available": result["success"],
                "dry_run_attempted": tool_path.exists()
            }
        finally:
            os.unlink(sample_file)

    def test_tanachat_find(self):
        """Test tanachat-find tool"""
        tool_path = self.bin_dir / "tanachat-find"
        if not tool_path.exists():
            # Try as module
            cmd = ["python", "-m", "tanachat.cli.find", "--help"]
        else:
            cmd = ["python", str(tool_path), "--help"]

        result = self.run_command(cmd)

        return {
            "tool_exists": tool_path.exists() or result["success"],
            "help_available": result["success"],
            "has_usage": "usage:" in result["stdout"].lower() if result["success"] else False
        }

    def test_tanachat_keytags(self):
        """Test tanachat-keytags tool"""
        tool_path = self.bin_dir / "tanachat-keytags"
        if not tool_path.exists():
            # Try as module
            cmd = ["python", "-m", "tanachat.cli.keytags", "--help"]
        else:
            cmd = ["python", str(tool_path), "--help"]

        result = self.run_command(cmd)

        return {
            "tool_exists": tool_path.exists() or result["success"],
            "help_available": result["success"],
            "has_usage": "usage:" in result["stdout"].lower() if result["success"] else False
        }

    def test_tanachat_obsidian(self):
        """Test tanachat-obsidian tool"""
        tool_path = self.bin_dir / "tanachat-obsidian"
        if not tool_path.exists():
            # Try as module
            cmd = ["python", "-m", "tanachat.cli.obsidian", "--help"]
        else:
            cmd = ["python", str(tool_path), "--help"]

        result = self.run_command(cmd)

        return {
            "tool_exists": tool_path.exists() or result["success"],
            "help_available": result["success"],
            "has_usage": "usage:" in result["stdout"].lower() if result["success"] else False
        }

    def test_environment_setup(self):
        """Test if environment is properly set up for CLI"""
        # Check if we can import the main module
        cmd = ["python", "-c", "import tanachat; print('Module imported successfully')"]
        result = self.run_command(cmd)

        return {
            "module_importable": result["success"],
            "import_output": result["stdout"].strip(),
            "error_if_any": result["stderr"] if not result["success"] else None
        }

    def run_all_tests(self):
        """Run all CLI tests"""
        print("🚀 Starting Local CLI Tools Tests")
        print("=" * 50)

        self.test("CLI Tools Directory", self.test_cli_tools_exist)
        self.test("Environment Setup", self.test_environment_setup)
        self.test("TanaChat Help", self.test_tanachat_help)
        self.test("TanaChat Version", self.test_tanachat_version)
        self.test("Create User Tool", self.test_tanachat_createuser)
        self.test("Login Tool", self.test_tanachat_login)
        self.test("Import JSON Tool", self.test_tanachat_importjson)
        self.test("Find Tool", self.test_tanachat_find)
        self.test("Keytags Tool", self.test_tanachat_keytags)
        self.test("Obsidian Tool", self.test_tanachat_obsidian)

        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)

        passed = sum(1 for r in self.results if r["status"] == "PASS")
        total = len(self.results)

        for result in self.results:
            status_emoji = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_emoji} {result['name']}: {result['status']}")
            if result["status"] == "FAIL":
                print(f"   Error: {result.get('error', 'Unknown error')}")

        print(f"\n🎯 Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All CLI tests passed!")
            return True
        else:
            print("⚠️  Some CLI tests failed")
            return False

def main():
    """Main test runner"""
    tester = CLITester()

    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()