# ADR 0001: English As Processing Language

## Status

Accepted

## Context

The UI supports English, Brazilian Portuguese, and Spanish. However, agent prompts and internal contracts are simpler and more stable when the processing language is consistent.

## Decision

Use English as the configured processing language. Detect user input language for metadata and UX, but keep internal processing in English. Translate or localize user-facing output into the selected UI language.

## Consequences

- Agent prompts remain simpler.
- Tests can assert stable English processing contracts.
- The UI can still serve PT-BR, EN, and ES users.
- Translation quality must be reviewed before production use.
