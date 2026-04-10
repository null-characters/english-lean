# tasks_11 — 考研英语（NETEM 等）公开词库：获取、转换、导入

> 依赖：tasks_09（建议）。与 tasks_10 **对称**；四级与考研 **数据源、转换器分离**，避免一个脚本里堆满 if。

## T11.1 锁定考研「首选数据源」并写入文档

- **目标**：可执行、可审计。
- **产出**：`docs/data/SOURCES.md` 小节 **「考研 — 已选方案」**：例如 [exam-data/NETEMVocabulary](https://github.com/exam-data/NETEMVocabulary) 的 `netem_full_list.json`，或 KyleBing 考研目录；注明 **LICENSE以仓库为准**、大文件不随本仓库分发。

## T11.2 新增 `docs/data/kaoyan.md`

- **产出**：下载/Release 链接、`external/` 建议文件名、上游 JSON 顶层结构说明（数组还是 `{"words":...}`）、字段到 `lemma` / `definition_zh` / `example` 的映射表。

## T11.3 实现 `src/english_lean/vocab/convert_kaoyan.py`

- **目标**：`convert_kaoyan_to_pack(in_path: Path, out_path: Path) -> int`。
- **输出 JSON**：`source` 填 `netem`（或实际来源名）、`tags` 含 `kaoyan`（或 `netem`+`kaoyan`，**一种约定写进文档**）。
- **验收**：对 fixture 可运行；缺字段时不崩溃（置 NULL）。

## T11.4 测试夹具 `tests/fixtures/kaoyan_fragment.json`

- **产出**：从上游结构**手工裁剪**的 ≥12 条（勿整库）；若上游字段名与公开样本不一致，夹具按**最终解析器**期望来写。

## T11.5 单测 `tests/test_convert_kaoyan.py`

- **验收**：条数、`tags`/`source`、**中文释义**非空比例（可对 fixture 断言固定 key）。

## T11.6 CLI `python -m english_lean.tools.import_kaoyan`

- **产出**：`--input` / `--output`；错误处理同 tasks_10。

## T11.7 与四级共存策略（文档）

- **产出**：`docs/data/kaoyan.md` 或 `SOURCES.md`：同一 `lemma` 两条记录时当前行为（IGNORE）；未来「合并 tags」指向 tasks_12。

## T11.8 可选：`tools/download_kaoyan.py`

- **目标**：仅当上游许可允许自动化拉取 raw。
- **产出**：`urllib` 或 `curl` 子进程；**默认不执行**；需显式 flag `--i-have-checked-license`；否则打印「请手动下载」。

## T11.9 导入后抽检 SQL（文档）

- **产出**：`docs/data/kaoyan.md` 末尾：`SELECT COUNT(*) FROM words WHERE tags LIKE '%kaoyan%';`

## T11.10 本清单门禁

- **验收**：`pytest tests/test_convert_kaoyan.py`；`ruff`；不在仓库内添加 >1MB 未授权二进制。
