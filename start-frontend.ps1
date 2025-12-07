# HireLens AI - Frontend Server
# Run this script to start a simple HTTP server for the frontend

Write-Host "🌐 Starting HireLens AI Frontend Server..." -ForegroundColor Cyan
Write-Host ""

# Change to frontend directory
cd frontend

Write-Host "🚀 Server starting at http://localhost:3000" -ForegroundColor Green
Write-Host "📱 Open http://localhost:3000 in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Python HTTP server
python -m http.server 3000
