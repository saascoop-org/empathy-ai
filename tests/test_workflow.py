from empathy_engine.orchestration.workflow import EmpathyWorkflow
from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.agents.context_decoder import ContextDecoderAgent
from empathy_engine.agents.double_empathy_analyzer import DoubleEmpathyAnalyzerAgent
from empathy_engine.agents.learning_coach import LearningCoachAgent
from empathy_engine.agents.perspective_translator import PerspectiveTranslatorAgent
from empathy_engine.agents.response_composer import ResponseComposerAgent
from empathy_engine.agents.sensory_load_agent import SensoryLoadAgent
from empathy_engine.safety.anonymizer import Anonymizer
from empathy_engine.storage.interaction_store import InteractionStore


def test_workflow():

    workflow = EmpathyWorkflow()

    result = workflow.run(
        "My coworker thought I was rude."
    )

    assert "translation" in result


def test_workflow_runs_full_pipeline():
    workflow = EmpathyWorkflow()

    result = workflow.run("My coworker thought I was rude.")

    assert set(result) == {
        "interaction",
        "context",
        "analysis",
        "translation",
        "sensory_load",
        "safety",
        "response",
        "learning",
    }
    assert "bridge_message" in result["response"]
    assert "reflection_question" in result["learning"]


def test_anonymizer_removes_common_sensitive_data():
    anonymizer = Anonymizer()

    result = anonymizer.anonymize(
        "Maria Silva emailed maria@example.com, called +55 11 99999-9999, "
        "shared CPF 123.456.789-10, and met at Rua das Flores 123."
    )

    assert "Maria" not in result
    assert "maria@example.com" not in result
    assert "+55 11 99999-9999" not in result
    assert "123.456.789-10" not in result
    assert "Rua das Flores" not in result
    assert "[PERSON]" in result
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "[NATIONAL_ID]" in result
    assert "[ADDRESS]" in result


def test_response_composer_falls_back_when_llm_fails():
    class FailingClient:

        def generate(self, prompt):
            raise RuntimeError("model unavailable")

    result = ResponseComposerAgent(FailingClient()).run({"analysis": "test"})

    assert result["llm_status"] == "unavailable"
    assert "bridge_message" in result


def test_bias_safety_flags_pathologizing_language():
    result = BiasSafetyAgent().run(
        {"message": "The other person is wrong, lazy, and overreacting."}
    )

    assert not result["safe"]
    assert "wrong" in result["removed_terms"]
    assert "lazy" in result["removed_terms"]
    assert "overreacting" in result["removed_terms"]


def test_interaction_store_persists_anonymized_result(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)

    record_id = store.save(
        "[PERSON] asked for clarification.",
        {"response": {"bridge_message": "Ask what would help."}},
        "Useful and safe",
    )

    assert record_id == 1
    assert db_path.exists()


def test_agents_return_expected_contracts():
    context = ContextDecoderAgent().run("A direct message was misunderstood.")
    analysis = DoubleEmpathyAnalyzerAgent().run(context)
    translation = PerspectiveTranslatorAgent().run(analysis)
    sensory_load = SensoryLoadAgent().run("A noisy meeting felt rushed.")
    safety = BiasSafetyAgent().run(translation)
    response = ResponseComposerAgent().run({"translation": translation})
    learning = LearningCoachAgent().run({"response": response})

    assert "literal_language" in context
    assert "gap_type" in analysis
    assert "translation_for_user" in translation
    assert "possible_factors" in sensory_load
    assert "safe" in safety
    assert "bridge_message" in response
    assert "reflection_question" in learning
