# tasks_05 — 数据访问层与今日学习队列

> 依赖：tasks_02、tasks_03、tasks_04。验收：单测可构造 DB，能列出「今日到期」与「新词」，并能写回 progress。

## T5.1 模块 `repository/words.py`

- **目标**：按 id 取词。
- **产出**：`get_word_by_id(conn, word_id) -> Row | None`。

## T5.2 `repository/progress.py`：读取

- **产出**：`get_progress(conn, word_id)`；`list_due_before(conn, when: datetime) -> list[int]`：`next_review_at <= when` 且非 NULL，或约定「NULL 表示新词可学」——**与 T2.5 文档一致**。

## T5.3 `list_never_seen` 或「新词」谓词

- **目标**：progress 中 `repetitions==0` 且 `last_reviewed_at IS NULL` 等；与产品约定写清。
- **产出**：`list_new_words(conn, limit: int) -> list[int]`。

## T5.4 `update_progress_after_success`

- **目标**：默写对后调用。
- **产出**：接收 `word_id`、当前 `SrsState`、由 T4 算出的新 state与 `next_review_at` ISO；`UPDATE progress SET ...`。

## T5.5 `update_progress_after_fail`

- **目标**：可选：默写错多次后调用 fail路径；或本轮不更新仅留在当前卡——**MVP 可先仅成功时写库**。
- **产出**：若实现：与 T4.5 一致写回。

## T5.6 服务 `study_queue.py`：`build_queue(conn, now, *, due_limit, new_limit) -> list[int]`

- **目标**：合并队列。
- **规则**：**先到期复习**（按 `next_review_at` 升序），再补新词至 `new_limit`；去重 `word_id`。
- **验收**：单测构造3 个到期、2 个新词，`due_limit=10,new_limit=2` 顺序与数量符合预期。

## T5.7 空队列行为

- **目标**：无词可学时有明确返回。
- **产出**：`build_queue` 返回 `[]`；调用方将显示「今日无任务」（T7）。

## T5.8 事务边界

- **目标**：一次复习成功：读-算-写同一连接内完成或显式 `commit()`。
- **产出**：文档或代码注释：`repository` 函数不隐式 commit，由 service 层 `conn.commit()`。

## T5.9 `tests/test_study_queue.py`

- **验收**：使用 `:memory:` 或 `tmp_path`：init → seed少量 words+progress → 断言 `build_queue` 顺序。

## T5.10 本清单门禁

- **验收**：`pytest tests/test_study_queue.py tests/test_import_vocab.py`（若相关）通过；`build_queue` 文档字符串说明 `now` 使用本地时间。
