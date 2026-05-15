UI_TRANSLATIONS = {
    "subtitle": "Mediación de comunicación con IA y controles locales de privacidad",
    "intro": (
        "Describe un desacuerdo de comunicación. El sistema anonimiza el texto, "
        "lo procesa en inglés y muestra un posible puente de entendimiento."
    ),
    "notice": (
        "Esta herramienta ofrece solo apoyo de comunicación. No brinda asesoría "
        "clínica, legal, de RR. HH. ni educativa especializada."
    ),
    "ui_language": "Idioma de la interfaz",
    "interaction_label": "Interacción para analizar",
    "interaction_placeholder": (
        "Ejemplo: Mi colega pensó que mi mensaje breve fue grosero, pero yo "
        "intentaba ser claro porque la reunión iba tarde."
    ),
    "interaction_help": (
        "Evita usar datos personales reales en demos. Si incluyes nombres, "
        "correos, teléfonos o direcciones, el workflow intentará enmascararlos."
    ),
    "consent": "Acepto el almacenamiento local de interacciones anonimizadas",
    "consent_help": "Si no está marcado, no se escribe ninguna interacción en SQLite local.",
    "feedback": "Comentarios sobre la respuesta",
    "feedback_options": ["Útil y segura", "Parcialmente útil", "No útil"],
    "feedback_help": (
        "El feedback opcional solo se almacena si se selecciona el consentimiento local."
    ),
    "analyze": "Analizar interacción",
    "missing_interaction": "Describe una interacción antes de analizar.",
    "spinner": "Ejecutando análisis multiagente de empatía...",
    "success": "Posible puente de empatía identificado.",
    "context_heading": "### Contexto",
    "context_text": (
        "El workflow encontró un posible desacuerdo en expectativas de tono "
        "y señales de comunicación."
    ),
    "language_note": (
        "Idioma detectado del usuario: {user_language}. Idioma de procesamiento: inglés."
    ),
    "translation_heading": "### Traducción de perspectiva",
    "for_user": "Para el usuario:",
    "for_other": "Para la otra persona:",
    "bridge_heading": "### Puente sugerido",
    "learning_heading": "### Insight de aprendizaje",
    "privacy_heading": "### Privacidad",
    "stored": "Interacción anonimizada almacenada localmente como registro {record_id}.",
    "not_stored": "No se almacenó ninguna interacción.",
}


OUTPUT_TRANSLATIONS = {
    "The other person may expect more emotional cues.": (
        "La otra persona puede esperar más señales emocionales."
    ),
    "Direct language may reflect efficiency, not hostility.": (
        "El lenguaje directo puede reflejar eficiencia, no hostilidad."
    ),
    "What assumptions existed in this interaction?": (
        "¿Qué supuestos existían en esta interacción?"
    ),
    (
        "Clarify intention, name the possible mismatch, and ask what "
        "would make the exchange easier for both people."
    ): (
        "Aclara la intención, nombra el posible desacuerdo y pregunta "
        "qué haría que el intercambio fuera más fácil para ambas personas."
    ),
    (
        "Frame outputs as possible interpretations, not diagnosis, "
        "fault, or behavioral normalization."
    ): (
        "Formula las salidas como interpretaciones posibles, no como "
        "diagnóstico, culpa o normalización conductual."
    ),
    (
        "Frame outputs as possible interpretations, not diagnosis, fault, "
        "or behavioral normalization. For abuse, risk, legal, medical, or HR "
        "questions, state that the case needs appropriate human support."
    ): (
        "Formula las salidas como interpretaciones posibles, no como diagnóstico, "
        "culpa o normalización conductual. En casos de abuso, riesgo o preguntas "
        "legales, médicas o de RR. HH., indica que el caso necesita apoyo humano "
        "apropiado."
    ),
}
