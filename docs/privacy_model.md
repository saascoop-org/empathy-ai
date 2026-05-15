# Privacy Model

## Local-first execution

The system prioritizes:
- local Gemma execution
- local SQLite storage
- anonymized interaction logs

## Data handling

- no third-party sharing
- anonymization before persistence
- consent-based storage

## Current persistence policy

- Raw user interaction text must not be stored.
- If consent is not selected in the interface, no interaction is written to disk.
- If consent is selected, the system stores the anonymized interaction, selected feedback, timestamp, consent version, and JSON result.
- The default SQLite database path is `data/interactions.sqlite3`.
- The `data/` directory is ignored by Git.
- Local demo retention is manual: delete `data/interactions.sqlite3` to remove stored interactions.

## Current anonymization coverage

The anonymizer masks common sensitive fields before persistence:

- e-mails
- URLs
- phone numbers
- Brazilian CPF/CNPJ-like national identifiers
- simple street addresses
- simple chat handles
- capitalized names and composed names

This is a defensive baseline for a demo, not a full privacy guarantee for production use.

## ChromaDB status

ChromaDB is not enabled in the local demo. It is deferred until there is a clear retrieval purpose and a privacy review for vectorized anonymized records.
