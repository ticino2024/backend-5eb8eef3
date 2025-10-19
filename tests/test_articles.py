"""Article endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestArticles:
    """Test article endpoints."""
    
    async def test_create_article(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test creating an article."""
        response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_article_data["title"]
        assert data["content"] == sample_article_data["content"]
        assert data["slug"] is not None
        assert "id" in data
    
    async def test_create_article_unauthorized(
        self,
        client: AsyncClient,
        sample_article_data: dict
    ):
        """Test creating article without authentication."""
        response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert response.status_code == 403
    
    async def test_list_articles(self, client: AsyncClient):
        """Test listing articles."""
        response = await client.get("/api/v1/articles/")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    async def test_get_article_by_id(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test getting article by ID."""
        # Create article
        create_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = create_response.json()["id"]
        
        # Get article
        response = await client.get(f"/api/v1/articles/{article_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == article_id
        assert data["title"] == sample_article_data["title"]
    
    async def test_get_article_by_slug(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test getting article by slug."""
        # Create article
        create_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        slug = create_response.json()["slug"]
        
        # Get article by slug
        response = await client.get(f"/api/v1/articles/slug/{slug}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == slug
    
    async def test_update_article(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test updating an article."""
        # Create article
        create_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = create_response.json()["id"]
        
        # Update article
        update_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = await client.put(
            f"/api/v1/articles/{article_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
    
    async def test_publish_article(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test publishing an article."""
        # Create article (draft by default)
        create_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = create_response.json()["id"]
        
        # Publish article
        response = await client.post(
            f"/api/v1/articles/{article_id}/publish",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "published"
    
    async def test_delete_article(
        self,
        client: AsyncClient,
        sample_article_data: dict,
        auth_headers: dict
    ):
        """Test deleting an article."""
        # Create article
        create_response = await client.post(
            "/api/v1/articles/",
            json=sample_article_data,
            headers=auth_headers
        )
        article_id = create_response.json()["id"]
        
        # Delete article
        response = await client.delete(
            f"/api/v1/articles/{article_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify article is deleted
        get_response = await client.get(f"/api/v1/articles/{article_id}")
        assert get_response.status_code == 404
