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

## T8.4 统计：`stats.py`

- **产出**：查询今日完成复习次数、队列剩余长度、连续学习天数（需 `meta` 表存 `last_open_date` 与 streak 逻辑）。

## T8.5 主窗口状态栏或侧栏展示统计

- **产出**：`QStatusBar` 显示「今日已完成 n / 队列 m」。

## T8.6 导出 progress CSV

- **目标**：备份。
- **产出**：菜单「导出学习记录」→ 写 `~/Downloads/english_lean_progress_YYYYMMDD.csv`（lemma + 间隔字段）。

## T8.7 导入/合并（可选，低优先级）

- **说明**：若做则必须文档冲突策略；**可标记为不做** 仅占位。

## T8.8 释义默认展开设置

- **产出**：`QSettings` 存「默认显示中文」开关；启动时应用到 `CardWidget`。

## T8.9 键盘：Enter 提交默写、Ctrl+N 下一张（仅 unlocked）

- **产出**：`QShortcut` 绑定；与按钮 enabled 状态一致。

## T8.10 更新 `docs/plan/roadmap.md` 阶段 2 勾选

- **验收**：已实现项打勾；未做项保留。
