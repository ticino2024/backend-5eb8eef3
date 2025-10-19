"""Application configuration."""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = Field(default="Blog Platform API", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="production", description="Environment")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # Database
    DATABASE_URL: str = Field(..., description="Database connection URL")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    
    # Security
    SECRET_KEY: str = Field(..., description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Token expiration")
    
    # CORS
    ALLOWED_ORIGINS: str = Field(default="*", description="Allowed origins for CORS")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get list of allowed origins."""
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
