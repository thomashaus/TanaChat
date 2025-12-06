"""TanaChat.ai API - FastAPI Application for Tana workflow integration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth, health, spaces, tana

app = FastAPI(
    title="TanaChat.ai API",
    description=(
        "AI-powered Tana workflow integration platform with REST APIs, MCP servers, and CLI tools."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness checks"},
        {
            "name": "Authentication",
            "description": "JWT-based user authentication and token management",
        },
        {"name": "Tana", "description": "Tana file validation, upload, and management operations"},
        {"name": "Spaces", "description": "S3 storage integration"},
    ],
    contact={
        "name": "TanaChat.ai",
        "url": "https://tanachat.ai",
        "email": "hello@tanachat.ai",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tana.router, prefix="/api/tana", tags=["Tana"])
app.include_router(spaces.router, prefix="/api/spaces", tags=["Spaces"])


@app.get("/")
async def root():
    """API root endpoint with service information."""
    return {
        "name": "TanaChat.ai API",
        "version": "0.1.0",
        "description": "AI-powered Tana workflow integration platform",
        "docs": "/docs",
        "health": "/health",
    }
