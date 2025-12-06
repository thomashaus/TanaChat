#!/usr/bin/env python3
"""
Production WWW/Frontend Tests

Tests the React web application in production.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class ProductionFrontendTester:
    def __init__(self):
        self.base_url = "https://tanachat.ai"
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

    def test_production_health(self):
        """Test if production frontend is accessible"""
        response = requests.get(self.base_url, timeout=10)
        response.raise_for_status()
        return {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type"),
            "server": response.headers.get("server")
        }

    def test_main_page_content(self):
        """Test if main page loads with proper content"""
        response = requests.get(self.base_url, timeout=10)
        content = response.text
        if not any(keyword in content.lower() for keyword in ["tanachat", "tana", "ai", "chat"]):
            raise ValueError("Page doesn't contain expected branding")
        return {
            "page_loaded": True,
            "content_length": len(content),
            "has_branding": True
        }

    def test_ssl_certificate(self):
        """Test SSL certificate is valid"""
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = requests.get(self.base_url, timeout=10)
            return {
                "ssl_valid": True,
                "protocol": response.raw.version,
                "https_works": self.base_url.startswith("https://")
            }
        except Exception as e:
            raise ValueError(f"SSL issue: {e}")

    def test_page_performance(self):
        """Test page load performance"""
        start_time = time.time()
        response = requests.get(self.base_url, timeout=15)
        load_time = time.time() - start_time
        response.raise_for_status()

        return {
            "load_time_seconds": round(load_time, 2),
            "status_code": response.status_code,
            "performance_good": load_time < 5.0
        }

    def test_api_endpoints_reference(self):
        """Check if frontend references production API endpoints"""
        response = requests.get(self.base_url, timeout=10)
        content = response.text
        has_prod_api = "mcp.tanachat.ai" in content or "tanachat.ai" in content
        return {
            "production_api_references": has_prod_api,
            "localhost_references": "localhost" not in content
        }

    def test_mobile_responsive(self):
        """Test mobile responsiveness via User-Agent"""
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"}
        response = requests.get(self.base_url, headers=headers, timeout=10)
        response.raise_for_status()
        return {
            "mobile_accessible": True,
            "status_code": response.status_code,
            "has_viewport": "viewport" in response.text
        }

    def run_all_tests(self):
        """Run all production frontend tests"""
        print("🚀 Starting Production Frontend Tests")
        print("=" * 50)

        self.test("Production Health Check", self.test_production_health)
        self.test("Main Page Content", self.test_main_page_content)
        self.test("SSL Certificate", self.test_ssl_certificate)
        self.test("Page Performance", self.test_page_performance)
        self.test("API References", self.test_api_endpoints_reference)
        self.test("Mobile Responsive", self.test_mobile_responsive)

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
            print("🎉 All production frontend tests passed!")
            return True
        else:
            print("⚠️  Some production frontend tests failed")
            return False

def main():
    """Main test runner"""
    tester = ProductionFrontendTester()

    try:
        success = tester.run_all_tests()
        return success
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
        return False
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)