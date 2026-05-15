from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from empathy_engine.config import load_settings
from empathy_engine.i18n.language import validate_translation_coverage
from empathy_engine.operations import get_local_runtime_status


def main():
    settings = load_settings()
    status = get_local_runtime_status(settings)
    db_parent = Path(settings.interaction_db_path).parent
    db_parent.mkdir(parents=True, exist_ok=True)

    missing_translations = validate_translation_coverage()
    if missing_translations:
        raise SystemExit(f"missing translations: {missing_translations}")

    print(f"model: {status.model}")
    print(f"ollama: {'available' if status.ollama_available else 'unavailable'}")
    print(f"processing_language: {status.processing_language}")
    print(f"default_ui_language: {settings.default_ui_language}")
    print(f"database_path: {status.database_path}")
    print("environment: ok")


if __name__ == "__main__":
    main()
