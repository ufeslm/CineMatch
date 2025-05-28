# Movie Recommendation System - Quick Deploy Script for Windows
# Run this in PowerShell to prepare your app for deployment

Write-Host "🎬 Movie Recommendation System - Quick Deploy" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "📦 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Creating template..." -ForegroundColor Yellow
    @"
# Copy this file to .env and fill in your actual values

# Flask Configuration
SECRET_KEY=your-super-secret-key-here

# TMDB API (Get from https://www.themoviedb.org/settings/api)
TMDB_API_KEY=your-tmdb-api-key

# Email Configuration (Optional - for notifications)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Database (Will be provided by hosting platform)
DATABASE_URL=sqlite:///app.db
"@ | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Host "📝 Please edit the .env file with your actual values" -ForegroundColor Yellow
}

Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit the .env file with your TMDB API key" -ForegroundColor White
Write-Host "2. Run: python deploy.py (to test locally)" -ForegroundColor White
Write-Host "3. Follow the DEPLOYMENT_GUIDE.md for online deployment" -ForegroundColor White
Write-Host "`n📖 Read DEPLOYMENT_GUIDE.md for detailed instructions" -ForegroundColor Green 