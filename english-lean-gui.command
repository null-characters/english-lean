#!/usr/bin/env bash
# macOS: 双击本文件会在终端中启动图形界面；关闭主窗口后进程结束。
# 首次若被拦截：右键 → 打开 → 仍要打开。
#
# Finder 用「脚本路径 ; exit」启动终端时，窗口里可能出现一行带「; exit」的提示，
# 那是系统为了跑完后关窗口加的，不是程序报错。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
# 与 main.py 一致，减轻 Qt 在 macOS 上解析显示器 ICC 配置时的刷屏（可忽略）。
export QT_LOGGING_RULES="${QT_LOGGING_RULES:-qt.gui.icc=false}"

if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PYTHON="${ROOT}/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
else
  echo "未找到 Python 3。请安装 3.11+，并在项目目录执行：" >&2
  echo "  python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'" >&2
  read -r -p "按回车关闭…"
  exit 1
fi

if ! "${PYTHON}" -m english_lean; then
  echo "启动失败，请查看上方报错。" >&2
  read -r -p "按回车关闭…"
  exit 1
fi
