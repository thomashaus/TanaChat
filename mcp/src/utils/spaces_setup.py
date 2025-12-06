"""Utility for setting up DigitalOcean Spaces directory structure."""

import boto3
import os
from typing import Dict, Any
from ..config import settings


def setup_spaces_directories() -> Dict[str, Any]:
    """Create required directories in DigitalOcean Spaces.

    Creates the standard TanaChat directory structure:
    - import/     # For imported Tana files
    - export/     # For exported/generated files
    - metadata/   # For metadata and configuration
    - users/      # For user-specific data
    - temp/       # For temporary files

    Returns:
        Dict with status and details of created directories
    """

    # Check if S3 credentials are configured
    if not settings.s3_access_key or not settings.s3_secret_key:
        return {
            "success": False,
            "error": "S3 credentials not configured",
            "message": "Set S3_ACCESS_KEY and S3_SECRET_KEY environment variables"
        }

    try:
        # Initialize S3 client for DigitalOcean Spaces
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access first
        s3_client.head_bucket(Bucket=settings.s3_bucket)

        # Directories to create (S3 uses empty objects with / suffix)
        directories = [
            'import/',
            'export/',
            'metadata/',
            'metadata/users/',
            'metadata/workspaces/',
            'metadata/config/',
            'users/',
            'temp/',
        ]

        results = []
        created_count = 0

        for directory in directories:
            try:
                # Create directory by uploading empty object with / suffix
                s3_client.put_object(
                    Bucket=settings.s3_bucket,
                    Key=directory,
                    Body=b'',
                    ContentType='application/x-directory'
                )
                results.append(f"✅ Created: {directory}")
                created_count += 1

            except Exception as e:
                # Directory might already exist, that's okay
                if "already exists" in str(e).lower() or "409" in str(e):
                    results.append(f"⚠️  Exists: {directory}")
                else:
                    results.append(f"❌ Failed: {directory} - {str(e)}")

        return {
            "success": True,
            "bucket": settings.s3_bucket,
            "endpoint": settings.s3_endpoint,
            "total_directories": len(directories),
            "created_count": created_count,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": settings.s3_bucket,
            "endpoint": settings.s3_endpoint
        }


def list_spaces_directories() -> Dict[str, Any]:
    """List directories in DigitalOcean Spaces bucket.

    Returns:
        Dict with directory listing and status
    """

    if not settings.s3_access_key or not settings.s3_secret_key:
        return {
            "success": False,
            "error": "S3 credentials not configured"
        }

    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # List common prefixes (directories)
        response = s3_client.list_objects_v2(
            Bucket=settings.s3_bucket,
            Delimiter='/',
            MaxKeys=100
        )

        directories = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                directories.append(prefix['Prefix'])

        return {
            "success": True,
            "bucket": settings.s3_bucket,
            "directories": directories,
            "count": len(directories)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": settings.s3_bucket
        }