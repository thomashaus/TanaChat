"""Configuration for MCP server"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    mcp_server_name: str = "tanachat"
    api_url: str = "http://localhost:8000"
    api_token: str = ""
    cors_origins: str = "*"

    # S3/DigitalOcean Spaces
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket: str = "tanachat"
    s3_region: str = "nyc3"
    s3_endpoint: str = "https://nyc3.digitaloceanspaces.com"

    # Tana API
    tana_api_key: str = ""

    # User Authentication
    default_username: str = "testuser"
    default_user_password: str = "changeme123"
    default_user_id: str = "default-user-id"
    default_user_name: str = "Default User"
    default_user_email: str = "user@example.com"
    default_user_created_at: str = ""
    jwt_secret_key: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import os
        # Set defaults after environment variable loading
        if not self.api_url:
            # Check for production first, then local
            self.api_url = (
                os.getenv("PROD_API_URL") or
                os.getenv("LOCAL_API_URL") or
                "http://localhost:8000"
            )
        if not self.s3_access_key:
            self.s3_access_key = os.getenv("SPACES_ACCESS_KEY", os.getenv("S3_ACCESS_KEY", ""))
        if not self.s3_secret_key:
            self.s3_secret_key = os.getenv("SPACES_SECRET_KEY", os.getenv("S3_SECRET_KEY", ""))
        if not self.s3_bucket:
            self.s3_bucket = os.getenv("SPACES_BUCKET", os.getenv("S3_BUCKET", "tanachat"))
        if not self.s3_region:
            self.s3_region = os.getenv("SPACES_REGION", os.getenv("S3_REGION", "nyc3"))
        if not self.s3_endpoint:
            self.s3_endpoint = os.getenv("SPACES_ENDPOINT", os.getenv("S3_ENDPOINT", "https://nyc3.digitaloceanspaces.com"))
        if not self.tana_api_key:
            self.tana_api_key = os.getenv("TANA_API_KEY", "")

        # User Authentication settings
        if not self.default_username:
            self.default_username = os.getenv("DEFAULT_USERNAME", "testuser")
        if not self.default_user_password:
            self.default_user_password = os.getenv("DEFAULT_USER_PASSWORD", "changeme123")
        if not self.default_user_id:
            self.default_user_id = os.getenv("DEFAULT_USER_ID", "default-user-id")
        if not self.default_user_name:
            self.default_user_name = os.getenv("DEFAULT_USER_NAME", "Default User")
        if not self.default_user_email:
            self.default_user_email = os.getenv("DEFAULT_USER_EMAIL", "user@example.com")
        if not self.jwt_secret_key:
            self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
