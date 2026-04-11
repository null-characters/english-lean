# tasks_08 — 阶段二（可选）：策略、统计、导出

> 依赖：tasks_07 MVP 完成后按需执行。每任务仍保持小步；本文件 ≤10 条。

## T8.1 配置模块 `config.py`

- **目标**：可调参数集中。
- **产出**：`NEW_WORDS_PER_DAY`、`DUE_LIMIT` 等常量或 `pydantic`/`toml` 读取（首版常量即可）。
- **状态**：已实现 — `src/english_lean/config/study_settings.py`（`DUE_LIMIT`、`DEFAULT_NEW_WORD_LIMIT`、`NEW_WORDS_PER_DAY`）。

## T8.2 新词每日上限

- **目标**：防一次塞太多新词。
- **产出**：`progress` 或单独 `meta` 表记录 `last_study_date` 与 `new_words_today`；跨本地日历日重置（用 `date.today()`）。
- **状态**：已实现 — `study_meta` 键值表、`repository/study_meta.py`；`StudySession.start` 用 `effective_new_word_limit`；首次复习成功时 `increment_new_words_today`。

## T8.3 复习优先于新词（强化）

- **目标**：与 overview 一致。
- **产出**：调整 `build_queue` 策略并补单测。
- **状态**：已强化单测 `test_build_queue_due_words_always_before_new_regardless_of_word_id`；策略仍为到期先于新词。

## T8.4 统计：`stats.py`

- **产出**：查询今日完成复习次数、队列剩余长度、连续学习天数（需 `meta` 表存 `last_open_date` 与 streak 逻辑）。
- **状态**：已实现 — `services/stats.py`（`review_count_on_local_day`、`session_cards_remaining`）；`study_meta` 增加 `last_open_date` / `streak_days` 与 `record_streak_on_open`。

## T8.5 主窗口状态栏或侧栏展示统计

- **产出**：`QStatusBar` 显示「今日已完成 n / 队列 m」。
- **状态**：已实现 — 底部状态栏文案：`今日已完成 n 次复习 · 本局队列剩余 m 张 · 连续 d 天`。

## T8.6 导出 progress CSV

- **目标**：备份。
- **产出**：菜单「导出学习记录」→ 写 `~/Downloads/english_lean_progress_YYYYMMDD.csv`（lemma + 间隔字段）。
- **状态**：已实现 — 「文件 → 导出学习记录…」，`export_progress_csv`（UTF-8 BOM）。

## T8.7 导入/合并（可选，低优先级）

- **说明**：若做则必须文档冲突策略；**可标记为不做** 仅占位。
- **状态**：跳过（未实现）。

## T8.8 释义默认展开设置

- **产出**：`QSettings` 存「默认显示中文」开关；启动时应用到 `CardWidget`。
- **状态**：已实现 — 键 `show_definition_default`；「设置 → 默认显示中文释义」。

## T8.9 键盘：Enter 提交默写、Ctrl+N 下一张（仅 unlocked）

- **产出**：`QShortcut` 绑定；与按钮 enabled 状态一致。
- **状态**：`Ctrl+N` 快捷键至「下一张」（与按钮相同 gate）；默写框内 **Enter** 沿用 `QLineEdit.returnPressed` → 检查（与「检查」按钮一致）。

## T8.10 更新 `docs/plan/roadmap.md` 阶段 2 勾选

- **验收**：已实现项打勾；未做项保留。
- **状态**：已更新。
