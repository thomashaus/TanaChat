"""Service health and readiness check endpoints."""

from fastapi import APIRouter

from ..services.spaces_client import get_spaces_client

router = APIRouter()


@router.get("/health", summary="Basic health check")
async def health_check():
    """
    Basic health check endpoint.

    Returns:
        Service status information
    """
    return {
        "status": "healthy",
        "service": "tanachat-api",
        "version": "0.1.0",
    }


@router.get("/health/ready", summary="Readiness check")
async def readiness_check():
    """
    Detailed readiness check with dependency verification.

    Checks:
    - Database connectivity (if applicable)
    - S3 storage connection
    - External service availability

    Returns:
        Detailed readiness status with all dependency checks
    """
    # Check S3 connectivity
    spaces_status = "not_configured"
    spaces_details = None

    try:
        spaces_client = get_spaces_client()
        if spaces_client:
            # Test actual connectivity
            test_result = spaces_client.test_connection()
            if test_result["success"]:
                spaces_status = "connected"
                spaces_details = {
                    "bucket": test_result["bucket"],
                    "region": test_result["region"],
                    "endpoint": test_result["endpoint"]
                }
            else:
                spaces_status = "connection_failed"
                spaces_details = {"error": test_result["error"]}
        else:
            spaces_status = "not_configured"
    except Exception as e:
        spaces_status = "error"
        spaces_details = {"error": str(e)}

    # Determine overall readiness
    overall_status = "ready"
    if spaces_status in ["not_configured", "connection_failed", "error"]:
        overall_status = "degraded" if spaces_status == "not_configured" else "not_ready"

    checks = {
        "database": "not_applicable",
        "spaces": spaces_status,
    }

    if spaces_details:
        checks["spaces_details"] = spaces_details

    return {
        "status": overall_status,
        "checks": checks,
    }
