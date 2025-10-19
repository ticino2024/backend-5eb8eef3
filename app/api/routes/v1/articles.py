"""Article management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.db.models.article import ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.article_service import ArticleService
from app.api.deps import get_current_active_user

router = APIRouter()


@router.post(
    "/",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
    description="Create a new article with markdown content",
    responses={
        201: {"description": "Article created successfully"}
    }
)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    """Create a new article."""
    article_service = ArticleService(db)
    article = await article_service.create_article(article_data, current_user.id)
    return ArticleResponse.from_orm(article)


@router.get(
    "/",
    response_model=PaginatedResponse[ArticleListResponse],
    summary="List articles",
    description="List articles with pagination and filters"
)
async def list_articles(
    pagination: PaginationParams = Depends(),
    status_filter: Optional[ArticleStatus] = Query(None, alias="status"),
    author_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> PaginatedResponse[ArticleListResponse]:
    """List articles with pagination and filters."""
    article_service = ArticleService(db)
    
    articles = await article_service.list_articles(
        skip=pagination.skip,
        limit=pagination.size,
        status=status_filter,
        author_id=author_id
    )
    total = await article_service.count_articles(status=status_filter, author_id=author_id)
    
    return PaginatedResponse(
        data=[ArticleListResponse.from_orm(article) for article in articles],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size
    )


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get article by ID",
    description="Get a specific article by ID",
    responses={
        200: {"description": "Article found"},
        404: {"description": "Article not found"}
    }
)
async def get_article(
    article_id: str,
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    """Get article by ID."""
    article_service = ArticleService(db)
    article = await article_service.get_by_id(article_id)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return ArticleResponse.from_orm(article)


@router.get(
    "/slug/{slug}",
    response_model=ArticleResponse,
    summary="Get article by slug",
    description="Get a specific article by its slug",
    responses={
        200: {"description": "Article found"},
        404: {"description": "Article not found"}
    }
)
async def get_article_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    """Get article by slug."""
    article_service = ArticleService(db)
    article = await article_service.get_by_slug(slug)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return ArticleResponse.from_orm(article)


@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Update article",
    description="Update an article (author or admin only)",
    responses={
        200: {"description": "Article updated successfully"},
        403: {"description": "Not authorized to update this article"},
        404: {"description": "Article not found"}
    }
)
async def update_article(
    article_id: str,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    """Update an article."""
    article_service = ArticleService(db)
    is_admin = current_user.role == UserRole.ADMIN
    
    article = await article_service.update_article(
        article_id,
        article_data,
        current_user.id,
        is_admin
    )
    return ArticleResponse.from_orm(article)


@router.post(
    "/{article_id}/publish",
    response_model=ArticleResponse,
    summary="Publish article",
    description="Publish an article (author only)",
    responses={
        200: {"description": "Article published successfully"},
        403: {"description": "Not authorized to publish this article"},
        404: {"description": "Article not found"}
    }
)
async def publish_article(
    article_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    """Publish an article."""
    article_service = ArticleService(db)
    article = await article_service.publish_article(article_id, current_user.id)
    return ArticleResponse.from_orm(article)


@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete article",
    description="Delete an article (author or admin only)",
    responses={
        204: {"description": "Article deleted successfully"},
        403: {"description": "Not authorized to delete this article"},
        404: {"description": "Article not found"}
    }
)
async def delete_article(
    article_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an article."""
    article_service = ArticleService(db)
    is_admin = current_user.role == UserRole.ADMIN
    
    await article_service.delete_article(article_id, current_user.id, is_admin)
    return None
