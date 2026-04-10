"""Word card with optional detail sections."""

from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout, QWidget


class CardWidget(QWidget):
    def __init__(
        self,
        lemma: str,
        definition_zh: str,
        *,
        phonetic: str | None = None,
        example: str | None = None,
        morphemes: str | None = None,
        synonyms: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._def_label: QLabel
        self._toggle_btn: QPushButton
        self._def_visible = False

        lemma_lbl = QLabel(lemma)
        f = QFont(lemma_lbl.font())
        f.setPointSize(f.pointSize() + 8)
        f.setBold(True)
        lemma_lbl.setFont(f)

        layout = QVBoxLayout(self)
        layout.addWidget(lemma_lbl)

        if phonetic:
            ph = QLabel(phonetic)
            ph.setStyleSheet("color: gray;")
            layout.addWidget(ph)

        self._def_label = QLabel(definition_zh or "")
        self._def_label.setVisible(False)
        layout.addWidget(self._def_label)

        self._toggle_btn = QPushButton("显示释义")
        self._toggle_btn.clicked.connect(self._toggle_definition)
        layout.addWidget(self._toggle_btn)

        if example:
            box = QGroupBox("例句")
            v = QVBoxLayout(box)
            v.addWidget(QLabel(example))
            layout.addWidget(box)

        if morphemes:
            box = QGroupBox("词根词缀")
            v = QVBoxLayout(box)
            v.addWidget(QLabel(morphemes))
            layout.addWidget(box)

        if synonyms:
            box = QGroupBox("近义词")
            v = QVBoxLayout(box)
            v.addWidget(QLabel(synonyms))
            layout.addWidget(box)

        layout.addStretch(1)

    def _toggle_definition(self) -> None:
        self._def_visible = not self._def_visible
        self._def_label.setVisible(self._def_visible)
        self._toggle_btn.setText("隐藏释义" if self._def_visible else "显示释义")
