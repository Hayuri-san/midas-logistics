Write-Host "======================================"
Write-Host "           MIDAS SETUP"
Write-Host "======================================"
Write-Host ""

# ======================================
# Check Python
# ======================================

Write-Host "Checking Python..."

$pythonVersionOutput = python --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Python is not installed or is not available in PATH."
    Write-Host "Please install Python 3.12 and try again."
    exit 1
}

Write-Host "Detected: $pythonVersionOutput"

# Get Python major/minor version
$pythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"

if ($pythonVersion -ne "3.12") {
    Write-Host ""
    Write-Host "ERROR: MIDAS requires Python 3.12."
    Write-Host "Detected Python version: $pythonVersion"
    Write-Host ""
    Write-Host "Please install Python 3.12 and make sure it is available in PATH."
    Write-Host "Then run this setup script again."
    exit 1
}

Write-Host "Python 3.12 detected."
Write-Host ""

# ======================================
# Create Python virtual environment
# ======================================

Write-Host "Creating Python virtual environment..."

if (!(Test-Path "backend\.venv")) {
    python -m venv backend\.venv

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: Failed to create Python virtual environment."
        exit 1
    }

    Write-Host "Virtual environment created."
}
else {
    Write-Host "Virtual environment already exists. Skipping creation."
}

Write-Host ""

# ======================================
# Install backend dependencies
# ======================================

Write-Host "Installing backend dependencies..."

& ".\backend\.venv\Scripts\python.exe" -m pip install --upgrade pip

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to upgrade pip."
    exit 1
}

& ".\backend\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Backend dependency installation failed."
    Write-Host "Check the error above."
    exit 1
}

Write-Host "Backend dependencies installed successfully."
Write-Host ""

# ======================================
# Check Node.js
# ======================================

Write-Host "Checking Node.js..."

$nodeVersionOutput = node --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Node.js is not installed or is not available in PATH."
    Write-Host "Please install Node.js and try again."
    exit 1
}

Write-Host "Detected Node.js: $nodeVersionOutput"

Write-Host ""

# ======================================
# Check npm
# ======================================

Write-Host "Checking npm..."

$npmVersionOutput = npm --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: npm is not installed or is not available in PATH."
    exit 1
}

Write-Host "Detected npm: $npmVersionOutput"
Write-Host ""

# ======================================
# Install frontend dependencies
# ======================================

Write-Host "Installing frontend dependencies..."

Set-Location frontend

npm install

if ($LASTEXITCODE -ne 0) {
    Set-Location ..
    Write-Host ""
    Write-Host "ERROR: Frontend dependency installation failed."
    exit 1
}

Set-Location ..

Write-Host "Frontend dependencies installed successfully."
Write-Host ""

# ======================================
# Setup complete
# ======================================

Write-Host "======================================"
Write-Host "        MIDAS SETUP COMPLETE"
Write-Host "======================================"
Write-Host ""

Write-Host "Backend:"
Write-Host "  cd backend"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  uvicorn app.main:app --reload"
Write-Host ""

Write-Host "Frontend:"
Write-Host "  cd frontend"
Write-Host "  npm run dev"
Write-Host ""

Write-Host "Happy coding!"