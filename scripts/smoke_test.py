import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from empathy_engine.orchestration.workflow import EmpathyWorkflow


SCENARIOS = [
    "My coworker thought my short message was rude, but I was trying to be clear.",
    "The meeting was noisy and rushed, so I answered briefly and the other person seemed upset.",
    (
        "Maria Silva emailed maria@example.com, called +55 11 99999-9999, "
        "shared CPF 123.456.789-10, and met at Rua das Flores 123."
    ),
]


def main():
    workflow = EmpathyWorkflow(use_llm=False)

    for index, scenario in enumerate(SCENARIOS, start=1):
        result = workflow.run(scenario)

        assert result["safety"]["safe"], f"Scenario {index} failed safety check"
        assert result["response"]["bridge_message"], f"Scenario {index} has no bridge"
        assert "translation_for_user" in result["translation"]

        if index == 3:
            anonymized = result["interaction"]
            assert "maria@example.com" not in anonymized
            assert "+55 11 99999-9999" not in anonymized
            assert "123.456.789-10" not in anonymized
            assert "Rua das Flores" not in anonymized

        print(f"scenario {index}: ok")


if __name__ == "__main__":
    main()
