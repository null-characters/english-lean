# tasks_02 — SQLite：路径、表结构、初始化

> 依赖：tasks_01 完成。验收：临时目录可初始化 DB，含 `words` / `progress`，外键与索引生效。

## T2.1 依赖 `platformdirs`

- **目标**：用户数据目录可移植。
- **产出**：`pyproject.toml` 增加依赖 `platformdirs`。
- **验收**：`pip install -e .` 后可 `import platformdirs`。

## T2.2 模块 `db/paths.py`

- **目标**：统一 DB 文件路径。
- **产出**：`src/english_lean/db/paths.py`，函数 `get_db_path() -> Path`：使用 `platformdirs.user_data_dir("english-lean", appauthor=False)`，确保父目录存在，返回 `.../english_lean.db`（文件名可常量）。

## T2.3 DDL 文件 `schema.sql`

- **目标**：表结构可审阅、可版本化。
- **产出**：`src/english_lean/db/schema.sql`，含 `CREATE TABLE IF NOT EXISTS words (...)` 与 `progress (...)`。

## T2.4 `words` 表字段

- **列**（可按实现微调名称，但与后续任务一致）：`id INTEGER PRIMARY KEY`；`lemma TEXT NOT NULL UNIQUE`；`phonetic TEXT`；`definition_zh TEXT`；`example TEXT`；`morphemes TEXT`；`synonyms TEXT`；`frequency_rank INTEGER`（可 NULL）。
- **验收**：DDL 可被 `sqlite3` 执行无语法错误。

## T2.5 `progress` 表字段

- **列**：`word_id INTEGER PRIMARY KEY REFERENCES words(id) ON DELETE CASCADE`；`ease_factor REAL NOT NULL`；`interval_days INTEGER NOT NULL`；`repetitions INTEGER NOT NULL`；`next_review_at TEXT`（ISO8601 本地或 UTC，文档注释约定）；`last_reviewed_at TEXT`；`lapses INTEGER NOT NULL DEFAULT 0`；`created_at TEXT`（可选）。
- **初值约定**：新词插入 progress 时 `ease_factor=2.5`，`interval_days=0`，`repetitions=0`，`next_review_at` 可为 NULL 表示「从未学」或「立即可学」——在 T5 写清查询规则。

## T2.6 `get_connection()` 与 PRAGMA

- **目标**：安全连接与行工厂。
- **产出**：`src/english_lean/db/__init__.py` 或 `connection.py`：`get_connection(path: Path | None = None) -> sqlite3.Connection`；默认路径 `get_db_path()`；执行 `PRAGMA foreign_keys = ON`；`row_factory = sqlite3.Row`。

## T2.7 `init_db(conn) -> None`

- **目标**：首次创建表。
- **产出**：读取包内 `schema.sql`（`importlib.resources` 或相对路径）并 `executescript`。
- **验收**：对内存 `:memory:` 连接调用后 `SELECT name FROM sqlite_master WHERE type='table'` 含 `words`、`progress`。

## T2.8 `ensure_schema` 幂等

- **目标**：重复启动不报错。
- **验收**：同一文件路径连续调用 `init_db` 两次无异常；表不重复。

## T2.9 索引

- **产出**：在 `schema.sql` 中 `CREATE INDEX IF NOT EXISTS idx_progress_next ON progress(next_review_at)`；`CREATE INDEX IF NOT EXISTS idx_words_lemma ON words(lemma)`。

## T2.10 单测 `tests/test_db_schema.py`

- **目标**：自动化验证结构。
- **验收**：临时 `tmp_path` 下创建 db文件 → `init_db` → 用 `conn.execute("PRAGMA table_info(words)")` 等断言关键列存在；`PRAGMA foreign_key_check` 通过。
