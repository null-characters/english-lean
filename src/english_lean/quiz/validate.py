"""Normalize user input and compare to stored lemmas."""

from __future__ import annotations


def normalize_answer(text: str) -> str:
    """Strip whitespace; lemmas are stored lowercase, so callers compare lowercased forms."""
    return text.strip().lower()


def check_spelling(user_input: str, expected_lemma: str) -> bool:
    return normalize_answer(user_input) == normalize_answer(expected_lemma)
