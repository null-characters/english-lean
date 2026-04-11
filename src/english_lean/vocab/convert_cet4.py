"""CET-4 vocabulary: convert external data to the project's import JSON format.

Primary format: **ECDICT** CSV (MIT, skywind3000/ECDICT). Rows whose ``tag`` field
contains ``cet4`` (space-separated tags per upstream docs) are exported.

Secondary format: lyandut-style JSON array (``word``, ``phonetic``, ``translation``, …).

Duplicate lemmas: import uses ``INSERT OR IGNORE`` in SQLite; first row wins. Merging
tags for the same lemma is out of scope (see tasks_12 / future work).
"""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any
from urllib.request import urlopen

# MIT-licensed; do not redistribute full CSV in this repo — fetch at build/runtime.
ECDICT_CSV_URL = "https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv"


def _norm_lemma(raw: str) -> str | None:
    s = raw.strip().lower()
    return s if s else None


def _int_or_none(s: str) -> int | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def record_from_ecdict_row(row: list[str], col: dict[str, int]) -> dict[str, Any] | None:
    """Map one ECDICT CSV row to import JSON object. Returns None if not CET-4."""
    if len(row) <= max(col.values()):
        return None
    tag = (row[col["tag"]] or "").strip()
    if not tag or "cet4" not in tag.split():
        return None
    word = row[col["word"]]
    lemma = _norm_lemma(word)
    if lemma is None:
        return None
    phonetic = row[col["phonetic"]].strip() or None
    translation = row[col["translation"]].strip()
    definition = row[col["definition"]].strip()
    definition_zh = translation if translation else (definition if definition else None)
    frq = _int_or_none(row[col["frq"]])
    bnc = _int_or_none(row[col["bnc"]])
    frequency_rank = frq if frq is not None else bnc
    return {
        "lemma": lemma,
        "phonetic": phonetic,
        "definition_zh": definition_zh,
        "example": None,
        "morphemes": None,
        "synonyms": None,
        "frequency_rank": frequency_rank,
        "source": "ecdict",
        "tags": ["cet4"],
    }


def _ecdict_column_indices(header: list[str]) -> dict[str, int]:
    needed = (
        "word",
        "phonetic",
        "definition",
        "translation",
        "pos",
        "tag",
        "bnc",
        "frq",
    )
    lower = {h.strip().lower(): i for i, h in enumerate(header)}
    out: dict[str, int] = {}
    for name in needed:
        if name not in lower:
            raise ValueError(f"ECDICT CSV missing column: {name}")
        out[name] = lower[name]
    return out


def iter_cet4_from_ecdict_rows(
    rows: Iterable[list[str]],
    header: list[str],
) -> Iterator[dict[str, Any]]:
    col = _ecdict_column_indices(header)
    for row in rows:
        rec = record_from_ecdict_row(row, col)
        if rec is not None:
            yield rec


def convert_lyandut_record(record: dict[str, Any]) -> dict[str, Any] | None:
    """Map one lyandut-style JSON object to import format (tags: cet4)."""
    word = record.get("word")
    if not word or not isinstance(word, str):
        return None
    lemma = _norm_lemma(word)
    if lemma is None:
        return None
    phonetic = record.get("phonetic")
    translation = record.get("translation")
    pos = (record.get("pos") or "").strip()
    definition_zh = None
    if translation:
        definition_zh = f"{pos} {translation}".strip() if pos else str(translation)
    return {
        "lemma": lemma,
        "phonetic": phonetic if phonetic else None,
        "definition_zh": definition_zh,
        "example": None,
        "morphemes": None,
        "synonyms": None,
        "frequency_rank": None,
        "source": "lyandut",
        "tags": ["cet4"],
    }


def _load_lyandut_json(data: Any) -> list[dict[str, Any]]:
    records = data if isinstance(data, list) else data.get("words", [])
    out: list[dict[str, Any]] = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        conv = convert_lyandut_record(rec)
        if conv:
            out.append(conv)
    return out


def _load_ecdict_csv_path(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    return list(iter_cet4_from_ecdict_rows(reader, header))


def convert_cet4_to_pack(in_path: Path, out_path: Path) -> int:
    """
    Read ``in_path`` (``.csv`` = ECDICT, ``.json`` = lyandut array / ``words`` wrapper),
    write import-ready JSON array to ``out_path``. Returns number of records written.
    """
    suffix = in_path.suffix.lower()
    if suffix == ".csv":
        records = _load_ecdict_csv_path(in_path)
    elif suffix == ".json":
        data = json.loads(in_path.read_text(encoding="utf-8"))
        records = _load_lyandut_json(data)
    else:
        raise ValueError(f"Unsupported CET-4 input type: {in_path.suffix}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(records)


def fetch_ecdict_cet4_pack(out_path: Path, url: str = ECDICT_CSV_URL) -> int:
    """
    Stream ECDICT CSV from ``url``, keep CET-4 rows, write JSON to ``out_path``.
    Returns number of records written.
    """
    records: list[dict[str, Any]] = []
    with urlopen(url, timeout=600) as resp:  # noqa: S310 — trusted MIT upstream URL
        raw = io.TextIOWrapper(resp, encoding="utf-8", newline="")
        reader = csv.reader(raw)
        header = next(reader)
        for rec in iter_cet4_from_ecdict_rows(reader, header):
            records.append(rec)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(records)
