class ContextDecoderAgent:

    def run(self, interaction: str) -> dict:
        return {
            "literal_language": True,
            "ambiguity_level": "medium"
        }
