# ATIO Chatbot - RAG-basierter Chatbot mit Ollama

Ein vollständig funktionsfähiger RAG (Retrieval-Augmented Generation) Chatbot für die ATIO-Website, der lokal mit Ollama läuft und keine Docker-Installation benötigt.

## 🎯 Features

- **RAG-System**: Intelligente Dokumentensuche basierend auf der ATIO Knowledge Base
- **Ollama Integration**: Nutzt lokale LLM-Modelle (Mistral, Llama 2, etc.)
- **FastAPI Backend**: Moderner REST API Server
- **Responsive Frontend**: Schönes Chatbot-Widget für Websites
- **Windows-kompatibel**: Einfache Installation ohne Docker
- **Mehrsprachig**: Unterstützt Deutsch und Englisch

## 📋 Voraussetzungen

### Erforderlich
- **Python 3.8+** - [Download](https://www.python.org/)
- **Ollama** - [Download](https://ollama.ai)
- **Windows 10/11** oder Linux/macOS

### Optional
- Git für Versionskontrolle
- Visual Studio Code für Entwicklung

## 🚀 Installation

### Schritt 1: Ollama installieren

1. Laden Sie Ollama von [https://ollama.ai](https://ollama.ai) herunter
2. Führen Sie das Installationsprogramm aus
3. Nach der Installation können Sie Ollama starten

### Schritt 2: Projekt klonen oder herunterladen

```bash
# Mit Git
git clone https://github.com/HoussemS24/AtioChatBot.git
cd AtioChatBot

# Oder manuell herunterladen und entpacken
```

### Schritt 3: Setup ausführen

#### Option A: Batch-Skript (einfacher)
```bash
setup.bat
```

#### Option B: PowerShell-Skript
```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

#### Option C: Manuell
```bash
pip install -r requirements.txt
mkdir data
mkdir logs
```

## 📖 Verwendung

### 1. Ollama starten

Öffnen Sie eine neue Eingabeaufforderung und geben Sie ein:

```bash
ollama serve
```

Dies startet den Ollama-Server auf `http://localhost:11434`

### 2. Chatbot Backend starten

Öffnen Sie eine zweite Eingabeaufforderung im Projektverzeichnis:

```bash
python app.py
```

Der Server läuft nun auf `http://localhost:8000`

### 3. Chatbot öffnen

#### Option A: HTML-Datei direkt öffnen
```bash
# Doppelklick auf: static/index.html
```

#### Option B: Im Browser öffnen
```
http://localhost:8000/static/index.html
```

#### Option C: API-Dokumentation
```
http://localhost:8000/docs
```

### 4. Mit dem Chatbot interagieren

- Klicken Sie auf den Chatbot-Button in der unteren rechten Ecke
- Stellen Sie Fragen über ATIO und seine Dienstleistungen
- Der Chatbot nutzt die Knowledge Base, um relevante Antworten zu geben

## 🏗️ Projektstruktur

```
AtioChatBot/
├── app.py                          # FastAPI Backend
├── rag_system.py                   # RAG-System mit Knowledge Base
├── requirements.txt                # Python Abhängigkeiten
├── setup.bat                       # Windows Setup (Batch)
├── setup.ps1                       # Windows Setup (PowerShell)
├── README.md                       # Diese Datei
├── data/
│   ├── atio_knowledge_base.json   # ATIO Knowledge Base
│   └── atio_rag.db                # SQLite RAG Datenbank (wird erstellt)
├── static/
│   ├── index.html                 # Chatbot Frontend
│   ├── style.css                  # Chatbot Styling
│   └── script.js                  # Chatbot JavaScript
└── logs/                          # Log-Dateien
```

## 🔧 Konfiguration

### Umgebungsvariablen

Sie können diese Variablen setzen, um das Verhalten anzupassen:

```bash
# Windows CMD
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL=mistral
set RAG_DB_PATH=data/atio_rag.db

# Windows PowerShell
$env:OLLAMA_BASE_URL="http://localhost:11434"
$env:OLLAMA_MODEL="mistral"
$env:RAG_DB_PATH="data/atio_rag.db"

# Linux/macOS
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=mistral
export RAG_DB_PATH=data/atio_rag.db
```

### Verfügbare Ollama Modelle

- **mistral** (7B) - Schnell und zuverlässig (empfohlen)
- **llama2** (7B) - Gutes Verständnis
- **neural-chat** (7B) - Spezialisiert auf Chat
- **orca-mini** (3B) - Sehr schnell, weniger Speicher

Modell herunterladen:
```bash
ollama pull mistral
ollama pull llama2
```

## 🎨 Anpassung

### Knowledge Base bearbeiten

Bearbeiten Sie `data/atio_knowledge_base.json`, um Inhalte hinzuzufügen oder zu ändern:

```json
{
  "solutions": [
    {
      "name": "Neue Lösung",
      "description": "Beschreibung...",
      "features": [...]
    }
  ]
}
```

Nach Änderungen neu starten Sie den Backend-Server.

### Chatbot-Styling anpassen

Bearbeiten Sie `static/style.css`:

```css
/* Farben ändern */
.chatbot-header {
    background: linear-gradient(135deg, #003366 0%, #004d99 100%);
}
```

### Frontend-Text anpassen

Bearbeiten Sie `static/index.html`:

```html
<h2>ATIO Chatbot</h2>
<p>Fragen Sie mich über ATIO und unsere IoT-Lösungen</p>
```

## 🐛 Fehlerbehebung

### Problem: "Ollama ist nicht erreichbar"

**Lösung:**
1. Stellen Sie sicher, dass Ollama läuft (`ollama serve`)
2. Überprüfen Sie die URL: `http://localhost:11434`
3. Firewall-Einstellungen überprüfen

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Lösung:**
```bash
pip install -r requirements.txt
```

### Problem: "Port 8000 ist bereits in Verwendung"

**Lösung:**
```bash
# Ändern Sie den Port in app.py
# Zeile: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Problem: Chatbot antwortet nicht

**Überprüfung:**
1. Ollama läuft? (`ollama serve`)
2. Backend läuft? (`python app.py`)
3. Modell heruntergeladen? (`ollama pull mistral`)
4. Browser-Konsole auf Fehler überprüfen (F12)

## 📊 API Endpoints

### Health Check
```
GET /health
```

Antwortet mit:
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "rag_ready": true,
  "model": "mistral"
}
```

### Chat
```
POST /chat
Content-Type: application/json

{
  "message": "Was ist atio?",
  "conversation_id": "conv_123",
  "language": "de"
}
```

### Knowledge Base Suche
```
GET /rag/search?query=IoT&limit=5
```

### Info
```
GET /info
```

## 🔒 Sicherheit

- Der Chatbot läuft lokal auf Ihrem Computer
- Keine Daten werden an externe Server gesendet
- Ollama läuft ebenfalls lokal
- Alle Kommunikation ist lokal

## 📈 Performance

- **Erste Antwort**: 2-5 Sekunden (abhängig vom Modell)
- **Speicherverbrauch**: 2-8 GB (abhängig vom Modell)
- **CPU-Auslastung**: Moderat während der Verarbeitung

### Optimierungstipps

1. Verwenden Sie ein kleineres Modell (z.B. orca-mini)
2. Erhöhen Sie den RAM auf mindestens 8 GB
3. Verwenden Sie eine SSD für bessere Performance
4. Schließen Sie andere Anwendungen

## 🚀 Deployment

### Lokal testen
```bash
python app.py
```

### Auf Website integrieren

Fügen Sie diesen Code in Ihre Website ein:

```html
<!-- ATIO Chatbot Widget -->
<script src="http://localhost:8000/static/script.js"></script>
<link rel="stylesheet" href="http://localhost:8000/static/style.css">
<div id="chatbot-container"></div>
```

### Production Deployment

Für Production-Umgebungen:

1. Verwenden Sie einen WSGI-Server (Gunicorn)
2. Setzen Sie einen Reverse Proxy (Nginx)
3. Verwenden Sie HTTPS
4. Implementieren Sie Rate Limiting
5. Fügen Sie Authentifizierung hinzu

## 📝 Lizenz

Dieses Projekt ist für die Verwendung mit ATIO konzipiert.

## 🤝 Support

Bei Fragen oder Problemen:

1. Überprüfen Sie die Fehlerbehebung oben
2. Schauen Sie in die Logs
3. Kontaktieren Sie ATIO: info@atio.de

## 📚 Weitere Ressourcen

- [Ollama Dokumentation](https://ollama.ai)
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [ATIO Website](https://www.atio.de/)

## ✨ Changelog

### v1.0.0 (2026-01-13)
- Initial Release
- RAG-System mit SQLite
- FastAPI Backend
- Responsive Frontend
- Windows Setup-Skripte
- Vollständige Dokumentation

---

**Viel Spaß mit dem ATIO Chatbot! 🎉**
