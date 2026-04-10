"""Database schema and init tests."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from english_lean.db.connection import get_connection, init_db


def _column_names(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {r[1] for r in rows}


def test_init_db_creates_tables_memory() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    names = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    }
    assert "words" in names
    assert "progress" in names


def test_init_db_idempotent_file(tmp_path: Path) -> None:
    db_path = tmp_path / "t.db"
    conn = get_connection(db_path)
    init_db(conn)
    init_db(conn)
    conn.close()
    conn2 = get_connection(db_path)
    n = conn2.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    assert n >= 2
    conn2.close()


def test_words_and_progress_columns(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "t.db")
    init_db(conn)
    words_cols = _column_names(conn, "words")
    expected_words = {
        "id",
        "lemma",
        "phonetic",
        "definition_zh",
        "example",
        "morphemes",
        "synonyms",
        "frequency_rank",
    }
    assert expected_words <= words_cols
    prog_cols = _column_names(conn, "progress")
    assert {
        "word_id",
        "ease_factor",
        "interval_days",
        "repetitions",
        "next_review_at",
        "last_reviewed_at",
        "lapses",
        "created_at",
    } <= prog_cols
    fk_ok = conn.execute("PRAGMA foreign_key_check").fetchall()
    assert fk_ok == []
    conn.close()


def test_foreign_key_enforced(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "t.db")
    init_db(conn)
    conn.execute("INSERT INTO words (lemma) VALUES ('test')")
    conn.commit()
    wid = conn.execute("SELECT id FROM words WHERE lemma = 'test'").fetchone()[0]
    conn.execute(
        "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses) "
        "VALUES (?, 2.5, 0, 0, 0)",
        (wid,),
    )
    conn.commit()
    bad_sql = (
        "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses) "
        "VALUES (99999, 2.5, 0, 0, 0)"
    )
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(bad_sql)
    conn.close()
