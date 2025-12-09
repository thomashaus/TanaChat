"""S3-backed user manager for persistent user storage in DigitalOcean Spaces"""

import json
import boto3
from datetime import datetime
from typing import Dict, Optional, List
import hashlib
import secrets
import uuid

from src.config import settings


class S3UserManager:
    """S3-backed user manager that stores users in DigitalOcean Spaces"""

    def __init__(self):
        """Initialize S3 client and validate configuration"""
        # Validate required environment variables
        if not settings.s3_access_key:
            raise ValueError("S3_ACCESS_KEY environment variable is required")
        if not settings.s3_secret_key:
            raise ValueError("S3_SECRET_KEY environment variable is required")
        if not settings.s3_bucket:
            raise ValueError("S3_BUCKET environment variable is required")
        if not settings.s3_endpoint:
            raise ValueError("S3_ENDPOINT environment variable is required")
        if not settings.s3_region:
            raise ValueError("S3_REGION environment variable is required")

        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.s3_endpoint,
                aws_access_key_id=settings.s3_access_key,
                aws_secret_access_key=settings.s3_secret_key,
                region_name=settings.s3_region
            )
            self.bucket = settings.s3_bucket
            self.users_key = "metadata/users.json"

            # Skip HeadBucket test to avoid CORS/permission issues
            # We'll test actual access during operations instead

        except Exception as e:
            raise ValueError(f"Failed to initialize S3 client: {str(e)}")

    def _load_users(self) -> Dict:
        """Load users from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=self.users_key)
            content = response['Body'].read().decode('utf-8')
            data = json.loads(content)
            return data.get("users", {})
        except self.s3_client.exceptions.NoSuchKey:
            # Users file doesn't exist, return empty dict
            return {}
        except Exception as e:
            raise Exception(f"Failed to load users from S3: {str(e)}")

    def _save_users(self, users: Dict):
        """Save users to S3"""
        try:
            data = {
                "version": "1.0",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "users": users
            }

            content = json.dumps(data, indent=2)
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=self.users_key,
                Body=content.encode('utf-8'),
                ContentType='application/json',
                CacheControl='no-cache, no-store, must-revalidate'
            )
        except Exception as e:
            raise Exception(f"Failed to save users to S3: {str(e)}")

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def list_users(self) -> List[Dict]:
        """List all users"""
        users = self._load_users()
        return list(users.values())

    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        users = self._load_users()
        return users.get(username)

    def create_user(self, name: str, username: str, password: str, email: str,
                   tana_api_key: str = None, node_id: str = None) -> Dict:
        """Create a new user"""
        users = self._load_users()

        # Check if user already exists
        if username in users:
            raise ValueError(f"User '{username}' already exists")

        # Create user object
        user = {
            "id": f"user_{secrets.token_hex(8)}",
            "name": name,
            "username": username,
            "email": email,
            "password_hash": self._hash_password(password),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_login": None,
            "is_active": True,
            "preferences": {
                "default_export_dir": "files/exports",
                "auto_backup": True,
                "theme": "auto"
            }
        }

        if tana_api_key:
            user["tana_api_key"] = tana_api_key
        if node_id:
            user["node_id"] = node_id

        # Save user
        users[username] = user
        self._save_users(users)

        return user

    def update_user(self, username: str, updates: Dict) -> bool:
        """Update user information"""
        users = self._load_users()

        if username not in users:
            return False

        user = users[username]

        # Update fields
        for field, value in updates.items():
            if field == "password":
                # Hash password if updating
                user["password_hash"] = self._hash_password(value)
            elif field in ["name", "email", "tana_api_key", "node_id", "is_active"]:
                user[field] = value

        user["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Save updated users
        users[username] = user
        self._save_users(users)

        return True

    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        users = self._load_users()

        if username not in users:
            return False

        del users[username]
        self._save_users(users)

        return True

    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        user = self.get_user(username)
        if not user:
            return False

        password_hash = self._hash_password(password)
        return user.get("password_hash") == password_hash

    def generate_api_token(self, username: str) -> str:
        """Generate API token for user"""
        token = str(uuid.uuid4())
        users = self._load_users()

        if username in users:
            users[username]["api_token"] = token
            users[username]["token_created_at"] = datetime.utcnow().isoformat() + "Z"
            self._save_users(users)

        return token

    def verify_api_token(self, token: str) -> Optional[Dict]:
        """Verify API token and return user data"""
        users = self._load_users()

        for username, user_data in users.items():
            if user_data.get("api_token") == token:
                return user_data

        return None

    def get_user_by_token(self, token: str) -> Optional[Dict]:
        """Get user by API token"""
        return self.verify_api_token(token)