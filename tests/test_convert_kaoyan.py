"""Kaoyan / NETEM converter tests (offline fixtures only)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from english_lean.vocab.convert_kaoyan import (
    convert_kaoyan_to_pack,
    record_from_netem_item,
)

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "kaoyan_fragment.json"


def test_convert_kaoyan_to_pack_fixture(tmp_path: Path) -> None:
    out = tmp_path / "out.json"
    n = convert_kaoyan_to_pack(FIXTURE_JSON, out)
    assert n == 14
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 14
    assert data[0]["lemma"] == "the"
    assert data[0]["source"] == "netem"
    assert data[0]["tags"] == ["kaoyan", "netem"]
    assert data[0]["frequency_rank"] == 1
    assert data[0]["definition_zh"] == "这个、这些"
    lemmas = [x["lemma"] for x in data]
    assert all(x == x.lower() for x in lemmas)
    nonempty_zh = sum(1 for x in data if x.get("definition_zh"))
    assert nonempty_zh == 14


def test_convert_kaoyan_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        convert_kaoyan_to_pack(tmp_path / "nope.json", tmp_path / "out.json")


def test_record_from_netem_item_skips_bad_word() -> None:
    assert record_from_netem_item({"序号": 1, "单词": "", "释义": "x"}) is None
    assert record_from_netem_item({"序号": 1, "释义": "x"}) is None


def test_record_from_netem_item_optional_definition() -> None:
    r = record_from_netem_item({"序号": 99, "单词": "testword", "释义": ""})
    assert r is not None
    assert r["lemma"] == "testword"
    assert r["definition_zh"] is None
