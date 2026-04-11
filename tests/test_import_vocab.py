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


def test_import_with_source_and_tags(tmp_path: Path) -> None:
    """Test that source and tags fields are correctly imported."""
    conn = get_connection(Path(":memory:"))
    init_db(conn)
    path = tmp_path / "tagged.json"
    path.write_text(
        '[{"lemma": "test", "source": "ecdict", "tags": ["cet4"]}]',
        encoding="utf-8",
    )
    import_words_from_json(conn, path)
    row = conn.execute(
        "SELECT source, tags FROM words WHERE lemma = 'test'"
    ).fetchone()
    assert row is not None
    assert row[0] == "ecdict"
    assert row[1] == '["cet4"]'
    conn.close()


def test_import_tags_comma_separated(tmp_path: Path) -> None:
    """Test that comma-separated tags are normalized to JSON array."""
    conn = get_connection(Path(":memory:"))
    init_db(conn)
    path = tmp_path / "comma.json"
    path.write_text(
        '[{"lemma": "word", "tags": "cet4, kaoyan"}]',
        encoding="utf-8",
    )
    import_words_from_json(conn, path)
    row = conn.execute(
        "SELECT tags FROM words WHERE lemma = 'word'"
    ).fetchone()
    assert row is not None
    # Should be normalized to JSON array
    assert row[0] == '["cet4", "kaoyan"]'
    conn.close()


def test_import_without_source_tags(tmp_path: Path) -> None:
    """Test that missing source/tags default to NULL."""
    conn = get_connection(Path(":memory:"))
    init_db(conn)
    path = tmp_path / "minimal.json"
    path.write_text('[{"lemma": "basic"}]', encoding="utf-8")
    import_words_from_json(conn, path)
    row = conn.execute(
        "SELECT source, tags FROM words WHERE lemma = 'basic'"
    ).fetchone()
    assert row is not None
    assert row[0] is None
    assert row[1] is None
    conn.close()
