"""Database file location (user data dir)."""

from __future__ import annotations

from pathlib import Path

import platformdirs

DB_FILENAME = "english_lean.db"


def get_db_path() -> Path:
    """Return path to the SQLite database, creating parent dirs if needed."""
    base = Path(platformdirs.user_data_dir("english-lean", appauthor=False))
    base.mkdir(parents=True, exist_ok=True)
    return base / DB_FILENAME
