from empathy_engine.schemas import PerspectiveTranslation


class PerspectiveTranslatorAgent:

    def run(self, analysis) -> PerspectiveTranslation:
        return PerspectiveTranslation(
            translation_for_user=(
                "The other person may expect more emotional cues."
            ),
            translation_for_other_person=(
                "Direct language may reflect efficiency, not hostility."
            )
        )
