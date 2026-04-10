# tasks_06 — 卡片 UI、默写区、释义展开

> 依赖：tasks_01。可与 tasks_05 并行开发，但 **T7 联调** 前需完成。验收：不连 DB 也可用假数据演示交互。

## T6.1 模块 `ui/card_widget.py`（或 `widgets/card.py`）

- **目标**：单卡展示。
- **产出**：`QWidget` 子类，构造函数接受：`lemma: str`、`definition_zh: str`、可选 `phonetic`、`example`、`morphemes`、`synonyms`。

## T6.2 布局：单词主标题

- **目标**：可读性。
- **产出**：`QLabel` 大字显示 `lemma`；可选音标小字。

## T6.3 释义折叠

- **目标**：减少偷看。
- **产出**：默认隐藏中文义；`QPushButton`「显示/隐藏释义」切换 `definition_zh` 可见性。

## T6.4 扩展区折叠

- **目标**：有内容才显示区块。
- **规则**：`example`/`morphemes`/`synonyms` 为空则隐藏对应 `QGroupBox` 或 `QLabel`。

## T6.5 模块 `ui/dictation_widget.py`

- **目标**：输入与提交。
- **产出**：`QLineEdit` + `QPushButton`「检查」或回车提交；信号 `submitted(str)`。

## T6.6 校验函数 `normalize_answer(s: str) -> str`

- **目标**：与 overview 一致。
- **产出**：`src/english_lean/quiz/validate.py`：`strip()` + **与词表约定一致的大小写**（推荐：比较时双方 `.lower()`）。

## T6.7 `check_spelling(user_input, expected_lemma) -> bool`

- **产出**：调用 `normalize_answer`，相等则 True。

## T6.8 视觉反馈

- **目标**：对错可感知。
- **产出**：错误时 `QLineEdit` 旁 `QLabel` 红色「再试一次」；正确时绿色「正确」或清除错误（具体样式简化即可）。

## T6.9 信号：`dictation_correct` / `dictation_wrong`

- **目标**：主窗口可门禁。
- **产出**：`DictationWidget` 在校验后 emit；**不**自动清空输入（可清空由主窗口决定）。

## T6.10 假数据演示 `if __name__ == "__main__"` 或 `tools/ui_preview.py`

- **目标**：人工验收 UI。
- **验收**：独立运行可看到一张卡 + 默写；输对 emit正确信号（打印或弹窗）。
