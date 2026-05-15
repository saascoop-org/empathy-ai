from empathy_engine.agents.response_composer import ResponseComposerAgent

from tests.helpers import build_response_input


def test_response_composer_falls_back_when_llm_unavailable():
    class FailingClient:

        def generate(self, prompt):
            raise RuntimeError("model unavailable")

    result = ResponseComposerAgent(FailingClient()).run(build_response_input())

    assert result.llm_status == "unavailable"
    assert result.bridge_message


def test_response_composer_falls_back_when_llm_times_out():
    class TimeoutClient:

        def generate(self, prompt):
            raise TimeoutError("timeout")

    result = ResponseComposerAgent(TimeoutClient()).run(build_response_input())

    assert result.llm_status == "unavailable"
    assert result.bridge_message


def test_response_composer_falls_back_when_llm_returns_empty_output():
    class EmptyClient:

        def generate(self, prompt):
            return "   "

    result = ResponseComposerAgent(EmptyClient()).run(build_response_input())

    assert result.llm_status == "empty_response"
    assert result.bridge_message


def test_response_composer_falls_back_when_model_missing():
    class MissingModelClient:

        def generate(self, prompt):
            raise RuntimeError("model not found")

    result = ResponseComposerAgent(MissingModelClient()).run(build_response_input())

    assert result.llm_status == "unavailable"
    assert result.bridge_message


def test_response_composer_falls_back_when_llm_uses_wrong_language():
    class EnglishClient:

        def generate(self, prompt):
            return "Clarify the intention and ask what would help both people."

    result = ResponseComposerAgent(EnglishClient()).run(
        build_response_input(output_language="es")
    )

    assert result.llm_status == "language_mismatch_fallback"
    assert "Aclara" in result.bridge_message
