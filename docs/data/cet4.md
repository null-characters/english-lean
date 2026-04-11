# CET-4 四级词库：生成与导入

首选 **MIT 许可的 ECDICT**（`skywind3000/ECDICT`），从官方 `ecdict.csv` **流式下载**并筛选 `tag` 中含 `cet4` 的词条，无需手动下载大文件。

---

## 一键生成词包（推荐）

在项目根目录执行（需联网，首次会下载完整 CSV，体积约数十 MB，请耐心等待）：

```bash
python -m english_lean.tools.import_cet4
```

- **默认行为**：从 `ECDICT_CSV_URL`（见 `english_lean.vocab.convert_cet4`）拉取 CSV，筛选 CET-4，写出  
  `data/vocab/generated/cet4_pack.json`
- **自定义输出**：`python -m english_lean.tools.import_cet4 --output /path/to/cet4_pack.json`
- **自备 CSV**：`python -m english_lean.tools.import_cet4 --input /path/to/ecdict.csv`（ECDICT 标准列名）
- **自备 lyandut 风格 JSON**：`--input ./foo.json`（根为数组或 `{ "words": [...] }`，字段见下文）

生成目录说明见 `data/vocab/generated/README.md`（生成物默认 **不纳入 Git**）。

---

## ECDICT CSV 字段（官方）

| 列名 | 用途 |
|------|------|
| `word` | 词形 → 导入为 `lemma`（小写） |
| `phonetic` | 音标 |
| `translation` | 中文释义（优先作为 `definition_zh`） |
| `definition` | 英文释义（`translation` 为空时用作 `definition_zh`） |
| `tag` | 空格分隔标签；含 `cet4` 则视为四级大纲词 |
| `frq` / `bnc` | 当代 / BNC 词频序，用于 `frequency_rank`（优先 `frq`） |

---

## lyandut 风格 JSON（可选）

若 `--input` 为 `.json`，按数组元素字段映射：

| 原始字段 | 项目字段 |
|----------|----------|
| `word` | `lemma`（小写） |
| `phonetic` | `phonetic` |
| `translation` + `pos` | `definition_zh` |
| 固定 | `source` = `lyandut`，`tags` = `["cet4"]` |

---

## 导入到本机 SQLite

生成 `cet4_pack.json` 后：

```bash
python -m english_lean.tools.seed data/vocab/generated/cet4_pack.json
```

未传参数时 `seed` 仍默认导入仓库内小样例 `data/vocab/sample_cet4.json`。

---

## 重复词条与同形异义

导入 SQLite 时使用 `INSERT OR IGNORE`，**先写入者优先**；同一 `lemma` 后出现重复行会被忽略。若需合并多词书的 `tags`，见后续 tasks_12 / 路线图。

---

*最后更新：2026-04-11*
