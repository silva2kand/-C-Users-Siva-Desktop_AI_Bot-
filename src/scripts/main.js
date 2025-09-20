const { ipcRenderer } = require('electron');

class SettingsInterface {
  constructor() {
    this.settings = {};
    this.initializeElements();
    this.setupEventListeners();
    this.loadSettings();
  }

  initializeElements() {
    this.botNameInput = document.getElementById('bot-name');
    this.alwaysOnTopCheckbox = document.getElementById('always-on-top');
    this.autoStartCheckbox = document.getElementById('auto-start');
    this.themeSelect = document.getElementById('theme');
    this.apiKeyInput = document.getElementById('api-key');
    this.saveBtn = document.getElementById('save-btn');
    this.toggleBotBtn = document.getElementById('toggle-bot-btn');
    this.closeSettingsBtn = document.getElementById('close-settings-btn');
  }

  setupEventListeners() {
    this.saveBtn.addEventListener('click', () => this.saveSettings());
    this.toggleBotBtn.addEventListener('click', () => this.toggleBotVisibility());
    this.closeSettingsBtn.addEventListener('click', () => this.closeSettings());

    // Save settings on Enter key in text inputs
    [this.botNameInput, this.apiKeyInput].forEach(input => {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.saveSettings();
        }
      });
    });

    // Auto-save on checkbox changes
    [this.alwaysOnTopCheckbox, this.autoStartCheckbox].forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        this.saveSettings();
      });
    });

    // Auto-save on theme change
    this.themeSelect.addEventListener('change', () => {
      this.saveSettings();
    });
  }

  async loadSettings() {
    try {
      this.settings = await ipcRenderer.invoke('get-settings');
      this.populateForm();
    } catch (error) {
      console.error('Error loading settings:', error);
      this.showNotification('Error loading settings', 'error');
    }
  }

  populateForm() {
    this.botNameInput.value = this.settings.botName || 'Assistant';
    this.alwaysOnTopCheckbox.checked = this.settings.alwaysOnTop !== false;
    this.autoStartCheckbox.checked = this.settings.autoStart === true;
    this.themeSelect.value = this.settings.theme || 'light';
    this.apiKeyInput.value = this.settings.apiKey || '';
  }

  async saveSettings() {
    try {
      // Collect current form values
      const newSettings = {
        botName: this.botNameInput.value.trim() || 'Assistant',
        alwaysOnTop: this.alwaysOnTopCheckbox.checked,
        autoStart: this.autoStartCheckbox.checked,
        theme: this.themeSelect.value,
        apiKey: this.apiKeyInput.value.trim()
      };

      // Save to main process
      await ipcRenderer.invoke('save-settings', newSettings);
      this.settings = newSettings;
            
      this.showNotification('Settings saved successfully!', 'success');
            
      // Update save button state
      this.saveBtn.textContent = 'Saved!';
      this.saveBtn.style.background = '#4caf50';
            
      setTimeout(() => {
        this.saveBtn.textContent = 'Save Settings';
        this.saveBtn.style.background = '';
      }, 2000);

    } catch (error) {
      console.error('Error saving settings:', error);
      this.showNotification('Error saving settings', 'error');
    }
  }

  async toggleBotVisibility() {
    try {
      const isVisible = await ipcRenderer.invoke('toggle-bot-visibility');
      this.toggleBotBtn.textContent = isVisible ? 'Hide Bot' : 'Show Bot';
      this.showNotification(
        isVisible ? 'Bot is now visible' : 'Bot is now hidden', 
        'info'
      );
    } catch (error) {
      console.error('Error toggling bot visibility:', error);
      this.showNotification('Error toggling bot visibility', 'error');
    }
  }

  closeSettings() {
    window.close();
  }

  showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Style the notification
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '12px 16px',
      borderRadius: '6px',
      color: 'white',
      fontWeight: '500',
      fontSize: '14px',
      zIndex: '1000',
      opacity: '0',
      transform: 'translateX(100%)',
      transition: 'all 0.3s ease'
    });

    // Set background color based on type
    const colors = {
      success: '#4caf50',
      error: '#f44336',
      info: '#2196f3',
      warning: '#ff9800'
    };
    notification.style.background = colors[type] || colors.info;

    // Add to document
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
      notification.style.opacity = '1';
      notification.style.transform = 'translateX(0)';
    }, 10);

    // Auto remove after 3 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateX(100%)';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // Method to validate API key format
  validateApiKey(apiKey) {
    if (!apiKey) return true; // Empty is okay
    return apiKey.startsWith('sk-') && apiKey.length > 20;
  }

  // Method to handle API key input validation
  setupApiKeyValidation() {
    this.apiKeyInput.addEventListener('blur', () => {
      const apiKey = this.apiKeyInput.value.trim();
      if (apiKey && !this.validateApiKey(apiKey)) {
        this.showNotification('Invalid API key format', 'warning');
        this.apiKeyInput.style.borderColor = '#ff9800';
      } else {
        this.apiKeyInput.style.borderColor = '';
      }
    });
  }
}

// Initialize settings interface when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const settingsInterface = new SettingsInterface();
  settingsInterface.setupApiKeyValidation();
    
  // Make it globally accessible for debugging
  window.settingsInterface = settingsInterface;
});