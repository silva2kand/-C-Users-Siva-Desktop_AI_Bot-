const { ipcRenderer } = require('electron');

class BotInterface {
  constructor() {
    this.messagesContainer = document.getElementById('messages');
    this.messageInput = document.getElementById('message-input');
    this.sendBtn = document.getElementById('send-btn');
    this.minimizeBtn = document.getElementById('minimize-btn');
    this.closeBtn = document.getElementById('close-btn');
    this.statusIndicator = document.querySelector('.status-indicator');
    this.statusText = document.querySelector('.status-text');
        
    this.setupEventListeners();
    this.updateStatus('online');
  }

  setupEventListeners() {
    // Send message on button click
    this.sendBtn.addEventListener('click', () => this.sendMessage());
        
    // Send message on Enter key
    this.messageInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Window controls
    this.minimizeBtn.addEventListener('click', () => {
      ipcRenderer.invoke('toggle-bot-visibility');
    });

    this.closeBtn.addEventListener('click', () => {
      ipcRenderer.invoke('toggle-bot-visibility');
    });

    // Auto-resize input
    this.messageInput.addEventListener('input', (e) => {
      e.target.style.height = 'auto';
      e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px';
    });
  }

  async sendMessage() {
    const message = this.messageInput.value.trim();
    if (!message) return;

    // Clear input
    this.messageInput.value = '';
    this.messageInput.style.height = 'auto';

    // Add user message to chat
    this.addMessage(message, 'user');

    // Update status to thinking
    this.updateStatus('thinking');
    this.sendBtn.disabled = true;

    try {
      // Send message to main process for AI processing
      const response = await ipcRenderer.invoke('send-message', message);
            
      // Add bot response to chat
      setTimeout(() => {
        this.addMessage(response, 'bot');
        this.updateStatus('online');
        this.sendBtn.disabled = false;
      }, 500); // Small delay for better UX

    } catch (error) {
      console.error('Error sending message:', error);
      this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
      this.updateStatus('online');
      this.sendBtn.disabled = false;
    }
  }

  addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
        
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
        
    messageDiv.appendChild(messageContent);
    this.messagesContainer.appendChild(messageDiv);
        
    // Scroll to bottom
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  updateStatus(status) {
    this.statusIndicator.className = `status-indicator ${status}`;
        
    switch (status) {
    case 'online':
      this.statusText.textContent = 'Online';
      break;
    case 'thinking':
      this.statusText.textContent = 'Thinking...';
      break;
    case 'offline':
      this.statusText.textContent = 'Offline';
      break;
    }
  }

  // Method to handle incoming messages from other parts of the app
  receiveMessage(content) {
    this.addMessage(content, 'bot');
  }
}

// Initialize bot interface when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new BotInterface();
});

// Handle any messages from main process
ipcRenderer.on('bot-message', (event, message) => {
  if (window.botInterface) {
    window.botInterface.receiveMessage(message);
  }
});