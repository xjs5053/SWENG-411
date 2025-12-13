@echo off
echo ========================================
echo Starting FileSense...
echo ========================================
echo.
python main.py
if errorlevel 1 (
    echo.
    echo ========================================
    echo FileSense crashed!
    echo ========================================
    pause
)
