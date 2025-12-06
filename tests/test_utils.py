#!/usr/bin/env python3
"""
Test utilities for loading environment configuration.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import json

class TestConfig:
    """Test configuration loader."""

    def __init__(self, env_file: str = ".env.test"):
        self.env_file = Path(__file__).parent / env_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment and .env file."""
        config = {}

        # Load from .env.test file if it exists
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()

        # Override with actual environment variables
        for key, value in os.environ.items():
            if key.startswith(('LOCAL_', 'PRODUCTION_', 'TEST_')):
                config[key] = value

        # Set defaults
        config.setdefault('TEST_TIMEOUT', '30')
        config.setdefault('PERFORMANCE_THRESHOLD_SLOW', '5.0')
        config.setdefault('PERFORMANCE_THRESHOLD_FAST', '2.0')
        config.setdefault('VERIFY_SSL', 'true')
        config.setdefault('FOLLOW_REDIRECTS', 'true')
        config.setdefault('REPORT_DIR', 'temp')
        config.setdefault('DETAILED_REPORTING', 'true')

        # Convert boolean and numeric values
        for key in ['VERIFY_SSL', 'FOLLOW_REDIRECTS', 'DETAILED_REPORTING']:
            config[key] = config[key].lower() in ('true', '1', 'yes', 'on')

        for key in ['TEST_TIMEOUT', 'PERFORMANCE_THRESHOLD_SLOW', 'PERFORMANCE_THRESHOLD_FAST']:
            config[key] = float(config[key])

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def get_local_urls(self) -> Dict[str, str]:
        """Get local development URLs."""
        return {
            'frontend': self.get('LOCAL_FRONTEND_URL', 'http://localhost:5173'),
            'api': self.get('LOCAL_API_URL', 'http://localhost:8000'),
            'mcp': self.get('LOCAL_MCP_URL', 'http://localhost:8000/mcp')
        }

    def get_production_urls(self) -> Dict[str, str]:
        """Get production URLs."""
        return {
            'frontend': self.get('PRODUCTION_FRONTEND_URL', 'https://tanachat.ai'),
            'api': self.get('PRODUCTION_API_URL', 'https://mcp.tanachat.ai'),
            'mcp': self.get('PRODUCTION_MCP_URL', 'https://mcp.tanachat.ai/mcp')
        }

    def get_test_config(self) -> Dict[str, Any]:
        """Get test configuration."""
        return {
            'timeout': self.get('TEST_TIMEOUT', 30),
            'slow_threshold': self.get('PERFORMANCE_THRESHOLD_SLOW', 5.0),
            'fast_threshold': self.get('PERFORMANCE_THRESHOLD_FAST', 2.0),
            'verify_ssl': self.get('VERIFY_SSL', True),
            'follow_redirects': self.get('FOLLOW_REDIRECTS', True),
            'report_dir': self.get('REPORT_DIR', 'temp'),
            'detailed_reporting': self.get('DETAILED_REPORTING', True)
        }

class TestResult:
    """Test result container."""

    def __init__(self, name: str, status: str = "PASS", result: Any = None, error: str = None):
        self.name = name
        self.status = status
        self.result = result
        self.error = error
        self.timestamp = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'timestamp': self.timestamp
        }

class TestSuite:
    """Base test suite class."""

    def __init__(self, config_file: str = ".env.test"):
        self.config = TestConfig(config_file)
        self.results = []
        self.start_time = None
        self.end_time = None

    def test(self, name: str, test_func):
        """Run a test and record results."""
        print(f"🧪 Testing {name}...")
        try:
            result = test_func()
            test_result = TestResult(name, "PASS", result)
            self.results.append(test_result)
            print(f"✅ {name} - PASS")
            return True
        except Exception as e:
            test_result = TestResult(name, "FAIL", error=str(e))
            self.results.append(test_result)
            print(f"❌ {name} - FAIL: {e}")
            return False

    def run_all_tests(self):
        """Run all tests (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement run_all_tests")

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)

        passed = sum(1 for r in self.results if r.status == "PASS")
        total = len(self.results)

        for result in self.results:
            status_emoji = "✅" if result.status == "PASS" else "❌"
            print(f"{status_emoji} {result.name}: {result.status}")
            if result.status == "FAIL":
                print(f"   Error: {result.error}")

        print(f"\n🎯 Results: {passed}/{total} tests passed")

        success = passed == total
        if success:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed")

        return success

    def get_results_dict(self) -> Dict[str, Any]:
        """Get test results as dictionary."""
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_tests': len(self.results),
            'passed_tests': sum(1 for r in self.results if r.status == "PASS"),
            'failed_tests': sum(1 for r in self.results if r.status == "FAIL"),
            'results': [r.to_dict() for r in self.results]
        }

def save_report(report_data: Dict[str, Any], report_path: str):
    """Save test report to file."""
    try:
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        print(f"📄 Report saved to: {report_path}")
    except Exception as e:
        print(f"⚠️  Failed to save report: {e}")

def ensure_report_dir(report_dir: str):
    """Ensure report directory exists."""
    try:
        Path(report_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"⚠️  Failed to create report directory: {e}")