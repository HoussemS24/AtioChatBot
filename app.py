"""
FastAPI Backend für ATIO Chatbot mit Ollama-Integration
"""

# ===== Imports (ALLES ganz oben) =====
import logging
import os
import json
import requests
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from rag_system import RAGSystem


# ===== Logging =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ===== FastAPI App =====
app = FastAPI(
    title="ATIO Chatbot API",
    description="RAG-basierter Chatbot für ATIO mit Ollama",
    version="1.0.0"
)

# 👉 STATIC FILES (DAS WAR DER FEHLENDE TEIL)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Konfiguration =====
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
RAG_DB_PATH = os.getenv("RAG_DB_PATH", "data/atio_rag.db")
KB_PATH = os.getenv("KB_PATH", "data/atio_knowledge_base.json")


# ===== RAG System =====
try:
    rag_system = RAGSystem(
        db_path=RAG_DB_PATH,
        knowledge_base_path=KB_PATH
    )
    logger.info("RAG System erfolgreich initialisiert")
except Exception as e:
    logger.error(f"Fehler beim Initialisieren des RAG Systems: {e}")
    rag_system = None


# ===== Pydantic Models =====
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


# ===== Hilfsfunktionen =====
def check_ollama_connection() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def query_ollama(prompt: str, context: str = "") -> str:
    system_prompt = f"""
Du bist ein hilfreicher Kundenservice-Chatbot für ATIO.

Kontext:
{context}

Antworte auf Deutsch, höflich und präzise.
"""

    try:
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
            },
            timeout=60
        )
        return r.json().get("response", "Keine Antwort generiert.")
    except Exception as e:
        logger.error(e)
        return "Fehler bei der Anfrage an Ollama."


# ===== API Endpoints =====
@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        ollama_connected=check_ollama_connection(),
        rag_ready=rag_system is not None,
        model=OLLAMA_MODEL
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(msg: ChatMessage):
    if not msg.message.strip():
        raise HTTPException(400, "Nachricht leer")

    if not rag_system:
        raise HTTPException(503, "RAG nicht verfügbar")

    context = rag_system.get_context(msg.message)
    answer = query_ollama(msg.message, context)

    return ChatResponse(
        response=answer,
        context=context[:500],
        model=OLLAMA_MODEL,
        conversation_id=msg.conversation_id or "default"
    )


@app.get("/")
async def root():
    return {
        "message": "ATIO Chatbot API",
        "docs": "/docs",
        "frontend": "/static/index.html"
    }


# ===== Startup / Shutdown =====
@app.on_event("startup")
async def startup():
    logger.info("ATIO Chatbot gestartet")
    logger.info(f"Ollama: {OLLAMA_BASE_URL}")
    logger.info(f"Model: {OLLAMA_MODEL}")


@app.on_event("shutdown")
async def shutdown():
    if rag_system:
        rag_system.close()
    logger.info("ATIO Chatbot gestoppt")


# ===== Main =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
