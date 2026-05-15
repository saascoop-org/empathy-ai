class BiasSafetyAgent:

    def run(self, content: dict) -> dict:
        unsafe_terms = {
            "diagnosis": "Avoid diagnostic framing.",
            "diagnose": "Avoid diagnostic framing.",
            "disorder": "Avoid clinical labeling.",
            "normal": "Avoid normalization language.",
            "abnormal": "Avoid normalization language.",
            "right": "Avoid deciding who is right.",
            "wrong": "Avoid deciding who is wrong.",
            "fault": "Avoid assigning fault.",
            "blame": "Avoid assigning blame.",
            "manipulative": "Avoid pathologizing intent.",
            "lazy": "Avoid character judgments.",
            "crazy": "Avoid stigmatizing language.",
            "overreacting": "Avoid dismissive language.",
        }
        text = str(content).lower()
        removed_terms = [term for term in unsafe_terms if term in text]
        safety_notes = sorted({unsafe_terms[term] for term in removed_terms})

        return {
            "safe": not removed_terms,
            "removed_terms": removed_terms,
            "safety_notes": safety_notes,
            "guidance": (
                "Frame outputs as possible interpretations, not diagnosis, "
                "fault, or behavioral normalization."
            )
        }
