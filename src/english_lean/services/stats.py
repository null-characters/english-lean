"""Aggregates for UI: reviews today, session queue length (tasks_08 T8.4)."""

from __future__ import annotations

import csv
import sqlite3
from datetime import date, datetime, time, timedelta
from pathlib import Path


def review_count_on_local_day(conn: sqlite3.Connection, d: date) -> int:
    """Count progress rows with ``last_reviewed_at`` falling on local calendar day ``d``."""
    start = datetime.combine(d, time.min).isoformat(timespec="seconds")
    end = datetime.combine(d + timedelta(days=1), time.min).isoformat(timespec="seconds")
    row = conn.execute(
        """
        SELECT COUNT(*) FROM progress
        WHERE last_reviewed_at IS NOT NULL
          AND last_reviewed_at >= ? AND last_reviewed_at < ?
        """,
        (start, end),
    ).fetchone()
    return int(row[0]) if row else 0


def session_cards_remaining(queue_len: int, index: int) -> int:
    """Cards left in the current session including the active card (if any)."""
    return max(0, queue_len - index)


def default_progress_export_path() -> Path:
    """``~/Downloads/english_lean_progress_YYYYMMDD.csv`` (tasks_08 T8.6)."""
    name = f"english_lean_progress_{date.today().strftime('%Y%m%d')}.csv"
    return Path.home() / "Downloads" / name


def export_progress_csv(conn: sqlite3.Connection, dest: Path) -> None:
    """Write all progress joined with lemma. Overwrites ``dest``. UTF-8 with BOM for Excel."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = conn.execute(
        """
        SELECT w.lemma, p.ease_factor, p.interval_days, p.repetitions, p.lapses,
               p.last_reviewed_at, p.next_review_at
        FROM progress p
        INNER JOIN words w ON w.id = p.word_id
        ORDER BY w.id
        """
    ).fetchall()
    with dest.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "lemma",
                "ease_factor",
                "interval_days",
                "repetitions",
                "lapses",
                "last_reviewed_at",
                "next_review_at",
            ]
        )
        w.writerows(rows)
