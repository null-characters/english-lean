"""Seed the user database from bundled sample vocabulary (dev / first run)."""

from __future__ import annotations

import argparse
from pathlib import Path

from english_lean.db.connection import get_connection, init_db
from english_lean.db.import_vocab import import_words_from_json


def _repo_root() -> Path:
    # english_lean/tools/seed.py -> parents[3] = repository root
    return Path(__file__).resolve().parents[3]


def default_sample_path() -> Path:
    return _repo_root() / "data" / "vocab" / "sample_cet4.json"


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="将词库 JSON 导入本机用户数据目录下的 SQLite")
    p.add_argument(
        "vocab",
        nargs="?",
        type=Path,
        default=None,
        help="词库 JSON 路径（默认：仓库内样例 data/vocab/sample_cet4.json）",
    )
    args = p.parse_args(argv)
    path = args.vocab.resolve() if args.vocab is not None else default_sample_path()
    if not path.is_file():
        raise SystemExit(f"找不到词库文件：{path}")

    conn = get_connection()
    try:
        init_db(conn)
        added = import_words_from_json(conn, path)
        print(f"Seed done. New word rows inserted this run: {added}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
