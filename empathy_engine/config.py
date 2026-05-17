import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from empathy_engine.i18n.language import normalize_language


class AppSettings(BaseModel):
    ollama_base_url: str = "http://localhost:11434"
    gemma_model: str = "gemma3:1b"
    interaction_db_path: Path = Path("data") / "interactions.sqlite3"
    default_ui_language: str = "en"
    processing_language: str = "en"
    session_timeout_ms: int = 180_000
    session_timeout_warning_ms: int = 150_000
    session_expired_url: str = "/session-expired.html"
    demo_token_secret: str = ""
    demo_token_ttl_seconds: int = 300

    @field_validator("default_ui_language", "processing_language")
    @classmethod
    def validate_language(cls, value):
        return normalize_language(value)

    @field_validator("gemma_model")
    @classmethod
    def validate_model(cls, value):
        if not value or not value.strip():
            raise ValueError("GEMMA_MODEL must not be empty")
        return value.strip()

    @field_validator("ollama_base_url")
    @classmethod
    def validate_ollama_url(cls, value):
        if not value or not value.strip():
            raise ValueError("OLLAMA_BASE_URL must not be empty")
        return value.strip()

    @field_validator("session_timeout_ms", "session_timeout_warning_ms")
    @classmethod
    def validate_positive_timeout(cls, value):
        if value <= 0:
            raise ValueError("Session timeout values must be positive")
        return value

    @field_validator("demo_token_ttl_seconds")
    @classmethod
    def validate_demo_token_ttl(cls, value):
        if value <= 0:
            raise ValueError("DEMO_TOKEN_TTL_SECONDS must be positive")
        return value

    @field_validator("session_expired_url")
    @classmethod
    def validate_session_expired_url(cls, value):
        if not value or not value.strip():
            raise ValueError("SESSION_EXPIRED_URL must not be empty")
        return value.strip()


def load_settings() -> AppSettings:
    load_dotenv()
    return AppSettings(
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        gemma_model=os.getenv("GEMMA_MODEL", "gemma3:1b"),
        interaction_db_path=Path(
            os.getenv("INTERACTION_DB_PATH", "data/interactions.sqlite3")
        ),
        default_ui_language=os.getenv("DEFAULT_UI_LANGUAGE", "en"),
        processing_language=os.getenv("PROCESSING_LANGUAGE", "en"),
        session_timeout_ms=int(os.getenv("SESSION_TIMEOUT_MS", "180000")),
        session_timeout_warning_ms=int(
            os.getenv("SESSION_TIMEOUT_WARNING_MS", "150000")
        ),
        session_expired_url=os.getenv(
            "SESSION_EXPIRED_URL",
            "/session-expired.html",
        ),
        demo_token_secret=os.getenv("DEMO_TOKEN_SECRET", ""),
        demo_token_ttl_seconds=int(os.getenv("DEMO_TOKEN_TTL_SECONDS", "300")),
    )
