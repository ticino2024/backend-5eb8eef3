"""Comment endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestComments:
    """Test comment endpoints."""
    
    async def test_create_comment(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test creating a comment on an article."""
        # Create article first
        article_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = article_response.json()["id"]
        
        # Create comment
        response = await client.post(
            f"/api/v1/articles/{article_id}/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == sample_comment_data["content"]
        assert data["article_id"] == article_id
        assert "id" in data
    
    async def test_create_comment_unauthorized(
        self,
        client: AsyncClient,
        sample_comment_data: dict
    ):
        """Test creating comment without authentication."""
        response = await client.post(
            "/api/v1/articles/some-id/comments",
            json=sample_comment_data
        )
        assert response.status_code == 403
    
    async def test_create_comment_nonexistent_article(
        self,
        client: AsyncClient,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test creating comment on non-existent article."""
        response = await client.post(
            "/api/v1/articles/nonexistent-id/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        assert response.status_code == 404
    
    async def test_list_comments(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test listing comments for an article."""
        # Create article
        article_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = article_response.json()["id"]
        
        # Create comment
        await client.post(
            f"/api/v1/articles/{article_id}/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        
        # List comments
        response = await client.get(f"/api/v1/articles/{article_id}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) >= 1
    
    async def test_get_comment_by_id(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test getting comment by ID."""
        # Create article
        article_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = article_response.json()["id"]
        
        # Create comment
        comment_response = await client.post(
            f"/api/v1/articles/{article_id}/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        comment_id = comment_response.json()["id"]
        
        # Get comment
        response = await client.get(f"/api/v1/comments/{comment_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == comment_id
    
    async def test_update_comment(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test updating a comment."""
        # Create article
        article_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = article_response.json()["id"]
        
        # Create comment
        comment_response = await client.post(
            f"/api/v1/articles/{article_id}/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        comment_id = comment_response.json()["id"]
        
        # Update comment
        update_data = {"content": "Updated comment content"}
        response = await client.put(
            f"/api/v1/comments/{comment_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated comment content"
    
    async def test_delete_comment(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        sample_comment_data: dict,
        auth_headers: dict
    ):
        """Test deleting a comment."""
        # Create article
        article_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = article_response.json()["id"]
        
        # Create comment
        comment_response = await client.post(
            f"/api/v1/articles/{article_id}/comments",
            json=sample_comment_data,
            headers=auth_headers
        )
        comment_id = comment_response.json()["id"]
        
        # Delete comment
        response = await client.delete(
            f"/api/v1/comments/{comment_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify comment is deleted
        get_response = await client.get(f"/api/v1/comments/{comment_id}")
        assert get_response.status_code == 404
