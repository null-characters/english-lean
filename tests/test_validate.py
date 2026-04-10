"""Spelling normalization tests."""

from __future__ import annotations

from english_lean.quiz.validate import check_spelling, normalize_answer


def test_normalize_answer() -> None:
    assert normalize_answer("  Hello ") == "hello"


def test_check_spelling_case_insensitive() -> None:
    assert check_spelling("HELLO", "hello")
    assert not check_spelling("hell0", "hello")
