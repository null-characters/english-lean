"""Smoke import tests (no GUI exec)."""

from __future__ import annotations

import english_lean
from english_lean.main import main


def test_package_version() -> None:
    assert english_lean.__version__ == "0.1.0"


def test_main_callable() -> None:
    assert callable(main)
