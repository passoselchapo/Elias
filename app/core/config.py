
"""
app/core/config.py

Central configuration loader. Reads .env and exposes relevant settings.
"""

from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:////content/Elias/sql_app_new.db")

    # FastAPI settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
