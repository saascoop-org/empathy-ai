# System Architecture

## Layers

1. Frontend Interface
2. Interaction Gateway
3. Safety & Consent Layer
4. Multi-Agent Empathy Engine
5. Gemma Runtime
6. Local Persistence Layer
7. Explainable Output Layer

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
- `EmpathyWorkflow` anonymizes the user input before the agent pipeline runs.
- `ResponseComposerAgent` attempts to use Ollama when enabled and falls back to a deterministic safe response if the model is unavailable.
- `InteractionStore` persists anonymized interactions to SQLite only when the user gives explicit consent.
- ChromaDB and LangGraph remain planned stack components and are not part of the current execution path.
