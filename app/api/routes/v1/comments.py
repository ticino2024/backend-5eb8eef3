"""Comment management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.comment_service import CommentService
from app.api.deps import get_current_active_user

router = APIRouter()


@router.post(
    "/articles/{article_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a comment",
    description="Create a new comment on an article",
    responses={
        201: {"description": "Comment created successfully"},
        404: {"description": "Article not found"}
    }
)
async def create_comment(
    article_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> CommentResponse:
    """Create a new comment on an article."""
    comment_service = CommentService(db)
    comment = await comment_service.create_comment(article_id, comment_data, current_user.id)
    return CommentResponse.from_orm(comment)


@router.get(
    "/articles/{article_id}/comments",
    response_model=PaginatedResponse[CommentResponse],
    summary="List comments",
    description="List all comments for a specific article"
)
async def list_comments(
    article_id: str,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db)
) -> PaginatedResponse[CommentResponse]:
    """List comments for an article."""
    comment_service = CommentService(db)
    
    comments = await comment_service.list_comments_by_article(
        article_id,
        skip=pagination.skip,
        limit=pagination.size
    )
    total = await comment_service.count_comments_by_article(article_id)
    
    return PaginatedResponse(
        data=[CommentResponse.from_orm(comment) for comment in comments],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size
    )


@router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
    summary="Get comment by ID",
    description="Get a specific comment by ID",
    responses={
        200: {"description": "Comment found"},
        404: {"description": "Comment not found"}
    }
)
async def get_comment(
    comment_id: str,
    db: AsyncSession = Depends(get_db)
) -> CommentResponse:
    """Get comment by ID."""
    comment_service = CommentService(db)
    comment = await comment_service.get_by_id(comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    return CommentResponse.from_orm(comment)


@router.put(
    "/comments/{comment_id}",
    response_model=CommentResponse,
    summary="Update comment",
    description="Update a comment (author or admin only)",
    responses={
        200: {"description": "Comment updated successfully"},
        403: {"description": "Not authorized to update this comment"},
        404: {"description": "Comment not found"}
    }
)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> CommentResponse:
    """Update a comment."""
    comment_service = CommentService(db)
    is_admin = current_user.role == UserRole.ADMIN
    
    comment = await comment_service.update_comment(
        comment_id,
        comment_data,
        current_user.id,
        is_admin
    )
    return CommentResponse.from_orm(comment)


@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete comment",
    description="Delete a comment (author or admin only)",
    responses={
        204: {"description": "Comment deleted successfully"},
        403: {"description": "Not authorized to delete this comment"},
        404: {"description": "Comment not found"}
    }
)
async def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a comment."""
    comment_service = CommentService(db)
    is_admin = current_user.role == UserRole.ADMIN
    
    await comment_service.delete_comment(comment_id, current_user.id, is_admin)
    return None
