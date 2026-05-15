class DoubleEmpathyAnalyzerAgent:

    def run(self, context: dict) -> dict:
        return {
            "gap_type": "tone_expectation_mismatch",
            "possible_misinterpretation": (
                "Directness perceived as hostility"
            )
        }
