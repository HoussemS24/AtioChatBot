@echo off
REM ATIO Chatbot Setup für Windows
REM Dieses Skript installiert alle Abhängigkeiten und startet den Chatbot

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   ATIO Chatbot - Windows Setup
echo ========================================
echo.

REM Überprüfe Python Installation
echo [1/5] Überprüfe Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python nicht gefunden!
    echo Bitte installieren Sie Python 3.8+ von https://www.python.org/
    echo Wählen Sie "Add Python to PATH" während der Installation
    pause
    exit /b 1
)
echo ✓ Python gefunden

REM Überprüfe Pip
echo [2/5] Überprüfe pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ pip nicht gefunden!
    pause
    exit /b 1
)
echo ✓ pip gefunden

REM Installiere Python Abhängigkeiten
echo [3/5] Installiere Python Abhängigkeiten...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Fehler beim Installieren von Abhängigkeiten
    pause
    exit /b 1
)
echo ✓ Abhängigkeiten installiert

REM Überprüfe Ollama
echo [4/5] Überprüfe Ollama Installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ Ollama nicht gefunden!
    echo Bitte installieren Sie Ollama von https://ollama.ai
    echo Nach der Installation müssen Sie Ollama starten
    pause
) else (
    echo ✓ Ollama gefunden
)

REM Erstelle Verzeichnisse
echo [5/5] Erstelle notwendige Verzeichnisse...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
echo ✓ Verzeichnisse erstellt

echo.
echo ========================================
echo   Setup abgeschlossen!
echo ========================================
echo.
echo Nächste Schritte:
echo.
echo 1. Starten Sie Ollama:
echo    - Öffnen Sie eine neue Eingabeaufforderung
echo    - Geben Sie ein: ollama serve
echo.
echo 2. Starten Sie den Chatbot Backend:
echo    - Öffnen Sie eine neue Eingabeaufforderung
echo    - Geben Sie ein: python app.py
echo.
echo 3. Öffnen Sie den Chatbot:
echo    - Öffnen Sie diese Datei in einem Browser: static/index.html
echo    - Oder besuchen Sie: http://localhost:8000
echo.
echo 4. Testen Sie den Chatbot:
echo    - Stellen Sie eine Frage über ATIO
echo.
echo Hinweise:
echo - Ollama muss laufen, damit der Chatbot funktioniert
echo - Der Backend-Server läuft auf http://localhost:8000
echo - Das Frontend läuft auf http://localhost:8000/static/
echo.
pause
