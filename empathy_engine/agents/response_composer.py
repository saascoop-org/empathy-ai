from empathy_engine.i18n.language import (
    is_likely_language,
    output_language_name,
    translate_output_text,
)
from empathy_engine.schemas import ResponseComposerInput, ResponseResult, to_plain_data


class ResponseComposerAgent:

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def run(self, payload: ResponseComposerInput) -> ResponseResult:
        payload_data = to_plain_data(payload)
        processing_language = payload.processing_language
        output_language = payload.output_language
        fallback = ResponseResult(
            bridge_message=translate_output_text(
                (
                    "Clarify intention, name the possible mismatch, and ask what "
                    "would make the exchange easier for both people."
                ),
                output_language,
            )
        )

        if not self.llm_client:
            return fallback

        prompt = (
            "Compose a concise, non-diagnostic empathy bridge from this "
            "analysis. Do not decide who is right or wrong. Do not tell one "
            "person to change their communication style as if it is the only "
            "problem. Return a neutral, practical bridge that supports mutual "
            "clarification in plain language. Process the analysis in English "
            f"because the configured processing language is {processing_language}. "
            "Translate only the final bridge for presentation, and write that "
            f"final bridge in {output_language_name(output_language)}."
            f"\n\nAnalysis:\n{payload_data}"
        )

        try:
            bridge_message = self.llm_client.generate(prompt).strip()
        except Exception:
            return fallback.model_copy(update={"llm_status": "unavailable"})

        if not bridge_message:
            return fallback.model_copy(update={"llm_status": "empty_response"})

        if not is_likely_language(bridge_message, output_language):
            return fallback.model_copy(update={"llm_status": "language_mismatch_fallback"})

        return ResponseResult(
            bridge_message=bridge_message,
            llm_status="ok"
        )
