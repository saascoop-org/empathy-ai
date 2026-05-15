from empathy_engine.schemas import LearningResult


class LearningCoachAgent:

    def run(self, interaction) -> LearningResult:
        return LearningResult(
            reflection_question=(
                "What assumptions existed in this interaction?"
            )
        )
