@echo off
setlocal
cd /d "%~dp0"

set "BUILD_ROOT=C:\_Local_DEV\codex_build\sqliteviewer"
set "BUILD_DIR=%BUILD_ROOT%\build"
set "DIST_DIR=%BUILD_ROOT%\dist"
set "TARGET_DIST=%~dp0dist"

if not exist "%BUILD_ROOT%" mkdir "%BUILD_ROOT%"
if not exist "%TARGET_DIST%" mkdir "%TARGET_DIST%"

where py >nul 2>&1
if not errorlevel 1 (
    py -3 -m PyInstaller --noconfirm --clean --workpath "%BUILD_DIR%" --distpath "%DIST_DIR%" "%~dp0SQLiteViewer.spec"
) else (
    python -m PyInstaller --noconfirm --clean --workpath "%BUILD_DIR%" --distpath "%DIST_DIR%" "%~dp0SQLiteViewer.spec"
)
if errorlevel 1 exit /b %ERRORLEVEL%

copy /Y "%DIST_DIR%\SQLiteViewer.exe" "%TARGET_DIST%\SQLiteViewer.exe"
if errorlevel 1 exit /b %ERRORLEVEL%

echo Built "%TARGET_DIST%\SQLiteViewer.exe"
