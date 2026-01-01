"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://hexahub:hexahub_password@localhost:5432/hexahub"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Authentik OAuth
    AUTHENTIK_URL: str = "https://auth.hexahub.local"
    AUTHENTIK_CLIENT_ID: str = ""
    AUTHENTIK_CLIENT_SECRET: str = ""
    AUTHENTIK_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Environment
    ENVIRONMENT: str = "development"

    # App Info
    APP_NAME: str = "HexaHub API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Self-hosted AI workspace for developers"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
