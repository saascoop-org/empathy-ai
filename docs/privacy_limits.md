# Privacy Limits And Retention

## Anonymization Limits

The current anonymizer is regex-based and intended for a local demo. It masks common sensitive patterns, but it is not a production-grade de-identification system.

Known limits:

- It can miss unusual names, addresses, handles, or identifiers.
- It can over-mask capitalized words that are not personal names.
- It does not prove that free text is anonymous.
- It does not infer context-specific sensitive information.

## Processing vs Persistence

The code now separates:

- `anonymize_for_processing`
- `anonymize_for_persistence`

Both currently use the same masking strategy. They are separated so stricter persistence rules can be added without changing the workflow contract.

## Logging

Application logging must not include raw user text. Use the safe logging helper in `empathy_engine/safety/logging.py` when adding runtime logs.

## Retention Policy

For the local demo:

- Data is stored only after explicit consent.
- Records are stored in local SQLite.
- Retention is manual.
- Delete `data/interactions.sqlite3` to remove local records.

For production or pilot use, retention must be revisited before real user data is collected.
