"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.user_service import UserService
from app.api.deps import get_current_active_user, get_current_admin_user

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information"
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    """Get current user profile."""
    return UserResponse.from_orm(current_user)


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    description="Update the currently authenticated user's information"
)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Update current user profile."""
    user_service = UserService(db)
    user = await user_service.update_user(current_user.id, user_data)
    return UserResponse.from_orm(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get a specific user's information by ID",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get user by ID."""
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


@router.get(
    "/",
    response_model=PaginatedResponse[UserResponse],
    summary="List users",
    description="List all users with pagination (admin only)"
)
async def list_users(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
) -> PaginatedResponse[UserResponse]:
    """List users with pagination (admin only)."""
    user_service = UserService(db)
    
    users = await user_service.list_users(skip=pagination.skip, limit=pagination.size)
    total = await user_service.count_users()
    
    return PaginatedResponse(
        data=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by ID (admin only)",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete user (admin only)."""
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return None
