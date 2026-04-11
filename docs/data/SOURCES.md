# 外部词库数据源记录

本文档记录本项目计划使用的**公开可用**词库数据源，包括链接、许可类型与人工核对状态。

> **重要提醒**：发布或商用前，**须自行复核每份数据的 LICENSE**。本文档仅作为候选来源记录，最终使用前请确认许可条款允许您的使用场景（如：离线分发、合并到本项目的 JSON 格式等）。

---

## 一、四级 CET-4 候选数据源

| # | 名称 | 仓库/链接 | 许可（以仓库为准） | 备注 |
|---|------|-----------|-------------------|------|
| 1 | **ECDICT** | https://github.com/skywind3000/ECDICT | MIT License | 大型英汉词典数据库，含词频、释义等。CSV 中 `tag` 字段为空格分隔标签，含 **cet4** 即为四级大纲词。数据格式：SQLite / CSV。 |
| 2 | **CET-4 Word List (kylebing)** | https://github.com/kylebing/words | 无明确 LICENSE 文件 | 整理的四级/六级/考研词表，JSON 格式。**注意**：需联系作者确认许可或仅作参考。 |
| 3 | **CET4-6 Vocabulary** | https://github.com/lyandut/CET4-6 | MIT License | 四级、六级词表整理，含音标、释义。格式：JSON / CSV。 |
| 4 | **Exam Vocabulary** | https://github.com/issiki/english-word-lists | MIT License | 包含 CET-4、CET-6、考研等多种考试词汇，格式为 JSON。 |

### 推荐首选
**ECDICT**（MIT 许可）— 数据全面、许可清晰，支持按等级筛选四级词汇。

---

## 四级 CET-4 — 已选方案（锁定）

### 首选数据源（实现与 CLI 一致）
**ECDICT（skywind3000）** — https://github.com/skywind3000/ECDICT

- **许可证**：MIT License（以仓库 `LICENSE` 为准）
- **格式**：`ecdict.csv`（UTF-8）
- **抽取规则**：仅保留 `tag` 字段中含 **`cet4`** 的词条（标签为**空格分隔**，见上游 README「单词标注」）。
- **字段映射**（导入 JSON）：
  - `lemma` ← `word`（小写）
  - `definition_zh` ← `translation`（无则回退 `definition`）
  - `phonetic` ← `phonetic`
  - `frequency_rank` ← `frq`（无效则 `bnc`）
  - `source` ← 固定 `ecdict`
  - `tags` ← `["cet4"]`

### 获取方式（推荐）
使用内置命令**流式下载**官方 CSV 并生成词包，无需手动下载大文件：

```bash
python -m english_lean.tools.import_cet4
```

输出默认：`data/vocab/generated/cet4_pack.json`（目录已 `.gitignore`，不纳入版本库）。

### 备选
- 自备 ECDICT 格式 `.csv`：`python -m english_lean.tools.import_cet4 --input /path/to/ecdict.csv`
- lyandut 风格 `.json`（`word` / `translation` 等）：同上，`--input` 指向文件即可（`source` 为 `lyandut`）。

### 分发策略
- **仓库不提交**完整 `ecdict.csv`（体积大）；生成 JSON 亦默认忽略。
- 详细步骤见 [`docs/data/cet4.md`](./cet4.md)。

---

## 二、考研英语 候选数据源

| # | 名称 | 仓库/链接 | 许可（以仓库为准） | 备注 |
|---|------|-----------|-------------------|------|
| 1 | **ECDICT** | https://github.com/skywind3000/ECDICT | MIT License | 同上，可通过 `level` 或词频筛选考研核心词汇。 |
| 2 | **考研英语词汇** | https://github.com/lyandut/CET4-6 | MIT License | 含考研词汇子集。格式：JSON / CSV。 |
| 3 | **Kaoyan Vocabulary** | https://github.com/HuiDBK/kaoyan-english | 无 LICENSE 文件 | 考研英语核心词汇。**注意**：需确认许可。 |
| 4 | **NETEM Word List** | https://github.com/dengxiyuan/NETEM-Words | 无 LICENSE 文件 | 考研英语（NETEM）词表。**注意**：需确认许可。 |
| 5 | **NETEMVocabulary（exam-data）** | https://github.com/exam-data/NETEMVocabulary | **数据**：`LICENSE` 为 **CC BY-NC-SA 4.0**（以仓库为准）；**代码**：`LICENSE-CODE` 为 MIT | 官方风格 **5530** 考研词汇词频排序表，`netem_full_list.json` 约 700KB+。 |

### 推荐首选（候选）
上表为候选对比；**本项目考研词包（tasks_11）的实现与 CLI** 已锁定数据源，见下文 **「考研 — 已选方案」**（与仅用 ECDICT 筛选考研子集不是同一路径）。

---

## 考研英语 — 已选方案（锁定）

### 首选数据源（实现与 `import_kaoyan` / `convert_kaoyan` 一致）
**NETEMVocabulary（exam-data）** — https://github.com/exam-data/NETEMVocabulary

- **许可证（以仓库文件为准，勿以本文档替代全文）**
  - **词汇数据**（如 `netem_full_list.json`）：仓库根目录 **`LICENSE`** — **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International（CC BY-NC-SA 4.0）**。含 **非商业（NC）** 与 **相同方式共享（SA）** 等义务；发布、再分发或商用前须自行复核条款。
  - **仓库内软件/脚本**：**`LICENSE-CODE`** — MIT License（与**数据**许可分离）。
- **主文件**：`netem_full_list.json`（默认分支 `master`；体积约 **0.7MB+**，**不随本仓库分发**）。
- **Raw 直链（便于本机下载核对）**：  
  `https://raw.githubusercontent.com/exam-data/NETEMVocabulary/master/netem_full_list.json`
- **JSON 顶层结构**：**单个 JSON 对象**，仅一个键（键名为中文表名，以仓库为准，形如 `5530考研词汇词频排序表`），值为 **对象数组**；**不是**顶层裸数组，也不是 `{"words": [...] }`。
- **数组元素字段（以当前上游为准）**：`序号`、`词频`、`单词`、`释义`、`其他拼写`（可能为 `null`）。
- **导入约定（与 `tasks_11` 实现一致）**
  - `source` ← 固定 **`netem`**
  - `tags` ← **`["kaoyan","netem"]`**（定稿见 [`docs/data/kaoyan.md`](./kaoyan.md)）
  - `lemma` ← `单词`（规范化小写等见转换器）
  - `definition_zh` ← `释义`
  - `frequency_rank` ← 可用 `词频` 作排序辅助（或单独字段策略见 `kaoyan.md`）

### 获取方式
- **推荐**：使用后续提供的 `python -m english_lean.tools.import_kaoyan`（与四级对称：可 `--input` 本地文件或默认拉取上游 raw）。
- **手动**：从上述仓库 Release/Raw 下载 `netem_full_list.json`，置于本机任意路径，导入时 `--input` 指向该文件。

### 分发策略
- **仓库不提交**完整 `netem_full_list.json` 或生成的 `kaoyan_pack.json`（体积与许可文件以用户本机下载为准）；生成目录仍遵循 `data/vocab/generated/` 的 `.gitignore` 约定。
- 字段映射、抽检 SQL 与四级并存策略见 [`docs/data/kaoyan.md`](./kaoyan.md)（T11.2+）。

### 备选（未锁定）
- 若需 **MIT 数据许可** 的考研子集，可考虑自行从 **lyandut/CET4-6**、**ECDICT** 等上游抽取并单独约定 `source`/`tags`；**默认考研词包路径不以该备选为准**。

---

## 三、其他可选数据源

| 名称 | 链接 | 许可 | 说明 |
|------|------|------|------|
| **wordfreq** | https://github.com/rspeer/wordfreq | Apache-2.0 | 多语言词频数据，可用于辅助排序。 |
| **COCA Corpus** | https://www.english-corpora.org/coca/ | 商业许可 | 需购买授权，不推荐个人项目使用。 |

---

## 四、许可核对 CheckList

在正式使用任何数据源前，请逐项确认：

### 下载前检查
- [ ] 确认目标仓库有 `LICENSE` 文件
- [ ] 阅读许可证全文（MIT / Apache-2.0 / GPL / CC-BY 等）
- [ ] 确认许可证允许：**离线分发**、**修改后分发**
- [ ] 记录许可证类型到本文档

### 下载后检查
- [ ] 记录文件名、大小
- [ ] （可选）计算并记录 SHA-256 校验和
- [ ] 确认数据无版权声明冲突

### 使用前检查
- [ ] 确认许可允许合并到本项目 JSON 格式
- [ ] 在 `THIRD_PARTY_NOTICES.md` 中记录数据来源
- [ ] 如需署名，确认署名方式符合许可证要求

### 发布前检查
- [ ] 复核所有依赖数据的许可证兼容性
- [ ] 确认 `THIRD_PARTY_NOTICES.md` 完整
- [ ] 商用场景需额外确认许可是否允许商业使用

---

## 五、数据格式约定

本项目统一使用以下 JSON 格式：

```json
[
  {
    "lemma": "example",
    "phonetic": "/ɪɡˈzæmpl/",
    "definition_zh": "n. 例子；榜样",
    "example": "This is an example sentence.",
    "morphemes": null,
    "synonyms": null,
    "frequency_rank": 1234,
    "source": "ecdict",
    "tags": ["cet4"]
  }
]
```

- `source`：数据来源标识，如 `ecdict`、`netem`、`kylebing` 等
- `tags`：标签数组，用于筛选，如 `["cet4"]`、`["kaoyan"]`、`["cet4", "kaoyan"]`

---

*最后更新：2026-04-11*
