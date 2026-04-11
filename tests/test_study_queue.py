"""Study queue ordering tests."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from english_lean.db.connection import get_connection, init_db
from english_lean.repository.progress import list_due_before, list_new_words
from english_lean.services.study_queue import build_queue


def _insert_word(conn: sqlite3.Connection, lemma: str) -> int:
    cur = conn.execute("INSERT INTO words (lemma) VALUES (?)", (lemma,))
    wid = int(cur.lastrowid)
    conn.execute(
        """
        INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses)
        VALUES (?, 2.5, 0, 0, 0)
        """,
        (wid,),
    )
    return wid


def _insert_word_tagged(conn: sqlite3.Connection, lemma: str, tags_json: str) -> int:
    cur = conn.execute(
        "INSERT INTO words (lemma, tags) VALUES (?, ?)",
        (lemma, tags_json),
    )
    wid = int(cur.lastrowid)
    conn.execute(
        """
        INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses)
        VALUES (?, 2.5, 0, 0, 0)
        """,
        (wid,),
    )
    return wid


def test_build_queue_due_then_new(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "q.db")
    init_db(conn)
    # Three words with staggered due times
    ids = []
    for i, lemma in enumerate(["due_a", "due_b", "due_c"]):
        wid = _insert_word(conn, lemma)
        ids.append(wid)
    # Two never-reviewed new words
    new1 = _insert_word(conn, "new_x")
    new2 = _insert_word(conn, "new_y")
    conn.commit()

    now = datetime(2026, 4, 10, 12, 0, 0)
    t_early = (now - timedelta(days=1)).isoformat(timespec="seconds")
    t_mid = now.isoformat(timespec="seconds")
    t_late = (now + timedelta(days=1)).isoformat(timespec="seconds")

    conn.execute(
        "UPDATE progress SET next_review_at = ? WHERE word_id = ?",
        (t_mid, ids[1]),
    )
    conn.execute(
        "UPDATE progress SET next_review_at = ? WHERE word_id = ?",
        (t_early, ids[0]),
    )
    conn.execute(
        "UPDATE progress SET next_review_at = ? WHERE word_id = ?",
        (t_late, ids[2]),
    )
    # new1, new2 keep NULL next_review_at and repetitions 0
    conn.commit()

    due = list_due_before(conn, now, limit=10)
    assert due == [ids[0], ids[1]]

    new_only = list_new_words(conn, limit=10)
    assert new1 in new_only and new2 in new_only

    q = build_queue(conn, now, due_limit=10, new_limit=2)
    assert q[:2] == [ids[0], ids[1]]
    assert set(q[2:]) == {new1, new2}
    assert len(q) == 4

    conn.close()


def test_build_queue_empty_when_no_words() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    now = datetime(2026, 4, 10, 12, 0, 0)
    assert build_queue(conn, now, due_limit=10, new_limit=5) == []
    conn.close()


def test_build_queue_filters_cet4_tag_only(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "tagged.db")
    init_db(conn)
    w_cet = _insert_word_tagged(conn, "cet_only", '["cet4"]')
    w_ky = _insert_word_tagged(conn, "ky_only", '["kaoyan","netem"]')
    conn.commit()

    now = datetime(2026, 4, 10, 12, 0, 0)
    all_ids = set(build_queue(conn, now, due_limit=10, new_limit=10))
    assert all_ids == {w_cet, w_ky}

    cet_only = build_queue(conn, now, due_limit=10, new_limit=10, tag="cet4")
    assert cet_only == [w_cet]

    ky_only = build_queue(conn, now, due_limit=10, new_limit=10, tag="kaoyan")
    assert ky_only == [w_ky]

    assert list_due_before(conn, now, limit=10, tag="cet4") == []
    assert list_new_words(conn, limit=10, tag="cet4") == [w_cet]

    conn.close()
