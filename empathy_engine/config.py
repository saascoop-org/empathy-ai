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
    )
