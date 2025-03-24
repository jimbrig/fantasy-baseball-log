import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings"""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fantasy Baseball API"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Database settings
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/db.sqlite"

    # Yahoo API settings
    YAHOO_CLIENT_ID: Optional[str] = None
    YAHOO_CLIENT_SECRET: Optional[str] = None
    YAHOO_REDIRECT_URI: Optional[str] = "oob"  # Out of band (default)

    # Data collection settings
    DATA_DIR: Path = BASE_DIR / "data"
    JSON_DATA_DIR: Path = DATA_DIR / "json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure data directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.JSON_DATA_DIR, exist_ok=True)
