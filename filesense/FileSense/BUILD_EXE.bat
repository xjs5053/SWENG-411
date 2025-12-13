@echo off
echo ============================================
echo FileSense - Build EXE
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Step 4: Building executable...
echo This may take several minutes...
echo.

REM Clean previous builds
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

REM Build with PyInstaller
pyinstaller FileSense.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Executable location: dist\FileSense\FileSense.exe
echo.
echo Next step: Run BUILD_INSTALLER.bat to create the installer
echo.
pause
