#!/usr/bin/pwsh
# Study Buddy App Installation Script for Windows
# This script will install all required dependencies and verify the setup

Write-Host "🚀 Installing Study Buddy App Dependencies" -ForegroundColor Green
Write-Host "=" * 50

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found! Please install pip first." -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "`n📦 Installing Python packages..." -ForegroundColor Blue
try {
    pip install -r requirements.txt
    Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install packages. Check your internet connection and try again." -ForegroundColor Red
    exit 1
}

# Verify setup
Write-Host "`n🔍 Verifying installation..." -ForegroundColor Blue
try {
    python verify_setup.py
} catch {
    Write-Host "❌ Setup verification failed. Check the error messages above." -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Installation complete!" -ForegroundColor Green
Write-Host "You can now run the app with: streamlit run app.py" -ForegroundColor Yellow
