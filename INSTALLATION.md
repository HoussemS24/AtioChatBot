# Installationsanleitung - ATIO Chatbot

Detaillierte Schritt-für-Schritt Anleitung zur Installation auf Windows.

## 📋 Systemanforderungen

- **Windows 10/11** (64-bit)
- **Mindestens 8 GB RAM** (16 GB empfohlen)
- **SSD mit mindestens 10 GB freiem Speicherplatz**
- **Internetverbindung** (für Downloads)

## 🔧 Installation in 5 Minuten

### Schritt 1: Python installieren

1. Besuchen Sie [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Klicken Sie auf "Download Python 3.11" (oder neuere Version)
3. Führen Sie das Installationsprogramm aus
4. **WICHTIG**: Aktivieren Sie "Add Python to PATH"
5. Klicken Sie "Install Now"
6. Warten Sie bis die Installation abgeschlossen ist

**Überprüfung:**
- Öffnen Sie Eingabeaufforderung (cmd)
- Geben Sie ein: `python --version`
- Sie sollten eine Versionsnummer sehen (z.B. Python 3.11.0)

### Schritt 2: Ollama installieren

1. Besuchen Sie [https://ollama.ai](https://ollama.ai)
2. Klicken Sie auf "Download"
3. Wählen Sie "Windows"
4. Führen Sie das Installationsprogramm aus
5. Folgen Sie den Anweisungen
6. Nach der Installation wird Ollama automatisch gestartet

**Überprüfung:**
- Öffnen Sie Eingabeaufforderung
- Geben Sie ein: `ollama --version`
- Sie sollten eine Versionsnummer sehen

### Schritt 3: Projekt herunterladen

**Option A: Mit Git (empfohlen)**

1. Öffnen Sie Eingabeaufforderung
2. Navigieren Sie zu Ihrem gewünschten Verzeichnis:
   ```bash
   cd C:\Users\IhrBenutzername\Dokumente
   ```
3. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/HoussemS24/AtioChatBot.git
   cd AtioChatBot
   ```

**Option B: Manuell herunterladen**

1. Besuchen Sie [GitHub Repository](https://github.com/HoussemS24/AtioChatBot)
2. Klicken Sie auf "Code" → "Download ZIP"
3. Entpacken Sie die ZIP-Datei
4. Öffnen Sie das Verzeichnis

### Schritt 4: Setup ausführen

**Option A: Batch-Skript (einfacher)**

1. Öffnen Sie das AtioChatBot Verzeichnis
2. Doppelklick auf `setup.bat`
3. Warten Sie bis die Installation abgeschlossen ist

**Option B: PowerShell-Skript**

1. Öffnen Sie PowerShell im AtioChatBot Verzeichnis
2. Geben Sie ein:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
3. Warten Sie bis die Installation abgeschlossen ist

**Option C: Manuell**

1. Öffnen Sie Eingabeaufforderung im AtioChatBot Verzeichnis
2. Geben Sie ein:
   ```bash
   pip install -r requirements.txt
   mkdir data
   mkdir logs
   ```

### Schritt 5: Ollama Modell herunterladen

1. Öffnen Sie Eingabeaufforderung
2. Geben Sie ein:
   ```bash
   ollama pull mistral
   ```
3. Warten Sie bis der Download abgeschlossen ist (ca. 4 GB)

**Alternative Modelle:**
```bash
ollama pull llama2
ollama pull neural-chat
ollama pull orca-mini
```

## 🚀 Starten des Chatbots

### Erste Eingabeaufforderung: Ollama starten

1. Öffnen Sie eine neue Eingabeaufforderung
2. Geben Sie ein:
   ```bash
   ollama serve
   ```
3. Sie sollten sehen: "Listening on 127.0.0.1:11434"
4. **Lassen Sie dieses Fenster offen!**

### Zweite Eingabeaufforderung: Backend starten

1. Öffnen Sie eine neue Eingabeaufforderung
2. Navigieren Sie zum AtioChatBot Verzeichnis:
   ```bash
   cd C:\Pfad\zum\AtioChatBot
   ```
3. Geben Sie ein:
   ```bash
   python app.py
   ```
4. Sie sollten sehen: "Uvicorn running on http://0.0.0.0:8000"
5. **Lassen Sie dieses Fenster auch offen!**

### Browser öffnen

1. Öffnen Sie Ihren Webbrowser (Chrome, Firefox, Edge, etc.)
2. Geben Sie ein: `http://localhost:8000/static/index.html`
3. Sie sollten den Chatbot sehen!

## 💬 Chatbot testen

1. Klicken Sie auf den Chatbot-Button in der unteren rechten Ecke
2. Stellen Sie eine Frage, z.B.:
   - "Was ist atio?"
   - "Welche Lösungen bietet ihr an?"
   - "Wie kann ich euch kontaktieren?"
3. Der Chatbot sollte antworten!

## 🎯 Häufige Probleme und Lösungen

### Problem: "Python nicht gefunden"

**Lösung:**
1. Deinstallieren Sie Python
2. Installieren Sie Python neu
3. **WICHTIG**: Aktivieren Sie "Add Python to PATH"
4. Starten Sie den Computer neu
5. Versuchen Sie erneut

### Problem: "pip: Befehl nicht gefunden"

**Lösung:**
1. Öffnen Sie Eingabeaufforderung als Administrator
2. Geben Sie ein: `python -m pip install --upgrade pip`
3. Versuchen Sie erneut

### Problem: "Ollama ist nicht erreichbar"

**Lösung:**
1. Stellen Sie sicher, dass Sie `ollama serve` ausgeführt haben
2. Überprüfen Sie, dass das Ollama-Fenster noch offen ist
3. Versuchen Sie, den Browser zu aktualisieren (F5)
4. Starten Sie Ollama neu

### Problem: "Port 8000 ist bereits in Verwendung"

**Lösung:**
1. Schließen Sie alle anderen Python-Prozesse
2. Oder ändern Sie den Port in app.py:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

### Problem: "Modell wird nicht heruntergeladen"

**Lösung:**
1. Überprüfen Sie Ihre Internetverbindung
2. Versuchen Sie ein kleineres Modell: `ollama pull orca-mini`
3. Überprüfen Sie den verfügbaren Speicherplatz (mindestens 5 GB)

### Problem: "Chatbot antwortet nicht"

**Überprüfung:**
1. Ist Ollama läuft? (Fenster sollte offen sein)
2. Ist der Backend läuft? (Fenster sollte offen sein)
3. Öffnen Sie Browser-Konsole (F12) und suchen Sie nach Fehlern
4. Versuchen Sie, die Seite zu aktualisieren (F5)

### Problem: "Sehr langsame Antworten"

**Lösungen:**
1. Verwenden Sie ein kleineres Modell: `ollama pull orca-mini`
2. Schließen Sie andere Anwendungen
3. Erhöhen Sie den RAM (mindestens 16 GB empfohlen)
4. Verwenden Sie eine SSD statt HDD

## 📊 Performance-Tipps

1. **Modellwahl**: Mistral ist schnell und zuverlässig
2. **RAM**: Mindestens 8 GB, besser 16 GB
3. **Speicher**: SSD ist viel schneller als HDD
4. **Hintergrund-Apps**: Schließen Sie unnötige Programme
5. **Browser**: Verwenden Sie Chrome oder Edge für beste Performance

## 🔄 Regelmäßige Wartung

### Logs überprüfen

Logs befinden sich im `logs/` Verzeichnis:
```bash
type logs\*.log
```

### Knowledge Base aktualisieren

Bearbeiten Sie `data/atio_knowledge_base.json` und starten Sie den Backend neu.

### Modell aktualisieren

```bash
ollama pull mistral  # Neueste Version herunterladen
```

## 🆘 Weitere Hilfe

- **Ollama Probleme**: [Ollama GitHub Issues](https://github.com/ollama/ollama/issues)
- **Python Probleme**: [Python Dokumentation](https://docs.python.org/)
- **ATIO Support**: [info@atio.de](mailto:info@atio.de)

## ✅ Checkliste

- [ ] Python installiert und in PATH
- [ ] Ollama installiert und läuft
- [ ] Projekt heruntergeladen
- [ ] Setup ausgeführt
- [ ] Ollama Modell heruntergeladen
- [ ] Ollama serve läuft
- [ ] Backend läuft (python app.py)
- [ ] Browser öffnet http://localhost:8000/static/index.html
- [ ] Chatbot antwortet auf Fragen

Wenn alle Punkte erfüllt sind, ist Ihr Chatbot bereit! 🎉

---

**Viel Erfolg bei der Installation!**
