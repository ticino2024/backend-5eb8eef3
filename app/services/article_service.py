"""Article service with business logic."""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.db.models.article import Article, ArticleStatus
from app.db.models.user import User
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.utils.markdown import generate_slug


class ArticleService:
    """Article service for business logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_article(self, article_data: ArticleCreate, author_id: str) -> Article:
        """Create a new article."""
        # Generate unique slug from title
        slug = generate_slug(article_data.title)
        
        # Create new article
        article = Article(
            title=article_data.title,
            slug=slug,
            content=article_data.content,
            summary=article_data.summary,
            status=article_data.status,
            author_id=author_id
        )
        
        self.db.add(article)
        await self.db.flush()
        await self.db.refresh(article, ['author'])
        
        return article
    
    async def get_by_id(self, article_id: str) -> Optional[Article]:
        """Get article by ID with author information."""
        result = await self.db.execute(
            select(Article)
            .options(selectinload(Article.author))
            .where(Article.id == article_id, Article.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def get_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug with author information."""
        result = await self.db.execute(
            select(Article)
            .options(selectinload(Article.author))
            .where(Article.slug == slug, Article.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def update_article(
        self,
        article_id: str,
        article_data: ArticleUpdate,
        user_id: str,
        is_admin: bool = False
    ) -> Optional[Article]:
        """Update article information."""
        article = await self.get_by_id(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Check authorization (only author or admin can update)
        if article.author_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this article"
            )
        
        # Update fields
        update_data = article_data.dict(exclude_unset=True)
        
        # Regenerate slug if title is being updated
        if 'title' in update_data and update_data['title']:
            update_data['slug'] = generate_slug(update_data['title'])
        
        for field, value in update_data.items():
            setattr(article, field, value)
        
        await self.db.flush()
        await self.db.refresh(article, ['author'])
        
        return article
    
    async def delete_article(self, article_id: str, user_id: str, is_admin: bool = False) -> bool:
        """Soft delete article."""
        article = await self.get_by_id(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Check authorization (only author or admin can delete)
        if article.author_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this article"
            )
        
        article.is_active = False
        await self.db.flush()
        
        return True
    
    async def list_articles(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ArticleStatus] = None,
        author_id: Optional[str] = None
    ) -> List[Article]:
        """List articles with pagination and filters."""
        query = select(Article).options(selectinload(Article.author))
        
        # Apply filters
        query = query.where(Article.is_active == True)
        
        if status:
            query = query.where(Article.status == status)
        
        if author_id:
            query = query.where(Article.author_id == author_id)
        
        # Apply pagination and ordering
        query = query.offset(skip).limit(limit).order_by(Article.created_at.desc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count_articles(
        self,
        status: Optional[ArticleStatus] = None,
        author_id: Optional[str] = None
    ) -> int:
        """Count total articles with filters."""
        query = select(func.count(Article.id)).where(Article.is_active == True)
        
        if status:
            query = query.where(Article.status == status)
        
        if author_id:
            query = query.where(Article.author_id == author_id)
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def publish_article(self, article_id: str, user_id: str) -> Optional[Article]:
        """Publish an article (change status to published)."""
        article = await self.get_by_id(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Check authorization (only author can publish)
        if article.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to publish this article"
            )
        
        article.status = ArticleStatus.PUBLISHED
        await self.db.flush()
        await self.db.refresh(article, ['author'])
        
        return article
