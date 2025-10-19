"""Comment Pydantic schemas."""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from app.schemas.user import UserResponse


class CommentCreate(BaseModel):
    """Schema for creating a comment."""
    content: str = Field(..., min_length=1, max_length=5000, description="Comment content")
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content is not empty."""
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: str = Field(..., min_length=1, max_length=5000, description="Comment content")
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content is not empty."""
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()


class CommentResponse(BaseModel):
    """Schema for comment response."""
    id: str = Field(..., description="Comment ID")
    content: str = Field(..., description="Comment content")
    article_id: str = Field(..., description="Article ID")
    author_id: str = Field(..., description="Author ID")
    author: UserResponse = Field(..., description="Comment author")
    is_active: bool = Field(..., description="Comment active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True
