# ADR 0002: Defer ChromaDB For Demo

## Status

Accepted

## Context

The current demo does not need semantic retrieval or long-term memory. SQLite already supports consented anonymized persistence.

## Decision

Do not enable ChromaDB in the local demo.

## Consequences

- Privacy scope stays smaller.
- Demo operations remain simpler.
- ChromaDB can be revisited when retrieval has a clear product purpose and retention/deletion policies are defined.
