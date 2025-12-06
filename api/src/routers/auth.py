"""JWT-based authentication endpoints for user management."""

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_user
from ..models.user import TokenResponse, UserCreate, UserLogin, UserResponse
from ..services.simple_auth import create_user, login_user

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(user_data: UserCreate):
    """
    Create a new user account and return JWT tokens.

    Args:
        user_data: User registration details (username, email, password)

    Returns:
        JWT access token and user information

    Raises:
        403: User already exists
    """
    result = await create_user(user_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )
    return result


@router.post("/login", response_model=TokenResponse, summary="User login")
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT tokens.

    Args:
        credentials: User login credentials (username, password)

    Returns:
        JWT access token and user information

    Raises:
        401: Invalid credentials
    """
    result = await login_user(credentials)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return result


@router.get("/me", response_model=UserResponse, summary="Get current user")
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.

    Returns:
        Current user profile information
    """
    return UserResponse(
        username=current_user["username"],
        email=current_user["email"],
        created_at=current_user.get("created_at"),
    )


@router.post("/refresh", response_model=TokenResponse, summary="Refresh JWT token")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh an existing JWT token.

    Returns:
        New JWT access token and user information

    Raises:
        501: Feature not implemented yet
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented",
    )
