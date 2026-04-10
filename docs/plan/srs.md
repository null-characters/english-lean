# 间隔复习（首版 SM-2 简化）

## 语义

- **成功**：用户默写正确 → `review_success`。
- **失败**：默写错误且需要记入算法时 → `review_fail`（MVP 也可仅在成功时写库，失败不写）。

## 规则（`english_lean.srs.sm2`）

- **初始状态**：`ease_factor = 2.5`，`interval_days = 0`，`repetitions = 0`。
- **连续成功**：
  - 第1 次成功：间隔 **1** 天；
  - 第 2 次成功：间隔 **6** 天；
  - 之后：`max(1, round(上一间隔 × ease_factor))`。
- **ease_factor**：首版成功/失败均**不调整**，仅做下限 **`1.3`** 钳制。
- **失败**：`repetitions` 置 **0**，`interval_days` 置 **0**，`lapses += 1`，`next_review_at = now`（立即再排）。
- **时间**：`now` 一律由调用方传入本地 `datetime`，模块内不读取系统时钟。

## 与数据库

`next_review_at` 建议存 ISO 8601 文本；由 `review_*` 返回的 `datetime` 转换后写入 `progress`。
