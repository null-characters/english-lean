"""Vocabulary import tests."""

from __future__ import annotations

from pathlib import Path

from english_lean.db.connection import get_connection, init_db
from english_lean.db.import_vocab import import_words_from_json

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "vocab" / "sample_cet4.json"


def test_import_sample_idempotent() -> None:
    conn = get_connection(Path(":memory:"))
    init_db(conn)
    n1 = import_words_from_json(conn, SAMPLE)
    assert n1 >= 20
    w = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    p = conn.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
    assert w >= 20
    assert p == w
    n2 = import_words_from_json(conn, SAMPLE)
    assert n2 == 0
    conn.close()


def test_lemma_stored_lowercase(tmp_path: Path) -> None:
    conn = get_connection(Path(":memory:"))
    init_db(conn)
    path = tmp_path / "case.json"
    path.write_text('[{"lemma": "  Hello "}]', encoding="utf-8")
    import_words_from_json(conn, path)
    row = conn.execute("SELECT lemma FROM words WHERE lemma = 'hello'").fetchone()
    assert row is not None
    conn.close()
