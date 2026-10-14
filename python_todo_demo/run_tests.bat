@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
call "%~dp0scripts\python.bat" -X utf8 -m unittest discover -s tests -v
set "RESULT=%errorlevel%"
echo.
pause
exit /b %RESULT%
