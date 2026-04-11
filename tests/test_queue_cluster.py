"""Morpheme cluster ordering for study queue."""

from __future__ import annotations

import random
from pathlib import Path

from english_lean.db.connection import get_connection, init_db
from english_lean.services.queue_cluster import cluster_shuffle_word_ids, morpheme_cluster_key


def test_morpheme_cluster_key_splits_on_plus() -> None:
    assert morpheme_cluster_key("a- + bandon") == morpheme_cluster_key("a- + broad")
    assert morpheme_cluster_key("able + -ity") == "able"
    assert morpheme_cluster_key(None) == "__none__"
    assert morpheme_cluster_key("") == "__none__"
    assert morpheme_cluster_key("  ") == "__none__"


def test_cluster_shuffle_groups_same_stem_together(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "c.db")
    init_db(conn)
    for lemma, morphemes in [
        ("w1", "pre- + view"),
        ("w2", "pre- + dict"),
        ("w3", "post- + war"),
    ]:
        conn.execute(
            "INSERT INTO words (lemma, morphemes) VALUES (?, ?)",
            (lemma, morphemes),
        )
        wid = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        conn.execute(
            "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses) "
            "VALUES (?, 2.5, 0, 0, 0)",
            (wid,),
        )
    conn.commit()
    ids = [
        int(r[0])
        for r in conn.execute("SELECT id FROM words ORDER BY lemma").fetchall()
    ]
    rng = random.Random(123)
    out = cluster_shuffle_word_ids(conn, ids, rng)
    assert set(out) == set(ids)
    # pre- group (2 words) should be contiguous block
    pre_ids = {
        int(r[0])
        for r in conn.execute(
            "SELECT id FROM words WHERE morphemes LIKE 'pre-%'",
        ).fetchall()
    }
    idxs = [out.index(i) for i in pre_ids]
    assert max(idxs) - min(idxs) == 1

    conn.close()


def test_cluster_shuffle_deterministic_with_seed(tmp_path: Path) -> None:
    conn = get_connection(tmp_path / "d.db")
    init_db(conn)
    for i in range(4):
        conn.execute("INSERT INTO words (lemma) VALUES (?)", (f"w{i}",))
        wid = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        conn.execute(
            "INSERT INTO progress (word_id, ease_factor, interval_days, repetitions, lapses) "
            "VALUES (?, 2.5, 0, 0, 0)",
            (wid,),
        )
    conn.commit()
    ids = [r[0] for r in conn.execute("SELECT id FROM words ORDER BY id").fetchall()]
    a = cluster_shuffle_word_ids(conn, ids, random.Random(42))
    b = cluster_shuffle_word_ids(conn, ids, random.Random(42))
    assert a == b
    conn.close()
