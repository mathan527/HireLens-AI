# HireLens AI - Setup Script
# Run this script to set up the entire project

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                    ║" -ForegroundColor Cyan
Write-Host "║          🔍 HireLens AI - Setup Wizard            ║" -ForegroundColor Cyan
Write-Host "║                                                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Python Version Check
Write-Host "Step 1: Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Create Virtual Environment
Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ⚠️  Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✅ Virtual environment created!" -ForegroundColor Green
}
Write-Host ""

# Step 3: Activate Virtual Environment
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  ✅ Virtual environment activated!" -ForegroundColor Green
Write-Host ""

# Step 4: Install Dependencies
Write-Host "Step 4: Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "  ✅ Dependencies installed!" -ForegroundColor Green
Write-Host ""

# Step 5: Download spaCy Model
Write-Host "Step 5: Downloading spaCy language model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm
Write-Host "  ✅ spaCy model downloaded!" -ForegroundColor Green
Write-Host ""

# Step 6: Setup Environment File
Write-Host "Step 6: Setting up environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ⚠️  .env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Copy-Item .env.example .env
    Write-Host "  ✅ .env file created from template!" -ForegroundColor Green
}
Write-Host ""

# Step 7: Initialize Database
Write-Host "Step 7: Initializing database..." -ForegroundColor Yellow
python init_db.py
Write-Host ""

# Step 7: Initialize Database
Write-Host "Step 7: Initializing database..." -ForegroundColor Yellow
python init_db.py
Write-Host ""

# Step 8: Configuration Instructions
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                    ║" -ForegroundColor Green
Write-Host "║              ✅ Setup Complete!                    ║" -ForegroundColor Green
Write-Host "║                                                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📝 IMPORTANT: Next Steps" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "1. Configure API Keys (Required for AI features):" -ForegroundColor Yellow
Write-Host "   • Edit the .env file" -ForegroundColor White
Write-Host "   • Add your Gemini or OpenAI API key" -ForegroundColor White
Write-Host ""
Write-Host "   To get API keys:" -ForegroundColor Gray
Write-Host "   • Gemini: https://makersuite.google.com/app/apikey" -ForegroundColor Gray
Write-Host "   • OpenAI: https://platform.openai.com/api-keys" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Start the Backend Server:" -ForegroundColor Yellow
Write-Host "   .\start.ps1" -ForegroundColor White
Write-Host ""

Write-Host "3. Start the Frontend (in a new terminal):" -ForegroundColor Yellow
Write-Host "   .\start-frontend.ps1" -ForegroundColor White
Write-Host ""

Write-Host "4. Open your browser:" -ForegroundColor Yellow
Write-Host "   http://localhost:3000" -ForegroundColor White
Write-Host ""

Write-Host "5. Login with test account:" -ForegroundColor Yellow
Write-Host "   Email: test@hirelens.ai" -ForegroundColor White
Write-Host "   Password: test123456" -ForegroundColor White
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation: README.md" -ForegroundColor Cyan
Write-Host "🐛 Issues? Check the Troubleshooting section in README.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
