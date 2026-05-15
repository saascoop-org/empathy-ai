# Feature Spec: Local LLM Runtime

## Intent

Use a local Ollama model to compose the bridge message while keeping the app resilient when model execution fails.

## Current Demo Model

- Default: `gemma3:1b`
- Higher-memory target: `gemma4:e2b`

## Rules

- Model and base URL come from environment variables.
- LLM execution is optional in workflow construction.
- If LLM execution fails, return a deterministic fallback.
- The fallback must be safe and localized when possible.

## Acceptance Criteria

- Ollama client reads `GEMMA_MODEL`.
- LLM failure returns `llm_status = unavailable`.
- Empty model output returns `llm_status = empty_response`.
- Smoke test runs without requiring LLM generation.
