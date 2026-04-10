"""In-memory study queue position and unlock flag."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from english_lean.services.study_queue import build_queue


class StudySession:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.queue: list[int] = []
        self.index: int = 0
        self.unlocked: bool = False

    def start(self, now: datetime, *, due_limit: int = 50, new_limit: int = 20) -> None:
        self.queue = build_queue(self.conn, now, due_limit=due_limit, new_limit=new_limit)
        self.index = 0
        self.unlocked = False

    def current_word_id(self) -> int | None:
        if self.index >= len(self.queue):
            return None
        return self.queue[self.index]

    def advance(self) -> None:
        self.index += 1
        self.unlocked = False
