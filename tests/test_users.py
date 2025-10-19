"""User endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUsers:
    """Test user endpoints."""
    
    async def test_get_current_user(
        self,
        client: AsyncClient,
        authenticated_user: dict,
        auth_headers: dict
    ):
        """Test getting current user profile."""
        response = await client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == authenticated_user["user"]["email"]
        assert data["id"] == authenticated_user["user"]["id"]
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/v1/users/me")
        assert response.status_code == 403  # No auth header
    
    async def test_update_current_user(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test updating current user profile."""
        update_data = {
            "name": "Updated Name"
        }
        response = await client.put(
            "/api/v1/users/me",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
    
    async def test_get_user_by_id(
        self,
        client: AsyncClient,
        authenticated_user: dict
    ):
        """Test getting user by ID."""
        user_id = authenticated_user["user"]["id"]
        response = await client.get(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
    
    async def test_get_nonexistent_user(self, client: AsyncClient):
        """Test getting non-existent user returns 404."""
        response = await client.get("/api/v1/users/nonexistent-id")
        assert response.status_code == 404
