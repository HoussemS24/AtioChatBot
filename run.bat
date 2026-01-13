@echo off
REM ATIO Chatbot - Schnellstart

echo.
echo ========================================
echo   ATIO Chatbot - Schnellstart
echo ========================================
echo.

REM Überprüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python nicht gefunden!
    echo Bitte führen Sie zuerst setup.bat aus
    pause
    exit /b 1
)

REM Überprüfe ob Ollama läuft
echo Überprüfe Ollama...
timeout /t 2 /nobreak >nul

REM Starte Backend
echo.
echo Starte ATIO Chatbot Backend...
echo Öffnen Sie http://localhost:8000/static/index.html im Browser
echo.
echo Drücken Sie Ctrl+C zum Beenden
echo.

python app.py
