"""Application entry: study main window."""

from __future__ import annotations

import os
import sqlite3
import sys

# Before importing Qt: reduce noisy macOS logs (ICC color profile parsing is harmless).
if sys.platform == "darwin":
    os.environ.setdefault("QT_LOGGING_RULES", "qt.gui.icc=false")

from PySide6.QtWidgets import QApplication, QMessageBox

from english_lean.db.connection import get_connection, init_db
from english_lean.ui.main_window import open_main_window


def main() -> None:
    app = QApplication(sys.argv)
    try:
        conn = get_connection()
        init_db(conn)
        win = open_main_window(conn)
    except sqlite3.Error as e:
        QMessageBox.critical(None, "数据库错误", str(e))
        sys.exit(1)
    except FileNotFoundError as e:
        QMessageBox.critical(None, "词库错误", str(e))
        sys.exit(1)

    win.show()
    sys.exit(app.exec())
