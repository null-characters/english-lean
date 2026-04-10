"""Preview card + dictation without DB: ``python tools/ui_preview.py`` from repo root."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without editable install
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from english_lean.ui.card_widget import CardWidget
from english_lean.ui.dictation_widget import DictationWidget


def main() -> None:
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("english-lean UI preview")
    layout = QVBoxLayout(w)
    layout.addWidget(
        CardWidget(
            "abandon",
            "放弃；抛弃",
            phonetic="ah-BAN-dun",
            example="They had to abandon the plan.",
            morphemes="a- + bandon",
            synonyms="desert, forsake",
        )
    )
    d = DictationWidget("abandon")
    d.dictation_correct.connect(lambda: print("correct"))
    d.dictation_wrong.connect(lambda: print("wrong"))
    layout.addWidget(d)
    w.resize(640, 480)
    w.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
