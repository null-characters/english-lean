"""Persistent study scope: which word list (tag) to drill."""

from __future__ import annotations

from typing import Literal

# Stored in QSettings and used for queue filtering.
StudyScope = Literal["all", "cet4", "kaoyan"]

# Short names must match JSON ``tags`` in imported packs
# (e.g. ``["cet4"]``, ``["kaoyan","netem"]``).
TAG_SHORT_CET4 = "cet4"
TAG_SHORT_KAOYAN = "kaoyan"

_ALLOWED_TAGS = frozenset({TAG_SHORT_CET4, TAG_SHORT_KAOYAN})


def scope_to_tag(scope: StudyScope) -> str | None:
    """``all`` → no SQL filter; ``cet4`` / ``kaoyan`` → filter by that tag."""
    if scope == "all":
        return None
    return scope


def tags_like_pattern(short: str) -> str:
    """
    Build ``LIKE`` pattern for ``words.tags`` TEXT that stores JSON array strings.

    Uses quoted substring ``\"cet4\"`` / ``\"kaoyan\"`` to reduce accidental substring
    matches (documented tradeoff vs JSON1).
    """
    if short not in _ALLOWED_TAGS:
        raise ValueError(f"unsupported tag filter: {short!r}")
    return f'%"{short}"%'
