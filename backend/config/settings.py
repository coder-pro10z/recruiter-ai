from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

# Resolve .env — works whether uvicorn is run from backend/ or the project root
_HERE = Path(__file__).resolve().parent.parent  # backend/
_ROOT = _HERE.parent                             # project root
_ENV_FILE = str(_HERE / ".env") if (_HERE / ".env").exists() else str(_ROOT / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://localhost/jobfinder"
    supabase_url: str = ""
    supabase_anon_key: str = ""

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Apollo
    apollo_api_key: str = ""

    # Hunter
    hunter_api_key: str = ""

    # Gmail
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_refresh_token: str = ""
    gmail_from_address: str = ""

    # Notion
    notion_api_key: str = ""
    notion_database_id: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # Application
    app_env: str = "development"
    app_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    # Scheduler intervals (seconds)
    job_detection_interval: int = 300
    followup_check_interval: int = 3600
    mailtrack_check_interval: int = 1800


@lru_cache
def get_settings() -> Settings:
    return Settings()
