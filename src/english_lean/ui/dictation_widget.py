"""Text dictation with feedback and pass/fail signals."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from english_lean.quiz.validate import check_spelling


class DictationWidget(QWidget):
    submitted = Signal(str)
    dictation_correct = Signal()
    dictation_wrong = Signal()

    def __init__(self, expected_lemma: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._expected = expected_lemma

        self._input = QLineEdit()
        self._input.setPlaceholderText("在此输入英文单词")
        self._input.returnPressed.connect(self._emit_check)

        self._check = QPushButton("检查")
        self._check.clicked.connect(self._emit_check)

        self._feedback = QLabel("")
        self._feedback.setStyleSheet("color: gray;")

        row = QHBoxLayout()
        row.addWidget(self._input, stretch=1)
        row.addWidget(self._check)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self._feedback)

    def set_expected(self, lemma: str) -> None:
        self._expected = lemma
        self._input.clear()
        self._feedback.clear()
        self._feedback.setStyleSheet("color: gray;")

    def _emit_check(self) -> None:
        text = self._input.text()
        self.submitted.emit(text)
        if check_spelling(text, self._expected):
            self._feedback.setText("正确")
            self._feedback.setStyleSheet("color: green;")
            self.dictation_correct.emit()
        else:
            self._feedback.setText("再试一次")
            self._feedback.setStyleSheet("color: red;")
            self.dictation_wrong.emit()
