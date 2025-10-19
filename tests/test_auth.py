"""Authentication endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuth:
    """Test authentication endpoints."""
    
    async def test_register_user(self, client: AsyncClient, sample_user_data: dict):
        """Test user registration."""
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["access_token"] is not None
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == sample_user_data["email"]
        assert data["user"]["name"] == sample_user_data["name"]
        assert "id" in data["user"]
    
    async def test_register_duplicate_email(self, client: AsyncClient, sample_user_data: dict):
        """Test registering with duplicate email returns 409."""
        # Register first user
        await client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Try to register second user with same email
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        assert response.status_code == 409
    
    async def test_register_invalid_password(self, client: AsyncClient):
        """Test registration with weak password fails."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "weak"  # Too short and no special chars
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
    
    async def test_login_success(self, client: AsyncClient, sample_user_data: dict):
        """Test successful login."""
        # Register user
        await client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] is not None
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == sample_user_data["email"]
    
    async def test_login_invalid_credentials(self, client: AsyncClient, sample_user_data: dict):
        """Test login with invalid credentials."""
        # Register user
        await client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Try to login with wrong password
        login_data = {
            "email": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "Password123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
