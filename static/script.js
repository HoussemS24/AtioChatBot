// ATIO Chatbot JavaScript

const API_BASE_URL = 'http://localhost:8000';
let conversationId = 'conv_' + Date.now();
let isOpen = false;

// DOM Elements
const chatbotContainer = document.querySelector('.chatbot-container');
const chatbotToggle = document.getElementById('chatbotToggle');
const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('userInput');
const loadingIndicator = document.getElementById('loading');

// Toggle Chatbot
function toggleChatbot() {
    isOpen = !isOpen;
    
    if (isOpen) {
        chatbotContainer.classList.remove('hidden');
        chatbotToggle.classList.add('hidden');
        userInput.focus();
    } else {
        chatbotContainer.classList.add('hidden');
        chatbotToggle.classList.remove('hidden');
    }
}

// Handle Enter Key
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send Message
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    addMessage(message, 'user');
    userInput.value = '';
    
    // Show loading
    loadingIndicator.style.display = 'flex';
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId,
                language: 'de'
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API Error');
        }
        
        const data = await response.json();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        
        let errorMessage = 'Entschuldigung, es gab einen Fehler.';
        
        if (error.message.includes('fetch')) {
            errorMessage = 'Verbindungsfehler. Bitte stellen Sie sicher, dass der Backend-Server läuft (http://localhost:8000)';
        } else if (error.message.includes('Ollama')) {
            errorMessage = 'Ollama ist nicht erreichbar. Bitte starten Sie Ollama auf Ihrem Computer.';
        } else {
            errorMessage = `Fehler: ${error.message}`;
        }
        
        addMessage(errorMessage, 'bot');
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

// Add Message to Chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parse text for links and formatting
    contentDiv.innerHTML = parseMessage(text);
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Parse Message for Formatting
function parseMessage(text) {
    // Escape HTML
    let escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Convert URLs to links
    escaped = escaped.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" style="color: inherit; text-decoration: underline;">$1</a>'
    );
    
    // Convert line breaks
    escaped = escaped.replace(/\n/g, '<br>');
    
    // Bold text between **
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    return escaped;
}

// Check API Health on Load
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('API Health:', data);
            
            if (!data.ollama_connected) {
                console.warn('⚠️ Ollama nicht verbunden');
            }
            if (!data.rag_ready) {
                console.warn('⚠️ RAG System nicht bereit');
            }
        }
    } catch (error) {
        console.error('API nicht erreichbar:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('ATIO Chatbot Widget geladen');
    checkApiHealth();
    
    // Set initial state
    chatbotContainer.classList.add('hidden');
    userInput.focus();
});

// Keyboard shortcut: Ctrl+Shift+A to toggle chatbot
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'A') {
        toggleChatbot();
    }
});
