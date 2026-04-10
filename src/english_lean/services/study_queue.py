"""Build ordered study queues from progress rows."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from english_lean.repository.progress import list_due_before, list_new_words


def build_queue(
    conn: sqlite3.Connection,
    now: datetime,
    *,
    due_limit: int = 50,
    new_limit: int = 20,
) -> list[int]:
    """
    Merge review queue for local time ``now``: due items first (earliest ``next_review_at``),
    then up to ``new_limit`` new words (never reviewed). Dedupes by ``word_id``.
    Repository functions do not commit; callers may ``commit`` after session updates.

    Returns an empty list when nothing is due and no new slots are available.
    """
    due = list_due_before(conn, now, limit=due_limit)
    seen: set[int] = set(due)
    fresh_pool = list_new_words(conn, limit=new_limit + len(due) + 50)
    new_picked: list[int] = []
    for wid in fresh_pool:
        if wid in seen:
            continue
        new_picked.append(wid)
        seen.add(wid)
        if len(new_picked) >= new_limit:
            break
    return due + new_picked
