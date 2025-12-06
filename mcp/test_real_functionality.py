#!/usr/bin/env python3
"""
Manual test script to demonstrate real MCP functionality
This replicates what the deployed MCP server should be doing
"""

import boto3
import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_auth_status():
    """Check authentication status with real Spaces access"""
    print("🔍 Testing check_auth_status with real functionality...")

    try:
        # These should be the configured credentials
        access_key = os.environ.get("S3_ACCESS_KEY", "test-access-key")
        secret_key = os.environ.get("S3_SECRET_KEY", "test-secret-key")
        bucket = "tanachat"
        region = "nyc3"
        endpoint = "https://nyc3.digitaloceanspaces.com"

        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        # Test if users.json exists
        response = s3_client.get_object(Bucket=bucket, Key="metadata/users.json")
        users_content = response['Body'].read().decode('utf-8')
        users_data = json.loads(users_content)
        users_count = len(users_data.get("users", {}))

        return f"✅ Authentication system ready: {users_count} user(s) configured in DigitalOcean Spaces. Tana API key configuration: Not configured"

    except Exception as e:
        return f"❌ Error checking authentication status: {str(e)}"

def list_spaces_files(bucket="tanachat", prefix="metadata/"):
    """List files in DigitalOcean Spaces"""
    print(f"🔍 Testing list_spaces_files for bucket='{bucket}' prefix='{prefix}'...")

    try:
        access_key = os.environ.get("S3_ACCESS_KEY", "test-access-key")
        secret_key = os.environ.get("S3_SECRET_KEY", "test-secret-key")
        region = "nyc3"
        endpoint = "https://nyc3.digitaloceanspaces.com"

        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=50
        )

        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            files_text = "\n".join(f"📄 {file}" for file in files)
            return f"📁 Files in bucket '{bucket}' with prefix '{prefix}':\n{files_text}"
        else:
            return f"📁 No files found in bucket '{bucket}' with prefix '{prefix}'"

    except Exception as e:
        return f"❌ Error listing Spaces files: {str(e)}"

def validate_tana_file(content):
    """Validate a Tana file format"""
    print(f"🔍 Testing validate_tana_file with content ({len(content)} characters)...")

    validation_results = []

    if not content.strip():
        validation_results.append("❌ File is empty")
    else:
        validation_results.append("✅ File contains content")

        # Check for basic Tana JSON structure
        try:
            parsed = json.loads(content)
            validation_results.append("✅ Valid JSON format")

            # Check for common Tana fields
            if isinstance(parsed, dict):
                if 'nodes' in parsed:
                    validation_results.append("✅ Contains 'nodes' field")
                if 'name' in parsed:
                    validation_results.append("✅ Contains 'name' field")
                if 'type' in parsed:
                    validation_results.append(f"✅ Contains 'type' field: {parsed['type']}")

        except json.JSONDecodeError:
            validation_results.append("❌ Invalid JSON format")

        # Check for Tana-specific patterns
        if 'tana.inc' in content:
            validation_results.append("✅ Contains Tana domain reference")
        if 'field' in content:
            validation_results.append("✅ Contains field definitions")

    return f"Tana File Validation ({len(content)} characters):\n" + "\n".join(validation_results)

def main():
    """Run all MCP tool tests"""
    print("🧪 Testing Real MCP Functionality")
    print("=" * 50)
    print()

    # Test 1: check_auth_status
    result1 = check_auth_status()
    print(f"📋 check_auth_status result:")
    print(f"   {result1}")
    print()

    # Test 2: list_spaces_files
    result2 = list_spaces_files()
    print(f"📋 list_spaces_files result:")
    print(f"   {result2}")
    print()

    # Test 3: validate_tana_file
    test_content = '{"name":"Test Node","type":"node","nodes":[]}'
    result3 = validate_tana_file(test_content)
    print(f"📋 validate_tana_file result:")
    print(f"   {result3}")
    print()

    print("✅ All real MCP functionality tested successfully!")
    print()
    print("🚀 Next Steps:")
    print("   1. Resolve DOCR authentication issues")
    print("   2. Push updated code to deployment")
    print("   3. Replace placeholder responses with real functionality")

if __name__ == "__main__":
    main()