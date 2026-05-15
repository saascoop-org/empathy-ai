# Specifications

This directory is the source of truth for the application's intended behavior.

Use this order when trying to understand or change the system:

1. `00-product.md` explains the product intent, audience, principles, and boundaries.
2. `01-architecture.md` explains runtime layers, data flow, and component ownership.
3. `02-requirements.md` lists functional and non-functional requirements.
4. `implementation-backlog.md` lists pending implementation work in precedence order.
5. `acceptance-matrix.md` maps scenarios to automated checks.
6. `features/` contains behavior-level specifications for each product capability.
7. `prompts/` contains versioned prompt specifications.
8. `adr/` records architectural decisions and tradeoffs.

Operational documents, deployment checklists, and troubleshooting notes remain in `docs/`.

## Traceability

| Concern | Spec | Implementation | Tests |
| --- | --- | --- | --- |
| Interaction analysis workflow | `features/interaction-analysis.md` | `empathy_engine/orchestration/workflow.py` | `tests/test_workflow.py` |
| Multilingual interface and output | `features/multilingual-output.md` | `app/streamlit_app.py`, `empathy_engine/i18n/language.py` | `tests/test_workflow.py` |
| Privacy and consented persistence | `features/privacy-consent-storage.md` | `empathy_engine/safety/anonymizer.py`, `empathy_engine/storage/interaction_store.py` | `tests/test_workflow.py` |
| Safety boundaries | `features/safety-boundaries.md` | `empathy_engine/agents/bias_safety_agent.py`, `empathy_engine/agents/response_composer.py` | `tests/test_workflow.py` |
| Safety policy | `safety-policy-v1.md` | `empathy_engine/safety/policy.py` | `tests/test_workflow.py` |
| Local LLM runtime | `features/local-llm-runtime.md` | `empathy_engine/llm/ollama_client.py` | `tests/test_workflow.py`, `scripts/smoke_test.py` |
