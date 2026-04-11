"""In-memory study queue position and unlock flag."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from english_lean.config.study_settings import (
    DEFAULT_DUE_LIMIT,
    DEFAULT_NEW_WORD_LIMIT,
    NEW_WORDS_PER_DAY,
)
from english_lean.repository.study_meta import effective_new_word_limit
from english_lean.services.study_queue import build_queue


class StudySession:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.queue: list[int] = []
        self.index: int = 0
        self.unlocked: bool = False
        self.tag: str | None = None

    def start(
        self,
        now: datetime,
        *,
        due_limit: int | None = None,
        new_limit: int | None = None,
        tag: str | None = None,
    ) -> None:
        self.tag = tag
        dl = DEFAULT_DUE_LIMIT if due_limit is None else due_limit
        req = DEFAULT_NEW_WORD_LIMIT if new_limit is None else new_limit
        cap = effective_new_word_limit(self.conn, req, NEW_WORDS_PER_DAY, now.date())
        self.queue = build_queue(
            self.conn,
            now,
            due_limit=dl,
            new_limit=cap,
            tag=tag,
        )
        self.index = 0
        self.unlocked = False

    def current_word_id(self) -> int | None:
        if self.index >= len(self.queue):
            return None
        return self.queue[self.index]

    def advance(self) -> None:
        self.index += 1
        self.unlocked = False
