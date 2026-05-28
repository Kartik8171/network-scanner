@echo off
echo.
echo  Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Python not found! Download from https://python.org
    pause
    exit
)
python network_scanner.py
pause
