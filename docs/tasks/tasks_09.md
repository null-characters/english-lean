# tasks_09 — 外部词库：合规、目录约定与数据模型扩展

> 依赖：tasks_02–03 已完成。与 **tasks_10（四级）**、**tasks_11（考研）** 并行准备；**建议先完成本清单再大规模导入**。每文件 ≤10 条。

## T9.1 新增 `docs/data/SOURCES.md`

- **目标**：集中记录「用哪份公开数据、链接、许可类型、最后人工核对日期」。
- **产出**：`docs/data/SOURCES.md`；含至少两段：**四级候选**、**考研候选**（各 ≥2 个 GitHub/官方链接，附一句许可提醒：以仓库 `LICENSE` 为准）。
- **验收**：文内明确写「发布/商用前须自行复核许可」。

## T9.2 新增 `THIRD_PARTY_NOTICES.md`

- **目标**：合规留痕。
- **产出**：根目录 `THIRD_PARTY_NOTICES.md`：项目名称、摘录许可名、仓库 URL、**不**粘贴整份许可证全文（链到上游即可）。

## T9.3 `words` 表扩展列（迁移）

- **目标**：区分词书来源与标签，供过滤队列。
- **产出**：`src/english_lean/db/migrations/001_words_source_tags.sql`（或等价）对 `words` 增加：`source TEXT`（可选，如 `ecdict` / `netem` / `kylebing`）、`tags TEXT`（建议存 JSON 数组字符串，如 `["cet4"]`）。
- **验收**：新库 `init_db` 或迁移脚本执行后 `PRAGMA table_info(words)` 含两列；**文档**说明老用户升级命令（`sqlite3 english_lean.db < ...`）。

## T9.4 更新 `schema.sql` 与 `init_db` 路径

- **目标**：全新安装与迁移一致。
- **产出**：`schema.sql` 中 `words` 定义包含 `source`、`tags`（默认 NULL）；`tests/test_db_schema.py` 断言新列。

## T9.5扩展 `import_words_from_json`

- **目标**：导入行可带 `source`、`tags`（数组或字符串，**一种约定写死**）。
- **产出**：`import_vocab.py` 写入新列；缺省仍为 NULL。
- **验收**：单测插入一条带 `tags=["cet4"]` 的 JSON，库中可读出。

## T9.6 `data/vocab/external/` 约定

- **目标**：大文件不进 Git。
- **产出**：`data/vocab/external/README.md`（说明：用户或脚本将 `.csv`/`.json` 放此目录）；根目录 `.gitignore` 增加 `data/vocab/external/*` 与 `!data/vocab/external/README.md`（若需保留说明文件）。

## T9.7 更新 `data/vocab/README.md`

- **目标**：与样例 + 外置词库并存说明一致。
- **产出**：指向 `docs/data/SOURCES.md` 与 `external/` 目录。

## T9.8 包目录占位 `src/english_lean/vocab/`

- **目标**：后续 `convert_*.py` 归属清晰。
- **产出**：`src/english_lean/vocab/__init__.py`（可为空或 re-export）。

## T9.9 合规检查清单（文档）

- **产出**：`docs/data/SOURCES.md` 末尾 **Checklist**：下载文件名、SHA（可选）、LICENSE 打开确认、是否允许离线分发合并后的 JSON。

## T9.10 本清单门禁

- **验收**：`pytest` 全绿；`ruff check` 通过；新迁移/ schema 在干净 DB 上可重复执行。
