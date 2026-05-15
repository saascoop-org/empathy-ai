import re


class Anonymizer:

    def anonymize(self, text: str):

        text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL]", text)
        text = re.sub(r"https?://\S+|www\.\S+", "[URL]", text)
        text = re.sub(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "[NATIONAL_ID]", text)
        text = re.sub(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b", "[NATIONAL_ID]", text)
        text = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[PHONE]", text)
        text = re.sub(r"\b(?:Rua|Avenida|Av\.|Alameda|Travessa)\s+[^,.]+", "[ADDRESS]", text)
        text = re.sub(r"\b(?:Slack|Teams|Discord|Telegram|WhatsApp):\s*\S+", "[HANDLE]", text)
        text = re.sub(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", "[PERSON]", text)
        text = re.sub(r"\b[A-Z][a-z]+\b", "[PERSON]", text)

        return text
