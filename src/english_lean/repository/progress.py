"""Progress / SRS rows."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from english_lean.config.study_scope import tags_like_pattern
from english_lean.srs.sm2 import SrsState


def get_progress(conn: sqlite3.Connection, word_id: int) -> sqlite3.Row | None:
    """Return progress row or None. Does not commit."""
    return conn.execute("SELECT * FROM progress WHERE word_id = ?", (word_id,)).fetchone()


def list_due_before(
    conn: sqlite3.Connection,
    when: datetime,
    *,
    limit: int,
    tag: str | None = None,
) -> list[int]:
    """
    Word IDs due for review: ``next_review_at`` is not NULL and <= ``when``,
    ordered by ``next_review_at`` ascending (earliest first).
    ``when`` should be local time from the caller. Does not commit.

    If ``tag`` is set (e.g. ``cet4``, ``kaoyan``), only words whose ``words.tags``
    JSON text matches that tag (see ``tags_like_pattern``).
    """
    iso = when.isoformat(timespec="seconds")
    if tag is None:
        rows = conn.execute(
            """
            SELECT word_id FROM progress
            WHERE next_review_at IS NOT NULL AND next_review_at <= ?
            ORDER BY next_review_at ASC
            LIMIT ?
            """,
            (iso, limit),
        ).fetchall()
    else:
        like = tags_like_pattern(tag)
        rows = conn.execute(
            """
            SELECT p.word_id FROM progress p
            INNER JOIN words w ON w.id = p.word_id
            WHERE p.next_review_at IS NOT NULL AND p.next_review_at <= ?
              AND w.tags LIKE ?
            ORDER BY p.next_review_at ASC
            LIMIT ?
            """,
            (iso, like, limit),
        ).fetchall()
    return [int(r[0]) for r in rows]


def list_new_words(conn: sqlite3.Connection, *, limit: int, tag: str | None = None) -> list[int]:
    """
    Never scheduled / never reviewed: ``repetitions = 0``, ``last_reviewed_at`` NULL,
    and ``next_review_at`` NULL (excludes items already pushed to a future date).
    Stable order by ``word_id``. Does not commit.

    Optional ``tag`` filters by ``words.tags`` like :func:`list_due_before`.
    """
    if tag is None:
        rows = conn.execute(
            """
            SELECT word_id FROM progress
            WHERE repetitions = 0
              AND last_reviewed_at IS NULL
              AND next_review_at IS NULL
            ORDER BY word_id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    else:
        like = tags_like_pattern(tag)
        rows = conn.execute(
            """
            SELECT p.word_id FROM progress p
            INNER JOIN words w ON w.id = p.word_id
            WHERE p.repetitions = 0
              AND p.last_reviewed_at IS NULL
              AND p.next_review_at IS NULL
              AND w.tags LIKE ?
            ORDER BY p.word_id ASC
            LIMIT ?
            """,
            (like, limit),
        ).fetchall()
    return [int(r[0]) for r in rows]


def update_progress_after_success(
    conn: sqlite3.Connection,
    word_id: int,
    state: SrsState,
    *,
    reviewed_at: datetime,
    next_review_at: datetime,
) -> None:
    """Persist SM-2 success outcome. Does not commit."""
    conn.execute(
        """
        UPDATE progress SET
            ease_factor = ?,
            interval_days = ?,
            repetitions = ?,
            lapses = ?,
            last_reviewed_at = ?,
            next_review_at = ?
        WHERE word_id = ?
        """,
        (
            state.ease_factor,
            state.interval_days,
            state.repetitions,
            state.lapses,
            reviewed_at.isoformat(timespec="seconds"),
            next_review_at.isoformat(timespec="seconds"),
            word_id,
        ),
    )


def update_progress_after_fail(
    conn: sqlite3.Connection,
    word_id: int,
    state: SrsState,
    *,
    next_review_at: datetime,
) -> None:
    """Persist SM-2 fail outcome (e.g. immediate requeue). Does not commit."""
    conn.execute(
        """
        UPDATE progress SET
            ease_factor = ?,
            interval_days = ?,
            repetitions = ?,
            lapses = ?,
            next_review_at = ?
        WHERE word_id = ?
        """,
        (
            state.ease_factor,
            state.interval_days,
            state.repetitions,
            state.lapses,
            next_review_at.isoformat(timespec="seconds"),
            word_id,
        ),
    )
