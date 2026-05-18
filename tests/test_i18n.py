from empathy_engine.config import AppSettings
from empathy_engine.i18n.language import (
    TRANSLATIONS,
    detect_language_from_accept_language,
    detect_language_from_locale,
    detect_language_from_timezone,
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


def test_locale_detection_supports_browser_language_tags():
    assert detect_language_from_locale("pt-BR") == "pt-BR"
    assert detect_language_from_locale("pt_BR") == "pt-BR"
    assert detect_language_from_locale("es-AR") == "es"
    assert detect_language_from_locale("en-US") == "en"
    assert detect_language_from_locale("fr-FR") is None


def test_accept_language_detection_uses_first_supported_language():
    assert (
        detect_language_from_accept_language("pt-BR,pt;q=0.9,en-US;q=0.8")
        == "pt-BR"
    )
    assert (
        detect_language_from_accept_language("fr-FR,es;q=0.9,en;q=0.8")
        == "es"
    )
    assert detect_language_from_accept_language("fr-FR,de;q=0.9") is None


def test_timezone_detection_supports_local_demo_regions():
    assert detect_language_from_timezone("America/Sao_Paulo") == "pt-BR"
    assert detect_language_from_timezone("America/Argentina/Buenos_Aires") == "es"
    assert detect_language_from_timezone("America/New_York") == "en"
    assert detect_language_from_timezone("Asia/Tokyo") is None


def test_language_detection_supports_pt_br_en_and_es():
    assert detect_user_language("Meu colega achou minha mensagem grosseira.") == "pt-BR"
    assert detect_user_language("Mi colega pensó que mi mensaje fue grosero.") == "es"
    assert detect_user_language("My coworker thought my message was rude.") == "en"


def test_translation_coverage_and_fallback_to_english():
    assert validate_translation_coverage() == {}
    assert translate("unknown", "analyze") == "Analyze Interaction"
    assert translate("pt-BR", "missing_test_key") == "missing_test_key"

    removed = TRANSLATIONS["es"].pop("analyze")
    try:
        assert translate("es", "analyze") == "Analyze Interaction"
    finally:
        TRANSLATIONS["es"]["analyze"] = removed


def test_pt_br_interface_uses_accented_copy():
    assert translate("pt-BR", "demo_scenario_heading") == "Cenário de demo"
    assert translate("pt-BR", "demo_scenario_select") == "Cenário"
    assert translate("pt-BR", "alterity_user_profile") == "Seu perfil de comunicação"
    assert translate("pt-BR", "step_context_factors") == "Etapa 3 - Situação e apoios"
    assert translate("pt-BR", "audio_input_label") == "Desabafar via áudio"
    assert translate("pt-BR", "learning_diary_search") == "Buscar no diário"
    assert translate("pt-BR", "save_to_diary_heading") == "Diário e feedback"


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


def test_localize_workflow_result_translates_dynamic_project_context():
    workflow = EmpathyWorkflow()
    result = workflow.run(
        "minha colega passa informacoes do projeto de forma confusa e desorganizada",
        output_language="pt-BR",
    )

    localized = localize_workflow_result(result, "pt-BR")

    assert "informações de projeto" in localized["context"]["interaction_summary"]
    assert "detalhes do projeto" in localized["translation"]["translation_for_user"]
    assert "Qual informação do projeto" in localized["learning"]["reflection_question"]


def test_app_settings_normalizes_languages():
    settings = AppSettings(
        ollama_base_url="http://localhost:11434",
        gemma_model="gemma3:1b",
        default_ui_language="pt",
        processing_language="EN",
    )

    assert settings.default_ui_language == "pt-BR"
    assert settings.processing_language == "en"
