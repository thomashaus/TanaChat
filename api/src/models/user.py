"""User models for authentication."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Request model for user registration."""

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Request model for user login."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Response model for user information."""

    username: str
    email: str
    created_at: datetime | None = None


class TokenResponse(BaseModel):
    """Response model for authentication token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token expiry in seconds")


class UserInDB(BaseModel):
    """User model stored in DO Spaces."""

    username: str
    email: str
    password_hash: str
    token: str
    created_at: datetime
    updated_at: datetime
