@echo off
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║           FILESENSE - COMPLETE BUILD SCRIPT                    ║
echo ║         Creates .EXE and Windows Installer                     ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo This script will:
echo   1. Create virtual environment
echo   2. Install dependencies
echo   3. Build FileSense.exe with PyInstaller
echo   4. Create Windows installer with Inno Setup
echo.
echo Requirements:
echo   - Python 3.8+ (with PATH)
echo   - Inno Setup (will check and prompt if missing)
echo.
echo This process takes 5-10 minutes.
echo.
pause

REM ============================================
REM STEP 1: CHECK PYTHON
REM ============================================
echo.
echo [STEP 1/5] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

python --version
echo ✓ Python found!

REM ============================================
REM STEP 2: SETUP ENVIRONMENT
REM ============================================
echo.
echo [STEP 2/5] Setting up build environment...
echo.

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
pip install pyinstaller --quiet

echo ✓ Environment ready!

REM ============================================
REM STEP 3: BUILD EXE
REM ============================================
echo.
echo [STEP 3/5] Building FileSense.exe...
echo.
echo This may take 3-5 minutes...

REM Clean previous builds
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

REM Build with PyInstaller
pyinstaller FileSense.spec --clean

if errorlevel 1 (
    echo.
    echo ERROR: EXE build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo ✓ EXE created successfully!
echo   Location: dist\FileSense\FileSense.exe

REM ============================================
REM STEP 4: CHECK INNO SETUP
REM ============================================
echo.
echo [STEP 4/5] Checking Inno Setup...
echo.

set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "%INNO_PATH%" (
    echo.
    echo WARNING: Inno Setup not found!
    echo.
    echo To create a Windows installer, please:
    echo   1. Download Inno Setup from: https://jrsoftware.org/isdl.php
    echo   2. Install it
    echo   3. Run BUILD_INSTALLER.bat
    echo.
    echo For now, you can use the standalone EXE in:
    echo   dist\FileSense\FileSense.exe
    echo.
    pause
    exit /b 0
)

echo ✓ Inno Setup found!

REM ============================================
REM STEP 5: BUILD INSTALLER
REM ============================================
echo.
echo [STEP 5/5] Building Windows installer...
echo.

"%INNO_PATH%" installer.iss

if errorlevel 1 (
    echo.
    echo ERROR: Installer build failed!
    echo However, the EXE was created successfully.
    echo You can find it at: dist\FileSense\FileSense.exe
    pause
    exit /b 1
)

echo ✓ Installer created successfully!

REM ============================================
REM COMPLETE
REM ============================================
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║                    BUILD COMPLETE!                             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Your files are ready:
echo.
echo 📦 Standalone EXE:
echo    dist\FileSense\FileSense.exe
echo    (Can be run directly, no installation needed)
echo.
echo 🔧 Windows Installer:
echo    installer_output\FileSense_v1.0_Setup.exe
echo    (Professional installer for distribution)
echo.
echo File sizes:
dir /b dist\FileSense\FileSense.exe 2>nul | find /v "" >nul && (
    for %%A in ("dist\FileSense\FileSense.exe") do echo    EXE: %%~zA bytes
)
dir /b installer_output\FileSense_v1.0_Setup.exe 2>nul | find /v "" >nul && (
    for %%A in ("installer_output\FileSense_v1.0_Setup.exe") do echo    Installer: %%~zA bytes
)
echo.
echo What to distribute:
echo   • For tech-savvy users: Give them the entire dist\FileSense folder
echo   • For regular users: Give them FileSense_v1.0_Setup.exe
echo.
echo Next steps:
echo   1. Test the installer on a clean Windows PC
echo   2. Make sure Ollama is mentioned in user instructions
echo   3. Distribute to users!
echo.
pause
