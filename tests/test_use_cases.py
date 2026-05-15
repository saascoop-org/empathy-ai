from empathy_engine.storage.interaction_store import InteractionStore
from empathy_engine.use_cases.analyze_interaction import (
    AnalyzeInteractionCommand,
    AnalyzeInteractionUseCase,
)


def test_analyze_interaction_use_case_localizes_without_persisting(tmp_path):
    store = InteractionStore(tmp_path / "interactions.sqlite3")
    use_case = AnalyzeInteractionUseCase(store=store)

    result = use_case.execute(
        AnalyzeInteractionCommand(
            interaction="My coworker thought my message was rude.",
            output_language="es",
            store_consent=False,
            use_llm=False,
        )
    )

    assert result.stored_record_id is None
    assert not (tmp_path / "interactions.sqlite3").exists()
    assert result.workflow_result["language"]["processing_language"] == "en"
    assert result.display_result["output_language"] == "es"
    assert "señales emocionales" in (
        result.display_result["translation"]["translation_for_user"]
    )


def test_analyze_interaction_use_case_persists_when_consented(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)
    use_case = AnalyzeInteractionUseCase(store=store)

    result = use_case.execute(
        AnalyzeInteractionCommand(
            interaction="Maria Silva emailed maria@example.com.",
            output_language="en",
            store_consent=True,
            feedback="Useful and safe",
            use_llm=False,
        )
    )

    assert result.stored_record_id == 1
    assert db_path.exists()
    assert "Maria" not in result.workflow_result["interaction"]
    assert "maria@example.com" not in result.workflow_result["interaction"]
