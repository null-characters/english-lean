# 路线图

## 阶段 0：仓库与规划

- [x] Git 与远程仓库
- [x] `docs/plan` 规划目录与概览文档

## 阶段 1：MVP（可每日使用）

- [x] 选定技术栈并初始化工程（Python + PySide6，见 `pyproject.toml`）
- [x] 离线词库：样例 JSON + SQLite Schema + 导入（`data/vocab/`，用户目录 `english_lean.db`）
- [x] 卡片界面：单词、中文释义折叠、例句/词根/近义词按需展示
- [x] 文本默写 + 校验；**未通过则禁止下一张**
- [x] 学习状态表 + **本地时间**下的到期队列（`build_queue` / `list_due_before`）
- [x] 间隔复习 v1：SM-2 简化（见 `docs/plan/srs.md`）

## 阶段 2：体验与可靠

- [x] 词书切换：按 ``words.tags`` 过滤学习队列（四级 / 考研 / 全部），见 `tasks_12`
- [x] 新词每日上限（`study_meta` + `config/study_settings.py`）；复习优先策略（到期优先于新词；`build_queue` 已到期优先）
- [x] 简单统计：连续天数、今日完成量、队列长度（状态栏 + `services/stats.py` + `study_meta` streak）
- [x] 数据备份/导出（`~/Downloads/english_lean_progress_YYYYMMDD.csv`，见 tasks_08 T8.6）

## 阶段 3：增强（按需）

- [ ] 释义折叠/自评粒度（若引入除默写外的记忆质量信号）
- [ ] 易混词专项或更细标签筛选（基础按考试标签筛选已在 tasks_12）
- [ ] 主题与字体、窗口布局记忆

---

**当前焦点**：阶段 2（统计、每日新词上限等，见 `tasks_08.md`）。
