# 外部词库目录

本目录用于存放**外部下载的大型词库文件**，这些文件通常体积较大，不适合纳入 Git 版本控制。

## 用途

- 存放从公开数据源下载的 CET-4、考研等词库原始文件
- 文件格式可以是 `.json`、`.csv` 或 `.sqlite`
- 转换器脚本会读取此目录的文件并转换为项目统一格式

## 数据来源

请参考 [`docs/data/SOURCES.md`](../../../docs/data/SOURCES.md) 获取推荐的数据源列表和许可信息。

## 使用方法

1. 从数据源下载词库文件
2. 将文件放置于本目录
3. 运行对应的转换器 CLI：
   ```bash
   # 示例（具体命令见 tasks_10 / tasks_11）
   python -m english_lean.vocab.convert_cet4 data/vocab/external/ecdict.csv
   ```

## 注意事项

- **本目录下的文件不会纳入 Git**（已在 `.gitignore` 中排除）
- 下载前请确认数据源的许可证允许您的使用场景
- 建议保留原始文件的压缩包以便重新提取

## 目录结构示例

```
data/vocab/external/
├── README.md           # 本文件
├── ecdict_stems.csv    # ECDICT 词根词文件
├── cet4_words.json     # 四级词表
└── kaoyan_words.csv    # 考研词表
```
