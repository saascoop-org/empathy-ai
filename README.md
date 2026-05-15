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

## Configuration

The `.env` file controls local model execution:

```bash
OLLAMA_BASE_URL=http://localhost:11434
GEMMA_MODEL=gemma3:1b
INTERACTION_DB_PATH=data/interactions.sqlite3
```

`gemma4:e2b` is available as a higher-memory target model, but the local demo uses `gemma3:1b` because it fits the available machine memory. If Ollama cannot run the configured model, the app keeps the deterministic multi-agent flow available and falls back to a safe bridge response.

## Current Implementation Notes

- The Streamlit app calls the real `EmpathyWorkflow`.
- The workflow anonymizes input before agent processing.
- The pipeline includes the agents listed in the architecture document.
- SQLite persists anonymized interactions only after explicit consent.
- ChromaDB and LangGraph are stack targets but are not wired into the current runtime yet.
- ChromaDB is deferred for the local demo; see `docs/chromadb_decision.md`.

## Architecture

See:
- docs/architecture.md
- docs/ethical_framework.md
- docs/privacy_model.md
- docs/troubleshooting.md
- docs/go_no_go.md
- docs/chromadb_decision.md
