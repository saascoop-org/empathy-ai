from empathy_engine.config import AppSettings
from empathy_engine.i18n.language import (
    TRANSLATIONS,
    detect_user_language,
    is_likely_language,
    localize_workflow_result,
    normalize_language,
    translate,
    validate_translation_coverage,
)
from empathy_engine.orchestration.workflow import EmpathyWorkflow


def test_language_detection_defaults_to_english():
    assert detect_user_language("") == "en"
    assert detect_user_language("???") == "en"
    assert normalize_language("unknown") == "en"


def test_language_detection_supports_pt_br_en_and_es():
    assert detect_user_language("Meu colega achou minha mensagem grosseira.") == "pt-BR"
    assert detect_user_language("Mi colega pensó que mi mensaje fue grosero.") == "es"
    assert detect_user_language("My coworker thought my message was rude.") == "en"


def test_translation_coverage_and_fallback_to_english():
    assert validate_translation_coverage() == {}
    assert translate("unknown", "analyze") == "Analyze Interaction"

    removed = TRANSLATIONS["es"].pop("analyze")
    try:
        assert translate("es", "analyze") == "Analyze Interaction"
    finally:
        TRANSLATIONS["es"]["analyze"] = removed


def test_output_language_validation():
    assert is_likely_language("Aclara la intención y pregunta qué ayudaría.", "es")
    assert is_likely_language("Esclareça a intenção e pergunte o que ajudaria.", "pt-BR")
    assert not is_likely_language("Clarify the intention and ask what would help.", "es")


def test_localize_workflow_result_translates_display_fields():
    workflow = EmpathyWorkflow()
    result = workflow.run("My coworker thought my message was rude.")

    localized = localize_workflow_result(result, "es")

    assert localized["output_language"] == "es"
    assert "señales emocionales" in localized["translation"]["translation_for_user"]
    assert "¿Qué supuestos" in localized["learning"]["reflection_question"]


def test_app_settings_normalizes_languages():
    settings = AppSettings(
        ollama_base_url="http://localhost:11434",
        gemma_model="gemma3:1b",
        default_ui_language="pt",
        processing_language="EN",
    )

    assert settings.default_ui_language == "pt-BR"
    assert settings.processing_language == "en"
