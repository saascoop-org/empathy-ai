from dataclasses import dataclass


SAFETY_POLICY_VERSION = "safety-policy-v1"


@dataclass(frozen=True)
class SafetyRule:
    category: str
    terms: tuple[str, ...]
    note: str
    severity: str = "warning"


SAFETY_RULES = (
    SafetyRule(
        category="diagnostic_framing",
        terms=("diagnosis", "diagnose", "disorder", "condition", "symptom"),
        note="Avoid diagnostic or clinical framing.",
    ),
    SafetyRule(
        category="clinical_labeling",
        terms=("autistic", "adhd", "narcissist", "psychopath", "trauma response"),
        note="Avoid clinical labeling of people.",
    ),
    SafetyRule(
        category="normalization",
        terms=("normal", "abnormal", "should behave", "proper way"),
        note="Avoid behavioral normalization.",
    ),
    SafetyRule(
        category="blame_assignment",
        terms=("right", "wrong", "fault", "blame", "guilty", "responsible for"),
        note="Avoid deciding who is right, wrong, or at fault.",
    ),
    SafetyRule(
        category="pathologizing_language",
        terms=("manipulative", "lazy", "crazy", "overreacting", "irrational"),
        note="Avoid stigmatizing, dismissive, or pathologizing language.",
    ),
    SafetyRule(
        category="harassment_or_abuse",
        terms=("harass", "harassment", "abuse", "abusive", "threat", "threatened"),
        note="Escalate sensitive conflict language instead of mediating as ordinary mismatch.",
        severity="high",
    ),
    SafetyRule(
        category="emotional_risk",
        terms=("self-harm", "suicide", "kill myself", "hurt myself", "unsafe"),
        note="Do not treat emotional risk as a routine communication mismatch.",
        severity="high",
    ),
    SafetyRule(
        category="out_of_scope",
        terms=("legal advice", "medical advice", "hr decision", "diagnose me"),
        note="Keep the tool inside communication support boundaries.",
        severity="high",
    ),
)


SAFETY_GUIDANCE = (
    "Frame outputs as possible interpretations, not diagnosis, fault, "
    "or behavioral normalization. For abuse, risk, legal, medical, or HR "
    "questions, state that the case needs appropriate human support."
)


def evaluate_safety(text: str):
    normalized = text.lower()
    findings = []

    for rule in SAFETY_RULES:
        matched_terms = [term for term in rule.terms if term in normalized]
        if matched_terms:
            findings.append(
                {
                    "category": rule.category,
                    "terms": matched_terms,
                    "note": rule.note,
                    "severity": rule.severity,
                }
            )

    return findings
