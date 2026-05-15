from empathy_engine.schemas import DoubleEmpathyAnalysis


class DoubleEmpathyAnalyzerAgent:

    def run(self, context) -> DoubleEmpathyAnalysis:
        return DoubleEmpathyAnalysis(
            gap_type="tone_expectation_mismatch",
            possible_misinterpretation=(
                "Directness perceived as hostility"
            )
        )
