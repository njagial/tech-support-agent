# Configuration Module
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    # API Settings
    APP_NAME: str = "Pocket Tech Support Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)

    # Anthropic API
    ANTHROPIC_API_KEY: str = Field(default="")

    # Vector Database (Qdrant)
    QDRANT_URL: str = Field(default="http://localhost:6333")
    QDRANT_COLLECTION_NAME: str = Field(default="tech_support_kb")

    # CORS
    CORS_ORIGINS: list = Field(default=["*"])

    # LLM Model Settings
    PRIMARY_MODEL: str = Field(default="claude-3-5-sonnet-20241022")
    FAST_MODEL: str = Field(default="claude-3-5-haiku-20241022")
    MAX_TOKENS: int = Field(default=4096)

    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    return Settings()
