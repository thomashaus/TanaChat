#!/usr/bin/env python3
"""
Local WWW/Frontend Tests

Tests the React web application running locally.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class FrontendTester:
    def __init__(self):
        self.base_url = "http://localhost:5173"
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

    def test_health_check(self):
        """Test if frontend is running"""
        response = requests.get(self.base_url, timeout=5)
        response.raise_for_status()
        return {"status_code": response.status_code, "content_type": response.headers.get("content-type")}

    def test_main_page_loads(self):
        """Test if main page loads with content"""
        response = requests.get(self.base_url, timeout=5)
        content = response.text
        if "TanaChat" not in content:
            raise ValueError("Page doesn't contain TanaChat branding")
        return {"page_title": "Loaded successfully", "branding_found": True}

    def test_static_assets(self):
        """Test if static assets are loading"""
        response = requests.get(f"{self.base_url}/vite.svg", timeout=5)
        response.raise_for_status()
        return {"vite_svg_loaded": True}

    def test_api_endpoint_reference(self):
        """Check if frontend has API configuration"""
        response = requests.get(self.base_url, timeout=5)
        content = response.text
        has_api_config = "VITE_API_URL" in content or "localhost:8000" in content
        if not has_api_config:
            raise ValueError("No API configuration found")
        return {"api_config_found": True}

    def run_all_tests(self):
        """Run all frontend tests"""
        print("🚀 Starting Local Frontend Tests")
        print("=" * 50)

        self.test("Frontend Health Check", self.test_health_check)
        self.test("Main Page Loads", self.test_main_page_loads)
        self.test("Static Assets", self.test_static_assets)
        self.test("API Configuration", self.test_api_endpoint_reference)

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
            print("🎉 All frontend tests passed!")
            return True
        else:
            print("⚠️  Some frontend tests failed")
            return False

def main():
    """Main test runner"""
    tester = FrontendTester()

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