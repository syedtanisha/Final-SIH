Write-Host "========================================" -ForegroundColor Cyan
Write-Host "      StatLearn Backend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed or not available in PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt

Write-Host ""
Write-Host "Backend setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Start the backend with:"
Write-Host "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --app-dir backend"
