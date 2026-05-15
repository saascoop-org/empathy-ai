# Requirements Specification

## Functional Requirements

### FR-001 Interaction Analysis

The system shall accept a free-text interaction description and return a structured empathy mediation result.

### FR-002 Multi-Agent Workflow

The system shall run the following agent sequence:

- Context Decoder
- Double Empathy Analyzer
- Perspective Translator
- Sensory Load Agent
- Bias & Safety Agent
- Response Composer
- Learning Coach

### FR-003 Multilingual Interface

The system shall support UI labels and guidance in:

- English
- Brazilian Portuguese
- Spanish

### FR-004 English Processing Language

The system shall use English as the default processing language regardless of selected UI language.

### FR-005 Localized Output

The system shall present user-facing output in the selected UI language when the selected language is supported.

### FR-006 Language Detection

The system shall try to detect the likely language of user input. If detection is inconclusive, it shall assume English.

### FR-007 Consent-Gated Persistence

The system shall store interaction records only when the user explicitly consents.

### FR-008 Anonymized Persistence

The system shall store only anonymized interaction text.

### FR-009 Local LLM Runtime

The system shall call Ollama locally when LLM generation is enabled.

### FR-010 LLM Fallback

The system shall provide a safe deterministic response if the configured LLM is unavailable, returns empty output, or fails.

## Non-Functional Requirements

### NFR-001 Local-First

The demo shall run locally without third-party API calls for model execution.

### NFR-002 Privacy Baseline

The demo shall mask common sensitive fields before processing persistence:

- e-mails
- URLs
- phone numbers
- CPF/CNPJ-like identifiers
- simple street addresses
- simple chat handles
- capitalized names and composed names

### NFR-003 Safety Baseline

The system shall avoid diagnosis, blame assignment, and behavioral normalization.

### NFR-004 Explainability

The output shall include perspective translation, suggested bridge, and learning insight.

### NFR-005 Demo Resilience

The UI shall remain usable if Ollama cannot run the configured model.

## Acceptance Checks

- `python -m pytest`
- `python scripts/smoke_test.py`
- Streamlit responds on the configured local port.
- Manual UI check for English, Brazilian Portuguese, and Spanish output.
