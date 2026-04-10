# tasks_10 — 四级（CET-4）公开词库：获取、转换、导入

> 依赖：tasks_09（建议）。目标：用户在本机放置**许可合规**的四级相关文件后，一键生成可 `import_words_from_json` 的包。**不**在任务中假设已侵权复制牛津等内容。

## T10.1 锁定四级「首选数据源」并写入文档

- **目标**：避免实现中途换马。
- **产出**：在 `docs/data/SOURCES.md` 增加小节 **「四级 — 已选方案」**：例如 *ECDICT 筛选 CET4 标签* 或 *KyleBing `english-vocabulary` 中 CET4 JSON*（二选一或主备）；写清**不随仓库分发**大文件，由用户下载。

## T10.2 新增 `docs/data/cet4.md`

- **目标**：可重复的人工/脚本步骤。
- **产出**：下载页链接、`external/` 下建议文件名、**最小**可用样本行说明；若用 ECDICT，写明用哪一列作 `lemma`、哪一列作 `definition_zh`。

## T10.3 实现 `src/english_lean/vocab/convert_cet4.py`

- **目标**：单一入口函数，如 `convert_cet4_to_pack(in_path: Path, out_path: Path) -> int`（返回导出条数）。
- **输入**：一种格式（优先 JSON；若 CSV 则 `csv` 模块）；**输出**：符合现有 `import_words_from_json` 的 JSON 数组（含 `source`/`tags`：`cet4`）。
- **验收**：对 **fixture**（小文件）运行后 `json.load` 合法且每条有 `lemma`。

## T10.4 新增测试夹具 `tests/fixtures/cet4_fragment.json`（或 `.csv`）

- **目标**：CI 不依赖外网大文件。
- **产出**：≥15 条代表性片段（含缺省字段）；**禁止**提交完整书稿。

## T10.5 单测 `tests/test_convert_cet4.py`

- **目标**：回归映射逻辑。
- **验收**：`convert_cet4_to_pack(fixture, tmp_path / "out.json")`；断言条数、首条 `lemma` 小写、`tags` 含 `cet4`。

## T10.6 CLI 包装 `python -m english_lean.tools.import_cet4`

- **目标**：与 `seed` 并列。
- **产出**：参数 `--input`（默认 `data/vocab/external/cet4_raw.*`）、`--output`（默认 `data/vocab/generated/cet4_pack.json`）；打印条数；**输入不存在**时退出码非 0 且中文错误信息。

## T10.7 `.gitignore` 忽略 `data/vocab/generated/*.json`（可选）

- **目标**：生成物可很大时不误提交。
- **产出**：若忽略，则在 `cet4.md` 写明生成路径。

## T10.8 文档：与现有 `import_words_from_json` 衔接

- **产出**：`README.md` 或 `docs/data/cet4.md` 增加：`sqlite3` / `python -c` 调用导入，或 `python -m english_lean.tools.seed --merge cet4_pack.json`（若实现 merge 子命令则写清；**未实现则仅文档手写步骤**）。

## T10.9 同形异义 / 重复 `lemma` 策略（文档 + 代码注释）

- **产出**：约定沿用 `INSERT OR IGNORE`：**先导入者优先**；若需合并标签，拆到 **tasks_12** 或本任务末尾 **不实现** 仅记 TODO。

## T10.10 本清单门禁

- **验收**：`pytest tests/test_convert_cet4.py`；`ruff`；人工用 fixture 跑通 CLI 一次（可在 CI 用 tmp）。
