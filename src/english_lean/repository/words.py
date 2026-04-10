"""Word rows."""

from __future__ import annotations

import sqlite3


def get_word_by_id(conn: sqlite3.Connection, word_id: int) -> sqlite3.Row | None:
    """Return the word row or None. Does not commit."""
    return conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
