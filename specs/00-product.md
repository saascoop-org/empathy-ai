# Product Specification

## Product

Empathy-Interactional-Expertise is a local-first AI application that helps mediate communication mismatches between people with different cognitive and communication styles.

## Primary User Goal

The user wants to describe an interaction and receive a possible empathy bridge that can help clarify intent, expectations, and communication cues without assigning blame.

## Audience

- Demo evaluators.
- Educators and facilitators exploring communication support tools.
- Teams interested in privacy-preserving AI mediation.
- Developers extending the prototype.

## Core Principles

- No diagnosis.
- No behavioral normalization.
- No judgment of who is right or wrong.
- Human-in-the-loop interpretation.
- Local-first processing.
- Explicit consent before persistence.
- Explainable, practical output.

## Product Boundaries

The system does not provide:

- clinical advice
- legal advice
- HR determinations
- educational diagnosis
- automated conflict resolution
- authority over intent, blame, or correctness

## Supported Demo Languages

- English
- Brazilian Portuguese
- Spanish

The application may display output in any supported UI language. The internal processing language remains English.

## Current Demo State

- Streamlit UI is operational.
- Ollama local model `gemma3:1b` is validated for demo use.
- `gemma4:e2b` is installed but requires more memory than the current machine has available.
- SQLite persistence is enabled only after explicit consent.
- ChromaDB is intentionally deferred.
