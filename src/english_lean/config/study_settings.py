"""Tunable study parameters (tasks_08 T8.1)."""

from __future__ import annotations

# Max due (review) cards to pull into one queue build.
DUE_LIMIT = 50
DEFAULT_DUE_LIMIT = DUE_LIMIT

# Default max *new* (never successfully reviewed) cards per queue build before daily cap.
DEFAULT_NEW_WORD_LIMIT = 20

# Daily cap on first-time successful reviews (new words). Enforced via ``study_meta``.
NEW_WORDS_PER_DAY = 20
