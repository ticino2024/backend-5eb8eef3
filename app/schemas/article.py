"""Article Pydantic schemas."""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import re

from app.db.models.article import ArticleStatus
from app.schemas.user import UserResponse


class ArticleCreate(BaseModel):
    """Schema for creating an article."""
    title: str = Field(..., min_length=1, max_length=255, description="Article title")
    content: str = Field(..., min_length=1, description="Article content in markdown")
    summary: Optional[str] = Field(None, max_length=500, description="Article summary")
    status: ArticleStatus = Field(default=ArticleStatus.DRAFT, description="Article status")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate and clean title."""
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content is not empty."""
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v


class ArticleUpdate(BaseModel):
    """Schema for updating an article."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Article title")
    content: Optional[str] = Field(None, min_length=1, description="Article content in markdown")
    summary: Optional[str] = Field(None, max_length=500, description="Article summary")
    status: Optional[ArticleStatus] = Field(None, description="Article status")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate and clean title."""
        if v is not None:
            return v.strip()
        return v
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content is not empty."""
        if v is not None and not v.strip():
            raise ValueError('Content cannot be empty')
        return v


class ArticleResponse(BaseModel):
    """Schema for article response."""
    id: str = Field(..., description="Article ID")
    title: str = Field(..., description="Article title")
    slug: str = Field(..., description="Article slug")
    content: str = Field(..., description="Article content")
    summary: Optional[str] = Field(None, description="Article summary")
    status: ArticleStatus = Field(..., description="Article status")
    author_id: str = Field(..., description="Author ID")
    author: UserResponse = Field(..., description="Article author")
    is_active: bool = Field(..., description="Article active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Schema for article list response (without full content)."""
    id: str = Field(..., description="Article ID")
    title: str = Field(..., description="Article title")
    slug: str = Field(..., description="Article slug")
    summary: Optional[str] = Field(None, description="Article summary")
    status: ArticleStatus = Field(..., description="Article status")
    author_id: str = Field(..., description="Author ID")
    author: UserResponse = Field(..., description="Article author")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True
