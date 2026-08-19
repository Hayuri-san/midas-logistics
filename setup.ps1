Write-Host "======================================"
Write-Host "          MIDAS SETUP"
Write-Host "======================================"

Write-Host ""
Write-Host "Checking Python..."
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed."
    exit 1
}

Write-Host ""
Write-Host "Creating Python virtual environment..."

if (!(Test-Path "backend\.venv")) {
    python -m venv backend\.venv
}

Write-Host ""
Write-Host "Installing backend dependencies..."

& ".\backend\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\backend\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt

Write-Host ""
Write-Host "Checking Node.js..."
node --version
npm --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Node.js/npm is not installed."
    exit 1
}

Write-Host ""
Write-Host "Installing frontend dependencies..."

Set-Location frontend
npm install
Set-Location ..

Write-Host ""
Write-Host "======================================"
Write-Host "        MIDAS SETUP COMPLETE"
Write-Host "======================================"

Write-Host ""
Write-Host "Start backend:"
Write-Host "  cd backend"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  uvicorn app.main:app --reload"

Write-Host ""
Write-Host "Start frontend:"
Write-Host "  cd frontend"
Write-Host "  npm run dev"