"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import settings
from app.database import engine, Base
from app.routes import health, auth, users

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints for monitoring and load balancer probes",
        },
        {
            "name": "auth",
            "description": "Authentication and authorization endpoints (JWT-based)",
        },
        {
            "name": "users",
            "description": "User management operations (CRUD)",
        },
        {
            "name": "metrics",
            "description": "Prometheus metrics endpoint for observability",
        },
    ],
    contact={
        "name": "HexaHub Team",
        "url": "https://github.com/yourusername/hexahub",
    },
    license_info={
        "name": "MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the API including version, documentation URLs, and available endpoints",
    response_description="API metadata and navigation links",
    tags=["info"],
)
async def root():
    """
    Get API Information

    Returns metadata about the HexaHub Backend API including:
    - API name and version
    - Description
    - Links to interactive documentation
    - Health check endpoint
    - Metrics endpoint
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "documentation": {
            "interactive": "/docs",
            "redoc": "/redoc",
        },
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
