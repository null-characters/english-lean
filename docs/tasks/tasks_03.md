# tasks_03 — 离线词库样例与导入

> 依赖：tasks_02。验收：导入后 `words` 行数 ≥ 20，lemma 唯一；可重复导入不爆炸。

## T3.1 数据目录与样例 JSON

- **目标**：版本化小词表。
- **产出**：`data/vocab/sample_cet4.json`（或 `jsonl`），**至少 20 条**；每条字段：`lemma`（必填）、`phonetic`、`definition_zh`、`example`、`morphemes`、`synonyms`、`frequency_rank`；允许部分为 `null` 或省略。

## T3.2 JSON Schema 或注释约定

- **目标**：避免导入歧义。
- **产出**：`data/vocab/README.md` 一行说明字段含义；或在 `sample_cet4.json` 顶部用 `_comment` 键（sqlite 导入前过滤）。

## T3.3 模块 `db/import_vocab.py`

- **目标**：幂等导入。
- **产出**：函数 `import_words_from_json(conn: sqlite3.Connection, path: Path) -> int`：返回新增行数；已存在 `lemma` 用 `INSERT OR IGNORE` 或 `ON CONFLICT(lemma) DO NOTHING`。

## T3.4 导入后为无 progress 的词建 progress行（可选策略）

- **目标**：新词可进入队列。
- **产出**：导入后触发 `ensure_progress_rows(conn)`：`INSERT INTO progress(word_id, ...) SELECT id, 2.5, 0, 0, NULL, ... FROM words WHERE id NOT IN (SELECT word_id FROM progress)`（具体列与 T2.5 一致）。
- **验收**：`words` 与 `progress` 行数相等（在仅本导入场景下）。

## T3.5 CLI 小入口或开发用脚本

- **目标**：手动重建库时可用。
- **产出**：`python -m english_lean.tools.seed`或 `scripts/seed_db.py`（二选一）：`init_db` + 导入 `sample_cet4.json`；**不**强制进正式 `main`（避免拖慢启动），文档说明即可。

## T3.6 单测 `tests/test_import_vocab.py`

- **目标**：导入逻辑可回归。
- **验收**：内存库 `init_db` → `import_words_from_json` → `assert count(words) >= 20`；第二次导入 `新增 == 0`。

## T3.7 样例内容质量（手工）

- **目标**：覆盖展示字段。
- **要求**：20 条中至少 5 条含非空 `example`；至少 3 条含非空 `morphemes` 或 `synonyms`（用于 UI 折叠测试）。

## T3.8 `lemma` 规范化

- **目标**：默写比对稳定。
- **产出**：导入时 `lemma.strip()`，拒绝空字符串；文档写明存储为小写或原样（与 T4/T6 校验一致）。

## T3.9 大包词表占位（不实现）

- **目标**：为未来扩展留接口。
- **产出**：`docs/plan/overview.md` 或 `data/vocab/README.md` 一句：正式 CET-4 大表可替换 JSON 或单独迁移脚本，**本任务不引入大文件**。

## T3.10 本清单门禁

- **验收**：`pytest tests/test_import_vocab.py` 通过；本地运行 seed 脚本后 `sqlite3` `SELECT COUNT(*) FROM words` ≥ 20。
