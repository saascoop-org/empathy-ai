class ResponseComposerAgent:

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def run(self, payload: dict) -> dict:
        fallback = {
            "bridge_message": (
                "Clarify intention, name the possible mismatch, and ask what "
                "would make the exchange easier for both people."
            )
        }

        if not self.llm_client:
            return fallback

        prompt = (
            "Compose a concise, non-diagnostic empathy bridge from this "
            "analysis. Do not decide who is right or wrong. Do not tell one "
            "person to change their communication style as if it is the only "
            "problem. Return a neutral, practical bridge that supports mutual "
            f"clarification in plain language.\n\nAnalysis:\n{payload}"
        )

        try:
            bridge_message = self.llm_client.generate(prompt).strip()
        except Exception:
            return {
                **fallback,
                "llm_status": "unavailable"
            }

        if not bridge_message:
            return {
                **fallback,
                "llm_status": "empty_response"
            }

        return {
            "bridge_message": bridge_message,
            "llm_status": "ok"
        }
