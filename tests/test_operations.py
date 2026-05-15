from pathlib import Path

from empathy_engine.config import AppSettings
from empathy_engine.operations import check_ollama_available, get_local_runtime_status


def test_check_ollama_available_returns_false_when_unreachable(monkeypatch):
    def raise_timeout(*args, **kwargs):
        raise TimeoutError("unreachable")

    monkeypatch.setattr("empathy_engine.operations.urlopen", raise_timeout)

    settings = AppSettings(ollama_base_url="http://localhost:11434")

    assert not check_ollama_available(settings, timeout=0.01)


def test_local_runtime_status_exposes_operational_fields(monkeypatch, tmp_path):
    monkeypatch.setattr("empathy_engine.operations.check_ollama_available", lambda _: True)
    settings = AppSettings(
        gemma_model="gemma3:1b",
        processing_language="en",
        interaction_db_path=tmp_path / "interactions.sqlite3",
    )

    status = get_local_runtime_status(settings)

    assert status.model == "gemma3:1b"
    assert status.ollama_available
    assert status.processing_language == "en"
    assert status.database_path == str(Path(tmp_path / "interactions.sqlite3"))
