"""Simple authentication service for API testing"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import jwt
from pydantic import BaseModel

from ..config import settings


class User(BaseModel):
    username: str
    email: str
    created_at: datetime
    tana_api_key: str | None = None


class SimpleAuthService:
    """Simple in-memory authentication service for testing"""

    def __init__(self):
        self.users_file = Path(__file__).parent.parent.parent / "files" / "metadata" / "users.json"
        self.users = self._load_users()

    def _load_users(self) -> dict[str, dict]:
        """Load users from JSON file"""
        try:
            if self.users_file.exists():
                with open(self.users_file) as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_users(self):
        """Save users to JSON file"""
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=2, default=str)

    def create_user(
        self, username: str, email: str, password: str, tana_api_key: str = ""
    ) -> dict[str, Any]:
        """Create a new user"""
        if username in self.users:
            raise ValueError(f"User '{username}' already exists")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "tana_api_key": tana_api_key,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None,
        }

        self.users[username] = user_data
        self._save_users()

        return {"username": username, "email": email, "created_at": user_data["created_at"]}

    def authenticate_user(self, username: str, password: str) -> dict[str, Any] | None:
        """Authenticate user and return user info with JWT token"""
        user_data = self.users.get(username)
        if not user_data:
            return None

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user_data["password_hash"] != password_hash:
            return None

        # Update last login
        self.users[username]["last_login"] = datetime.utcnow().isoformat()
        self._save_users()

        # Generate JWT token
        token = self._generate_token(username)

        return {
            "username": username,
            "email": user_data["email"],
            "tana_api_key": user_data.get("tana_api_key", ""),
            "last_login": self.users[username]["last_login"],
            "jwt_token": token,
        }

    def validate_token(self, token: str) -> dict[str, Any] | None:
        """Validate JWT token and return user info"""
        try:
            payload = jwt.decode(token, settings.api_secret_key, algorithms=["HS256"])
            username = payload.get("sub")
            if not username:
                return None

            user_data = self.users.get(username)
            if not user_data:
                return None

            return {
                "username": username,
                "email": user_data["email"],
                "tana_api_key": user_data.get("tana_api_key", ""),
            }

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user(self, username: str) -> dict[str, Any] | None:
        """Get user by username"""
        user_data = self.users.get(username)
        if not user_data:
            return None

        return {
            "username": username,
            "email": user_data["email"],
            "created_at": user_data["created_at"],
        }

    def _generate_token(self, username: str) -> str:
        """Generate JWT token for user"""
        expires_delta = timedelta(days=settings.jwt_expiry_days)
        expire = datetime.utcnow() + expires_delta

        payload = {"sub": username, "iat": datetime.utcnow(), "exp": expire}

        return jwt.encode(payload, settings.api_secret_key, algorithm="HS256")


# Global instance
auth_service = SimpleAuthService()


def create_user(username: str, email: str, password: str, tana_api_key: str = "") -> dict[str, Any]:
    """Create a new user"""
    return auth_service.create_user(username, email, password, tana_api_key)


def login_user(username: str, password: str) -> dict[str, Any] | None:
    """Login user and return JWT token"""
    return auth_service.authenticate_user(username, password)


def verify_token(token: str) -> dict[str, Any] | None:
    """Verify JWT token"""
    return auth_service.validate_token(token)


def get_user(username: str) -> dict[str, Any] | None:
    """Get user by username"""
    return auth_service.get_user(username)
