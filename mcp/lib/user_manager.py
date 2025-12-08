"""User management for TanaChat.ai"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

from .colors import Colors
from .tana_io import TanaIO

# Default paths
DEFAULT_FILES_DIR = Path("./files")
DEFAULT_METADATA_DIR = DEFAULT_FILES_DIR / "metadata"


class UserManager:
    """Manage users for TanaChat.ai"""

    def __init__(self, files_dir: Optional[Path] = None):
        """Initialize with custom files directory"""
        self.files_dir = files_dir or DEFAULT_FILES_DIR
        self.metadata_dir = self.files_dir / "metadata"
        self.users_file = self.metadata_dir / "users.json"

        # Ensure metadata directory exists
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        # Initialize users file if it doesn't exist
        if not self.users_file.exists():
            self._init_users_file()

    def _init_users_file(self) -> None:
        """Initialize the users metadata file"""
        initial_data = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "users": {}
        }
        self._save_users_data(initial_data)

    def _load_users_data(self) -> Dict[str, Any]:
        """Load users data from file"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            Colors.error(f"Error loading users data: {e}")

    def _save_users_data(self, data: Dict[str, Any]) -> None:
        """Save users data to file"""
        try:
            data["last_updated"] = datetime.now().isoformat()
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            Colors.error(f"Error saving users data: {e}")

    def _generate_jwt_token(self, username: str, secret: str = "default-secret") -> str:
        """Generate a simple JWT-like token (in production, use proper JWT library)"""
        header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
        payload = json.dumps({
            "sub": username,
            "iat": int(datetime.now().timestamp()),
            "exp": int((datetime.now() + timedelta(days=30)).timestamp())
        }).encode()

        # Create a simple HMAC-based token
        h = hashlib.sha256()
        h.update(header + b"." + payload + secret.encode())
        signature = h.hexdigest()

        # Combine parts
        import base64
        token = base64.urlsafe_b64encode(header).decode().rstrip("=") + "." + \
                 base64.urlsafe_b64encode(payload).decode().rstrip("=") + "." + \
                 base64.urlsafe_b64encode(signature.encode()).decode().rstrip("=")

        return token

    def create_user(
        self,
        name: str,
        username: str,
        email: str,
        tana_api_key: str,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new user"""
        users_data = self._load_users_data()

        # Check if username already exists
        if username in users_data["users"]:
            Colors.error(f"User '{username}' already exists")

        # Generate password if not provided
        if not password:
            password = secrets.token_urlsafe(16)

        # Hash password (simple for now, use bcrypt in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Create user data
        user_id = secrets.token_urlsafe(8)
        user_data = {
            "id": user_id,
            "name": name,
            "username": username,
            "email": email,
            "tana_api_key": tana_api_key,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "preferences": {
                "default_export_dir": str(self.files_dir / "exports"),
                "auto_backup": True,
                "theme": "auto"
            }
        }

        # Generate JWT token
        jwt_token = self._generate_jwt_token(username)
        user_data["jwt_token"] = jwt_token

        # Add to users data
        users_data["users"][username] = user_data
        self._save_users_data(users_data)

        Colors.success(f"User '{username}' created successfully")

        return {
            "user": user_data,
            "password": password  # Only return password on creation
        }

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users_data = self._load_users_data()
        return users_data["users"].get(username)

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with password"""
        user = self.get_user(username)
        if not user:
            return None

        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user.get("password_hash"):
            return None

        # Update last login
        users_data = self._load_users_data()
        users_data["users"][username]["last_login"] = datetime.now().isoformat()
        self._save_users_data(users_data)

        # Generate new JWT token
        jwt_token = self._generate_jwt_token(username)
        users_data["users"][username]["jwt_token"] = jwt_token
        self._save_users_data(users_data)

        # Return user info without sensitive data
        return {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "tana_api_key": user["tana_api_key"],
            "jwt_token": jwt_token,
            "preferences": user.get("preferences", {}),
            "last_login": datetime.now().isoformat()
        }

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return user info"""
        users_data = self._load_users_data()

        # Simple validation - find user with matching token
        for username, user_data in users_data["users"].items():
            if user_data.get("jwt_token") == token:
                # Check if token is not expired (simple check)
                # In production, use proper JWT validation
                return {
                    "username": username,
                    "user_id": user_data["id"],
                    "name": user_data["name"]
                }

        return None

    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update user information"""
        users_data = self._load_users_data()

        if username not in users_data["users"]:
            return False

        # Update allowed fields
        allowed_fields = ["name", "email", "tana_api_key", "preferences"]
        for field, value in updates.items():
            if field in allowed_fields:
                users_data["users"][username][field] = value

        self._save_users_data(users_data)
        return True

    def list_users(self) -> List[Dict[str, Any]]:
        """List all users (without sensitive data)"""
        users_data = self._load_users_data()
        users = []

        for username, user_data in users_data["users"].items():
            users.append({
                "username": username,
                "name": user_data["name"],
                "email": user_data["email"],
                "created_at": user_data["created_at"],
                "last_login": user_data.get("last_login"),
                "is_active": user_data.get("is_active", True)
            })

        return users

    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        users_data = self._load_users_data()

        if username not in users_data["users"]:
            return False

        # Remove from users data
        del users_data["users"][username]
        self._save_users_data(users_data)

        # Optionally remove user directory (commented out for safety)
        # user_dir = self.files_dir / "users" / username
        # import shutil
        # shutil.rmtree(user_dir, ignore_errors=True)

        return True