# tasks_07 — 主窗口会话：数据库、门禁、下一张、MVP 收尾

> 依赖：tasks_01–06。验收：真实 DB 跑通「队列 → 展示 → 默写对 → 更新 progress → 下一张」；默写错无法下一张。

## T7.1 `SessionState` 或控制器类

- **目标**：集中管理当前索引与队列。
- **产出**：`src/english_lean/session/controller.py`：`StudySession` 持有 `conn`、`queue: list[int]`、`index: int`、`unlocked: bool`（本卡是否已因默写通过解锁）。

## T7.2 启动时 `init_db` + `import`（若空）

- **目标**：首次打开可用。
- **产出**：`main` 或 `AppContext`：`get_connection()` → `init_db` → `SELECT COUNT(*) FROM words` 为 0 则调用 seed/import（与 T3.5 一致）。

## T7.3 构建队列并加载首张

- **产出**：`StudySession.start(now)` 调用 `build_queue`，加载 `get_word_by_id` 填 `CardWidget`。

## T7.4 绑定默写信号

- **规则**：`submitted` → `check_spelling`；错：`unlocked=False`，禁用「下一张」；对：调用 `update_progress_after_success` + `commit`，`unlocked=True`，启用「下一张」。

## T7.5 「下一张」按钮与快捷键

- **目标**：显式导航（滑动可后续）。
- **产出**：`QPushButton`「下一张」：`unlocked` 为 False 时 `setEnabled(False)`；为 True 时 `index+=1` 加载下一词并重置默写区与 `unlocked=False`。

## T7.6 队列结束

- **产出**：`index >= len(queue)` 时显示「今日完成」占位，禁用默写与下一张。

## T7.7 错误处理：DB 只读或损坏

- **目标**：不静默崩溃。
- **产出**：`try/except sqlite3.Error`：`QMessageBox.critical` 一条可读中文错误（MVP 级）。

## T7.8窗口关闭时 `conn.close()`

- **验收**：无句柄泄漏；可选 `commit` 在每次成功后已调用。

## T7.9 手工验收脚本（清单）

- **产出**：`docs/tasks/README.md` 或本文件附录：步骤 1 删库 2 启动 3 默写错 4 确认不能下一张 5 默写对 6 下一张 7 重启验证 `next_review_at`（高级，可选）。

## T7.10 MVP 定义完成

- **目标**：与 `docs/plan/roadmap.md` 阶段 1 对齐。
- **产出**：在 `docs/plan/roadmap.md` 将阶段 1 项勾选或链接至本 tasks；提交一版「MVP done」说明。
