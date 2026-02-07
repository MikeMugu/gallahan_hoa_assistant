# Quick Start Script for HOA Bylaws App

Write-Host "🏘️  Starting Backend..." -ForegroundColor Cyan

# Check if .env exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  No .env file found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "❗ Please edit .env and add your OPENAI_API_KEY before proceeding!" -ForegroundColor Red
    Write-Host "   Press any key to continue once you've added your API key..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Start the backend server
Write-Host "🚀 Launching FastAPI server on http://localhost:8000" -ForegroundColor Green
python main.py
