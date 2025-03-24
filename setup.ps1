# Fantasy Baseball Decision Log Setup Script for Windows

# Colors for output
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red

Write-Host "Fantasy Baseball Decision Log Setup" -ForegroundColor $Green
Write-Host "This script will set up the project for development."

# Check for required tools
Write-Host "`nChecking prerequisites..." -ForegroundColor $Yellow

# Check Python
try {
    $pythonVersion = (python --version).Split(" ")[1]
    Write-Host "✅ Python $pythonVersion installed"
} catch {
    Write-Host "❌ Python 3.9+ is required but not found" -ForegroundColor $Red
    Write-Host "Please install Python 3.9 or higher: https://www.python.org/downloads/"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = (node --version)
    Write-Host "✅ Node.js $nodeVersion installed"
} catch {
    Write-Host "❌ Node.js 18+ is required but not found" -ForegroundColor $Red
    Write-Host "Please install Node.js 18 or higher: https://nodejs.org/"
    exit 1
}

# Check Bun
try {
    $bunVersion = (bun --version)
    Write-Host "✅ Bun $bunVersion installed"
} catch {
    Write-Host "❌ Bun is required but not found" -ForegroundColor $Red
    Write-Host "Please install Bun: https://bun.sh/"
    exit 1
}

# Check uv
try {
    $uvVersion = (uv --version)
    Write-Host "✅ uv $uvVersion installed"
} catch {
    Write-Host "❌ uv is required but not found" -ForegroundColor $Red
    Write-Host "Please install uv: https://github.com/astral-sh/uv"
    exit 1
}

# Check Docker (optional)
try {
    $dockerVersion = (docker --version).Split(" ")[2].TrimEnd(",")
    Write-Host "✅ Docker $dockerVersion installed"

    try {
        $dockerComposeVersion = (docker-compose --version).Split(" ")[2].TrimEnd(",")
        Write-Host "✅ Docker Compose $dockerComposeVersion installed"
    } catch {
        Write-Host "⚠️ Docker Compose not found (optional)" -ForegroundColor $Yellow
    }
} catch {
    Write-Host "⚠️ Docker not found (optional)" -ForegroundColor $Yellow
}

# Create .env file if it doesn't exist
Write-Host "`nSetting up environment..." -ForegroundColor $Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file from .env.example"
    Write-Host "⚠️ Please edit .env file with your Yahoo API credentials" -ForegroundColor $Yellow
} else {
    Write-Host "✅ .env file already exists"
}

# Set up backend
Write-Host "`nSetting up backend..." -ForegroundColor $Yellow
Set-Location -Path backend
uv venv
& .\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
Write-Host "✅ Backend dependencies installed"

# Set up frontend
Write-Host "`nSetting up frontend..." -ForegroundColor $Yellow
Set-Location -Path ..\frontend
bun install
Write-Host "✅ Frontend dependencies installed"

# Set up database directories
Write-Host "`nSetting up data directories..." -ForegroundColor $Yellow
Set-Location -Path ..
New-Item -ItemType Directory -Force -Path data\json | Out-Null
Write-Host "✅ Data directories created"

Write-Host "`nSetup complete!" -ForegroundColor $Green
Write-Host "To start the backend: cd backend; python run.py --reload"
Write-Host "To start the frontend: cd frontend; bun run dev"
Write-Host "To start PostgreSQL (optional): cd docker; docker-compose up -d"
Write-Host "`nHappy fantasy baseball managing! 🎯⚾"
