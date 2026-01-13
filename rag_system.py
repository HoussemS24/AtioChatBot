"""
RAG (Retrieval-Augmented Generation) System für ATIO Chatbot
Nutzt lokale Embeddings und SQLite für Vektorsuche
"""

import json
import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

class RAGSystem:
    def __init__(self, db_path: str = "data/atio_rag.db", knowledge_base_path: str = "data/atio_knowledge_base.json"):
        self.db_path = db_path
        self.knowledge_base_path = knowledge_base_path
        self.conn = None
        self.init_database()
        self.load_knowledge_base()
    
    def init_database(self):
        """Initialisiere SQLite Datenbank für RAG"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Erstelle Tabelle für Dokumente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Erstelle Tabelle für Embeddings (vereinfacht - nur Text-Hash)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                doc_id TEXT PRIMARY KEY,
                embedding_hash TEXT NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        ''')
        
        self.conn.commit()
    
    def load_knowledge_base(self):
        """Lade die Knowledge Base aus JSON und speichere in Datenbank"""
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        cursor = self.conn.cursor()
        
        # Leere alte Einträge
        cursor.execute('DELETE FROM documents')
        cursor.execute('DELETE FROM embeddings')
        
        # Speichere Company Info
        company_text = f"Unternehmen: {kb['company']['name']}. {kb['company']['description']}"
        doc_id = self._generate_id(company_text)
        cursor.execute('''
            INSERT OR REPLACE INTO documents (id, content, source, category)
            VALUES (?, ?, ?, ?)
        ''', (doc_id, company_text, 'company', 'Unternehmen'))
        self._save_embedding(cursor, doc_id, company_text)
        
        # Speichere Kontaktinformationen
        contact_text = f"Kontakt: {kb['company']['contact']['address']}, Tel: {kb['company']['contact']['phone']}, Email: {kb['company']['contact']['email']}"
        doc_id = self._generate_id(contact_text)
        cursor.execute('''
            INSERT OR REPLACE INTO documents (id, content, source, category)
            VALUES (?, ?, ?, ?)
        ''', (doc_id, contact_text, 'contact', 'Kontakt'))
        self._save_embedding(cursor, doc_id, contact_text)
        
        # Speichere Lösungen
        for solution in kb['solutions']:
            sol_text = f"{solution['name']}: {solution['description']}"
            doc_id = self._generate_id(sol_text)
            cursor.execute('''
                INSERT OR REPLACE INTO documents (id, content, source, category)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, sol_text, 'solution', solution['name']))
            self._save_embedding(cursor, doc_id, sol_text)
            
            # Speichere Features
            if 'features' in solution:
                for feature in solution['features']:
                    feat_text = f"{solution['name']} - {feature['name']}: {feature['description']}"
                    feat_id = self._generate_id(feat_text)
                    cursor.execute('''
                        INSERT OR REPLACE INTO documents (id, content, source, category)
                        VALUES (?, ?, ?, ?)
                    ''', (feat_id, feat_text, 'feature', f"{solution['name']} - {feature['name']}"))
                    self._save_embedding(cursor, feat_id, feat_text)
        
        # Speichere Kompetenzen
        for comp in kb['competencies']:
            comp_text = f"{comp['name']}: {comp['description']}"
            doc_id = self._generate_id(comp_text)
            cursor.execute('''
                INSERT OR REPLACE INTO documents (id, content, source, category)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, comp_text, 'competency', comp['name']))
            self._save_embedding(cursor, doc_id, comp_text)
        
        # Speichere Partnerschaften
        for partner in kb['partnerships']:
            partner_text = f"Partner: {partner['name']} ({partner['status']}). {partner['description']}"
            doc_id = self._generate_id(partner_text)
            cursor.execute('''
                INSERT OR REPLACE INTO documents (id, content, source, category)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, partner_text, 'partnership', partner['name']))
            self._save_embedding(cursor, doc_id, partner_text)
        
        # Speichere FAQ
        for faq in kb['faq']:
            faq_text = f"Frage: {faq['question']} Antwort: {faq['answer']}"
            doc_id = self._generate_id(faq_text)
            cursor.execute('''
                INSERT OR REPLACE INTO documents (id, content, source, category)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, faq_text, 'faq', faq['question']))
            self._save_embedding(cursor, doc_id, faq_text)
        
        self.conn.commit()
        print(f"Knowledge Base geladen: {self._count_documents()} Dokumente")
    
    def _generate_id(self, text: str) -> str:
        """Generiere eindeutige ID aus Text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _save_embedding(self, cursor, doc_id: str, text: str):
        """Speichere Embedding-Hash"""
        embedding_hash = hashlib.sha256(text.encode()).hexdigest()
        cursor.execute('''
            INSERT OR REPLACE INTO embeddings (doc_id, embedding_hash)
            VALUES (?, ?)
        ''', (doc_id, embedding_hash))
    
    def _count_documents(self) -> int:
        """Zähle Dokumente in der Datenbank"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM documents')
        return cursor.fetchone()[0]
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Rufe die relevantesten Dokumente für eine Anfrage ab
        Nutzt einfache Keyword-Matching für lokale Suche
        """
        cursor = self.conn.cursor()
        
        # Einfache Keyword-Suche (kann durch echte Embeddings erweitert werden)
        query_words = query.lower().split()
        
        # Suche nach Dokumenten, die Query-Wörter enthalten
        placeholders = ' OR '.join(['content LIKE ?' for _ in query_words])
        params = [f'%{word}%' for word in query_words]
        
        cursor.execute(f'''
            SELECT id, content, source, category FROM documents
            WHERE {placeholders}
            LIMIT ?
        ''', params + [top_k])
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'content': row[1],
                'source': row[2],
                'category': row[3]
            })
        
        # Wenn keine Ergebnisse, gib die letzten Dokumente zurück
        if not results:
            cursor.execute('''
                SELECT id, content, source, category FROM documents
                LIMIT ?
            ''', (top_k,))
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'content': row[1],
                    'source': row[2],
                    'category': row[3]
                })
        
        return results
    
    def get_context(self, query: str, max_tokens: int = 2000) -> str:
        """
        Rufe Kontext für die LLM-Eingabe ab
        """
        documents = self.retrieve(query, top_k=5)
        
        context = "Relevante Informationen:\n\n"
        token_count = 0
        
        for doc in documents:
            doc_text = f"[{doc['category']}] {doc['content']}\n\n"
            token_count += len(doc_text.split())
            
            if token_count > max_tokens:
                break
            
            context += doc_text
        
        return context
    
    def close(self):
        """Schließe Datenbankverbindung"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Test
    rag = RAGSystem()
    
    # Test Retrieval
    test_queries = [
        "Was ist atio?",
        "Welche Lösungen bietet ihr an?",
        "Wie kann ich euch kontaktieren?",
        "AR Mixed Reality"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        context = rag.get_context(query)
        print(context)
    
    rag.close()
