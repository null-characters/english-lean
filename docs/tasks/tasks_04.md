# tasks_04 — 间隔复习（SM-2）纯逻辑与单测

> 依赖：无 DB（仅纯函数）。验收：`pytest tests/test_srs.py` 全绿；时间与间隔可预测。

## T4.1 模块 `srs/sm2.py`文件创建

- **目标**：算法与 UI/DB 解耦。
- **产出**：`src/english_lean/srs/sm2.py`。

## T4.2 定义状态数据类或 TypedDict

- **目标**：类型清晰。
- **产出**：如 `@dataclass class SrsState:`字段：`ease_factor: float`、`interval_days: int`、`repetitions: int`；可选 `lapses: int`。

## T4.3 初值工厂 `new_state() -> SrsState`

- **目标**：与新词一致。
- **验收**：`ease_factor == 2.5`，`interval_days == 0`，`repetitions == 0`。

## T4.4 成功路径 `review_success(state, now) -> tuple[SrsState, next_review_at]`

- **目标**：默写正确时调用。
- **规则**（与 overview 一致，可文档化）：首成功 `interval=1` 天；随后按 SM-2：`interval = round(prev_interval * ease_factor)`（首两次可按 Anki 简化：rep0→1d, rep1→6d，再乘 EF）；`repetitions += 1`；`ease_factor` 成功时不变或微调（首版可 **不变** 以降低复杂度）。
- **产出**：`next_review_at` 为 `datetime` 或 ISO 字符串，由调用方写入 DB。
- **验收**：单测给定固定 `now`，断言间隔序列合理（至少覆盖第 1、2、3 次成功）。

## T4.5 失败路径 `review_fail(state, now) -> tuple[SrsState, next_review_at]`

- **目标**：默写错或「未记住」时调用（本应用默写错不更新成功，但可调用 fail 缩短间隔）。
- **规则**：`repetitions = 0` 或减 1；`interval_days` 置为 0 或 1；`lapses += 1`；`next_review_at = now` 或 `now + 1 分钟`（同日再出现）——**在单测与文档中固定一种**。

## T4.6 边界：EF 下限

- **目标**：防止除零或负间隔。
- **规则**：`ease_factor` 不低于 `1.3`（常见 SM-2 实现）。

## T4.7 纯函数：不读系统时钟（可选）

- **目标**：可测性。
- **要求**：`now` 由参数传入；禁止在 `sm2.py` 内调用 `datetime.now()`（或仅包装函数 `review_success_at_now` 调用于非测试路径）。

## T4.8 `tests/test_srs_sm2.py`：成功三次

- **验收**：三次 `review_success` 后 `repetitions == 3` 且 `interval_days` 递增或符合固定表。

## T4.9 `tests/test_srs_sm2.py`：失败后重置

- **验收**：成功一次后 `review_fail`，`repetitions` 与 `interval` 符合 T4.5。

## T4.10 文档 `docs/plan/srs.md`（短）

- **目标**：人与 AI 对齐公式。
- **产出**：`docs/plan/srs.md` ≤ 40 行：成功/失败语义、与「默写对/错」的映射、首版是否简化 EF。
