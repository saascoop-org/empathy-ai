from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.agents.context_decoder import ContextDecoderAgent
from empathy_engine.agents.double_empathy_analyzer import DoubleEmpathyAnalyzerAgent
from empathy_engine.agents.learning_coach import LearningCoachAgent
from empathy_engine.agents.perspective_translator import PerspectiveTranslatorAgent
from empathy_engine.agents.response_composer import ResponseComposerAgent
from empathy_engine.agents.sensory_load_agent import SensoryLoadAgent
from empathy_engine.orchestration.workflow import EmpathyWorkflow

from tests.helpers import build_response_input


def test_workflow_runs_full_pipeline():
    workflow = EmpathyWorkflow()

    result = workflow.run("My coworker thought I was rude.")

    assert set(result) == {
        "interaction",
        "language",
        "context",
        "analysis",
        "translation",
        "sensory_load",
        "safety",
        "response",
        "learning",
        "execution",
    }
    assert result["language"]["processing_language"] == "en"
    assert result["language"]["output_language"] == "en"
    assert result["response"]["bridge_message"]
    assert result["learning"]["reflection_question"]
    assert result["execution"]["total_duration_ms"] >= 0
    assert {
        step["name"] for step in result["execution"]["steps"]
    } == {
        "detect_language",
        "anonymize",
        "context_decoder",
        "double_empathy_analyzer",
        "perspective_translator",
        "sensory_load",
        "bias_safety",
        "response_composer",
        "learning_coach",
    }


def test_workflow_keeps_processing_english_and_sets_output_language():
    workflow = EmpathyWorkflow()

    result = workflow.run(
        "Meu colega achou minha mensagem grosseira.",
        output_language="pt-BR",
    )

    assert result["language"]["user_language"] == "pt-BR"
    assert result["language"]["processing_language"] == "en"
    assert result["language"]["output_language"] == "pt-BR"
    assert "Esclareça" in result["response"]["bridge_message"]


def test_agents_return_expected_contracts():
    context = ContextDecoderAgent().run("A direct message was misunderstood.")
    analysis = DoubleEmpathyAnalyzerAgent().run(context)
    translation = PerspectiveTranslatorAgent().run(analysis)
    sensory_load = SensoryLoadAgent().run("A noisy meeting felt rushed.")
    safety = BiasSafetyAgent().run(translation)
    response = ResponseComposerAgent().run(build_response_input())
    learning = LearningCoachAgent().run({"response": response})

    assert context.literal_language
    assert analysis.gap_type
    assert translation.translation_for_user
    assert sensory_load.possible_factors
    assert safety.safe
    assert response.bridge_message
    assert learning.reflection_question
