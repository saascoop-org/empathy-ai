from empathy_engine.presentation.demo_scenarios import (
    demo_scenario_options,
    get_demo_scenario,
)


REQUIRED_FIELDS = {
    "label",
    "user_profile",
    "other_profile",
    "context_factors",
    "repair_supports",
    "interaction",
}


def test_demo_scenarios_exist_for_supported_languages():
    for language in ("pt-BR", "en", "es"):
        options = demo_scenario_options(language)

        assert options
        for scenario_id, label in options:
            scenario = get_demo_scenario(scenario_id, language)
            assert label == scenario["label"]
            assert REQUIRED_FIELDS <= set(scenario)
            assert all(scenario[field] for field in REQUIRED_FIELDS)


def test_pt_br_demo_scenarios_use_accented_copy():
    scenario = get_demo_scenario("project_clarity", "pt-BR")

    assert scenario["label"] == "Projeto com informações confusas"
    assert "informações organizadas" in scenario["user_profile"]
    assert "pressão" in scenario["other_profile"]
    assert "responsáveis" in scenario["repair_supports"]
    assert "está passando informações" in scenario["interaction"]
