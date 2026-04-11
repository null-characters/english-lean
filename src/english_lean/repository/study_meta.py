"""Key/value meta for study quotas (daily new words, streak, future stats)."""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta

_KEY_LAST_STUDY_DATE = "last_study_date"
_KEY_NEW_WORDS_TODAY = "new_words_today"
_KEY_LAST_OPEN_DATE = "last_open_date"
_KEY_STREAK_DAYS = "streak_days"


def ensure_day_boundary(conn: sqlite3.Connection, today: date) -> None:
    """
    If ``last_study_date`` is not ``today`` (local calendar), reset ``new_words_today`` to 0.
    Initializes keys on first use. Does not commit.
    """
    today_s = today.isoformat()
    row = conn.execute(
        "SELECT value FROM study_meta WHERE key = ?",
        (_KEY_LAST_STUDY_DATE,),
    ).fetchone()
    if row is None:
        conn.execute(
            """
            INSERT INTO study_meta (key, value) VALUES (?, ?), (?, ?)
            """,
            (_KEY_LAST_STUDY_DATE, today_s, _KEY_NEW_WORDS_TODAY, "0"),
        )
        return
    if str(row[0]) != today_s:
        conn.execute(
            "UPDATE study_meta SET value = ? WHERE key = ?",
            (today_s, _KEY_LAST_STUDY_DATE),
        )
        conn.execute(
            "UPDATE study_meta SET value = '0' WHERE key = ?",
            (_KEY_NEW_WORDS_TODAY,),
        )


def get_new_words_today(conn: sqlite3.Connection) -> int:
    """Return counter for successful first reviews today. Does not commit."""
    row = conn.execute(
        "SELECT value FROM study_meta WHERE key = ?",
        (_KEY_NEW_WORDS_TODAY,),
    ).fetchone()
    if row is None:
        return 0
    try:
        return int(row[0])
    except ValueError:
        return 0


def increment_new_words_today(conn: sqlite3.Connection, delta: int = 1) -> None:
    """Bump today's new-word count after a first successful review. Does not commit."""
    ensure_day_boundary(conn, date.today())
    n = get_new_words_today(conn)
    conn.execute(
        "UPDATE study_meta SET value = ? WHERE key = ?",
        (str(n + delta), _KEY_NEW_WORDS_TODAY),
    )


def effective_new_word_limit(
    conn: sqlite3.Connection,
    requested_limit: int,
    daily_cap: int,
    today: date,
) -> int:
    """
    ``min(requested_limit, max(0, daily_cap - new_words_today))`` after day reset.
    Does not commit.
    """
    ensure_day_boundary(conn, today)
    used = get_new_words_today(conn)
    remaining = max(0, daily_cap - used)
    return min(requested_limit, remaining)


def _get_value(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM study_meta WHERE key = ?", (key,)).fetchone()
    return str(row[0]) if row else None


def _upsert_value(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        """
        INSERT INTO study_meta (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, value),
    )


def get_streak_days(conn: sqlite3.Connection) -> int:
    """Current consecutive-day streak (local calendar). Does not commit."""
    raw = _get_value(conn, _KEY_STREAK_DAYS)
    if raw is None:
        return 0
    try:
        return max(0, int(raw))
    except ValueError:
        return 0


def record_streak_on_open(conn: sqlite3.Connection, today: date) -> int:
    """
    Call once per app open. If ``last_open_date`` is yesterday, increment streak;
    if today, unchanged; if gap, reset to 1. Persists ``last_open_date`` and
    ``streak_days``. Does not commit.
    """
    today_s = today.isoformat()
    lo = _get_value(conn, _KEY_LAST_OPEN_DATE)
    sd_raw = _get_value(conn, _KEY_STREAK_DAYS)
    try:
        streak = int(sd_raw) if sd_raw is not None else 0
    except ValueError:
        streak = 0

    if lo == today_s:
        return max(1, streak) if streak > 0 else 1

    if lo is None:
        new_streak = 1
    else:
        try:
            last = date.fromisoformat(lo)
        except ValueError:
            last = None
        if last is None:
            new_streak = 1
        elif last == today - timedelta(days=1):
            new_streak = max(1, streak) + 1
        else:
            new_streak = 1

    _upsert_value(conn, _KEY_LAST_OPEN_DATE, today_s)
    _upsert_value(conn, _KEY_STREAK_DAYS, str(new_streak))
    return new_streak
