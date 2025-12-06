"""Configuration for MCP server"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    mcp_server_name: str = "tanachat"
    api_url: str = "http://localhost:8000"
    api_token: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
