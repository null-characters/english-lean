"""Stats and export (tasks_08 T8.4, T8.6)."""

from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path

from english_lean.db.connection import get_connection, init_db
from english_lean.services.stats import (
    export_progress_csv,
    review_count_on_local_day,
    session_cards_remaining,
)


def test_review_count_on_local_day(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "s.db")
    init_db(conn)
    conn.execute("INSERT INTO words (lemma) VALUES ('a'), ('b')")
    conn.commit()
    w1 = conn.execute("SELECT id FROM words WHERE lemma='a'").fetchone()[0]
    w2 = conn.execute("SELECT id FROM words WHERE lemma='b'").fetchone()[0]
    d = date(2026, 7, 1)
    t1 = datetime(2026, 7, 1, 10, 0, 0).isoformat(timespec="seconds")
    t2 = datetime(2026, 7, 1, 23, 59, 0).isoformat(timespec="seconds")
    t_other = datetime(2026, 7, 2, 0, 0, 0).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses, last_reviewed_at) "
        "VALUES (?, 2.5, 1, 1, 0, ?)",
        (w1, t1),
    )
    conn.execute(
        "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses, last_reviewed_at) "
        "VALUES (?, 2.5, 1, 1, 0, ?)",
        (w2, t2),
    )
    conn.commit()
    assert review_count_on_local_day(conn, d) == 2
    assert review_count_on_local_day(conn, date(2026, 6, 30)) == 0
    conn.execute(
        "UPDATE progress SET last_reviewed_at = ? WHERE word_id = ?",
        (t_other, w1),
    )
    conn.commit()
    assert review_count_on_local_day(conn, d) == 1
    conn.close()


def test_session_cards_remaining() -> None:
    assert session_cards_remaining(5, 0) == 5
    assert session_cards_remaining(5, 4) == 1
    assert session_cards_remaining(5, 5) == 0


def test_export_progress_csv_writes_utf8(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "e.db")
    init_db(conn)
    conn.execute("INSERT INTO words (lemma) VALUES ('hello')")
    conn.commit()
    wid = conn.execute("SELECT id FROM words").fetchone()[0]
    ts = datetime(2026, 1, 1, 12, 0, 0).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses, last_reviewed_at) "
        "VALUES (?, 2.5, 1, 1, 0, ?)",
        (wid, ts),
    )
    conn.commit()
    out = tmp_path / "out.csv"
    export_progress_csv(conn, out)
    text = out.read_text(encoding="utf-8-sig")
    assert "lemma" in text
    assert "hello" in text
    assert "2.5" in text
    conn.close()


def test_export_empty_progress(tmp_path: Path) -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    out = tmp_path / "empty.csv"
    export_progress_csv(conn, out)
    assert "lemma" in out.read_text(encoding="utf-8-sig")
    conn.close()
