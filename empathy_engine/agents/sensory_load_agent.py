from empathy_engine.schemas import SensoryLoadResult


class SensoryLoadAgent:

    def run(self, interaction: str) -> SensoryLoadResult:
        return SensoryLoadResult(
            possible_factors=[
                "noise",
                "time pressure"
            ]
        )
