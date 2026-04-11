# english-lean

自用、离线的桌面英语单词学习工具（开发中）。

## 环境

- Python **3.11+**

## 安装与运行

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m english_lean
```

## 开发

```bash
pytest -q
ruff check src tests
```

### 导入样例词库（写入本机用户数据目录下的 SQLite）

```bash
python -m english_lean.tools.seed
```

### 四级 CET-4 词包（MIT · ECDICT，自动拉取）

联网时一键从官方 CSV 流式下载并筛选 `tag` 含 `cet4` 的词条，生成 `data/vocab/generated/cet4_pack.json`，再导入本机库：

```bash
python -m english_lean.tools.import_cet4
python -m english_lean.tools.seed data/vocab/generated/cet4_pack.json
```

说明见 `docs/data/cet4.md`、`docs/data/SOURCES.md`。

规划与任务清单见 `docs/plan/`、`docs/tasks/`。
