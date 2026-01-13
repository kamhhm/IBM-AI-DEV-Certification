/**
 * RAG for Tech Docs - Frontend
 */

// State
let isFirstMessage = true;
let documentLoaded = false;

const baseUrl = window.location.origin;

// DOM elements
const messageList = document.getElementById('message-list');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const resetButton = document.getElementById('reset-button');
const loadingIndicator = document.getElementById('loading-indicator');
const chatWindow = document.getElementById('chat-window');
const fileUpload = document.getElementById('file-upload');

// Helper functions
function scrollToBottom() {
    chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}

function showLoading() {
    loadingIndicator.classList.remove('hidden');
    sendButton.disabled = true;
}

function hideLoading() {
    loadingIndicator.classList.add('hidden');
    if (documentLoaded) {
        sendButton.disabled = false;
    }
}

function sanitize(text) {
    return text.trim().replace(/<[^>]*>/g, '').replace(/[<>&]/g, '');
}

// Add a message to the chat
function addMessage(content, isUser, extraHtml = '') {
    const div = document.createElement('div');
    div.className = `message message--${isUser ? 'user' : 'assistant'}`;
    div.innerHTML = `
        <div class="message-avatar">${isUser ? 'You' : 'AI'}</div>
        <div class="message-content">${content}${extraHtml}</div>
    `;
    messageList.appendChild(div);
    scrollToBottom();
}

// Upload UI HTML
function getUploadHtml() {
    return `
        <div class="upload-area" id="upload-area">
            <p class="upload-label">Document Upload</p>
            <p class="upload-text">Drag and drop a <strong>PDF file</strong> here, or click to browse</p>
            <button type="button" class="btn-upload" id="upload-button">Select PDF</button>
        </div>
    `;
}

// Setup upload button and drag/drop
function setupUpload() {
    const uploadArea = document.getElementById('upload-area');
    const uploadButton = document.getElementById('upload-button');
    
    if (uploadButton) {
        uploadButton.onclick = () => fileUpload.click();
    }
    
    if (uploadArea) {
        uploadArea.onclick = (e) => {
            if (e.target.id !== 'upload-button') fileUpload.click();
        };
        
        uploadArea.ondragover = (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#333';
        };
        
        uploadArea.ondragleave = () => {
            uploadArea.style.borderColor = '';
        };
        
        uploadArea.ondrop = (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '';
            if (e.dataTransfer.files.length > 0) {
                handleFileUpload(e.dataTransfer.files[0]);
            }
        };
    }
}

// Handle file upload
async function handleFileUpload(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        alert('Please upload a PDF file');
        return;
    }
    
    const uploadButton = document.getElementById('upload-button');
    if (uploadButton) {
        uploadButton.disabled = true;
        uploadButton.textContent = 'Processing...';
    }
    
    showLoading();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${baseUrl}/process-document`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        hideLoading();
        
        if (response.ok) {
            documentLoaded = true;
            const uploadArea = document.getElementById('upload-area');
            if (uploadArea) uploadArea.remove();
        }
        
        addMessage(data.botResponse, false);
        
        if (documentLoaded) {
            isFirstMessage = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    } catch (error) {
        hideLoading();
        addMessage('Error uploading file. Please try again.', false);
    }
}

// Send a message
async function sendMessage() {
    const message = sanitize(messageInput.value);
    if (!message) return;
    
    addMessage(message, true);
    messageInput.value = '';
    showLoading();
    
    try {
        const response = await fetch(`${baseUrl}/process-message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userMessage: message })
        });
        const data = await response.json();
        
        hideLoading();
        addMessage(data.botResponse || data.error, false);
    } catch (error) {
        hideLoading();
        addMessage('Error sending message. Please try again.', false);
    }
}

// Reset conversation
async function resetChat() {
    messageList.innerHTML = '';
    isFirstMessage = true;
    documentLoaded = false;
    
    try {
        await fetch(`${baseUrl}/clear-history`, { method: 'POST' });
    } catch (e) {
        // ignore
    }
    
    showWelcome();
}

// Show welcome message
function showWelcome() {
    const welcomeText = "Welcome! I'm your technical documentation assistant. Upload a PDF document to get started.";
    addMessage(welcomeText, false, getUploadHtml());
    setTimeout(setupUpload, 0);
    sendButton.disabled = true;
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    showWelcome();
    
    sendButton.onclick = sendMessage;
    resetButton.onclick = resetChat;
    
    messageInput.onkeydown = (e) => {
        if (e.key === 'Enter') sendMessage();
    };
    
    messageInput.oninput = () => {
        if (documentLoaded) {
            sendButton.disabled = !messageInput.value.trim();
        }
    };
    
    fileUpload.onchange = () => {
        if (fileUpload.files.length > 0) {
            handleFileUpload(fileUpload.files[0]);
        }
    };
});
