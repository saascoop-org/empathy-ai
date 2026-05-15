import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from empathy_engine.config import load_settings
from empathy_engine.schemas import (
    StoredInteractionRecord,
    StoredInteractionSummary,
    normalize_feedback,
)


DEFAULT_DB_PATH = Path("data") / "interactions.sqlite3"
SCHEMA_VERSION = 1


class InteractionStore:

    def __init__(self, db_path=None):
        settings = load_settings()
        self.db_path = Path(db_path or settings.interaction_db_path or DEFAULT_DB_PATH)

    def initialize(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    consent_version TEXT NOT NULL,
                    anonymized_interaction TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    feedback TEXT
                )
                """
            )
            connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def schema_version(self):
        if not self.db_path.exists():
            return 0

        with sqlite3.connect(self.db_path) as connection:
            return connection.execute("PRAGMA user_version").fetchone()[0]

    def save(self, anonymized_interaction: str, result: dict, feedback=None):
        record = StoredInteractionRecord(
            anonymized_interaction=anonymized_interaction,
            result_json=self._sanitize_result_for_storage(result),
            feedback=normalize_feedback(feedback),
            db_path=self.db_path,
        )
        self.initialize()

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO interactions (
                    created_at,
                    consent_version,
                    anonymized_interaction,
                    result_json,
                    feedback
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    record.consent_version,
                    record.anonymized_interaction,
                    json.dumps(record.result_json, ensure_ascii=True),
                    record.feedback,
                ),
            )

        return cursor.lastrowid

    def get(self, record_id: int):
        if not self.db_path.exists():
            return None

        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                """
                SELECT id, created_at, consent_version, anonymized_interaction,
                       result_json, feedback
                FROM interactions
                WHERE id = ?
                """,
                (record_id,),
            ).fetchone()

        if not row:
            return None

        return StoredInteractionRecord(
            id=row["id"],
            created_at=row["created_at"],
            consent_version=row["consent_version"],
            anonymized_interaction=row["anonymized_interaction"],
            result_json=json.loads(row["result_json"]),
            feedback=row["feedback"],
            db_path=self.db_path,
        )

    def list(self, limit=20):
        if not self.db_path.exists():
            return []

        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, created_at, consent_version, anonymized_interaction,
                       feedback
                FROM interactions
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            StoredInteractionSummary(
                id=row["id"],
                created_at=row["created_at"],
                consent_version=row["consent_version"],
                anonymized_interaction=row["anonymized_interaction"],
                feedback=row["feedback"],
            )
            for row in rows
        ]

    def delete(self, record_id: int):
        self.initialize()

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                "DELETE FROM interactions WHERE id = ?",
                (record_id,),
            )

        return cursor.rowcount

    def delete_all(self):
        self.initialize()

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute("DELETE FROM interactions")

        return cursor.rowcount

    def _sanitize_result_for_storage(self, result: dict):
        sanitized = dict(result)
        if "raw_interaction" in sanitized:
            sanitized.pop("raw_interaction")
        return sanitized
