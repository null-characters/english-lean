# tasks_12 — 应用侧：词书切换与按标签过滤队列

> 依赖：tasks_05、tasks_07、**tasks_09**（`words.tags` 可用）。在四级/考研包均可导入后，让用户**只背某一词书**或**全部**。

## T12.1 配置键设计

- **目标**：持久化学习范围。
- **产出**：文档 +常量：如 `study_scope: Literal["all","cet4","kaoyan"]`；映射到 SQL过滤条件（`tags` JSON 含 `"cet4"` / `"kaoyan"`）。

## T12.2 扩展 `build_queue` 签名

- **目标**：可选过滤。
- **产出**：`build_queue(conn, now, *, due_limit=..., new_limit=..., tag: str | None = None)`；`tag is None` 时行为与现网一致。
- **实现提示**：`JOIN words w ON w.id = progress.word_id` + `w.tags LIKE '%"cet4"%'`（若用 JSON 数组字符串）或更稳妥的 JSON 函数（SQLite JSON1需开启）— **首版可用 LIKE约定 tags无子串误匹配**（文档写明 tag 短名）。

## T12.3 扩展 `list_due_before` / `list_new_words`

- **目标**：与 `build_queue` 一致过滤；或仅在 `build_queue` 内联 SQL **二选一**（选一种，删另一种重复逻辑）。
- **验收**：单测 `test_study_queue.py` 增加「仅 cet4」用例。

## T12.4 `StudySession` 接受 `tag_filter`

- **产出**：`StudySession.start(..., tag: str | None = None)` 传入 `build_queue`。

## T12.5 `MainWindow`：词书 `QComboBox`

- **产出**：选项：**全部 / 四级 / 考研**（文案中文）；切换时 `session.start(..., tag=...)` 并 `_render()`；当前卡索引重置为 0。

## T12.6 `QSettings` 持久化

- **产出**：键如 `english_lean/study_scope`；启动恢复 ComboBox。

## T12.7 空队列文案

- **产出**：当过滤后队列为空：`QLabel` 提示「当前词书没有可用单词；请导入对应词包或切换为全部」。

## T12.8 更新 `README.md`

- **产出**：一节「导入四级 / 考研」链到 `docs/data/cet4.md`、`docs/data/kaoyan.md`。

## T12.9 更新 `docs/plan/roadmap.md` 阶段 2

- **产出**：将「新词每日上限」等与词书切换相关的项打勾或注明「见 tasks_12」。

## T12.10 本清单门禁

- **验收**：`pytest`；手工：导入两包后切换词书，队列内容变化；`ruff`。
