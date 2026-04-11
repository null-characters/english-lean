"""SQLite connections and schema initialization."""

from __future__ import annotations

import sqlite3
from importlib import resources
from pathlib import Path

from english_lean.db.paths import get_db_path


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    """Open SQLite with foreign keys and row factory. Default path: user data dir."""
    target = path if path is not None else get_db_path()
    conn = sqlite3.connect(str(target))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _load_schema_sql() -> str:
    return resources.files("english_lean.db").joinpath("schema.sql").read_text(encoding="utf-8")


def _words_column_names(conn: sqlite3.Connection) -> set[str]:
    return {str(r[1]) for r in conn.execute("PRAGMA table_info(words)").fetchall()}


def _migrate_words_source_tags(conn: sqlite3.Connection) -> None:
    """
    Upgrade pre--tasks_09 databases where ``words`` existed without ``source`` / ``tags``.

    ``CREATE TABLE IF NOT EXISTS`` does not add new columns to an existing table;
    this applies the same changes as ``migrations/001_words_source_tags.sql`` when needed.
    """
    if not conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='words'"
    ).fetchone():
        return
    cols = _words_column_names(conn)
    if "source" not in cols:
        conn.execute("ALTER TABLE words ADD COLUMN source TEXT")
    if "tags" not in cols:
        conn.execute("ALTER TABLE words ADD COLUMN tags TEXT")


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables and indexes if missing (idempotent); apply lightweight migrations."""
    conn.executescript(_load_schema_sql())
    _migrate_words_source_tags(conn)
    conn.commit()


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Alias for :func:`init_db` (explicit name for callers)."""
    init_db(conn)
