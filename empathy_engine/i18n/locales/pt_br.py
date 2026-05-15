UI_TRANSLATIONS = {
    "subtitle": "Mediação de comunicação com IA e controles locais de privacidade",
    "intro": (
        "Descreva um desencontro de comunicação. O sistema anonimiza o texto, "
        "processa em inglês e mostra uma possível ponte de entendimento."
    ),
    "notice": (
        "Esta ferramenta oferece apenas apoio de comunicação. Ela não fornece "
        "aconselhamento clínico, jurídico, de RH ou educacional especializado."
    ),
    "ui_language": "Idioma da interface",
    "interaction_label": "Interação para analisar",
    "interaction_placeholder": (
        "Exemplo: Meu colega achou minha mensagem curta grosseira, mas eu "
        "estava tentando ser claro porque a reunião estava atrasada."
    ),
    "interaction_help": (
        "Evite usar dados pessoais reais em demos. Se incluir nomes, e-mails, "
        "telefones ou endereços, o workflow tentará mascará-los."
    ),
    "consent": "Autorizo o armazenamento local de interações anonimizadas",
    "consent_help": "Quando desmarcado, nenhuma interação é gravada no banco SQLite local.",
    "feedback": "Feedback da resposta",
    "feedback_options": ["Útil e segura", "Parcialmente útil", "Não útil"],
    "feedback_help": (
        "O feedback opcional só é armazenado se o consentimento local estiver marcado."
    ),
    "analyze": "Analisar interação",
    "missing_interaction": "Descreva uma interação antes de analisar.",
    "spinner": "Executando análise multiagente de empatia...",
    "success": "Possível ponte de empatia identificada.",
    "context_heading": "### Contexto",
    "context_text": (
        "O workflow encontrou um possível desencontro de expectativas de tom "
        "e pistas de comunicação."
    ),
    "language_note": (
        "Idioma detectado do usuário: {user_language}. Idioma de processamento: inglês."
    ),
    "translation_heading": "### Tradução de perspectiva",
    "for_user": "Para o usuário:",
    "for_other": "Para a outra pessoa:",
    "bridge_heading": "### Ponte sugerida",
    "learning_heading": "### Insight de aprendizagem",
    "privacy_heading": "### Privacidade",
    "stored": "Interação anonimizada armazenada localmente como registro {record_id}.",
    "not_stored": "Nenhuma interação foi armazenada.",
}


OUTPUT_TRANSLATIONS = {
    "The other person may expect more emotional cues.": (
        "A outra pessoa pode esperar mais pistas emocionais."
    ),
    "Direct language may reflect efficiency, not hostility.": (
        "Linguagem direta pode refletir eficiência, não hostilidade."
    ),
    "What assumptions existed in this interaction?": (
        "Quais pressupostos existiam nesta interação?"
    ),
    (
        "Clarify intention, name the possible mismatch, and ask what "
        "would make the exchange easier for both people."
    ): (
        "Esclareça a intenção, nomeie o possível desencontro e pergunte "
        "o que tornaria a conversa mais fácil para ambas as pessoas."
    ),
    (
        "Frame outputs as possible interpretations, not diagnosis, "
        "fault, or behavioral normalization."
    ): (
        "Formule as saídas como interpretações possíveis, não como "
        "diagnóstico, culpa ou normalização comportamental."
    ),
    (
        "Frame outputs as possible interpretations, not diagnosis, fault, "
        "or behavioral normalization. For abuse, risk, legal, medical, or HR "
        "questions, state that the case needs appropriate human support."
    ): (
        "Formule as saídas como interpretações possíveis, não como diagnóstico, "
        "culpa ou normalização comportamental. Em casos de abuso, risco ou "
        "questões jurídicas, médicas ou de RH, indique que o caso precisa "
        "de apoio humano apropriado."
    ),
}
