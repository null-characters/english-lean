"""CLI: build CET-4 JSON pack for ``import_words_from_json`` (ECDICT MIT or local CSV/JSON)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from english_lean.vocab.convert_cet4 import (
    ECDICT_CSV_URL,
    convert_cet4_to_pack,
    fetch_ecdict_cet4_pack,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_output() -> Path:
    return _repo_root() / "data" / "vocab" / "generated" / "cet4_pack.json"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="生成四级（CET-4）词包 JSON（供 import_words_from_json 导入）",
    )
    p.add_argument(
        "--input",
        type=Path,
        default=None,
        help="本地源文件：.csv（ECDICT 格式）或 .json（lyandut 格式）。省略则从网络拉取 ECDICT。",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=_default_output(),
        help=f"输出 JSON 路径（默认：{_default_output()}）",
    )
    p.add_argument(
        "--url",
        default=ECDICT_CSV_URL,
        help="未指定 --input 时使用的 ECDICT CSV URL（默认官方 raw 主表）",
    )
    args = p.parse_args(argv)

    out = args.output.resolve()
    try:
        in_path = args.input
        if in_path is None:
            n = fetch_ecdict_cet4_pack(out, url=args.url)
            print(f"已从网络生成 CET-4 词包：{n} 条 → {out}")
            return 0
        in_path = in_path.resolve()
        if not in_path.is_file():
            print(f"错误：找不到输入文件：{in_path}", file=sys.stderr)
            return 2
        n = convert_cet4_to_pack(in_path, out)
        print(f"已生成 CET-4 词包：{n} 条 → {out}")
        return 0
    except OSError as e:
        print(f"错误：网络或文件读写失败：{e}", file=sys.stderr)
        return 3
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
