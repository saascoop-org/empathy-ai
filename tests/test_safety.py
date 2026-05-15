import logging

from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.safety.logging import RedactingFormatter
from empathy_engine.safety.policy import SAFETY_POLICY_VERSION, evaluate_safety


def test_bias_safety_flags_pathologizing_language():
    result = BiasSafetyAgent().run(
        {"message": "The other person is wrong, lazy, and overreacting."}
    )

    assert not result.safe
    assert "wrong" in result.removed_terms
    assert "lazy" in result.removed_terms
    assert "overreacting" in result.removed_terms


def test_safety_policy_flags_required_categories():
    findings = evaluate_safety(
        "Give legal advice because this abusive coworker is wrong, abnormal, "
        "manipulative, and might self-harm."
    )
    categories = {finding["category"] for finding in findings}

    assert SAFETY_POLICY_VERSION == "safety-policy-v1"
    assert "out_of_scope" in categories
    assert "harassment_or_abuse" in categories
    assert "blame_assignment" in categories
    assert "normalization" in categories
    assert "pathologizing_language" in categories
    assert "emotional_risk" in categories


def test_bias_safety_flags_high_risk_and_out_of_scope_language():
    result = BiasSafetyAgent().run(
        {
            "message": (
                "I need legal advice about an abusive threat and medical advice "
                "to diagnose me."
            )
        }
    )

    assert not result.safe
    assert "legal advice" in result.removed_terms
    assert "abusive" in result.removed_terms
    assert "threat" in result.removed_terms
    assert "medical advice" in result.removed_terms
    assert "diagnose" in result.removed_terms


def test_safe_logging_formatter_redacts_sensitive_text():
    record = logging.LogRecord(
        name="empathy_engine.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Maria Silva emailed maria@example.com",
        args=(),
        exc_info=None,
    )

    formatted = RedactingFormatter("%(message)s").format(record)

    assert "Maria" not in formatted
    assert "maria@example.com" not in formatted
    assert "[PERSON]" in formatted
    assert "[EMAIL]" in formatted


def test_structured_log_event_is_redacted():
    logger = logging.getLogger("empathy_engine.test")
    record = logging.LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='{"event": "workflow_completed", "note": "Maria maria@example.com"}',
        args=(),
        exc_info=None,
    )

    formatted = RedactingFormatter("%(message)s").format(record)

    assert "workflow_completed" in formatted
    assert "Maria" not in formatted
    assert "maria@example.com" not in formatted
