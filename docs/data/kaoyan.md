# 考研英语（NETEM）词库：生成与导入

首选上游为 **[exam-data/NETEMVocabulary](https://github.com/exam-data/NETEMVocabulary)** 的 **`netem_full_list.json`**。许可与锁定说明见 [`SOURCES.md`](./SOURCES.md) 中 **「考研英语 — 已选方案」**；**数据**为 **CC BY-NC-SA 4.0**（以仓库 `LICENSE` 为准），**非 MIT**。

---

## 上游位置与建议本地路径

| 说明 | 地址 / 路径 |
|------|-------------|
| 仓库 | https://github.com/exam-data/NETEMVocabulary |
| 主文件（分支 `master`） | `netem_full_list.json` |
| Raw（便于下载或 CLI 拉取） | `https://raw.githubusercontent.com/exam-data/NETEMVocabulary/master/netem_full_list.json` |
| 建议本地原文件（**不纳入 Git**，见 `data/vocab/external/.gitignore`） | `data/vocab/external/netem_full_list.json` |

也可从仓库页面打开 [`netem_full_list.json`](https://github.com/exam-data/NETEMVocabulary/blob/master/netem_full_list.json) 再另存为上述路径。

---

## 上游 JSON 结构

顶层为 **一个 JSON 对象**，**不是**顶层数组，也**不是** `{ "words": [...] }`。

- **键**：唯一键，名称为中文表名（以仓库为准），例如 **`5530考研词汇词频排序表`**。
- **值**：**对象数组**，每个元素描述一词。

数组元素字段（当前上游；缺字段时转换器应容错）：

| 上游字段 | 类型说明 |
|----------|----------|
| `序号` | 整数，表内排序位次（从 1 起） |
| `词频` | 整数，语料中的出现次数（与 `序号` 含义不同） |
| `单词` | 字符串，词形 |
| `释义` | 字符串，中文释义 |
| `其他拼写` | 字符串或 `null` |

---

## 字段映射：上游 → 项目词包 JSON

项目统一词包格式见 [`SOURCES.md`](./SOURCES.md)「五、数据格式约定」。映射如下（**定稿约定**，实现以 `convert_kaoyan` 为准）：

| 项目字段 | 来源 / 规则 |
|----------|----------------|
| `lemma` | `单词` 去首尾空白后 **转小写**（与四级一致，便于去重） |
| `phonetic` | 上游无 → **`null`** |
| `definition_zh` | `释义`；缺省或空字符串 → **`null`** |
| `example` | 上游无 → **`null`** |
| `morphemes` | **`null`** |
| `synonyms` | **`null`** |
| `frequency_rank` | **`序号`**（考研表内**位次**，适合与学习队列排序对齐）；**不**用 `词频` 整型填入本列，以免与 ECDICT 式「词频序」混淆 |
| `source` | 固定 **`netem`** |
| `tags` | 固定 **`["kaoyan","netem"]`**（JSON 数组；`kaoyan` 供考试维度筛选，`netem` 标明数据来源） |

`其他拼写`：首版 **不写入**单独列；若日后需要可扩展为拼入 `definition_zh` 前缀或新列，见路线图。

---

## 一键生成词包（实现后）

与四级对称，实现 **`python -m english_lean.tools.import_kaoyan`** 后（见 `tasks_11` T11.6），预期用法为：

```bash
# 默认：从上游 Raw 拉取 netem_full_list.json，写出词包
python -m english_lean.tools.import_kaoyan

# 自定义输出
python -m english_lean.tools.import_kaoyan --output /path/to/kaoyan_pack.json

# 使用已下载到本地的上游文件
python -m english_lean.tools.import_kaoyan --input data/vocab/external/netem_full_list.json
```

- **默认输出路径（约定）**：`data/vocab/generated/kaoyan_pack.json`（目录已 `.gitignore`，与 `cet4_pack.json` 相同策略）。
- 生成目录说明见 [`data/vocab/generated/README.md`](../../data/vocab/generated/README.md)。

在 CLI 尚未合并前，可先仅使用转换器 API 或本地脚本调用 `convert_kaoyan_to_pack`（T11.3）。

---

## 导入到本机 SQLite

生成 `kaoyan_pack.json` 后：

```bash
python -m english_lean.tools.seed data/vocab/generated/kaoyan_pack.json
```

未传路径时 `seed` 的默认行为以 `tools.seed` 实现为准（通常仍指向仓库内小样例）。

---

## 与四级并存、重复 `lemma`

导入使用 **`INSERT OR IGNORE`**：**先写入者优先**；同一 `lemma` 后到的行会被忽略。因此若先导入 CET-4、再导入考研，**已存在的四级词条不会自动补上 `kaoyan` 标签**。合并多词书标签见后续 **`tasks_12`**。

---

## 导入后抽检（SQLite）

在检查本机库（默认路径因平台而异，见应用配置）中考研相关词条数量：

```sql
SELECT COUNT(*) FROM words WHERE tags LIKE '%kaoyan%';
```

更严谨的标签匹配可在支持 **JSON1** 的 SQLite 上使用 `json_each(tags)`；首版筛选实现见 `tasks_12`。

---

*最后更新：2026-04-11*
