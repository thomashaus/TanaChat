#!/usr/bin/env python3
"""
Local API Tests

Tests the FastAPI backend running locally.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class APITester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
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
        """Test API health endpoint"""
        response = requests.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "healthy":
            raise ValueError(f"Health check failed: {data}")
        return data

    def test_api_docs(self):
        """Test API documentation endpoint"""
        response = requests.get(f"{self.base_url}/docs", timeout=5)
        response.raise_for_status()
        return {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type"),
            "docs_available": "swagger-ui" in response.text
        }

    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        response.raise_for_status()
        schema = response.json()
        if "openapi" not in schema:
            raise ValueError("Invalid OpenAPI schema")
        return {"version": schema.get("openapi"), "title": schema.get("info", {}).get("title")}

    def test_auth_status(self):
        """Test authentication status endpoint"""
        response = requests.get(f"{self.base_url}/api/v1/auth/status", timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "authenticated": data.get("authenticated"),
            "setup_required": data.get("setup_required"),
            "has_s3_config": bool(data.get("s3_test", {}).get("access_key"))
        }

    def test_tools_endpoint(self):
        """Test tools listing endpoint"""
        response = requests.get(f"{self.base_url}/api/v1/tools", timeout=5)
        response.raise_for_status()
        data = response.json()
        tools = data.get("tools", [])
        if not tools:
            raise ValueError("No tools found")
        tool_names = [tool.get("name") for tool in tools]
        return {
            "tool_count": len(tools),
            "tools": tool_names,
            "spaces_status": data.get("spaces_status")
        }

    def test_mcp_endpoint(self):
        """Test MCP protocol endpoint"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }

        response = requests.post(
            f"{self.base_url}/mcp",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if data.get("jsonrpc") != "2.0":
            raise ValueError("Invalid MCP response")
        return {
            "protocol_version": data.get("result", {}).get("protocolVersion"),
            "server_name": data.get("result", {}).get("serverInfo", {}).get("name"),
            "server_version": data.get("result", {}).get("serverInfo", {}).get("version")
        }

    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = requests.options(f"{self.base_url}/api/v1/tools", timeout=5)
        headers = response.headers
        cors_headers = {
            "access_control_allow_origin": headers.get("access-control-allow-origin"),
            "access_control_allow_methods": headers.get("access-control-allow-methods"),
            "access_control_allow_headers": headers.get("access-control-allow-headers")
        }
        return cors_headers

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Local API Tests")
        print("=" * 50)

        self.test("API Health Check", self.test_health_check)
        self.test("API Documentation", self.test_api_docs)
        self.test("OpenAPI Schema", self.test_openapi_schema)
        self.test("Authentication Status", self.test_auth_status)
        self.test("Tools Endpoint", self.test_tools_endpoint)
        self.test("MCP Protocol", self.test_mcp_endpoint)
        self.test("CORS Headers", self.test_cors_headers)

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
            print("🎉 All API tests passed!")
            return True
        else:
            print("⚠️  Some API tests failed")
            return False

def main():
    """Main test runner"""
    tester = APITester()

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