"""Health check endpoints for MCP server."""

import json
import time
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse


def setup_health_endpoints(app: FastAPI) -> None:
    """Set up health check endpoints."""

    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Basic health check endpoint."""
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "service": "TanaChat MCP Server",
                "timestamp": int(time.time()),
                "version": "0.1.0"
            }
        )

    @app.get("/health/ready")
    async def readiness_check() -> JSONResponse:
        """Readiness check - verifies external dependencies."""
        checks = await perform_readiness_checks()

        status_code = 200 if all(check["healthy"] for check in checks.values()) else 503

        return JSONResponse(
            status_code=status_code,
            content={
                "status": "ready" if status_code == 200 else "not ready",
                "checks": checks,
                "timestamp": int(time.time())
            }
        )

    @app.get("/health/live")
    async def liveness_check() -> JSONResponse:
        """Liveness check - verifies the service is running."""
        return JSONResponse(
            status_code=200,
            content={
                "status": "alive",
                "timestamp": int(time.time())
            }
        )


async def perform_readiness_checks() -> Dict[str, Any]:
    """Perform readiness checks on external dependencies."""
    checks = {}

    # Check S3 connectivity
    try:
        import boto3
        from src.config import settings

        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access
        s3_client.head_bucket(Bucket=settings.s3_bucket)
        checks["s3"] = {"healthy": True, "message": "S3 connection successful"}
    except Exception as e:
        checks["s3"] = {"healthy": False, "message": f"S3 connection failed: {str(e)}"}

    # Check Tana API connectivity (if key is configured)
    try:
        from src.config import settings

        if settings.tana_api_key:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://europe-west1.tagr-consolidated-prod.cloudfunctions.net/api/v1",
                    headers={"Authorization": f"Bearer {settings.tana_api_key}"},
                    timeout=5.0
                )

                if response.status_code == 200:
                    checks["tana_api"] = {"healthy": True, "message": "Tana API accessible"}
                else:
                    checks["tana_api"] = {
                        "healthy": False,
                        "message": f"Tana API returned status {response.status_code}"
                    }
        else:
            checks["tana_api"] = {"healthy": True, "message": "Tana API key not configured"}
    except Exception as e:
        checks["tana_api"] = {"healthy": False, "message": f"Tana API check failed: {str(e)}"}

    return checks