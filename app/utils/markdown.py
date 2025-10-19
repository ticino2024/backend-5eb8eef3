"""Markdown processing utilities."""

import markdown
import bleach
from typing import List

# Allowed HTML tags for sanitization
ALLOWED_TAGS: List[str] = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img', 'hr',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
]

# Allowed HTML attributes
ALLOWED_ATTRIBUTES: dict = {
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title'],
    'code': ['class']
}


def markdown_to_html(markdown_text: str) -> str:
    """Convert markdown to sanitized HTML."""
    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_text,
        extensions=['extra', 'codehilite', 'fenced_code', 'tables']
    )
    
    # Sanitize HTML to prevent XSS attacks
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    return clean_html


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    import re
    import uuid
    
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Add unique identifier to ensure uniqueness
    unique_id = str(uuid.uuid4())[:8]
    slug = f"{slug}-{unique_id}"
    
    return slug
