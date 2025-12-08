#!/usr/bin/env python3
"""
Test script for new password management API endpoints
"""

import requests
import json
import os

BASE_URL = os.getenv("LOCAL_API_URL", "http://localhost:8000")

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)

        print(f"\n{'='*60}")
        print(f"Testing: {method} {endpoint}")
        print(f"Status: {response.status_code}")

        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response: {response.text}")

        return response.status_code == 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    print("Testing TanaChat Password Management API Endpoints")
    print("=" * 60)

    # Test endpoints
    tests = [
        {
            "name": "Change Password",
            "endpoint": "/api/auth/change-password",
            "method": "POST",
            "data": {
                "username": "testuser",
                "current_password": "testpass123",
                "new_password": "newpassword123"
            }
        },
        {
            "name": "Reset Password",
            "endpoint": "/api/auth/reset-password",
            "method": "POST",
            "data": {
                "username": "testuser",
                "new_password": "resetpassword123",
                "admin_key": "test-admin-key"
            }
        },
        {
            "name": "Set Password",
            "endpoint": "/api/auth/set-password",
            "method": "POST",
            "data": {
                "username": "testuser",
                "new_password": "setpassword123",
                "admin_key": "test-admin-key"
            }
        },
        {
            "name": "Password Too Short",
            "endpoint": "/api/auth/change-password",
            "method": "POST",
            "data": {
                "username": "testuser",
                "current_password": "testpass123",
                "new_password": "123"  # Too short
            }
        },
        {
            "name": "Invalid User",
            "endpoint": "/api/auth/set-password",
            "method": "POST",
            "data": {
                "username": "nonexistentuser",
                "new_password": "validpassword123",
                "admin_key": "test-admin-key"
            }
        }
    ]

    results = []
    for test in tests:
        print(f"\n{'#'*60}")
        print(f"Test: {test['name']}")
        success = test_endpoint(test['endpoint'], test['method'], test['data'])
        results.append((test['name'], success))

    # Summary
    print(f"\n{'#'*60}")
    print("TEST SUMMARY")
    print(f"{'#'*60}")

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

if __name__ == "__main__":
    main()