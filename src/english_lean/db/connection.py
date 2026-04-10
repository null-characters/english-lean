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


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables and indexes if missing (idempotent)."""
    conn.executescript(_load_schema_sql())
    conn.commit()


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Alias for :func:`init_db` (explicit name for callers)."""
    init_db(conn)
