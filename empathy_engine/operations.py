from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import urlopen

from empathy_engine.config import AppSettings, load_settings


@dataclass(frozen=True)
class LocalRuntimeStatus:
    model: str
    ollama_base_url: str
    ollama_available: bool
    processing_language: str
    database_path: str


def check_ollama_available(settings: AppSettings, timeout=1.0) -> bool:
    try:
        with urlopen(f"{settings.ollama_base_url}/api/tags", timeout=timeout) as response:
            return 200 <= response.status < 500
    except (OSError, URLError, TimeoutError):
        return False


def get_local_runtime_status(settings: AppSettings | None = None) -> LocalRuntimeStatus:
    settings = settings or load_settings()
    return LocalRuntimeStatus(
        model=settings.gemma_model,
        ollama_base_url=settings.ollama_base_url,
        ollama_available=check_ollama_available(settings),
        processing_language=settings.processing_language,
        database_path=str(settings.interaction_db_path),
    )
