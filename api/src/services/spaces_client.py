"""S3 client service"""

from typing import Any

import boto3

from ..config import settings


class SpacesClient:
    """Client for interacting with S3 storage"""

    def __init__(self, key: str, secret: str, bucket: str, region: str, endpoint: str = None):
        self.bucket = bucket
        self.region = region
        self.client = boto3.client(
            "s3",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            region_name=region,
            endpoint_url=endpoint,
        )

    def upload_file(self, key: str, data: bytes, content_type: str = None) -> dict[str, Any]:
        """Upload a file to S3"""
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=data, ContentType=content_type)
            return {
                "success": True,
                "key": key,
                "url": f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def download_file(self, key: str) -> bytes | None:
        """Download a file from S3"""
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            return response["Body"].read()
        except Exception:
            return None

    def list_files(self, prefix: str = "") -> list[dict[str, Any]]:
        """List files in S3"""
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            files = []
            for obj in response.get("Contents", []):
                files.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "url": f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{obj['Key']}",
                    }
                )
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def delete_file(self, key: str) -> bool:
        """Delete a file from S3"""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except Exception:
            return False

    def file_exists(self, key: str) -> bool:
        """Check if a file exists in S3"""
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except Exception:
            return False

    def test_connection(self) -> dict[str, Any]:
        """Test connection to S3"""
        try:
            # Try to list bucket contents (limited to 1 item)
            self.client.list_objects_v2(Bucket=self.bucket, MaxKeys=1)
            return {
                "success": True,
                "bucket": self.bucket,
                "region": self.region,
                "endpoint": self.client.meta.endpoint_url,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "bucket": self.bucket, "region": self.region}


def get_spaces_client() -> SpacesClient | None:
    """Get a configured SpacesClient instance"""
    if not all([settings.s3_access_key, settings.s3_secret_key]):
        return None

    return SpacesClient(
        key=settings.s3_access_key,
        secret=settings.s3_secret_key,
        bucket=settings.s3_bucket,
        region=settings.s3_region,
        endpoint=settings.s3_endpoint,
    )
