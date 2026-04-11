@echo off
setlocal
cd /d "%~dp0"
set "PYTHONPATH=%cd%\src;%PYTHONPATH%"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m english_lean
) else (
  py -3 -m english_lean 2>nul || python -m english_lean
)
endlocal
