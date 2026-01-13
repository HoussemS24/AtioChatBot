# ATIO Chatbot Setup für Windows (PowerShell)
# Führen Sie aus: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ATIO Chatbot - Windows Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Überprüfe Python Installation
Write-Host "[1/5] Überprüfe Python Installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python gefunden: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python nicht gefunden!" -ForegroundColor Red
    Write-Host "Bitte installieren Sie Python 3.8+ von https://www.python.org/" -ForegroundColor Red
    Write-Host "Wählen Sie 'Add Python to PATH' während der Installation" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}

# Überprüfe Pip
Write-Host "[2/5] Überprüfe pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip gefunden: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip nicht gefunden!" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}

# Installiere Python Abhängigkeiten
Write-Host "[3/5] Installiere Python Abhängigkeiten..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Fehler beim Installieren von Abhängigkeiten" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}
Write-Host "✓ Abhängigkeiten installiert" -ForegroundColor Green

# Überprüfe Ollama
Write-Host "[4/5] Überprüfe Ollama Installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama gefunden: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Ollama nicht gefunden!" -ForegroundColor Yellow
    Write-Host "Bitte installieren Sie Ollama von https://ollama.ai" -ForegroundColor Yellow
    Write-Host "Nach der Installation müssen Sie Ollama starten" -ForegroundColor Yellow
}

# Erstelle Verzeichnisse
Write-Host "[5/5] Erstelle notwendige Verzeichnisse..." -ForegroundColor Yellow
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
Write-Host "✓ Verzeichnisse erstellt" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup abgeschlossen!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Nächste Schritte:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Starten Sie Ollama:" -ForegroundColor White
Write-Host "   - Öffnen Sie eine neue Eingabeaufforderung" -ForegroundColor Gray
Write-Host "   - Geben Sie ein: ollama serve" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Starten Sie den Chatbot Backend:" -ForegroundColor White
Write-Host "   - Öffnen Sie eine neue Eingabeaufforderung" -ForegroundColor Gray
Write-Host "   - Geben Sie ein: python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Öffnen Sie den Chatbot:" -ForegroundColor White
Write-Host "   - Öffnen Sie diese Datei in einem Browser: static/index.html" -ForegroundColor Gray
Write-Host "   - Oder besuchen Sie: http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Testen Sie den Chatbot:" -ForegroundColor White
Write-Host "   - Stellen Sie eine Frage über ATIO" -ForegroundColor Gray
Write-Host ""

Write-Host "Hinweise:" -ForegroundColor Cyan
Write-Host "- Ollama muss laufen, damit der Chatbot funktioniert" -ForegroundColor Gray
Write-Host "- Der Backend-Server läuft auf http://localhost:8000" -ForegroundColor Gray
Write-Host "- Das Frontend läuft auf http://localhost:8000/static/" -ForegroundColor Gray
Write-Host ""

Read-Host "Drücken Sie Enter zum Beenden"
