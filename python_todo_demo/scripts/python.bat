@echo off
setlocal
py -3 --version >nul 2>&1
if not errorlevel 1 goto use_py
python --version >nul 2>&1
if not errorlevel 1 goto use_python
set "BUNDLED_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BUNDLED_PYTHON%" goto use_bundled
echo Python 3.9 or newer is required. Install Python, then try again.
exit /b 1

:use_py
py -3 %*
exit /b %errorlevel%

:use_python
python %*
exit /b %errorlevel%

:use_bundled
"%BUNDLED_PYTHON%" %*
exit /b %errorlevel%
