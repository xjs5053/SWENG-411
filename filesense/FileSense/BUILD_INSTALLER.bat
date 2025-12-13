@echo off
echo ============================================
echo FileSense - Build Installer
echo ============================================
echo.

REM Check if dist\FileSense exists
if not exist "dist\FileSense\FileSense.exe" (
    echo ERROR: FileSense.exe not found!
    echo Please run BUILD_EXE.bat first to create the executable.
    pause
    exit /b 1
)

REM Check if Inno Setup is installed
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "%INNO_PATH%" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo Creating installer with Inno Setup...
echo This may take a few minutes...
echo.

REM Build installer
"%INNO_PATH%" installer.iss

if errorlevel 1 (
    echo.
    echo ERROR: Installer build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installer Build Complete!
echo ============================================
echo.
echo Installer location: installer_output\FileSense_v1.0_Setup.exe
echo.
echo You can now distribute this installer file!
echo Users can run it to install FileSense on their Windows PC.
echo.
pause
