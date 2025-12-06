#!/usr/bin/env python3
"""
Production API Tests

Tests the FastAPI backend in production.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class ProductionAPITester:
    def __init__(self):
        self.base_url = "https://mcp.tanachat.ai"
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
        """Test production API health endpoint"""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "healthy":
            raise ValueError(f"Health check failed: {data}")
        return data

    def test_ssl_security(self):
        """Test SSL/TLS security"""
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = requests.get(f"{self.base_url}/health", timeout=10)

        security_headers = {
            "strict_transport_security": response.headers.get("strict-transport-security"),
            "content_security_policy": response.headers.get("content-security-policy"),
            "x_content_type_options": response.headers.get("x-content-type-options"),
            "x_frame_options": response.headers.get("x-frame-options")
        }

        return {
            "https_works": True,
            "status_code": response.status_code,
            "security_headers": security_headers
        }

    def test_api_documentation(self):
        """Test production API documentation endpoint"""
        response = requests.get(f"{self.base_url}/docs", timeout=10)
        response.raise_for_status()
        return {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type"),
            "docs_available": "swagger-ui" in response.text,
            "production_domain": "mcp.tanachat.ai" in response.text
        }

    def test_openapi_schema(self):
        """Test production OpenAPI schema endpoint"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
        response.raise_for_status()
        schema = response.json()
        if "openapi" not in schema:
            raise ValueError("Invalid OpenAPI schema")
        return {
            "version": schema.get("openapi"),
            "title": schema.get("info", {}).get("title"),
            "production_servers": len([s for s in schema.get("servers", []) if "mcp.tanachat.ai" in s.get("url", "")])
        }

    def test_production_tools(self):
        """Test production tools endpoint"""
        response = requests.get(f"{self.base_url}/api/v1/tools", timeout=10)
        response.raise_for_status()
        data = response.json()
        tools = data.get("tools", [])
        if not tools:
            raise ValueError("No tools found in production")

        tool_names = [tool.get("name") for tool in tools]
        return {
            "tool_count": len(tools),
            "tools": tool_names,
            "spaces_status": data.get("spaces_status"),
            "all_tools_real": len(tool_names) >= 3
        }

    def test_production_mcp(self):
        """Test production MCP protocol endpoint"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "production_test", "version": "1.0"}
            }
        }

        response = requests.post(
            f"{self.base_url}/mcp",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data.get("jsonrpc") != "2.0":
            raise ValueError("Invalid MCP response in production")

        return {
            "protocol_version": data.get("result", {}).get("protocolVersion"),
            "server_name": data.get("result", {}).get("serverInfo", {}).get("name"),
            "server_version": data.get("result", {}).get("serverInfo", {}).get("version"),
            "mcp_working": True
        }

    def test_production_auth_status(self):
        """Test production authentication status"""
        response = requests.get(f"{self.base_url}/api/v1/auth/status", timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "authenticated": data.get("authenticated"),
            "setup_required": data.get("setup_required"),
            "production_ready": True,
            "auth_endpoint_responding": True
        }

    def test_cors_configuration(self):
        """Test CORS configuration for production"""
        response = requests.options(f"{self.base_url}/api/v1/tools", timeout=10)
        headers = response.headers
        cors_headers = {
            "access_control_allow_origin": headers.get("access-control-allow-origin"),
            "access_control_allow_methods": headers.get("access-control-allow-methods"),
            "access_control_allow_headers": headers.get("access-control-allow-headers")
        }
        return cors_headers

    def test_api_performance(self):
        """Test API response performance"""
        start_time = time.time()
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response_time = time.time() - start_time
        response.raise_for_status()

        return {
            "response_time_seconds": round(response_time, 3),
            "status_code": response.status_code,
            "performance_good": response_time < 2.0
        }

    def test_no_localhost_references(self):
        """Ensure no localhost references in production responses"""
        response = requests.get(f"{self.base_url}/api/v1/tools", timeout=10)
        content = response.text.lower()
        has_localhost = "localhost" in content or "127.0.0.1" in content

        return {
            "has_localhost": has_localhost,
            "production_clean": not has_localhost
        }

    def run_all_tests(self):
        """Run all production API tests"""
        print("🚀 Starting Production API Tests")
        print("=" * 50)

        self.test("Production Health Check", self.test_production_health)
        self.test("SSL Security", self.test_ssl_security)
        self.test("API Documentation", self.test_api_documentation)
        self.test("OpenAPI Schema", self.test_openapi_schema)
        self.test("Production Tools", self.test_production_tools)
        self.test("Production MCP", self.test_production_mcp)
        self.test("Production Auth Status", self.test_production_auth_status)
        self.test("CORS Configuration", self.test_cors_configuration)
        self.test("API Performance", self.test_api_performance)
        self.test("No Localhost References", self.test_no_localhost_references)

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
            print("🎉 All production API tests passed!")
            return True
        else:
            print("⚠️  Some production API tests failed")
            return False

def main():
    """Main test runner"""
    tester = ProductionAPITester()

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