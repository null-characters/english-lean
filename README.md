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

### 图形界面快捷启动（双击）

- **macOS**：仓库根目录 **`english-lean-gui.command`** — 双击后由终端启动 GUI；**关闭主窗口后进程退出**。依赖：已按上文安装依赖（推荐用项目内 `.venv`）。若首次提示来自未识别开发者，可右键 → **打开** → **仍要打开**。若提示无执行权限，在终端执行一次：`chmod +x english-lean-gui.command`。
- **Windows**：双击 **`english-lean-gui.bat`**（同样先完成 `pip install -e ".[dev]"` 并建议使用 `.venv`）。

脚本会为当前会话设置 `PYTHONPATH=src`，因此即使未做可编辑安装也可从源码启动（仍须已安装 PySide6 等依赖）。

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

### 考研 NETEM 词包（CC BY-NC-SA · exam-data）

默认从上游 Raw 拉取 `netem_full_list.json`，生成 `data/vocab/generated/kaoyan_pack.json`，许可见上游仓库 `LICENSE`。

```bash
python -m english_lean.tools.import_kaoyan
python -m english_lean.tools.seed data/vocab/generated/kaoyan_pack.json
```

说明见 `docs/data/kaoyan.md`。

### 主界面：词书切换

启动应用后，窗口顶部 **词书** 可选「全部 / 四级 / 考研」：学习队列只包含对应 `tags` 的单词（需已用上文命令导入相应词包）。选择会保存在本机 Qt 设置中。

### 文档索引

- 四级：`docs/data/cet4.md`
- 考研：`docs/data/kaoyan.md`
- 数据源与许可：`docs/data/SOURCES.md`

规划与任务清单见 `docs/plan/`、`docs/tasks/`。
