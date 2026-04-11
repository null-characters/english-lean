# 外部词库数据源记录

本文档记录本项目计划使用的**公开可用**词库数据源，包括链接、许可类型与人工核对状态。

> **重要提醒**：发布或商用前，**须自行复核每份数据的 LICENSE**。本文档仅作为候选来源记录，最终使用前请确认许可条款允许您的使用场景（如：离线分发、合并到本项目的 JSON 格式等）。

---

## 一、四级 CET-4 候选数据源

| # | 名称 | 仓库/链接 | 许可（以仓库为准） | 备注 |
|---|------|-----------|-------------------|------|
| 1 | **ECDICT** | https://github.com/skywind3000/ECDICT | MIT License | 大型英汉词典数据库，含词频、释义等。包含四级词表（可按 `level` 字段筛选）。数据格式：SQLite / CSV。 |
| 2 | **CET-4 Word List (kylebing)** | https://github.com/kylebing/words | 无明确 LICENSE 文件 | 整理的四级/六级/考研词表，JSON 格式。**注意**：需联系作者确认许可或仅作参考。 |
| 3 | **CET4-6 Vocabulary** | https://github.com/lyandut/CET4-6 | MIT License | 四级、六级词表整理，含音标、释义。格式：JSON / CSV。 |
| 4 | **Exam Vocabulary** | https://github.com/issiki/english-word-lists | MIT License | 包含 CET-4、CET-6、考研等多种考试词汇，格式为 JSON。 |

### 推荐首选
**ECDICT**（MIT 许可）— 数据全面、许可清晰，支持按等级筛选四级词汇。

---

## 二、考研英语 候选数据源

| # | 名称 | 仓库/链接 | 许可（以仓库为准） | 备注 |
|---|------|-----------|-------------------|------|
| 1 | **ECDICT** | https://github.com/skywind3000/ECDICT | MIT License | 同上，可通过 `level` 或词频筛选考研核心词汇。 |
| 2 | **考研英语词汇** | https://github.com/lyandut/CET4-6 | MIT License | 含考研词汇子集。格式：JSON / CSV。 |
| 3 | **Kaoyan Vocabulary** | https://github.com/HuiDBK/kaoyan-english | 无 LICENSE 文件 | 考研英语核心词汇。**注意**：需确认许可。 |
| 4 | **NETEM Word List** | https://github.com/dengxiyuan/NETEM-Words | 无 LICENSE 文件 | 考研英语（NETEM）词表。**注意**：需确认许可。 |

### 推荐首选
**ECDICT**（MIT 许可）— 可通过 `level` 字段或词频排名筛选考研核心词汇，许可清晰。

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

*最后更新：2026-04-10*
