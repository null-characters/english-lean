"""Cluster words by morpheme affinity and shuffle for varied study order."""

from __future__ import annotations

import random
import sqlite3


def morpheme_cluster_key(raw: str | None) -> str:
    """
    Bucket key so similar morpheme lines (e.g. same first stem before ``+``) group together.

    Empty / NULL morphemes share the ``__none__`` bucket (still shuffled among themselves).
    """
    if raw is None:
        return "__none__"
    s = str(raw).strip()
    if not s:
        return "__none__"
    s_lower = " ".join(s.lower().split())
    if "+" in s_lower:
        head = s_lower.split("+", 1)[0].strip()
        head = head.strip("- ")
        if head:
            return head
    return s_lower


def cluster_shuffle_word_ids(
    conn: sqlite3.Connection,
    word_ids: list[int],
    rng: random.Random,
) -> list[int]:
    """
    Group ``word_ids`` by :func:`morpheme_cluster_key`, randomize group order, shuffle inside each group.
    Preserves multiset of ids. Empty input returns ``[]``.
    """
    if not word_ids:
        return []
    placeholders = ",".join("?" * len(word_ids))
    rows = conn.execute(
        f"SELECT id, morphemes FROM words WHERE id IN ({placeholders})",
        word_ids,
    ).fetchall()
    morpheme_by_id = {int(r[0]): r[1] for r in rows}

    buckets: dict[str, list[int]] = {}
    for wid in word_ids:
        key = morpheme_cluster_key(morpheme_by_id.get(wid))
        buckets.setdefault(key, []).append(wid)

    keys = list(buckets.keys())
    rng.shuffle(keys)
    out: list[int] = []
    for k in keys:
        chunk = buckets[k]
        rng.shuffle(chunk)
        out.extend(chunk)
    return out
