"""Common Pydantic schemas."""

from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    
    @property
    def skip(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    data: List[T] = Field(..., description="Response data")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
