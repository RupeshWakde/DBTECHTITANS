# KYC API Application Runner - PowerShell Script
# This PowerShell script provides easy access to run the KYC application

param(
    [string]$Host = "0.0.0.0",
    [int]$Port = 8000,
    [switch]$Dev,
    [int]$Workers = 1,
    [switch]$HealthCheck
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎯 KYC API Application Runner - PowerShell" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and add it to your PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Get the script directory and change to parent directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$parentDir = Split-Path -Parent $scriptDir

# Change to parent directory
Set-Location $parentDir

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "❌ main.py not found in parent directory" -ForegroundColor Red
    Write-Host "Please run this script from the new_runapp folder" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ main.py located successfully" -ForegroundColor Green
Write-Host ""

# Display configuration
Write-Host "🚀 Starting KYC API Application..." -ForegroundColor Green
Write-Host "📍 Host: $Host" -ForegroundColor White
Write-Host "🔌 Port: $Port" -ForegroundColor White
Write-Host "🔄 Dev Mode: $Dev" -ForegroundColor White
Write-Host "👥 Workers: $Workers" -ForegroundColor White
Write-Host "🏥 Health Check: $HealthCheck" -ForegroundColor White
Write-Host ""

# Build the command
$cmdArgs = @(
    "new_runapp\run_app.py"
    "--host", $Host
    "--port", $Port.ToString()
    "--workers", $Workers.ToString()
)

if ($Dev) {
    $cmdArgs += "--dev"
}

if ($HealthCheck) {
    $cmdArgs += "--health-check"
}

$command = "python " + ($cmdArgs -join " ")
Write-Host "Executing: $command" -ForegroundColor Yellow
Write-Host ""

try {
    # Run the application
    & python $cmdArgs
} catch {
    Write-Host "❌ Error running application: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "🛑 Application stopped" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
} 