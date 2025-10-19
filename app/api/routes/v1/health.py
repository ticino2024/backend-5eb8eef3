"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel, Field
from datetime import datetime

from app.db.session import get_db
from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database status")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API and its dependencies",
    tags=["Health"]
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """Check API health status."""
    # Check database connection
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return HealthResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION,
        database=db_status
    )


@router.get(
    "/",
    summary="Root endpoint",
    description="Root endpoint providing API information",
    tags=["Health"]
)
async def root():
    """Root endpoint."""
    return {
        "message": "Blog Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
