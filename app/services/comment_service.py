"""Comment service with business logic."""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.db.models.comment import Comment
from app.db.models.article import Article
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    """Comment service for business logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_comment(
        self,
        article_id: str,
        comment_data: CommentCreate,
        author_id: str
    ) -> Comment:
        """Create a new comment on an article."""
        # Check if article exists and is published
        result = await self.db.execute(
            select(Article).where(
                Article.id == article_id,
                Article.is_active == True
            )
        )
        article = result.scalar_one_or_none()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Create new comment
        comment = Comment(
            content=comment_data.content,
            article_id=article_id,
            author_id=author_id
        )
        
        self.db.add(comment)
        await self.db.flush()
        await self.db.refresh(comment, ['author'])
        
        return comment
    
    async def get_by_id(self, comment_id: str) -> Optional[Comment]:
        """Get comment by ID with author information."""
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.author))
            .where(Comment.id == comment_id, Comment.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def update_comment(
        self,
        comment_id: str,
        comment_data: CommentUpdate,
        user_id: str,
        is_admin: bool = False
    ) -> Optional[Comment]:
        """Update comment content."""
        comment = await self.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        # Check authorization (only author or admin can update)
        if comment.author_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this comment"
            )
        
        comment.content = comment_data.content
        
        await self.db.flush()
        await self.db.refresh(comment, ['author'])
        
        return comment
    
    async def delete_comment(
        self,
        comment_id: str,
        user_id: str,
        is_admin: bool = False
    ) -> bool:
        """Soft delete comment."""
        comment = await self.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        # Check authorization (only author or admin can delete)
        if comment.author_id != user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )
        
        comment.is_active = False
        await self.db.flush()
        
        return True
    
    async def list_comments_by_article(
        self,
        article_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Comment]:
        """List comments for a specific article."""
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.author))
            .where(
                Comment.article_id == article_id,
                Comment.is_active == True
            )
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def count_comments_by_article(self, article_id: str) -> int:
        """Count comments for a specific article."""
        result = await self.db.execute(
            select(func.count(Comment.id))
            .where(
                Comment.article_id == article_id,
                Comment.is_active == True
            )
        )
        return result.scalar_one()
