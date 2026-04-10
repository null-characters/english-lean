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

规划与任务清单见 `docs/plan/`、`docs/tasks/`。
