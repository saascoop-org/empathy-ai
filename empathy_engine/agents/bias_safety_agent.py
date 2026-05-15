from empathy_engine.safety.policy import SAFETY_GUIDANCE, evaluate_safety
from empathy_engine.schemas import SafetyResult, to_plain_data


class BiasSafetyAgent:

    def run(self, content) -> SafetyResult:
        text = str(to_plain_data(content)).lower()
        findings = evaluate_safety(text)
        removed_terms = sorted(
            {term for finding in findings for term in finding["terms"]}
        )
        safety_notes = sorted({finding["note"] for finding in findings})

        return SafetyResult(
            safe=not removed_terms,
            removed_terms=removed_terms,
            safety_notes=safety_notes,
            guidance=SAFETY_GUIDANCE,
        )
