# 离线词表数据

本目录存放词汇数据，分为**样例词库**和**外部词库**两部分。

## 目录结构

```
data/vocab/
├── README.md           # 本文件
├── sample_cet4.json    # 样例词库（小规模，纳入 Git）
└── external/           # 外部大型词库（不纳入 Git）
    └── README.md       # 外部词库使用说明
```

## 样例词库

`sample_cet4.json` 是一个小规模样例，用于开发测试和应用首次启动时的自动导入。

### JSON 字段规范

| 字段 | 必填 | 说明 |
|------|------|------|
| `lemma` | 是 | 单词词干，导入时会 `strip` 并存为**小写** |
| `phonetic` | 否 | 音标 |
| `definition_zh` | 否 | 中文释义 |
| `example` | 否 | 例句 |
| `morphemes` | 否 | 词根词缀 |
| `synonyms` | 否 | 同义词 |
| `frequency_rank` | 否 | 词频排名 |
| `source` | 否 | 数据来源标识（如 `ecdict`、`netem`） |
| `tags` | 否 | 标签数组（如 `["cet4"]`、`["kaoyan"]`），也支持逗号分隔字符串 |

### 格式示例

```json
[
  {
    "lemma": "example",
    "phonetic": "/ɪɡˈzæmpl/",
    "definition_zh": "n. 例子；榜样",
    "example": "This is an example sentence.",
    "source": "ecdict",
    "tags": ["cet4"]
  }
]
```

JSON 根节点可以是：
- **数组**：直接包含单词对象
- **对象**：`{"words": [...]}` 格式，抽取 `words` 数组

可含 `_comment` 键的对象会被跳过（用于文档注释）。

## 外部词库

大型词库文件请放置于 `external/` 目录，该目录不纳入 Git 版本控制。

### 数据来源

推荐的数据源列表和许可信息请参考：

- [`docs/data/SOURCES.md`](../../docs/data/SOURCES.md) — 候选数据源与许可核对清单

### 使用流程

1. 从推荐数据源下载原始文件到 `external/`
2. 运行转换器 CLI（见 `tasks_10`、`tasks_11`）生成统一 JSON
3. 使用导入工具加载到 SQLite

## 注意事项

- **仓库内仅保留小样例**，不引入大文件
- 使用外部数据前请确认许可证兼容性
- `THIRD_PARTY_NOTICES.md` 中记录了第三方数据来源
