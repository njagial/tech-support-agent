# Settings Module
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
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
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    return Settings()
