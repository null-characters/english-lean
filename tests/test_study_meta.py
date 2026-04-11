"""study_meta daily new-word quota."""

from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path

from english_lean.config.study_settings import NEW_WORDS_PER_DAY
from english_lean.db.connection import get_connection, init_db
from english_lean.repository.study_meta import (
    effective_new_word_limit,
    ensure_day_boundary,
    get_new_words_today,
    increment_new_words_today,
)


def test_ensure_day_boundary_inits_keys(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "m.db")
    init_db(conn)
    d = date(2026, 6, 1)
    ensure_day_boundary(conn, d)
    conn.commit()
    assert (
        conn.execute(
            "SELECT value FROM study_meta WHERE key = 'last_study_date'",
        ).fetchone()[0]
        == "2026-06-01"
    )
    assert get_new_words_today(conn) == 0
    conn.close()


def test_ensure_day_boundary_resets_counter_on_new_calendar_day(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "m.db")
    init_db(conn)
    ensure_day_boundary(conn, date(2026, 6, 1))
    conn.execute(
        "UPDATE study_meta SET value = '5' WHERE key = 'new_words_today'",
    )
    conn.commit()
    ensure_day_boundary(conn, date(2026, 6, 2))
    conn.commit()
    assert get_new_words_today(conn) == 0
    assert (
        conn.execute(
            "SELECT value FROM study_meta WHERE key = 'last_study_date'",
        ).fetchone()[0]
        == "2026-06-02"
    )
    conn.close()


def test_effective_new_word_limit_respects_daily_cap(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "m.db")
    init_db(conn)
    today = date(2026, 6, 15)
    ensure_day_boundary(conn, today)
    conn.execute(
        "UPDATE study_meta SET value = ? WHERE key = 'new_words_today'",
        (str(NEW_WORDS_PER_DAY - 3),),
    )
    conn.commit()
    assert effective_new_word_limit(conn, 10, NEW_WORDS_PER_DAY, today) == 3
    conn.close()


def test_increment_new_words_today(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "m.db")
    init_db(conn)
    ensure_day_boundary(conn, date.today())
    increment_new_words_today(conn)
    conn.commit()
    assert get_new_words_today(conn) == 1
    conn.close()


def test_effective_limit_zero_when_quota_exhausted_memory() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    today = date(2026, 4, 10)
    ensure_day_boundary(conn, today)
    conn.execute(
        "UPDATE study_meta SET value = ? WHERE key = 'new_words_today'",
        (str(NEW_WORDS_PER_DAY),),
    )
    assert effective_new_word_limit(conn, 50, NEW_WORDS_PER_DAY, today) == 0
    conn.close()
