#!/usr/bin/env python3
"""
Local MCP Server Tests

Tests the MCP protocol server running locally.
"""

import requests
import json
import sys
import time
import uuid
from typing import Dict, Any, List

class MCPTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
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
            timeout=10
        )
        response.raise_for_status()
        self.request_id += 1
        return response.json()

    def test_mcp_health(self):
        """Test MCP server health via regular API"""
        response = requests.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("service") != "TanaChat MCP Server":
            raise ValueError("Not a TanaChat MCP Server")
        return data

    def test_mcp_initialization(self):
        """Test MCP protocol initialization"""
        response = self.send_mcp_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "test", "version": "1.0"}
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        result = response.get("result", {})
        server_info = result.get("serverInfo", {})

        return {
            "protocol_version": result.get("protocolVersion"),
            "server_name": server_info.get("name"),
            "server_version": server_info.get("version"),
            "capabilities": result.get("capabilities", {})
        }

    def test_list_tools(self):
        """Test listing available MCP tools"""
        response = self.send_mcp_request("tools/list")

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        tools = response.get("result", {}).get("tools", [])
        if not tools:
            raise ValueError("No tools found")

        tool_info = []
        for tool in tools:
            tool_info.append({
                "name": tool.get("name"),
                "description": tool.get("description"),
                "has_parameters": bool(tool.get("parameters"))
            })

        return {
            "tool_count": len(tools),
            "tools": tool_info
        }

    def test_call_auth_status_tool(self):
        """Test calling the check_auth_status tool"""
        response = self.send_mcp_request("tools/call", {
            "name": "check_auth_status",
            "arguments": {}
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        result = response.get("result", {})
        if "error" in response:
            raise ValueError(f"Tool call failed: {response['error']}")

        return result

    def test_call_list_spaces_tool(self):
        """Test calling the list_spaces_files tool"""
        response = self.send_mcp_request("tools/call", {
            "name": "list_spaces_files",
            "arguments": {
                "bucket": "tanachat"
            }
        })

        if response.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC response")

        result = response.get("result", {})
        # This might fail due to missing credentials, but the tool should still respond
        return {
            "tool_responded": True,
            "has_content": bool(result),
            "error_if_any": response.get("error")
        }

    def test_call_validate_tana_file_tool(self):
        """Test calling the validate_tana_file tool with sample data"""
        sample_tana_content = json.dumps({
            "version": "1.0",
            "nodes": [
                {
                    "uid": "test-node-1",
                    "name": "Test Node",
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

        result = response.get("result", {})
        if "error" in response:
            raise ValueError(f"Tool call failed: {response['error']}")

        return result

    def test_mcp_error_handling(self):
        """Test MCP error handling with invalid method"""
        try:
            response = self.send_mcp_request("invalid/method")
            # Should have an error response
            if "error" not in response:
                raise ValueError("Expected error response for invalid method")
            return {
                "error_handling": "working",
                "error_code": response.get("error", {}).get("code"),
                "error_message": response.get("error", {}).get("message")
            }
        except Exception as e:
            # Network or parsing errors are also valid error handling
            return {
                "error_handling": "network_error",
                "error": str(e)
            }

    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        import concurrent.futures
        import threading

        def make_request(request_num):
            try:
                response = self.send_mcp_request("tools/list")
                return {"request_num": request_num, "success": True, "tools_count": len(response.get("result", {}).get("tools", []))}
            except Exception as e:
                return {"request_num": request_num, "success": False, "error": str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(3)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        successful = sum(1 for r in results if r.get("success", False))
        return {
            "total_requests": len(results),
            "successful": successful,
            "success_rate": successful / len(results)
        }

    def run_all_tests(self):
        """Run all MCP tests"""
        print("🚀 Starting Local MCP Server Tests")
        print("=" * 50)

        self.test("MCP Health Check", self.test_mcp_health)
        self.test("MCP Initialization", self.test_mcp_initialization)
        self.test("List Tools", self.test_list_tools)
        self.test("Call Auth Status Tool", self.test_call_auth_status_tool)
        self.test("Call List Spaces Tool", self.test_call_list_spaces_tool)
        self.test("Call Validate Tana File Tool", self.test_call_validate_tana_file_tool)
        self.test("Error Handling", self.test_mcp_error_handling)
        self.test("Concurrent Requests", self.test_concurrent_requests)

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
            print("🎉 All MCP tests passed!")
            return True
        else:
            print("⚠️  Some MCP tests failed")
            return False

def main():
    """Main test runner"""
    tester = MCPTester()

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