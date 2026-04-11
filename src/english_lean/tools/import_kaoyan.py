"""CLI: build Kaoyan (NETEM) JSON pack for ``import_words_from_json``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from english_lean.vocab.convert_kaoyan import (
    NETEM_JSON_URL,
    convert_kaoyan_to_pack,
    fetch_netem_kaoyan_pack,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_output() -> Path:
    return _repo_root() / "data" / "vocab" / "generated" / "kaoyan_pack.json"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="生成考研（NETEM）词包 JSON（供 import_words_from_json 导入）",
    )
    p.add_argument(
        "--input",
        type=Path,
        default=None,
        help="本地 netem_full_list.json。省略则从上游 Raw 下载。",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=_default_output(),
        help=f"输出 JSON 路径（默认：{_default_output()}）",
    )
    p.add_argument(
        "--url",
        default=NETEM_JSON_URL,
        help="未指定 --input 时使用的 NETEM JSON URL",
    )
    args = p.parse_args(argv)

    out = args.output.resolve()
    try:
        in_path = args.input
        if in_path is None:
            n = fetch_netem_kaoyan_pack(out, url=args.url)
            print(f"已从网络生成考研词包：{n} 条 → {out}")
            return 0
        in_path = in_path.resolve()
        if not in_path.is_file():
            print(f"错误：找不到输入文件：{in_path}", file=sys.stderr)
            return 2
        n = convert_kaoyan_to_pack(in_path, out)
        print(f"已生成考研词包：{n} 条 → {out}")
        return 0
    except OSError as e:
        print(f"错误：网络或文件读写失败：{e}", file=sys.stderr)
        return 3
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 4
    except json.JSONDecodeError as e:
        print(f"错误：JSON 解析失败：{e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
