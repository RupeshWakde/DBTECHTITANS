@echo off
REM KYC API Application Runner - Windows Batch File
REM This batch file provides easy access to run the KYC application

echo ============================================================
echo 🎯 KYC API Application Runner - Windows
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

REM Change to the parent directory (where main.py is located)
cd ..

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found in parent directory
    echo Please run this script from the new_runapp folder
    pause
    exit /b 1
)

echo ✅ Python found and main.py located
echo.

REM Parse command line arguments
set DEV_MODE=false
set HOST=0.0.0.0
set PORT=8000
set WORKERS=1
set HEALTH_CHECK=false
set INSTALL_DEPS=false

:parse_args
if "%1"=="" goto check_deps
if "%1"=="--dev" set DEV_MODE=true
if "%1"=="-d" set DEV_MODE=true
if "%1"=="--host" (
    set HOST=%2
    shift
)
if "%1"=="--port" (
    set PORT=%2
    shift
)
if "%1"=="--workers" (
    set WORKERS=%2
    shift
)
if "%1"=="--health-check" set HEALTH_CHECK=true
if "%1"=="--install-deps" set INSTALL_DEPS=true
shift
goto parse_args

:check_deps
REM Check for PostgreSQL driver
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    python -c "import psycopg" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  PostgreSQL driver not found
        echo.
        echo Available options:
        echo 1. Run with --install-deps to automatically install dependencies
        echo 2. Manually install: pip install psycopg2-binary
        echo 3. Try alternative: pip install psycopg2
        echo 4. Continue anyway (application may not work properly)
        echo.
        set /p choice="Choose option (1-4): "
        if "%choice%"=="1" set INSTALL_DEPS=true
        if "%choice%"=="2" (
            echo 🔄 Installing psycopg2-binary...
            pip install psycopg2-binary
            if errorlevel 1 (
                echo ❌ psycopg2-binary installation failed
                echo 🔄 Trying psycopg2...
                pip install psycopg2
            )
        )
        if "%choice%"=="3" (
            echo 🔄 Installing psycopg2...
            pip install psycopg2
        )
        if "%choice%"=="4" (
            echo ⚠️  Continuing without PostgreSQL driver...
        )
    )
)

:install_deps
if "%INSTALL_DEPS%"=="true" (
    echo 🔄 Installing dependencies...
    echo.
    echo 🐘 Installing PostgreSQL driver...
    python new_runapp\install_postgres.py
    echo.
    echo 📦 Installing other dependencies...
    pip install -r requirements.txt
    echo.
)

:run_app
echo 🚀 Starting KYC API Application...
echo 📍 Host: %HOST%
echo 🔌 Port: %PORT%
echo 🔄 Dev Mode: %DEV_MODE%
echo 👥 Workers: %WORKERS%
echo 🏥 Health Check: %HEALTH_CHECK%
echo.

REM Build the command
set CMD=python new_runapp\run_app.py --host %HOST% --port %PORT% --workers %WORKERS%

if "%DEV_MODE%"=="true" set CMD=%CMD% --dev
if "%HEALTH_CHECK%"=="true" set CMD=%CMD% --health-check

echo Executing: %CMD%
echo.

REM Run the application
%CMD%

echo.
echo 🛑 Application stopped
pause 