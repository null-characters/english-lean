"""Load vocabulary entries from JSON into SQLite."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


def normalize_lemma(raw: str) -> str | None:
    """Strip and lower-case lemma for stable spelling checks; empty -> None."""
    s = raw.strip().lower()
    return s if s else None


def _iter_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict) and "words" in data:
        inner = data["words"]
        if isinstance(inner, list):
            return [x for x in inner if isinstance(x, dict)]
    return []


def ensure_progress_rows(conn: sqlite3.Connection) -> int:
    """Create progress rows for words that lack them. Returns number of rows inserted."""
    before = conn.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
    conn.execute(
        """
        INSERT INTO progress (
            word_id, ease_factor, interval_days, repetitions, lapses,
            next_review_at, last_reviewed_at
        )
        SELECT id, 2.5, 0, 0, 0, NULL, NULL
        FROM words
        WHERE NOT EXISTS (SELECT 1 FROM progress p WHERE p.word_id = words.id)
        """
    )
    conn.commit()
    after = conn.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
    return after - before


def import_words_from_json(conn: sqlite3.Connection, path: Path) -> int:
    """
    Insert words from JSON (array of objects or { "words": [...] }).
    Skips entries without a non-empty lemma after normalization.
    Returns number of newly inserted word rows (not progress rows).
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    records = _iter_records(data)
    before = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]

    for rec in records:
        if rec and all(str(k).startswith("_") for k in rec):
            continue
        raw_lemma = rec.get("lemma")
        if raw_lemma is None:
            continue
        lemma = normalize_lemma(str(raw_lemma))
        if lemma is None:
            continue

        phonetic = rec.get("phonetic")
        definition_zh = rec.get("definition_zh")
        example = rec.get("example")
        morphemes = rec.get("morphemes")
        synonyms = rec.get("synonyms")
        frequency_rank = rec.get("frequency_rank")

        conn.execute(
            """
            INSERT OR IGNORE INTO words (
                lemma, phonetic, definition_zh, example, morphemes, synonyms, frequency_rank
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (lemma, phonetic, definition_zh, example, morphemes, synonyms, frequency_rank),
        )

    conn.commit()
    after = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    added = after - before
    ensure_progress_rows(conn)
    return added
