from pathlib import Path

import pytest

from empathy_engine.config import AppSettings, load_settings


def test_session_timeout_settings_have_safe_defaults():
    settings = AppSettings()

    assert settings.session_timeout_ms == 180_000
    assert settings.session_timeout_warning_ms == 150_000
    assert settings.session_expired_url.endswith("/session-expired.html")


def test_session_timeout_settings_load_from_environment(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("GEMMA_MODEL", "gemma3:1b")
    monkeypatch.setenv("INTERACTION_DB_PATH", "data/interactions.sqlite3")
    monkeypatch.setenv("DEFAULT_UI_LANGUAGE", "en")
    monkeypatch.setenv("PROCESSING_LANGUAGE", "en")
    monkeypatch.setenv("SESSION_TIMEOUT_MS", "240000")
    monkeypatch.setenv("SESSION_TIMEOUT_WARNING_MS", "210000")
    monkeypatch.setenv("SESSION_EXPIRED_URL", "https://example.test/expired")

    settings = load_settings()

    assert settings.session_timeout_ms == 240_000
    assert settings.session_timeout_warning_ms == 210_000
    assert settings.session_expired_url == "https://example.test/expired"
    assert settings.interaction_db_path == Path("data/interactions.sqlite3")


def test_session_timeout_settings_reject_invalid_values():
    with pytest.raises(ValueError):
        AppSettings(session_timeout_ms=0)

    with pytest.raises(ValueError):
        AppSettings(session_timeout_warning_ms=-1)

    with pytest.raises(ValueError):
        AppSettings(session_expired_url=" ")
