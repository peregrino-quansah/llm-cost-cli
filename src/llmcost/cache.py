"""SQLite cache for LLM responses."""

import hashlib
import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS responses (
    key TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL
)
"""

SELECT_SQL = "SELECT text, input_tokens, output_tokens FROM responses WHERE key = ?"
UPSERT_SQL = (
    "INSERT OR REPLACE INTO responses (key, text, input_tokens, output_tokens) VALUES (?, ?, ?, ?)"
)


@dataclass(frozen=True)
class CachedResponse:
    """One saved API answer and its token counts"""

    text: str
    input_tokens: int
    output_tokens: int


def make_key(model: str, prompt: str, max_tokens: int) -> str:
    """Return a SHA-256 key for one request."""
    payload = json.dumps(
        {"model": model, "prompt": prompt, "max_tokens": max_tokens}, sort_keys=True
    )
    key = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return key


class ResponseCache:
    """Stores responses in a SQLite file."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(CREATE_TABLE_SQL)

    def get(self, key: str) -> CachedResponse | None:
        """Return the saved response for key, or None"""
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            row = conn.execute(SELECT_SQL, (key,)).fetchone()

        if row is None:
            return None
        return CachedResponse(text=row[0], input_tokens=row[1], output_tokens=row[2])

    def put(self, key: str, response: CachedResponse) -> None:
        """Save a response under key. Replace any old value."""
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(
                UPSERT_SQL, (key, response.text, response.input_tokens, response.output_tokens)
            )
