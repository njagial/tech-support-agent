# Settings Module
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    APP_NAME: str = "Pocket Tech Support Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Anthropic API
    ANTHROPIC_API_KEY: str = ""

    # Vector Database (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "tech_support_kb"

    # Database
    DATABASE_URL: str = "sqlite:///./tech_support.db"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]


def get_settings() -> Settings:
    return Settings()
