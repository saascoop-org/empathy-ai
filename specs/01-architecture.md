# Architecture Specification

## Runtime Layers

1. Frontend Interface
2. Interaction Gateway
3. Safety & Consent Layer
4. Language Detection & UI Localization
5. Multi-Agent Empathy Engine
6. Local LLM Runtime
7. Local Persistence Layer
8. Explainable Output Layer

## Component Map

| Layer | Responsibility | Code |
| --- | --- | --- |
| Frontend Interface | Render multilingual Streamlit UI and collect consent/feedback | `app/streamlit_app.py` |
| Interaction Gateway | Pass submitted text into the application use case | `empathy_engine/use_cases/analyze_interaction.py` |
| Safety & Consent Layer | Anonymize data and gate persistence by consent | `empathy_engine/safety/anonymizer.py`, `empathy_engine/storage/interaction_store.py` |
| Language Detection & UI Localization | Detect likely user language, localize UI/output, keep processing in English | `empathy_engine/i18n/language.py` |
| Multi-Agent Empathy Engine | Run the staged empathy analysis pipeline | `empathy_engine/agents/`, `empathy_engine/orchestration/workflow.py` |
| Local LLM Runtime | Call Ollama and fall back safely on failure | `empathy_engine/llm/ollama_client.py`, `empathy_engine/agents/response_composer.py` |
| Local Persistence Layer | Store anonymized consented interactions in SQLite | `empathy_engine/storage/interaction_store.py` |
| Explainable Output Layer | Present context, perspective translation, bridge, and learning insight | `app/streamlit_app.py` |

## Application Boundaries

- `app/streamlit_app.py` is presentation only.
- `AnalyzeInteractionUseCase` coordinates workflow execution, result presentation, and consented persistence.
- `ResultPresenter` owns localization of workflow output for display.
- UI translations are stored per language in `empathy_engine/i18n/locales/`.
- `InteractionStore` owns SQLite persistence.
- `ports.py` defines lightweight interfaces for LLM and storage dependencies.
- `errors.py` defines recoverable application errors for workflow and persistence failures.

## Data Flow

1. User selects a UI language.
2. User enters an interaction.
3. UI passes text, selected output language, consent, and feedback into `AnalyzeInteractionUseCase`.
4. Use case invokes `EmpathyWorkflow`.
5. Workflow detects likely user language.
6. Workflow sets processing language to English.
7. Workflow anonymizes the interaction.
8. Agents run in sequence:
   - Context Decoder
   - Double Empathy Analyzer
   - Perspective Translator
   - Sensory Load Agent
   - Bias & Safety Agent
   - Response Composer
   - Learning Coach
9. Response Composer processes in English and presents the bridge in the selected output language.
10. `ResultPresenter` localizes deterministic output fields for display.
11. If consent is selected, the use case stores the anonymized interaction and result locally.

## Agent Pipeline Contract

Agent inputs and outputs are represented with Pydantic schemas in `empathy_engine/schemas.py`. The workflow keeps returning plain dictionaries at the application boundary for UI compatibility.

The workflow result must include:

- `interaction`
- `language.user_language`
- `language.processing_language`
- `language.output_language`
- `context`
- `analysis`
- `translation`
- `sensory_load`
- `safety`
- `response`
- `learning`

## Failure Modes

- If language detection is inconclusive, assume English.
- If Ollama is unavailable, use a deterministic safe bridge.
- If the user does not consent to storage, do not write to SQLite.
- If unsafe framing is detected, warn the user and keep the response framed as possible interpretation.

## Deferred Architecture

ChromaDB and LangGraph are planned stack elements but are not part of the current demo runtime.
