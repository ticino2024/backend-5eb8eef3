"""Article database model."""

from sqlalchemy import Column, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class ArticleStatus(str, enum.Enum):
    """Article status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Article(BaseModel):
    """Article model."""
    
    __tablename__ = "articles"
    
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    status = Column(SQLEnum(ArticleStatus), default=ArticleStatus.DRAFT, nullable=False, index=True)
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title}, status={self.status})>"
