@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0dist\SQLiteViewer.exe" (
    start "" "%~dp0dist\SQLiteViewer.exe" %*
    exit /b 0
)
where py >nul 2>&1
if not errorlevel 1 (
    py -3 "%~dp0SQLiteViewer.py" %*
    set "exit_code=%ERRORLEVEL%"
) else (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Python 3 wurde nicht gefunden.
        pause
        exit /b 1
    )
    python "%~dp0SQLiteViewer.py" %*
    set "exit_code=%ERRORLEVEL%"
)
if not "%exit_code%"=="0" pause
exit /b %exit_code%
