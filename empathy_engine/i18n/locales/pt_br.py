UI_TRANSLATIONS = {
    "product_kicker": "Mediador cognitivo",
    "subtitle": "Mediação de comunicação com IA e controles locais de privacidade",
    "intro": (
        "Descreva um desencontro de comunicação. O sistema anonimiza o texto, "
        "processa em inglês e mostra uma possível ponte de entendimento."
    ),
    "notice": (
        "Esta ferramenta oferece apenas apoio de comunicação. Ela não fornece "
        "aconselhamento clínico, jurídico, de RH ou educacional especializado."
    ),
    "demo_scenario_heading": "Cenário de demo",
    "demo_scenario_intro": "Carregue um cenário corporativo preparado para apresentar o fluxo completo com mais rapidez.",
    "demo_scenario_select": "Cenário",
    "load_demo_scenario": "Carregar cenário",
    "demo_scenario_loaded": "Cenário de demo carregado. Revise os campos antes de analisar.",
    "alterity_heading": "Mapa de alteridade",
    "alterity_intro": (
        "Cadastre um contexto opcional sobre as duas pessoas antes da análise. "
        "Use papéis ou iniciais em vez de dados pessoais reais."
    ),
    "alterity_user_profile": "Seu perfil de comunicação",
    "alterity_user_profile_placeholder": (
        "Exemplo: costumo ser direto, literal e breve quando estou sob pressão."
    ),
    "alterity_other_profile": "Possível perfil de comunicação da outra pessoa",
    "alterity_other_profile_placeholder": (
        "Exemplo: ela pode esperar mais acolhimento, contexto ou pistas emocionais."
    ),
    "alterity_context_factors": "Fatores sensoriais ou contextuais",
    "alterity_context_factors_placeholder": (
        "Exemplo: sala barulhenta, reunião atrasada, cansaço, mensagem escrita sem tom."
    ),
    "alterity_repair_supports": "Apoios que podem reparar a troca",
    "alterity_repair_supports_placeholder": (
        "Exemplo: esclarecer a intenção, perguntar preferência, oferecer próximo passo concreto."
    ),
    "alterity_help": (
        "Opcional. Estas notas entram na análise e seguem as mesmas regras de "
        "anonimização e armazenamento local da interação."
    ),
    "step_user_context": "Etapa 1 - Seu contexto",
    "step_other_context": "Etapa 2 - Contexto da outra pessoa",
    "step_context_factors": "Etapa 3 - Situação e apoios",
    "step_interaction": "Etapa 4 - Mensagem para analisar",
    "audio_input_heading": "Nota de voz opcional",
    "audio_input_intro": (
        "Grave um desabafo curto para ensaiar o futuro fluxo de áudio para insight. "
        "Nesta demo, revise a gravação e escreva a interação abaixo antes de analisar."
    ),
    "audio_input_label": "Desabafar via áudio",
    "audio_input_help": (
        "O navegador grava o áudio e envia para esta sessão local do Streamlit. "
        "Transcrição automática e extração do mapa ficam planejadas para a API pós-demo."
    ),
    "audio_input_received": (
        "Áudio recebido localmente. A transcrição automática não está ativa nesta demo; "
        "use a gravação como referência e escreva a interação abaixo."
    ),
    "local_status": "Status local",
    "status_model": "Modelo",
    "status_available": "disponível",
    "status_unavailable": "indisponível",
    "status_processing_language": "Idioma de processamento",
    "status_database": "Banco de dados",
    "learning_diary_heading": "Diário de aprendizado mútuo",
    "learning_diary_intro": (
        "Revise registros locais consentidos e as perguntas de reflexão geradas "
        "a partir de trocas anteriores."
    ),
    "learning_diary_count": "Registros exibidos no diário: {count}",
    "learning_diary_empty": (
        "Ainda não há entradas no diário. Ative o consentimento de armazenamento "
        "local antes de analisar uma interação para salvar registros anonimizados."
    ),
    "learning_diary_record_title": "Entrada #{record_id} - {created_at}",
    "learning_diary_privacy_note": "Somente conteúdo anonimizado e consentido aparece aqui.",
    "learning_diary_interaction": "Interação anonimizada:",
    "learning_diary_bridge": "Ponte sugerida:",
    "learning_diary_reflection": "Pergunta de reflexão:",
    "learning_diary_feedback": "Feedback: {feedback}",
    "learning_diary_search": "Buscar no diário",
    "learning_diary_search_placeholder": "Busque por interação, ponte ou reflexão",
    "learning_diary_no_results": "Nenhuma entrada do diário corresponde a esta busca.",
    "delete_diary_entry": "Excluir esta entrada",
    "diary_entry_deleted": "Entrada do diário excluída.",
    "no_feedback": "sem feedback",
    "delete_record_id": "ID do registro para excluir",
    "delete_selected_record": "Excluir registro local selecionado",
    "delete_all_records": "Excluir todos os registros locais",
    "deleted_records": "Registros excluídos: {count}",
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
    "save_to_diary_heading": "Diário e feedback",
    "save_to_diary": "Salvar esta análise no diário de aprendizado mútuo",
    "save_to_diary_help": (
        "Com esta opção marcada, a análise é salva localmente em versão anonimizada."
    ),
    "save_to_diary_note": (
        "O diário guarda apenas registros anonimizados e consentidos neste computador."
    ),
    "consent": "Salvar esta análise no diário de aprendizado mútuo",
    "consent_help": "Quando desmarcado, nenhuma interação é salva no diário local.",
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
    "bridge_card_label": "Ponte pronta para usar",
    "copy_response": "Copiar resposta",
    "result_tab_context": "Contexto",
    "result_tab_perspectives": "Perspectivas",
    "result_tab_learning": "Aprendizagem",
    "result_tab_privacy": "Privacidade",
    "learning_heading": "### Insight de aprendizagem",
    "privacy_heading": "### Privacidade",
    "stored": "Análise anonimizada salva no diário como entrada {record_id}.",
    "not_stored": "Esta análise não foi salva no diário.",
    "save_after_analysis": "Salvar esta análise no diário",
    "saved_after_analysis": "Análise salva no diário como entrada {record_id}.",
}


OUTPUT_TRANSLATIONS = {
    (
        "The exchange is about project information that the user "
        "experiences as confusing or disorganized."
    ): (
        "A troca envolve informações de projeto que o usuário percebe como "
        "confusas ou desorganizadas."
    ),
    (
        "The other person may not realize which project details feel "
        "unclear, incomplete, or out of order."
    ): (
        "A outra pessoa talvez não perceba quais detalhes do projeto parecem "
        "pouco claros, incompletos ou fora de ordem."
    ),
    (
        "The user may need the project information organized into "
        "clear points, priorities, and next steps."
    ): (
        "O usuário pode precisar que as informações do projeto sejam organizadas "
        "em pontos claros, prioridades e próximos passos."
    ),
    (
        "Which project information needs to be clarified first: "
        "priority, deadline, responsibility, or next step?"
    ): (
        "Qual informação do projeto precisa ser esclarecida primeiro: "
        "prioridade, prazo, responsabilidade ou próximo passo?"
    ),
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
