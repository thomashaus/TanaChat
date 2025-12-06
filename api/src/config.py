"""Configuration settings for TanaChat API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Settings
    api_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 30

    # S3 Storage
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket: str = "tanachat"
    s3_region: str = "us-east-1"
    s3_endpoint: str = "https://s3.amazonaws.com"

    # API URL
    api_url: str = "http://localhost:8000"

    # MCP Configuration
    mcp_server_name: str = "tanachat"
    mcp_api_token: str = ""

    # Frontend Configuration
    vite_api_url: str = "http://localhost:8000"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "https://tanachat.ai",
    ]

    # Database
    database_url: str = "sqlite:///./tanachat.db"

    # Debug
    debug: bool = False

    # Tana API
    tana_api_key: str = ""

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
