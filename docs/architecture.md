# System Architecture

Canonical architecture spec: `../specs/01-architecture.md`.

## Layers

1. Frontend Interface
2. Interaction Gateway
3. Safety & Consent Layer
4. Language Detection & UI Localization
5. Multi-Agent Empathy Engine
6. Gemma Runtime
7. Local Persistence Layer
8. Explainable Output Layer

## Multi-Agent Pipeline

Context Decoder
|
Double Empathy Analyzer
|
Perspective Translator
|
Sensory Load Agent
|
Bias & Safety Agent
|
Response Composer
|
Learning Coach

## Current Runtime

- `app/streamlit_app.py` renders the Streamlit interface and calls `EmpathyWorkflow`.
- The interface supports English, Brazilian Portuguese, and Spanish.
- The workflow detects the user's likely language and defaults to English when detection is inconclusive.
- The configured processing language is English.
- User-facing output is localized to the selected interface language after English processing.
- `EmpathyWorkflow` anonymizes the user input before the agent pipeline runs.
- `ResponseComposerAgent` attempts to use Ollama when enabled and falls back to a deterministic safe response if the model is unavailable.
- `InteractionStore` persists anonymized interactions to SQLite only when the user gives explicit consent.
- ChromaDB and LangGraph remain planned stack components and are not part of the current execution path.
