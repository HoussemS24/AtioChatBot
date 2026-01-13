"""
FastAPI Backend für ATIO Chatbot mit Ollama-Integration
"""

from fastapi import FastAPI, HTTPException, CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import requests
import json
import os
from rag_system import RAGSystem
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="ATIO Chatbot API",
    description="RAG-basierter Chatbot für ATIO mit Ollama",
    version="1.0.0"
)

# CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfiguration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
RAG_DB_PATH = os.getenv("RAG_DB_PATH", "data/atio_rag.db")
KB_PATH = os.getenv("KB_PATH", "data/atio_knowledge_base.json")

# RAG System initialisieren
try:
    rag_system = RAGSystem(db_path=RAG_DB_PATH, knowledge_base_path=KB_PATH)
    logger.info("RAG System erfolgreich initialisiert")
except Exception as e:
    logger.error(f"Fehler beim Initialisieren des RAG Systems: {e}")
    rag_system = None

# Pydantic Models
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: str = "de"

class ChatResponse(BaseModel):
    response: str
    context: str
    model: str
    conversation_id: str

class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    rag_ready: bool
    model: str

# Hilfsfunktionen
def check_ollama_connection() -> bool:
    """Überprüfe Ollama-Verbindung"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def query_ollama(prompt: str, context: str = "") -> str:
    """Frage Ollama LLM ab"""
    try:
        # Erstelle System-Prompt mit Kontext
        system_prompt = f"""Du bist ein hilfreicher Kundenservice-Chatbot für ATIO, ein Unternehmen spezialisiert auf Industrial IoT Projekte und Software.

Folgende Informationen sind dir bekannt:
{context}

Antworte auf Deutsch, sei höflich und hilfreich. Wenn du die Antwort nicht weißt, sag es ehrlich."""

        # Sende Request an Ollama
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Entschuldigung, ich konnte keine Antwort generieren.")
        else:
            logger.error(f"Ollama API Fehler: {response.status_code}")
            return "Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage."
    
    except requests.exceptions.ConnectionError:
        logger.error("Ollama ist nicht erreichbar")
        return "Entschuldigung, der Chatbot-Service ist momentan nicht verfügbar. Bitte stellen Sie sicher, dass Ollama läuft."
    except Exception as e:
        logger.error(f"Fehler bei Ollama Query: {e}")
        return f"Entschuldigung, es gab einen Fehler: {str(e)}"

# API Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Überprüfe Systemstatus"""
    ollama_ok = check_ollama_connection()
    rag_ok = rag_system is not None
    
    return HealthResponse(
        status="healthy" if (ollama_ok and rag_ok) else "degraded",
        ollama_connected=ollama_ok,
        rag_ready=rag_ok,
        model=OLLAMA_MODEL
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Hauptchat-Endpoint
    
    - **message**: Die Benutzer-Nachricht
    - **conversation_id**: Optional für Konversationsverlauf
    - **language**: Sprache (de/en)
    """
    
    if not message.message or len(message.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Nachricht darf nicht leer sein")
    
    if not check_ollama_connection():
        raise HTTPException(
            status_code=503,
            detail="Ollama ist nicht erreichbar. Bitte stellen Sie sicher, dass Ollama läuft."
        )
    
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="RAG System ist nicht verfügbar"
        )
    
    try:
        # Hole Kontext aus RAG
        context = rag_system.get_context(message.message)
        
        # Query Ollama
        response = query_ollama(message.message, context)
        
        return ChatResponse(
            response=response,
            context=context[:500],  # Begrenzte Kontextanzeige
            model=OLLAMA_MODEL,
            conversation_id=message.conversation_id or "default"
        )
    
    except Exception as e:
        logger.error(f"Fehler in Chat-Endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Interner Fehler: {str(e)}")

@app.get("/rag/search")
async def search_knowledge_base(query: str, limit: int = 5):
    """
    Suche in der Knowledge Base
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query darf nicht leer sein")
    
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG System ist nicht verfügbar")
    
    try:
        results = rag_system.retrieve(query, top_k=limit)
        return {"query": query, "results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Fehler in RAG Search: {e}")
        raise HTTPException(status_code=500, detail=f"Fehler bei der Suche: {str(e)}")

@app.get("/info")
async def get_info():
    """Hole Informationen über den Chatbot"""
    return {
        "name": "ATIO Chatbot",
        "description": "RAG-basierter Chatbot für ATIO Industrial IoT",
        "version": "1.0.0",
        "ollama_model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_BASE_URL,
        "language": "German"
    }

@app.get("/")
async def root():
    """Root Endpoint"""
    return {
        "message": "ATIO Chatbot API",
        "docs": "/docs",
        "health": "/health"
    }

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialisierung beim Start"""
    logger.info("ATIO Chatbot API startet...")
    logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
    logger.info(f"Ollama Model: {OLLAMA_MODEL}")
    
    # Überprüfe Ollama
    if not check_ollama_connection():
        logger.warning("⚠️ Ollama ist nicht erreichbar!")
        logger.warning(f"Bitte stellen Sie sicher, dass Ollama auf {OLLAMA_BASE_URL} läuft")
    else:
        logger.info("✓ Ollama verbunden")
    
    if rag_system:
        logger.info("✓ RAG System bereit")
    else:
        logger.error("✗ RAG System nicht verfügbar")

# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup beim Herunterfahren"""
    if rag_system:
        rag_system.close()
    logger.info("ATIO Chatbot API heruntergefahren")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
