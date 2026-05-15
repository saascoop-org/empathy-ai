from empathy_engine.orchestration.workflow import EmpathyWorkflow


ACCEPTANCE_SCENARIOS = [
    {
        "name": "direct communication perceived as rude",
        "text": "My coworker thought my short message was rude.",
        "output_language": "en",
    },
    {
        "name": "sensory or time pressure mismatch",
        "text": "The meeting was noisy and rushed, so I answered briefly.",
        "output_language": "en",
    },
    {
        "name": "sensitive data is anonymized",
        "text": (
            "Maria Silva emailed maria@example.com, called +55 11 99999-9999, "
            "shared CPF 123.456.789-10, and met at Rua das Flores 123."
        ),
        "output_language": "en",
    },
    {
        "name": "portuguese output",
        "text": "Meu colega achou minha mensagem grosseira.",
        "output_language": "pt-BR",
    },
    {
        "name": "spanish output",
        "text": "Mi colega pensó que mi mensaje fue grosero.",
        "output_language": "es",
    },
]


def test_acceptance_matrix():
    workflow = EmpathyWorkflow(use_llm=False)

    for scenario in ACCEPTANCE_SCENARIOS:
        result = workflow.run(
            scenario["text"],
            output_language=scenario["output_language"],
        )

        assert result["response"]["bridge_message"], scenario["name"]
        assert result["translation"]["translation_for_user"], scenario["name"]
        assert result["language"]["processing_language"] == "en"
        assert result["language"]["output_language"] == scenario["output_language"]

    anonymized = workflow.run(ACCEPTANCE_SCENARIOS[2]["text"])["interaction"]
    assert "maria@example.com" not in anonymized
    assert "+55 11 99999-9999" not in anonymized
    assert "123.456.789-10" not in anonymized
