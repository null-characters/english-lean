# tasks_01 — 工程基线与可运行空窗

> 验收总览：安装可编辑包后执行 `python -m english_lean` 能弹出空白主窗口并正常退出。

## T1.1 添加 `pyproject.toml`

- **目标**：声明 Python 包与运行时依赖。
- **产出**：仓库根目录 `pyproject.toml`。
- **要求**：`requires-python >= 3.11`；运行时依赖包含 `PySide6`（版本下限如 `>=6.6.0`）；包名可用 `english-lean`，import 名 `english_lean`（`[tool.setuptools]` 或 hatchling 配置 `packages` 指向 `src/english_lean`）。
- **验收**：`pip install -e .` 无报错。

## T1.2 建立 `src` 布局与包初始化

- **目标**：可导入的包目录。
- **产出**：`src/english_lean/__init__.py`（可定义 `__version__ = "0.1.0"`）。

## T1.3 模块入口 `__main__.py`

- **目标**：支持 `python -m english_lean`。
- **产出**：`src/english_lean/__main__.py`，调用 `main()`（从 `english_lean.main` 导入）。

## T1.4 最小 `main.py` 启动 GUI

- **目标**：弹出空主窗口。
- **产出**：`src/english_lean/main.py`，含 `def main() -> None:`：创建 `QApplication(sys.argv)`、`QMainWindow`（设标题如 `english-lean`）、`show()`、`sys.exit(app.exec())`。
- **验收**：运行后出现窗口；关闭进程退出码为 0。

## T1.5 根目录 `.gitignore`

- **目标**：忽略虚拟环境、缓存与本地数据库占位。
- **产出**：`.gitignore` 含 `venv/`、`.venv/`、`__pycache__/`、`*.py[cod]`、`.pytest_cache/`、`*.db`、`data/*.db`（若采用）、`.DS_Store`。

## T1.6 根目录 `README.md`（最小）

- **目标**：他人/未来自己能跑起来。
- **产出**：`README.md` 含：Python 版本要求、`pip install -e .`、`python -m english_lean`。

## T1.7 开发依赖与测试脚手架

- **目标**：为后续单测留钩子。
- **产出**：`pyproject.toml` 中 `[project.optional-dependencies] dev` 含 `pytest`；或 `[dependency-groups]` dev。
- **验收**：`pip install -e ".[dev]"` 可执行 `pytest -q`（允许当前0 test 通过）。

## T1.8 首个冒烟测试

- **目标**：CI/本地快速验证导入与 `main` 可引用。
- **产出**：`tests/test_smoke.py`：`import english_lean`、`from english_lean.main import main`，`callable(main)`。
- **验收**：`pytest -q` 通过。

## T1.9 可选：Ruff 配置占位

- **目标**：统一风格（可选，不阻塞）。
- **产出**：`pyproject.toml` 中 `[tool.ruff]` 基础段，或注明「后续启用」；若添加则 `ruff check src tests` 通过。

## T1.10 本清单门禁

- **目标**：冻结 tasks_01 完成定义。
- **验收**：在干净 venv 中从零执行：创建 venv → `pip install -e ".[dev]"` → `pytest -q` → `python -m english_lean` 手动见窗。将结果记入提交说明或 issue（自用可省略）。
