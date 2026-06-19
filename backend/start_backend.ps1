$ErrorActionPreference = "Stop"

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python311 = "C:\Users\apurv\AppData\Local\Programs\Python\Python311\python.exe"
$venvDir = Join-Path $backendDir ".venv311"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

Write-Host ""
Write-Host "IntelliSurg backend launcher"
Write-Host "Backend directory: $backendDir"
Write-Host ""

if (-not (Test-Path $python311)) {
    Write-Host "Python 3.11 was not found at:"
    Write-Host "  $python311"
    Write-Host ""
    Write-Host "Install Python 3.11 first, then re-run this script."
    exit 1
}

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating fresh backend virtual environment..."
    & $python311 -m venv $venvDir
}

Write-Host "Installing backend requirements..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $backendDir "requirements.txt")

Write-Host ""
Write-Host "Starting FastAPI backend on http://127.0.0.1:8000"
Write-Host ""

Set-Location $backendDir
& $venvPython -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
