"""CET-4 converter tests (offline fixtures only)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from english_lean.vocab.convert_cet4 import convert_cet4_to_pack

FIXTURE_CSV = Path(__file__).resolve().parent / "fixtures" / "cet4_fragment.csv"


def test_convert_cet4_to_pack_csv_fixture(tmp_path: Path) -> None:
    out = tmp_path / "out.json"
    n = convert_cet4_to_pack(FIXTURE_CSV, out)
    assert n == 12
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 12
    assert data[0]["lemma"] == "abandon"
    assert data[0]["tags"] == ["cet4"]
    assert data[0]["source"] == "ecdict"
    lemmas = [x["lemma"] for x in data]
    assert all(x == x.lower() for x in lemmas)
    assert "cet4" in data[0]["tags"]


def test_convert_cet4_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        convert_cet4_to_pack(tmp_path / "nope.csv", tmp_path / "out.json")
