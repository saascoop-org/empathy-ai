# Empathy-Interactional-Expertise

AI-powered cognitive communication infrastructure designed for local Gemma-based mediation.

## Vision

Empathy-Interactional-Expertise is a multi-agent AI platform designed to mediate communication between people with different cognitive and communication styles.

The platform is based on:
- Double Empathy Problem
- Neurodiversity paradigm
- Human-centered AI
- Privacy-preserving AI
- Explainable AI

## Core Principles

- No diagnosis
- No normalization
- Human-in-the-loop
- Explainable outputs
- Local-first AI
- Ethical mediation

## Stack

- Streamlit
- Python
- Ollama
- Gemma 4
- SQLite
- ChromaDB
- LangGraph

## Tracks

- Main Track
- Digital Equity & Inclusivity
- Safety & Trust
- Future of Education
- Ollama Track

## Run

Prerequisites:

- Python 3.11+.
- Ollama running locally.
- Gemma model available in Ollama. Current local demo default: `gemma3:1b`.

```bash
cp .env.example .env
pip install -r requirements.txt
ollama list
streamlit run app/streamlit_app.py
```

If the configured model is missing, download it with:

```bash
ollama pull gemma3:1b
```

Run tests with:

```bash
python -m pytest
```

Run the local smoke test with:

```bash
python scripts/smoke_test.py
```

If Streamlit is running, check the UI endpoint with:

```bash
python scripts/check_streamlit.py
```

## Configuration

The `.env` file controls local model execution:

```bash
OLLAMA_BASE_URL=http://localhost:11434
GEMMA_MODEL=gemma3:1b
INTERACTION_DB_PATH=data/interactions.sqlite3
DEFAULT_UI_LANGUAGE=en
PROCESSING_LANGUAGE=en
SESSION_TIMEOUT_MS=180000
SESSION_TIMEOUT_WARNING_MS=150000
SESSION_EXPIRED_URL=/session-expired.html
```

`gemma4:e2b` is available as a higher-memory target model, but the local demo uses `gemma3:1b` because it fits the available machine memory. If Ollama cannot run the configured model, the app keeps the deterministic multi-agent flow available and falls back to a safe bridge response.

The interface supports English, Brazilian Portuguese, and Spanish. The default UI language is controlled by `DEFAULT_UI_LANGUAGE`. Text processing remains English by default through `PROCESSING_LANGUAGE=en`; when user language detection is inconclusive, the app assumes English. User-facing output is translated for presentation into the selected interface language.

Locale files live in `empathy_engine/i18n/locales/`, with English as the fallback language when a translation key is missing.

The Streamlit demo includes a browser-side inactivity timeout guard. It listens only to human interaction events such as mouse, keyboard, click, scroll, and touch activity. If the user is inactive for `SESSION_TIMEOUT_MS`, the browser leaves the Streamlit app and opens `SESSION_EXPIRED_URL`, allowing WebSocket connections to close naturally so VM idle-shutdown automation can detect zero active sessions.

## Spec Driven Development

The project is organized so behavior is described before implementation details:

- `specs/00-product.md`: product intent, audience, boundaries, and principles.
- `specs/01-architecture.md`: runtime layers, component ownership, data flow, and contracts.
- `specs/02-requirements.md`: functional and non-functional requirements.
- `specs/implementation-backlog.md`: pending implementation work in precedence order.
- `specs/acceptance-matrix.md`: acceptance scenarios mapped to automated checks.
- `specs/features/`: feature-level specifications and acceptance criteria.
- `specs/prompts/`: versioned prompt specifications.
- `specs/adr/`: architectural decisions and tradeoffs.

Use `specs/` as the starting point for understanding or changing behavior. Use `docs/` for deployment, troubleshooting, operational readiness, and issue/decision records.

## Current Implementation Notes

- The Streamlit app calls the real `EmpathyWorkflow`.
- The workflow anonymizes input before agent processing.
- The pipeline includes the agents listed in the architecture document.
- SQLite persists anonymized interactions only after explicit consent.
- ChromaDB and LangGraph are stack targets but are not wired into the current runtime yet.
- ChromaDB is deferred for the local demo; see `docs/chromadb_decision.md`.

## Architecture

See:
- specs/README.md
- specs/00-product.md
- specs/01-architecture.md
- specs/02-requirements.md
- docs/troubleshooting.md
- docs/go_no_go.md
- docs/chromadb_decision.md
- docs/privacy_limits.md
