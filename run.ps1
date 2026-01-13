# ATIO Chatbot - Schnellstart (PowerShell)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ATIO Chatbot - Schnellstart" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Überprüfe ob Python installiert ist
try {
    $pythonVersion = python --version 2>&1
} catch {
    Write-Host "✗ Python nicht gefunden!" -ForegroundColor Red
    Write-Host "Bitte führen Sie zuerst setup.ps1 aus" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}

# Überprüfe ob Ollama läuft
Write-Host "Überprüfe Ollama..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Starte Backend
Write-Host ""
Write-Host "Starte ATIO Chatbot Backend..." -ForegroundColor Green
Write-Host "Öffnen Sie http://localhost:8000/static/index.html im Browser" -ForegroundColor Green
Write-Host ""
Write-Host "Drücken Sie Ctrl+C zum Beenden" -ForegroundColor Yellow
Write-Host ""

python app.py
