"""Kaoyan / NETEM vocabulary: convert exam-data NETEM JSON to project import format.

Upstream: https://github.com/exam-data/NETEMVocabulary (``netem_full_list.json``).
Data license: CC BY-NC-SA 4.0 — see upstream ``LICENSE``; do not commit raw JSON.

Field mapping and tags: ``docs/data/kaoyan.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

# Upstream raw JSON; large file not shipped in this repo.
NETEM_JSON_URL = (
    "https://raw.githubusercontent.com/exam-data/NETEMVocabulary/master/netem_full_list.json"
)


def _norm_lemma(raw: str) -> str | None:
    s = raw.strip().lower()
    return s if s else None


def _int_or_none(v: Any) -> int | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v) if v == int(v) else None
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return None
        try:
            return int(s)
        except ValueError:
            return None
    return None


def _extract_netem_word_list(data: Any) -> list[dict[str, Any]]:
    """Return the word entry list from NETEM top-level JSON object."""
    if not isinstance(data, dict):
        raise ValueError("NETEM JSON must be a top-level object")
    candidates: list[list[Any]] = [v for v in data.values() if isinstance(v, list)]
    if not candidates:
        raise ValueError("NETEM JSON: no list value found under top-level keys")
    for lst in candidates:
        if not lst:
            return []
        first = lst[0]
        if isinstance(first, dict) and "单词" in first:
            return lst  # type: ignore[return-value]
    return candidates[0]  # type: ignore[return-value]


def record_from_netem_item(item: dict[str, Any]) -> dict[str, Any] | None:
    """Map one NETEM row to import JSON object. Returns None if unusable."""
    word = item.get("单词")
    if not isinstance(word, str):
        return None
    lemma = _norm_lemma(word)
    if lemma is None:
        return None

    raw_def = item.get("释义")
    definition_zh: str | None
    if raw_def is None:
        definition_zh = None
    elif isinstance(raw_def, str):
        definition_zh = raw_def.strip() or None
    else:
        definition_zh = str(raw_def).strip() or None

    # ``frequency_rank`` stores 序号 (list position in NETEM table), not raw 词频 counts.
    frequency_rank = _int_or_none(item.get("序号"))

    return {
        "lemma": lemma,
        "phonetic": None,
        "definition_zh": definition_zh,
        "example": None,
        "morphemes": None,
        "synonyms": None,
        "frequency_rank": frequency_rank,
        "source": "netem",
        "tags": ["kaoyan", "netem"],
    }


def _records_from_netem_obj(data: Any) -> list[dict[str, Any]]:
    rows = _extract_netem_word_list(data)
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        rec = record_from_netem_item(row)
        if rec is not None:
            out.append(rec)
    return out


def convert_kaoyan_to_pack(in_path: Path, out_path: Path) -> int:
    """
    Read NETEM ``netem_full_list.json`` from ``in_path``, write import JSON to ``out_path``.

    Returns number of records written.
    """
    if not in_path.is_file():
        raise FileNotFoundError(in_path)
    text = in_path.read_text(encoding="utf-8")
    data = json.loads(text)
    records = _records_from_netem_obj(data)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(records)


def fetch_netem_kaoyan_pack(out_path: Path, url: str = NETEM_JSON_URL) -> int:
    """
    Download NETEM JSON from ``url``, convert, write to ``out_path``.

    Returns number of records written.
    """
    with urlopen(url, timeout=600) as resp:  # noqa: S310 — documented upstream URL
        raw = resp.read()
    data = json.loads(raw.decode("utf-8"))
    records = _records_from_netem_obj(data)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(records)
