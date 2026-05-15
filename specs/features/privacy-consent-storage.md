# Feature Spec: Privacy, Consent, And Storage

## Intent

Keep demo data local and prevent raw interaction text from being persisted without explicit user consent.

## Rules

- Do not persist anything when consent is unchecked.
- Store only anonymized interaction text.
- Keep processing anonymization and persistence anonymization as separate methods, even when they currently share implementation.
- Store feedback only when saving a consented record.
- Normalize feedback values before persistence.
- Store records in SQLite at `INTERACTION_DB_PATH`.
- Keep local data out of Git through `.gitignore`.
- Listing local records must not create a database file.
- Users must be able to delete one local record or all local records from the interface.

## Stored Fields

- created timestamp
- consent version
- anonymized interaction
- result JSON
- optional feedback

## Schema Version

SQLite `PRAGMA user_version` is used as the local schema version marker.

## Anonymization Coverage

- e-mails
- URLs
- phone numbers
- CPF/CNPJ-like identifiers
- simple street addresses
- simple chat handles
- capitalized names and composed names

## Acceptance Criteria

- Storage creates a SQLite database.
- Storage writes one row per consented save.
- Tests prove sensitive sample data is masked.
- Logging helpers redact sensitive text before output.
- Known anonymization limits and retention policy are documented in `docs/privacy_limits.md`.
- Storage supports read, list, delete one, and delete all operations.
- Stored `result_json` must not include a `raw_interaction` key.
