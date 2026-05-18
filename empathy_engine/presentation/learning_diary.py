import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from empathy_engine.i18n.language import normalize_language, translate
from empathy_engine.schemas import FeedbackValue


LANGUAGE_SECTION_LABELS = {
    "pt-BR": ("Brazilian Portuguese", "Portuguese", "PT-BR"),
    "es": ("Spanish", "ES"),
    "en": ("English", "EN"),
}


def extract_diary_interaction(anonymized_interaction: str) -> str:
    text = (anonymized_interaction or "").strip()
    if not text:
        return ""

    marker_match = re.search(
        r"(?:interaction|\[person\])\s+to\s+analy[sz]e:\s*",
        text,
        flags=re.IGNORECASE,
    )
    if marker_match:
        return _clean_anonymized_display(text[marker_match.end():])

    return _clean_anonymized_display(text)


def display_bridge_for_language(bridge_message: str | None, language: str | None) -> str:
    text = (bridge_message or "").strip()
    if not text:
        return ""

    normalized = normalize_language(language)
    labels = LANGUAGE_SECTION_LABELS.get(normalized, ())

    for label in labels:
        pattern = rf"{re.escape(label)}(?:\s+translation)?\s*:\s*"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            section = text[match.end():].strip()
            return _clean_bridge_text(_trim_next_language_section(section))

    return _clean_bridge_text(text)


def display_feedback_for_language(feedback: str | None, language: str | None) -> str:
    if not feedback:
        return translate(language or "en", "no_feedback")

    options = translate(language or "en", "feedback_options")
    localized_feedback = {
        FeedbackValue.USEFUL_SAFE: options[0],
        FeedbackValue.PARTIALLY_USEFUL: options[1],
        FeedbackValue.NOT_USEFUL: options[2],
    }

    return localized_feedback.get(feedback, feedback)


def diary_entry_title(
    anonymized_interaction: str,
    created_at: str | None,
    language: str | None,
    timezone: str | None = None,
) -> str:
    interaction = extract_diary_interaction(anonymized_interaction)
    summary = _summarize_interaction(interaction)
    date = _format_created_at(created_at, language, timezone)

    if date:
        return f"{summary} - {date}"
    return summary


def _trim_next_language_section(text: str) -> str:
    labels = [
        label
        for language_labels in LANGUAGE_SECTION_LABELS.values()
        for label in language_labels
    ]
    pattern = (
        r"\n\s*(?:"
        + "|".join(re.escape(label) for label in labels)
        + r")(?:\s+translation)?\s*:"
    )
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return text[:match.start()].strip()
    return text.strip()


def _clean_bridge_text(text: str) -> str:
    cleaned = (text or "").strip()
    cleaned = re.sub(r"^\*+\s*", "", cleaned)
    cleaned = re.sub(r"\s*\*+$", "", cleaned)
    cleaned = re.sub(r"^\s*-{3,}\s*", "", cleaned)
    return cleaned.strip()


def _clean_anonymized_display(text: str) -> str:
    return re.sub(r"\[PERSON\]\s*", "", (text or "")).strip()


def _summarize_interaction(interaction: str) -> str:
    text = " ".join((interaction or "").split())
    if not text:
        return "Registro do diário"

    text = re.sub(r"^\[PERSON\]\s+", "", text, flags=re.IGNORECASE)
    max_length = 64
    if len(text) <= max_length:
        return text
    return f"{text[:max_length].rstrip()}..."


def _format_created_at(
    created_at: str | None,
    language: str | None,
    timezone: str | None,
) -> str:
    if not created_at:
        return ""

    try:
        parsed = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return ""

    if timezone:
        try:
            parsed = parsed.astimezone(ZoneInfo(timezone))
        except ZoneInfoNotFoundError:
            pass

    normalized = normalize_language(language)
    if normalized == "en":
        return parsed.strftime("%Y-%m-%d %H:%M")
    return parsed.strftime("%d/%m/%Y %H:%M")
