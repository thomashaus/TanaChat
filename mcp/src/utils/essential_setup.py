"""Essential setup for TanaChat Spaces - uploads critical files."""

import boto3
import os
import json
from ..config import settings


def ensure_users_json():
    """Ensure users.json exists in Spaces for login system."""

    # Check if credentials are available
    if not settings.s3_access_key or not settings.s3_secret_key:
        return {
            "success": False,
            "error": "S3 credentials not configured",
            "message": "Cannot access DigitalOcean Spaces without credentials"
        }

    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access
        s3_client.head_bucket(Bucket=settings.s3_bucket)

        # Read local users.json
        users_file_path = "../../files/metadata/users.json"
        if os.path.exists(users_file_path):
            with open(users_file_path, 'r') as f:
                users_data = f.read()
        else:
            # Create minimal users.json if not exists
            users_data = json.dumps({
                "version": "1.0",
                "created_at": "2025-12-06T05:15:00.000Z",
                "users": {
                    "testuser": {
                        "id": "oBJXXTOlwLA",
                        "name": "Test User",
                        "username": "testuser",
                        "email": "test@example.com",
                        "tana_api_key": "dummykey",
                        "password_hash": "7e6e0c3079a08c5cc6036789b57e951f65f82383913ba1a49ae992544f1b4b6e",
                        "created_at": "2025-12-05T22:52:26.833824",
                        "last_login": None,
                        "is_active": True,
                        "preferences": {
                            "default_export_dir": "files/exports",
                            "auto_backup": True,
                            "theme": "auto"
                        }
                    }
                }
            }, indent=2)

        # Upload users.json to Spaces
        s3_client.put_object(
            Bucket=settings.s3_bucket,
            Key="metadata/users.json",
            Body=users_data.encode('utf-8'),
            ContentType='application/json',
            CacheControl='no-cache'
        )

        return {
            "success": True,
            "message": "users.json uploaded successfully",
            "bucket": settings.s3_bucket,
            "key": "metadata/users.json",
            "url": f"https://{settings.s3_bucket}.{settings.s3_region}.digitaloceanspaces.com/metadata/users.json"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to upload users.json to Spaces"
        }


def test_spaces_access():
    """Test basic Spaces access with configured credentials."""

    if not settings.s3_access_key or not settings.s3_secret_key:
        return {
            "success": False,
            "error": "S3 credentials not configured",
            "bucket": settings.s3_bucket,
            "endpoint": settings.s3_endpoint
        }

    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access
        s3_client.head_bucket(Bucket=settings.s3_bucket)

        # Test if users.json exists
        try:
            response = s3_client.get_object(Bucket=settings.s3_bucket, Key="metadata/users.json")
            users_content = response['Body'].read().decode('utf-8')
            users_data = json.loads(users_content)

            return {
                "success": True,
                "message": "Spaces access successful",
                "bucket": settings.s3_bucket,
                "users_json_exists": True,
                "users_count": len(users_data.get("users", {})),
                "endpoint": settings.s3_endpoint
            }

        except s3_client.exceptions.NoSuchKey:
            return {
                "success": True,
                "message": "Spaces access successful but users.json missing",
                "bucket": settings.s3_bucket,
                "users_json_exists": False,
                "endpoint": settings.s3_endpoint
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": settings.s3_bucket,
            "endpoint": settings.s3_endpoint
        }