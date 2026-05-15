import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB_PATH = Path("data") / "interactions.sqlite3"


class InteractionStore:

    def __init__(self, db_path=None):
        configured_path = os.getenv("INTERACTION_DB_PATH")
        self.db_path = Path(db_path or configured_path or DEFAULT_DB_PATH)

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

    def save(self, anonymized_interaction: str, result: dict, feedback=None):
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
                    "local-demo-v1",
                    anonymized_interaction,
                    json.dumps(result, ensure_ascii=True),
                    feedback,
                ),
            )

        return cursor.lastrowid
