"""Main entry point for TanaChat MCP server."""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str

class CreateUserRequest(BaseModel):
    """Create user request model."""
    username: str
    password: str
    email: str
    name: str = None
    tana_api_key: str = None
    node_id: str = None

class UpdateUserRequest(BaseModel):
    """Update user request model."""
    email: str = None
    name: str = None
    tana_api_key: str = None
    password: str = None
    is_active: bool = None
    node_id: str = None

from src.config import settings
# from src.server import mcp  # Commented out to avoid fastmcp dependency for user management
from lib.s3_user_manager import S3UserManager

# Security
security = HTTPBearer()

# Authentication functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from API token."""
    try:
        token = credentials.credentials
        user_manager = S3UserManager()
        user = user_manager.verify_api_token(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired API token"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication"
        )

async def get_mcp_user(request: Request):
    """Get user from MCP request Authorization header."""
    try:
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Valid Bearer token required"
            )

        token = auth_header[7:]  # Remove "Bearer " prefix
        user_manager = S3UserManager()
        user = user_manager.verify_api_token(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired API token"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication"
        )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Validate required environment variables on startup
def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        ("S3_ACCESS_KEY", settings.s3_access_key),
        ("S3_SECRET_KEY", settings.s3_secret_key),
        ("S3_BUCKET", settings.s3_bucket),
        ("S3_ENDPOINT", settings.s3_endpoint),
        ("S3_REGION", settings.s3_region)
    ]

    missing_vars = [var_name for var_name, var_value in required_vars if not var_value]

    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logging.error(error_msg)
        raise ValueError(error_msg)

# Validate environment on startup
try:
    validate_environment()
    logging.info("Environment variables validated successfully")
except ValueError as e:
    logging.error(f"Environment validation failed: {str(e)}")
    # We'll let the app start but endpoints will fail with proper 500 errors

# Create FastAPI app
app = FastAPI(
    title="TanaChat API & MCP Server",
    description="API server and MCP endpoint for Tana workspace management - Updated with real functionality",
    version="0.1.1",
    docs_url="/docs",  # Enable docs
    redoc_url="/redoc",  # Enable redoc
    openapi_components={
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your Bearer token"
            }
        }
    }
)

# Configure CORS
# Parse comma-separated origins string into list
cors_origins_list = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
if "*" in settings.cors_origins:
    cors_origins_list = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    """MCP request model."""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = {}
    id: Any = None

class MCPResponse(BaseModel):
    """MCP response model."""
    jsonrpc: str = "2.0"
    result: Any = None
    error: Dict[str, Any] = None
    id: Any = None

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service info."""
    return {
        "service": "TanaChat API & MCP Server",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "api": "/api",
            "mcp": "/mcp",
            "health": "/health",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "TanaChat MCP Server",
        "version": "0.1.0"
    }

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    """Get OpenAPI schema."""
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI documentation."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Documentation",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# API Endpoints for REST access
@app.get("/api/v1/tools", tags=["API"])
async def list_tools():
    """List available tools via REST API."""

    # Try to upload users.json to Spaces when this endpoint is called
    try:
        import boto3
        import json

        if settings.s3_access_key and settings.s3_secret_key:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                endpoint_url=settings.s3_endpoint,
                aws_access_key_id=settings.s3_access_key,
                aws_secret_access_key=settings.s3_secret_key,
                region_name=settings.s3_region
            )

            # Create users.json content
            users_data = json.dumps({
                "version": "1.0",
                "created_at": "2025-12-06T05:23:00.000Z",
                "users": {
                    "testuser": {
                        "id": "oBJXXTOlwLA",
                        "name": "Test User",
                        "username": "testuser",
                        "email": "test@example.com",
                        "tana_api_key": "dummykey",
                        "password_hash": "7e6e0c3079a08c5cc6036789b57e951f65f82383913ba1a49ae992544f1b4b6e",
                        "created_at": "2025-12-05T22:52:26.833824",
                        "last_login": None,
                        "is_active": True,
                        "preferences": {
                            "default_export_dir": "files/exports",
                            "auto_backup": True,
                            "theme": "auto"
                        }
                    }
                }
            }, indent=2)

            # Upload users.json to Spaces
            s3_client.put_object(
                Bucket=settings.s3_bucket,
                Key="metadata/users.json",
                Body=users_data.encode('utf-8'),
                ContentType='application/json'
            )

            spaces_status = "users.json uploaded successfully"
        else:
            spaces_status = "S3 credentials not configured"

    except Exception as e:
        spaces_status = f"Spaces upload failed: {str(e)} | Type: {type(e).__name__}"

    return {
        "tools": [
            {
                "name": "check_auth_status",
                "description": "Check authentication status with Tana",
                "parameters": {}
            },
            {
                "name": "list_spaces_files",
                "description": "List files in DigitalOcean Spaces",
                "parameters": {
                    "bucket": {"type": "string", "default": "tanachat"},
                    "prefix": {"type": "string", "optional": True}
                }
            },
            {
                "name": "validate_tana_file",
                "description": "Validate a Tana file format",
                "parameters": {
                    "content": {"type": "string", "required": True}
                }
            }
        ],
        "spaces_status": spaces_status,
        "test_update": "deployment_test_" + str(hash("test"))
    }

@app.get("/api/v1/auth/status", tags=["API"])
async def get_auth_status():
    """Get authentication status."""

    # Test S3 credentials availability
    s3_test = {
        "access_key": bool(settings.s3_access_key) if hasattr(settings, 's3_access_key') else False,
        "secret_key": bool(settings.s3_secret_key) if hasattr(settings, 's3_secret_key') else False,
        "bucket": getattr(settings, 's3_bucket', 'not_set'),
        "region": getattr(settings, 's3_region', 'not_set'),
        "endpoint": getattr(settings, 's3_endpoint', 'not_set')
    }

    return {
        "authenticated": False,
        "message": "Configure TANA_API_KEY environment variable",
        "setup_required": True,
        "s3_test": s3_test
    }

# Spaces essential setup endpoints - inline implementation
@app.post("/api/v1/spaces/setup-essential", tags=["API"])
async def setup_essential_spaces():
    """Setup essential files in DigitalOcean Spaces for login system."""
    try:
        import boto3
        import os
        import json

        # Use the configured settings
        if not settings.s3_access_key or not settings.s3_secret_key:
            raise Exception("S3 credentials not configured")

        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access
        s3_client.head_bucket(Bucket=settings.s3_bucket)

        # Create users.json content
        users_data = json.dumps({
            "version": "1.0",
            "created_at": "2025-12-06T05:20:00.000Z",
            "users": {
                "testuser": {
                    "id": "oBJXXTOlwLA",
                    "name": "Test User",
                    "username": "testuser",
                    "email": "test@example.com",
                    "tana_api_key": "dummykey",
                    "password_hash": "7e6e0c3079a08c5cc6036789b57e951f65f82383913ba1a49ae992544f1b4b6e",
                    "created_at": "2025-12-05T22:52:26.833824",
                    "last_login": None,
                    "is_active": True,
                    "preferences": {
                        "default_export_dir": "files/exports",
                        "auto_backup": True,
                        "theme": "auto"
                    }
                }
            }
        }, indent=2)

        # Upload users.json to Spaces
        s3_client.put_object(
            Bucket=settings.s3_bucket,
            Key="metadata/users.json",
            Body=users_data.encode('utf-8'),
            ContentType='application/json',
            CacheControl='no-cache'
        )

        return {
            "message": "Essential Spaces setup completed",
            "details": {
                "success": True,
                "bucket": settings.s3_bucket,
                "key": "metadata/users.json",
                "url": f"https://{settings.s3_bucket}.{settings.s3_region}.digitaloceanspaces.com/metadata/users.json"
            }
        }

    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/spaces/test", tags=["API"])
async def test_spaces_connection():
    """Test DigitalOcean Spaces connection and users.json availability."""
    try:
        import boto3
        import json

        if not settings.s3_access_key or not settings.s3_secret_key:
            raise Exception("S3 credentials not configured")

        s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )

        # Test bucket access
        s3_client.head_bucket(Bucket=settings.s3_bucket)

        # Test if users.json exists
        try:
            response = s3_client.get_object(Bucket=settings.s3_bucket, Key="metadata/users.json")
            users_content = response['Body'].read().decode('utf-8')
            users_data = json.loads(users_content)

            return {
                "message": "Spaces connection successful",
                "details": {
                    "success": True,
                    "bucket": settings.s3_bucket,
                    "users_json_exists": True,
                    "users_count": len(users_data.get("users", {})),
                    "endpoint": settings.s3_endpoint
                }
            }

        except Exception:
            return {
                "message": "Spaces connection successful but users.json missing",
                "details": {
                    "success": True,
                    "bucket": settings.s3_bucket,
                    "users_json_exists": False,
                    "endpoint": settings.s3_endpoint
                }
            }

    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

# Authentication endpoints for frontend login
@app.post("/api/auth/login", tags=["Authentication"])
async def login_user(login_data: LoginRequest):
    """Authenticate user and return JWT token."""
    username = login_data.username
    password = login_data.password

    # For now, accept the test user we created
    if username == "testuser" and password == "testpass123":
        # Generate a simple JWT-like token using settings
        import jwt
        import datetime

        secret_key = "your-secret-key-change-in-production"  # Should use settings.api_secret_key
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 2592000  # 30 days in seconds
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/api/auth/me", tags=["Authentication"])
async def get_current_user():
    """Get current user information (placeholder)."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "created_at": "2025-12-06T04:55:00Z"
    }

@app.get("/api/test-endpoint", tags=["Test"])
async def test_endpoint():
    """Test endpoint to verify registration."""
    return {"message": "Test endpoint working!", "timestamp": "2025-12-08"}

# User Management endpoints
@app.get("/api/users", tags=["Users"], dependencies=[Depends(get_current_user)])
async def list_users():
    """List all users (requires authentication)."""
    try:
        user_manager = S3UserManager()
        users = user_manager.list_users()
        return {
            "users": users,
            "count": len(users)
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list users: {str(e)}")

@app.get("/api/users/{username}", tags=["Users"], dependencies=[Depends(get_current_user)])
async def get_user(username: str):
    """Get specific user by username (requires authentication)."""
    try:
        user_manager = S3UserManager()
        user = user_manager.get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@app.post("/api/users", tags=["Users"])
async def create_user(user_data: CreateUserRequest):
    """Create a new user."""
    try:
        user_manager = S3UserManager()

        # Check if user already exists
        existing_user = user_manager.get_user(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Create the user
        user = user_manager.create_user(
            name=user_data.name or user_data.username,
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            tana_api_key=user_data.tana_api_key or "default_key"
        )

        # Update node_id if provided
        if user_data.node_id:
            user_manager.update_user(user_data.username, {"node_id": user_data.node_id})
            updated_user = user_manager.get_user(user_data.username)
        else:
            updated_user = user

        return {
            "message": "User created successfully",
            "user": updated_user
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.post("/api/users/{username}/generate-token", tags=["Users"])
async def generate_api_token(username: str):
    """Generate API token for user."""
    try:
        user_manager = S3UserManager()

        # Check if user exists
        user = user_manager.get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate API token
        api_token = user_manager.generate_api_token(username)

        return {
            "message": "API token generated successfully",
            "api_token": api_token,
            "username": username
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate API token: {str(e)}")

@app.put("/api/users/{username}", tags=["Users"])
async def update_user(username: str, updates: UpdateUserRequest):
    """Update user information."""
    try:
        user_manager = S3UserManager()

        # Check if user exists
        existing_user = user_manager.get_user(username)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare update data
        update_data = {}
        if updates.email is not None:
            update_data["email"] = updates.email
        if updates.name is not None:
            update_data["name"] = updates.name
        if updates.tana_api_key is not None:
            update_data["tana_api_key"] = updates.tana_api_key
        if updates.password is not None:
            update_data["password"] = updates.password
        if updates.is_active is not None:
            update_data["is_active"] = updates.is_active
        if updates.node_id is not None:
            update_data["node_id"] = updates.node_id

        # Update the user
        success = user_manager.update_user(username, update_data)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to update user")

        updated_user = user_manager.get_user(username)

        return {
            "message": "User updated successfully",
            "user": updated_user
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

@app.delete("/api/users/{username}", tags=["Users"])
async def delete_user(username: str):
    """Delete a user."""
    try:
        user_manager = S3UserManager()

        # Check if user exists
        existing_user = user_manager.get_user(username)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        success = user_manager.delete_user(username)

        if success:
            return {
                "message": "User deleted successfully",
                "username": username
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to delete user")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

# Spaces management endpoints
@app.post("/api/spaces/setup", tags=["Spaces"])
async def setup_spaces():
    """Setup directory structure in DigitalOcean Spaces."""
    from .utils.spaces_setup import setup_spaces_directories

    result = setup_spaces_directories()

    if result["success"]:
        return {
            "message": "Spaces directory setup completed",
            "details": result
        }
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/api/spaces/list", tags=["Spaces"])
async def list_spaces():
    """List directories in DigitalOcean Spaces."""
    from .utils.spaces_setup import list_spaces_directories

    result = list_spaces_directories()

    if result["success"]:
        return {
            "message": "Spaces directory listing",
            "details": result
        }
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=result["error"])

# MCP Protocol Endpoint (for ChatGPT/Claude Desktop)
@app.post("/mcp", tags=["MCP"])
@app.post("/", tags=["MCP"], include_in_schema=False)  # Alternative endpoint for some MCP clients
async def handle_mcp(request: MCPRequest, http_request: Request):
    """Handle MCP protocol requests."""
    try:
        # Skip authentication for initialize method
        if request.method != "initialize":
            current_user = await get_mcp_user(http_request)
            logging.info(f"MCP Request: {request.method} from user {current_user.get('username', 'unknown')}")
        else:
            logging.info(f"MCP Request: {request.method}")

        # Process the MCP request
        if request.method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": True
                    }
                },
                "serverInfo": {
                    "name": "tanachat",
                    "version": "0.1.0"
                }
            }
        elif request.method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "check_auth_status",
                        "description": "Check authentication status with Tana",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "list_spaces_files",
                        "description": "List files in DigitalOcean Spaces",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "bucket": {"type": "string", "default": "tanachat"},
                                "prefix": {"type": "string"}
                            }
                        }
                    },
                    {
                        "name": "validate_tana_file",
                        "description": "Validate a Tana file format",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"}
                            },
                            "required": ["content"]
                        }
                    }
                ]
            }
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})

            if tool_name == "check_auth_status":
                # Check if Tana API key is configured and test Spaces access
                try:
                    import boto3
                    import json

                    if settings.s3_access_key and settings.s3_secret_key:
                        s3_client = boto3.client(
                            's3',
                            endpoint_url=settings.s3_endpoint,
                            aws_access_key_id=settings.s3_access_key,
                            aws_secret_access_key=settings.s3_secret_key,
                            region_name=settings.s3_region
                        )

                        # Test if users.json exists
                        try:
                            response = s3_client.get_object(Bucket=settings.s3_bucket, Key="metadata/users.json")
                            users_content = response['Body'].read().decode('utf-8')
                            users_data = json.loads(users_content)
                            users_count = len(users_data.get("users", {}))

                            result = {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"✅ Authentication system ready: {users_count} user(s) configured in DigitalOcean Spaces. Tana API key configuration: {'Configured' if hasattr(settings, 'tana_api_key') and settings.tana_api_key else 'Not configured'}"
                                    }
                                ]
                            }
                        except Exception as spaces_error:
                            result = {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"⚠️  Spaces access configured but users.json not found: {str(spaces_error)}"
                                    }
                                ]
                            }
                    else:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "❌ DigitalOcean Spaces credentials not configured"
                                }
                            ]
                        }

                except Exception as e:
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"❌ Error checking authentication status: {str(e)}"
                            }
                        ]
                    }

            elif tool_name == "list_spaces_files":
                bucket = arguments.get("bucket", "tanachat")
                prefix = arguments.get("prefix", "")

                try:
                    import boto3

                    if settings.s3_access_key and settings.s3_secret_key:
                        s3_client = boto3.client(
                            's3',
                            endpoint_url=settings.s3_endpoint,
                            aws_access_key_id=settings.s3_access_key,
                            aws_secret_access_key=settings.s3_secret_key,
                            region_name=settings.s3_region
                        )

                        response = s3_client.list_objects_v2(
                            Bucket=bucket,
                            Prefix=prefix,
                            MaxKeys=50
                        )

                        if 'Contents' in response:
                            files = [obj['Key'] for obj in response['Contents']]
                            files_text = "\n".join(f"📄 {file}" for file in files)
                            result = {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"📁 Files in bucket '{bucket}' with prefix '{prefix}':\n{files_text}"
                                    }
                                ]
                            }
                        else:
                            result = {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"📁 No files found in bucket '{bucket}' with prefix '{prefix}'"
                                    }
                                ]
                            }
                    else:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "❌ Spaces credentials not configured"
                                }
                            ]
                        }

                except Exception as e:
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"❌ Error listing Spaces files: {str(e)}"
                            }
                        ]
                    }

            elif tool_name == "validate_tana_file":
                content = arguments.get("content", "")

                # Basic Tana file validation
                validation_results = []

                if not content.strip():
                    validation_results.append("❌ File is empty")
                else:
                    validation_results.append("✅ File contains content")

                    # Check for basic Tana JSON structure
                    try:
                        import json
                        parsed = json.loads(content)
                        validation_results.append("✅ Valid JSON format")

                        # Check for common Tana fields
                        if isinstance(parsed, dict):
                            if 'nodes' in parsed:
                                validation_results.append("✅ Contains 'nodes' field")
                            if 'name' in parsed:
                                validation_results.append("✅ Contains 'name' field")
                            if 'type' in parsed:
                                validation_results.append(f"✅ Contains 'type' field: {parsed['type']}")

                    except json.JSONDecodeError:
                        validation_results.append("❌ Invalid JSON format")

                    # Check for Tana-specific patterns
                    if 'tana.inc' in content:
                        validation_results.append("✅ Contains Tana domain reference")
                    if 'field' in content:
                        validation_results.append("✅ Contains field definitions")

                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Tana File Validation ({len(content)} characters):\n" + "\n".join(validation_results)
                        }
                    ]
                }
            else:
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unknown tool: {tool_name}"
                        }
                    ]
                }
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")

        return MCPResponse(result=result, id=request.id)

    except Exception as e:
        logging.error(f"Error handling MCP request: {e}")
        return MCPResponse(
            error={
                "code": -1,
                "message": str(e)
            },
            id=request.id
        )

def main():
    """Run the HTTP server."""
    logging.info("Starting TanaChat API & MCP HTTP server...")
    logging.info("Available endpoints:")
    logging.info("  - REST API: /api/v1/*")
    logging.info("  - MCP Protocol: /mcp (for ChatGPT/Claude Desktop)")
    logging.info("  - Documentation: /docs")
    logging.info("  - Health Check: /health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()