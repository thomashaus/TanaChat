"""S3 storage management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..dependencies import get_current_user
from ..services.spaces_client import get_spaces_client

router = APIRouter()


@router.get("/status", summary="Check Spaces connectivity")
async def spaces_status(current_user: dict = Depends(get_current_user)):
    """
    Check S3 connection status and configuration.

    Tests actual connectivity to the configured S3 bucket and returns
    detailed connection information for troubleshooting.

    Returns:
        S3 connection status with configuration details

    Raises:
        401: Authentication required
    """
    client = get_spaces_client()
    if not client:
        return {
            "connected": False,
            "error": "Spaces client not configured",
            "bucket": None,
            "region": None,
        }

    try:
        result = client.test_connection()
        return {
            "connected": result["success"],
            "bucket": result["bucket"],
            "region": result["region"],
            "endpoint": result.get("endpoint"),
            "error": result.get("error") if not result["success"] else None,
        }
    except Exception as e:
        return {
            "connected": False,
            "bucket": client.bucket,
            "region": client.region,
            "error": str(e),
        }


@router.get("/list", summary="List Spaces files")
async def list_files(
    prefix: str = Query("", description="File path prefix to filter results"),
    current_user: dict = Depends(get_current_user),
):
    """
    List files in the user's S3 storage.

    Files are scoped to user directories for security. Only files within
    the user's designated storage space can be accessed.

    Args:
        prefix: Optional path prefix to filter listed files
        current_user: Authenticated user context

    Returns:
        List of files with metadata and prefix information

    Raises:
        401: Authentication required
        503: S3 service not configured
        500: Failed to list files
    """
    client = get_spaces_client()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="S3 not configured",
        )

    try:
        user_prefix = f"tana/{current_user['username']}/"
        full_prefix = f"{user_prefix}{prefix}" if prefix else user_prefix

        files = client.list_files(prefix=full_prefix)
        return {"files": files, "prefix": prefix, "user_prefix": user_prefix}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}",
        )
