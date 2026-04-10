"""Main study window: queue, card, dictation gate, next."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from english_lean.db.import_vocab import import_words_from_json
from english_lean.repository.progress import get_progress, update_progress_after_success
from english_lean.repository.words import get_word_by_id
from english_lean.session.controller import StudySession
from english_lean.srs.sm2 import SrsState, review_success
from english_lean.tools.seed import default_sample_path
from english_lean.ui.card_widget import CardWidget
from english_lean.ui.dictation_widget import DictationWidget


def _progress_row_to_state(row: sqlite3.Row) -> SrsState:
    return SrsState(
        ease_factor=float(row["ease_factor"]),
        interval_days=int(row["interval_days"]),
        repetitions=int(row["repetitions"]),
        lapses=int(row["lapses"]),
    )


def _ensure_sample_vocab(conn: sqlite3.Connection) -> None:
    n = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    if n == 0:
        path = default_sample_path()
        if not path.is_file():
            raise FileNotFoundError(f"缺少样例词库: {path}")
        import_words_from_json(conn, path)
        conn.commit()


class MainWindow(QMainWindow):
    def __init__(self, conn: sqlite3.Connection) -> None:
        super().__init__()
        self.setWindowTitle("english-lean")
        self.resize(720, 560)

        self._conn = conn
        self._session = StudySession(conn)

        self._body = QVBoxLayout()
        root = QWidget()
        root.setLayout(self._body)
        self.setCentralWidget(root)

        self._status = QLabel("")
        self._body.addWidget(self._status)

        self._card_host = QVBoxLayout()
        self._body.addLayout(self._card_host)

        self._dictation: DictationWidget | None = None

        row = QHBoxLayout()
        self._next_btn = QPushButton("下一张")
        self._next_btn.setEnabled(False)
        self._next_btn.clicked.connect(self._on_next)
        row.addStretch(1)
        row.addWidget(self._next_btn)
        self._body.addLayout(row)

        self._session.start(datetime.now())
        self._render()

    def _clear_card_area(self) -> None:
        while self._card_host.count():
            item = self._card_host.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        if self._dictation is not None:
            self._dictation.deleteLater()
            self._dictation = None

    def _render(self) -> None:
        self._clear_card_area()
        wid = self._session.current_word_id()
        if wid is None:
            if not self._session.queue:
                self._status.setText("今日无任务（词库为空或队列已用尽）。")
            else:
                self._status.setText("今日完成。")
            self._next_btn.setEnabled(False)
            return

        row = get_word_by_id(self._conn, wid)
        if row is None:
            self._status.setText("内部错误：找不到单词。")
            return

        lemma = row["lemma"]
        self._status.setText(f"进度 {self._session.index + 1}/{len(self._session.queue)}")

        card = CardWidget(
            lemma,
            row["definition_zh"] or "",
            phonetic=row["phonetic"],
            example=row["example"],
            morphemes=row["morphemes"],
            synonyms=row["synonyms"],
        )
        self._card_host.addWidget(card)

        d = DictationWidget(lemma)
        d.dictation_correct.connect(self._on_spelling_ok)
        d.dictation_wrong.connect(self._on_spelling_bad)
        self._dictation = d
        self._card_host.addWidget(d)

        self._next_btn.setEnabled(self._session.unlocked)

    def _on_spelling_ok(self) -> None:
        if self._session.unlocked:
            return
        wid = self._session.current_word_id()
        if wid is None:
            return
        prow = get_progress(self._conn, wid)
        if prow is None:
            QMessageBox.critical(self, "数据库错误", "找不到学习进度记录。")
            return
        now = datetime.now()
        state = _progress_row_to_state(prow)
        new_state, next_at = review_success(state, now)
        update_progress_after_success(
            self._conn,
            wid,
            new_state,
            reviewed_at=now,
            next_review_at=next_at,
        )
        self._conn.commit()
        self._session.unlocked = True
        self._next_btn.setEnabled(True)

    def _on_spelling_bad(self) -> None:
        self._session.unlocked = False
        self._next_btn.setEnabled(False)

    def _on_next(self) -> None:
        if not self._session.unlocked:
            return
        self._session.advance()
        self._render()

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            self._conn.close()
        except sqlite3.Error:
            pass
        super().closeEvent(event)


def open_main_window(conn: sqlite3.Connection) -> MainWindow:
    _ensure_sample_vocab(conn)
    return MainWindow(conn)
