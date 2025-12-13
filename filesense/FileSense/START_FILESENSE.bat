@echo off
echo ============================================
echo FileSense - AI-Powered File Search
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run SETUP.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Ollama is not running!
    echo FileSense will start, but AI features won't work until Ollama is running.
    echo.
    echo To use AI features:
    echo 1. Install Ollama from: https://ollama.com/download
    echo 2. Start Ollama (it runs automatically after installation)
    echo 3. Pull a model from the FileSense UI (Ollama Setup tab)
    echo.
) else (
    echo Ollama is running!
    echo.
)

REM Start Flask app
echo Starting FileSense...
echo.
echo Opening browser at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Wait a moment then open browser
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Run the app
python app.py

pause
