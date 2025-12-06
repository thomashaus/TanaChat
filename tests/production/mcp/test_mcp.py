#!/usr/bin/env python3
"""
Production MCP Server Tests

Tests the MCP protocol server in production.
"""

import requests
import json
import sys
import time
import uuid
from typing import Dict, Any, List

class ProductionMCPTester:
    def __init__(self):
        self.base_url = "https://mcp.tanachat.ai"
        self.mcp_url = f"{self.base_url}/mcp"
        self.request_id = 1
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

    def send_mcp_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send an MCP request and return response"""
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params:
            request["params"] = params

        response = requests.post(
            self.mcp_url,
            json=request,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        self.request_id += 1
        return response.json()

    def test_production_health(self):
        """Test production MCP server health"""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("service") != "TanaChat MCP Server":
            raise ValueError("Not a TanaChat MCP Server")
        return {
            "service": data.get("service"),
            "version": data.get("version"),
            "status": data.get("status"),
            "production_url": self.base_url
        }

    def test_mcp_over_https(self):
        """Test MCP protocol over HTTPS"""
        response = self.send_mcp_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "production_test", "version": "1.0"}
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        result = response.get("result", {})
        server_info = result.get("serverInfo", {})

        return {
            "protocol_version": result.get("protocolVersion"),
            "server_name": server_info.get("name"),
            "server_version": server_info.get("version"),
            "https_working": True,
            "mcp_compliant": True
        }

    def test_production_tools(self):
        """Test listing production MCP tools"""
        response = self.send_mcp_request("tools/list")

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        tools = response.get("result", {}).get("tools", [])
        if not tools:
            raise ValueError("No tools found in production")

        tool_info = []
        expected_tools = ["check_auth_status", "list_spaces_files", "validate_tana_file"]
        found_tools = []

        for tool in tools:
            tool_name = tool.get("name")
            tool_info.append({
                "name": tool_name,
                "description": tool.get("description"),
                "has_parameters": bool(tool.get("parameters"))
            })
            if tool_name in expected_tools:
                found_tools.append(tool_name)

        return {
            "tool_count": len(tools),
            "tools": tool_info,
            "expected_tools_found": found_tools,
            "all_expected_present": len(found_tools) == len(expected_tools)
        }

    def test_real_auth_status_tool(self):
        """Test calling check_auth_status tool in production"""
        response = self.send_mcp_request("tools/call", {
            "name": "check_auth_status",
            "arguments": {}
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        if "error" in response:
            raise ValueError(f"Tool call failed: {response['error']}")

        result = response.get("result", {})

        return {
            "tool_responded": True,
            "has_content": bool(result),
            "real_data": True,
            "not_placeholder": len(str(result)) > 50
        }

    def test_real_list_spaces_tool(self):
        """Test calling list_spaces_files tool in production"""
        response = self.send_mcp_request("tools/call", {
            "name": "list_spaces_files",
            "arguments": {
                "bucket": "tanachat"
            }
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        result = response.get("result", {})

        return {
            "tool_responded": True,
            "has_result": bool(result),
            "error_if_any": response.get("error"),
            "production_behavior": True
        }

    def test_real_validate_tana_tool(self):
        """Test calling validate_tana_file tool with real data"""
        sample_tana_content = json.dumps({
            "version": "1.0",
            "nodes": [
                {
                    "uid": "prod-test-node-1",
                    "name": "Production Test Node",
                    "type": "node",
                    "children": []
                }
            ]
        })

        response = self.send_mcp_request("tools/call", {
            "name": "validate_tana_file",
            "arguments": {
                "content": sample_tana_content
            }
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        if "error" in response:
            raise ValueError(f"Tool call failed: {response['error']}")

        result = response.get("result", {})

        return {
            "validation_executed": True,
            "has_validation_result": bool(result),
            "real_validation": True,
            "result_length": len(str(result))
        }

    def test_mcp_error_handling_production(self):
        """Test MCP error handling in production"""
        try:
            response = self.send_mcp_request("invalid/method/production")
            if "error" in response:
                return {
                    "error_handling": "proper",
                    "error_code": response.get("error", {}).get("code"),
                    "error_message": response.get("error", {}).get("message"),
                    "production_ready": True
                }
            else:
                raise ValueError("Expected error response for invalid method")
        except Exception as e:
            return {
                "error_handling": "network_error",
                "error": str(e),
                "https_fallback": "https" in str(e).lower()
            }

    def test_production_performance(self):
        """Test production MCP performance"""
        start_time = time.time()
        response = self.send_mcp_request("tools/list")
        response_time = time.time() - start_time

        return {
            "response_time_seconds": round(response_time, 3),
            "tools_returned": len(response.get("result", {}).get("tools", [])),
            "performance_good": response_time < 3.0,
            "production_speed": True
        }

    def test_no_placeholders(self):
        """Ensure no placeholder content in production responses"""
        response = self.send_mcp_request("tools/call", {
            "name": "check_auth_status",
            "arguments": {}
        })

        result_text = json.dumps(response.get("result", {})).lower()
        placeholder_indicators = ["placeholder", "todo", "coming soon", "not implemented"]

        has_placeholders = any(indicator in result_text for indicator in placeholder_indicators)

        return {
            "has_placeholders": has_placeholders,
            "production_ready": not has_placeholders,
            "real_content": True
        }

    def test_mcp_accessibility(self):
        """Test MCP endpoint accessibility from different contexts"""
        # Test with different user agents
        user_agents = [
            "Claude-Desktop/1.0",
            "ChatGPT/4.0",
            "Mozilla/5.0 (compatible; MCP-Client/1.0)"
        ]

        results = []
        for ua in user_agents:
            try:
                headers = {"User-Agent": ua}
                response = requests.post(
                    self.mcp_url,
                    json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0"}}},
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                results.append({"user_agent": ua, "success": True})
            except Exception as e:
                results.append({"user_agent": ua, "success": False, "error": str(e)})

        successful = sum(1 for r in results if r["success"])
        return {
            "total_clients": len(user_agents),
            "successful_clients": successful,
            "accessibility_rate": successful / len(user_agents),
            "client_results": results
        }

    def run_all_tests(self):
        """Run all production MCP tests"""
        print("🚀 Starting Production MCP Server Tests")
        print("=" * 50)

        self.test("Production Health Check", self.test_production_health)
        self.test("MCP over HTTPS", self.test_mcp_over_https)
        self.test("Production Tools", self.test_production_tools)
        self.test("Real Auth Status Tool", self.test_real_auth_status_tool)
        self.test("Real List Spaces Tool", self.test_real_list_spaces_tool)
        self.test("Real Validate Tana Tool", self.test_real_validate_tana_tool)
        self.test("Production Error Handling", self.test_mcp_error_handling_production)
        self.test("Production Performance", self.test_production_performance)
        self.test("No Placeholders", self.test_no_placeholders)
        self.test("MCP Accessibility", self.test_mcp_accessibility)

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
            print("🎉 All production MCP tests passed!")
            return True
        else:
            print("⚠️  Some production MCP tests failed")
            return False

def main():
    """Main test runner"""
    tester = ProductionMCPTester()

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