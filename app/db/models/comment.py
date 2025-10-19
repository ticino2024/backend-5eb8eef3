"""Comment database model."""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class Comment(BaseModel):
    """Comment model."""
    
    __tablename__ = "comments"
    
    content = Column(Text, nullable=False)
    article_id = Column(String, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, article_id={self.article_id}, author_id={self.author_id})>"
