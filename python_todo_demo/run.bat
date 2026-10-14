@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
call "%~dp0scripts\python.bat" -X utf8 main.py %*
set "RESULT=%errorlevel%"
echo.
pause
exit /b %RESULT%
