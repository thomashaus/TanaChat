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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
