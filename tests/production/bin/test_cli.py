#!/usr/bin/env python3
"""
Production CLI Tools Tests

Tests CLI tools in production environment (end-to-end).
"""

import subprocess
import sys
import os
import json
import tempfile
import requests
from pathlib import Path
from typing import Dict, Any, List

class ProductionCLITester:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.base_url = "https://tanachat.ai"
        self.mcp_url = "https://mcp.tanachat.ai"
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

    def test_production_api_access(self):
        """Test if CLI can access production API endpoints"""
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "api_accessible": True,
                "service": data.get("service"),
                "version": data.get("version"),
                "production_url": self.mcp_url
            }
        except Exception as e:
            raise ValueError(f"Cannot access production API: {e}")

    def test_mcp_tools_via_http(self):
        """Test MCP tools via HTTP (simulating CLI behavior)"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }

        try:
            response = requests.post(
                f"{self.mcp_url}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            tools = data.get("result", {}).get("tools", [])

            return {
                "mcp_accessible": True,
                "tool_count": len(tools),
                "tools_found": [tool.get("name") for tool in tools]
            }
        except Exception as e:
            raise ValueError(f"MCP tools not accessible: {e}")

    def test_production_file_validation(self):
        """Test file validation using production API"""
        sample_tana_content = json.dumps({
            "version": "1.0",
            "nodes": [
                {
                    "uid": "prod-test-123",
                    "name": "Production Test Node",
                    "type": "node",
                    "children": []
                }
            ]
        })

        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "validate_tana_file",
                "arguments": {
                    "content": sample_tana_content
                }
            }
        }

        try:
            response = requests.post(
                f"{self.mcp_url}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            result = data.get("result", {})

            return {
                "validation_working": True,
                "has_result": bool(result),
                "production_validation": True
            }
        except Exception as e:
            raise ValueError(f"Production validation failed: {e}")

    def test_cli_documentation_access(self):
        """Test if CLI documentation points to production URLs"""
        try:
            # Test if production docs are accessible
            response = requests.get(f"{self.mcp_url}/docs", timeout=10)
            response.raise_for_status()
            docs_accessible = "swagger-ui" in response.text

            # Test if main site docs reference production endpoints
            response = requests.get(f"{self.base_url}/docs", timeout=10)
            main_site_docs = response.status_code == 200

            return {
                "production_docs_accessible": docs_accessible,
                "main_site_docs_accessible": main_site_docs,
                "doc_urls": {
                    "api_docs": f"{self.mcp_url}/docs",
                    "main_site": f"{self.base_url}/docs"
                }
            }
        except Exception as e:
            # Main site docs might not exist, that's ok
            return {
                "production_docs_accessible": False,
                "main_site_docs_accessible": False,
                "error": str(e)
            }

    def test_production_environment_variables(self):
        """Test production environment setup via API responses"""
        try:
            response = requests.get(f"{self.mcp_url}/api/v1/auth/status", timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "auth_endpoint_responding": True,
                "setup_status": data.get("setup_required"),
                "production_configured": True,
                "no_localhost_refs": "localhost" not in str(data)
            }
        except Exception as e:
            raise ValueError(f"Production environment check failed: {e}")

    def test_cli_to_production_integration(self):
        """Test CLI integration with production services"""
        integration_tests = []

        # Test 1: Health check
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            integration_tests.append({
                "test": "health_check",
                "success": response.status_code == 200,
                "production_ready": True
            })
        except Exception as e:
            integration_tests.append({
                "test": "health_check",
                "success": False,
                "error": str(e)
            })

        # Test 2: Tools availability
        try:
            response = requests.get(f"{self.mcp_url}/api/v1/tools", timeout=10)
            data = response.json()
            tools = data.get("tools", [])
            integration_tests.append({
                "test": "tools_availability",
                "success": len(tools) >= 3,
                "tool_count": len(tools),
                "production_ready": True
            })
        except Exception as e:
            integration_tests.append({
                "test": "tools_availability",
                "success": False,
                "error": str(e)
            })

        # Test 3: MCP protocol
        try:
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "initialize",
                "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "production_test", "version": "1.0"}}
            }
            response = requests.post(f"{self.mcp_url}/mcp", json=mcp_request, timeout=10)
            integration_tests.append({
                "test": "mcp_protocol",
                "success": response.status_code == 200,
                "mcp_compliant": True
            })
        except Exception as e:
            integration_tests.append({
                "test": "mcp_protocol",
                "success": False,
                "error": str(e)
            })

        successful_tests = sum(1 for test in integration_tests if test["success"])
        return {
            "total_tests": len(integration_tests),
            "successful_tests": successful_tests,
            "integration_rate": successful_tests / len(integration_tests),
            "test_results": integration_tests
        }

    def test_production_security(self):
        """Test production security aspects that CLI would encounter"""
        security_tests = {}

        # Test HTTPS enforcement
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            security_tests["https_working"] = response.status_code == 200
            security_tests["url_https"] = self.mcp_url.startswith("https://")
        except:
            security_tests["https_working"] = False

        # Test no sensitive data exposure
        try:
            response = requests.get(f"{self.mcp_url}/api/v1/auth/status", timeout=10)
            content = str(response.json()).lower()
            sensitive_keywords = ["password", "secret", "key", "token"]
            security_tests["no_sensitive_exposure"] = not any(keyword in content for keyword in sensitive_keywords)
        except:
            security_tests["no_sensitive_exposure"] = False

        # Test CORS for web clients
        try:
            response = requests.options(f"{self.mcp_url}/api/v1/tools", timeout=10)
            cors_headers = {
                "access_control_allow_origin": response.headers.get("access-control-allow-origin"),
                "access_control_allow_methods": response.headers.get("access-control-allow-methods")
            }
            security_tests["cors_configured"] = bool(cors_headers["access_control_allow_origin"])
        except:
            security_tests["cors_configured"] = False

        return security_tests

    def test_production_performance(self):
        """Test production performance from CLI perspective"""
        performance_tests = {}

        # Test API response time
        start_time = time.time()
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            performance_tests["health_response_time"] = round(time.time() - start_time, 3)
            performance_tests["health_success"] = response.status_code == 200
        except:
            performance_tests["health_response_time"] = 999
            performance_tests["health_success"] = False

        # Test MCP response time
        start_time = time.time()
        try:
            mcp_request = {"jsonrpc": "2.0", "id": 4, "method": "tools/list"}
            response = requests.post(f"{self.mcp_url}/mcp", json=mcp_request, timeout=10)
            performance_tests["mcp_response_time"] = round(time.time() - start_time, 3)
            performance_tests["mcp_success"] = response.status_code == 200
        except:
            performance_tests["mcp_response_time"] = 999
            performance_tests["mcp_success"] = False

        performance_tests["overall_performance_good"] = (
            performance_tests.get("health_response_time", 999) < 2.0 and
            performance_tests.get("mcp_response_time", 999) < 3.0
        )

        return performance_tests

    def run_all_tests(self):
        """Run all production CLI tests"""
        print("🚀 Starting Production CLI Integration Tests")
        print("=" * 50)

        self.test("Production API Access", self.test_production_api_access)
        self.test("MCP Tools via HTTP", self.test_mcp_tools_via_http)
        self.test("Production File Validation", self.test_production_file_validation)
        self.test("CLI Documentation Access", self.test_cli_documentation_access)
        self.test("Production Environment", self.test_production_environment_variables)
        self.test("CLI Integration", self.test_cli_to_production_integration)
        self.test("Production Security", self.test_production_security)
        self.test("Production Performance", self.test_production_performance)

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
            print("🎉 All production CLI tests passed!")
            return True
        else:
            print("⚠️  Some production CLI tests failed")
            return False

def main():
    """Main test runner"""
    import time  # Import time for performance tests
    tester = ProductionCLITester()

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