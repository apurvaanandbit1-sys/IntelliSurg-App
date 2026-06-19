$ErrorActionPreference = "Stop"

$frontendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Split-Path -Parent $frontendDir
$backendVenvPython = Join-Path $appRoot "backend\.venv311\Scripts\python.exe"
$appFile = Join-Path $frontendDir "app.py"

Write-Host ""
Write-Host "IntelliSurg frontend launcher"
Write-Host "Frontend directory: $frontendDir"
Write-Host ""

if (-not (Test-Path $backendVenvPython)) {
    Write-Host "Backend virtual environment not found at:"
    Write-Host "  $backendVenvPython"
    Write-Host ""
    Write-Host "Run backend\start_backend.ps1 once first."
    exit 1
}

Write-Host "Starting Streamlit frontend on http://localhost:8501"
Write-Host ""

Set-Location $frontendDir
& $backendVenvPython -m streamlit run $appFile
