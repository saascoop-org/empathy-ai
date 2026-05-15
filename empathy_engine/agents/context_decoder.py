from empathy_engine.schemas import ContextResult


class ContextDecoderAgent:

    def run(self, interaction: str) -> ContextResult:
        return ContextResult(
            literal_language=True,
            ambiguity_level="medium"
        )
