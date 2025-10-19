"""User Pydantic schemas."""

from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Optional
import re

from app.db.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    name: str = Field(..., min_length=1, max_length=100, description="User full name")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name contains only letters and spaces."""
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Name can only contain letters and spaces')
        return v.strip()


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = Field(None, description="User email address")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User full name")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not re.match(r'^[a-zA-Z\s]+$', v):
                raise ValueError('Name can only contain letters and spaces')
            return v.strip()
        return v


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
    role: UserRole = Field(..., description="User role")
    is_active: bool = Field(..., description="User active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="User information")
