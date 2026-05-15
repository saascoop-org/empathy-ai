# ChromaDB Decision

## Decision

ChromaDB is deferred for the local demonstrative deployment.

## Rationale

- The current demo does not require semantic retrieval or long-term memory.
- SQLite already covers consented local persistence for anonymized interaction records.
- Adding vector storage before the demo would increase privacy review scope and operational risk.
- ChromaDB should only receive anonymized text and should have a clear retrieval purpose before integration.

## Revisit Criteria

Integrate ChromaDB when the product needs at least one of these capabilities:

- retrieve prior anonymized communication patterns with user consent
- compare similar interaction scenarios across consented records
- support learning insights over multiple sessions

Before integration, define retention policy, deletion workflow, embedding model, and tests proving raw text is not indexed.
