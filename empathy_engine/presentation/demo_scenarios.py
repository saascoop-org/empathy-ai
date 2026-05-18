from empathy_engine.i18n.language import normalize_language


DEMO_SCENARIOS = {
    "project_clarity": {
        "pt-BR": {
            "label": "Projeto com informações confusas",
            "user_profile": "Costumo ser direto e preciso de informações organizadas para agir.",
            "other_profile": "A outra pessoa pode estar respondendo sob pressão e sem perceber que faltam detalhes.",
            "context_factors": "Projeto atrasado, mensagens fragmentadas e expectativa de resposta rápida.",
            "repair_supports": "Pedir prioridades, responsáveis, prazo e próximo passo em uma lista curta.",
            "interaction": (
                "Minha colega de trabalho está passando informações sobre o projeto "
                "de forma confusa e desorganizada."
            ),
        },
        "en": {
            "label": "Project with unclear information",
            "user_profile": "I tend to be direct and need organized information before acting.",
            "other_profile": "The other person may be responding under pressure and may not notice which details are missing.",
            "context_factors": "Delayed project, fragmented messages, and expectation of a quick response.",
            "repair_supports": "Ask for priorities, owners, deadline, and next step in a short list.",
            "interaction": (
                "My coworker is sharing project information in a confusing and "
                "disorganized way."
            ),
        },
        "es": {
            "label": "Proyecto con informacion confusa",
            "user_profile": "Suelo ser directo y necesito informacion organizada antes de actuar.",
            "other_profile": "La otra persona puede estar respondiendo bajo presion y no notar que faltan detalles.",
            "context_factors": "Proyecto retrasado, mensajes fragmentados y expectativa de respuesta rapida.",
            "repair_supports": "Pedir prioridades, responsables, plazo y siguiente paso en una lista breve.",
            "interaction": (
                "Mi colega esta compartiendo informacion del proyecto de forma "
                "confusa y desorganizada."
            ),
        },
    },
    "short_message": {
        "pt-BR": {
            "label": "Mensagem curta interpretada como grosseria",
            "user_profile": "Costumo escrever mensagens curtas para ser objetivo.",
            "other_profile": "A outra pessoa pode esperar mais contexto ou sinais de acolhimento.",
            "context_factors": "Reunião atrasada, pouco tempo e conversa por texto sem tom de voz.",
            "repair_supports": "Explicar a intenção e perguntar qual formato de mensagem ajuda mais.",
            "interaction": (
                "Meu colega achou minha mensagem curta grosseira, mas eu estava "
                "tentando ser claro porque a reunião estava atrasada."
            ),
        },
        "en": {
            "label": "Short message read as rude",
            "user_profile": "I often write short messages to be efficient.",
            "other_profile": "The other person may expect more context or warmer cues.",
            "context_factors": "Delayed meeting, limited time, and written chat without tone of voice.",
            "repair_supports": "Clarify intention and ask what message format helps more.",
            "interaction": (
                "My coworker thought my short message was rude, but I was trying "
                "to be clear because the meeting was running late."
            ),
        },
        "es": {
            "label": "Mensaje breve leido como grosero",
            "user_profile": "Suelo escribir mensajes breves para ser eficiente.",
            "other_profile": "La otra persona puede esperar mas contexto o senales de calidez.",
            "context_factors": "Reunion retrasada, poco tiempo y chat escrito sin tono de voz.",
            "repair_supports": "Aclarar la intencion y preguntar que formato de mensaje ayuda mas.",
            "interaction": (
                "Mi colega penso que mi mensaje breve fue grosero, pero intentaba "
                "ser claro porque la reunion iba tarde."
            ),
        },
    },
}


def demo_scenario_options(language: str | None) -> list[tuple[str, str]]:
    normalized = normalize_language(language)
    return [
        (scenario_id, scenario[normalized]["label"])
        for scenario_id, scenario in DEMO_SCENARIOS.items()
    ]


def get_demo_scenario(scenario_id: str, language: str | None) -> dict[str, str]:
    normalized = normalize_language(language)
    return DEMO_SCENARIOS[scenario_id][normalized]
