# 生成的词包（不纳入 Git）

`python -m english_lean.tools.import_cet4` 默认将 **CET-4 词包** 写入本目录下的 `cet4_pack.json`（见 `docs/data/cet4.md`）。

该目录中的 `*.json` 已在根目录 `.gitignore` 中忽略，避免误提交大体积文件。可将生成的 JSON 再通过 `python -m english_lean.tools.seed <路径>` 导入本机 SQLite。
