# 离线词表数据

字段：`lemma`（必填，导入时会 `strip` 并**存为小写**）、`phonetic`、`definition_zh`、`example`、`morphemes`、`synonyms`、`frequency_rank`（均可省略或 `null`）。JSON 根为**数组**；可含 `_comment` 键的对象会被跳过。

正式 CET-4 大表可替换本目录下的 JSON或使用单独迁移脚本导入 SQLite；**仓库内仅保留小样例**，不引入大文件。
