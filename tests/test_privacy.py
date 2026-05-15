from empathy_engine.safety.anonymizer import Anonymizer


def test_anonymizer_removes_common_sensitive_data():
    anonymizer = Anonymizer()

    result = anonymizer.anonymize(
        "Maria Silva emailed maria@example.com, called +55 11 99999-9999, "
        "shared CPF 123.456.789-10, and met at Rua das Flores 123."
    )

    assert "Maria" not in result
    assert "maria@example.com" not in result
    assert "+55 11 99999-9999" not in result
    assert "123.456.789-10" not in result
    assert "Rua das Flores" not in result
    assert "[PERSON]" in result
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "[NATIONAL_ID]" in result
    assert "[ADDRESS]" in result


def test_anonymizer_separates_processing_and_persistence():
    anonymizer = Anonymizer()
    text = "My coworker Maria Silva emailed maria@example.com."

    processing = anonymizer.anonymize_for_processing(text)
    persistence = anonymizer.anonymize_for_persistence(text)

    assert processing == persistence
    assert "My coworker" in processing
    assert "Maria" not in processing
    assert "maria@example.com" not in persistence
