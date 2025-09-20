const { app, BrowserWindow, Tray, Menu, ipcMain, screen } = require('electron');
const path = require('path');
const Store = require('electron-store');
const AIService = require('./services/aiService');

// Initialize electron store for settings persistence
const store = new Store();
const aiService = new AIService();

class DesktopFloatingBot {
  constructor() {
    this.mainWindow = null;
    this.botWindow = null;
    this.tray = null;
    this.isQuitting = false;
  }

  createMainWindow() {
    // Create the main control window
    this.mainWindow = new BrowserWindow({
      width: 400,
      height: 600,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
      },
      show: false,
      skipTaskbar: true,
      alwaysOnTop: true,
      frame: false,
      resizable: false
    });

    this.mainWindow.loadFile('src/renderer/main.html');

    // Hide window instead of closing when user clicks X
    this.mainWindow.on('close', (event) => {
      if (!this.isQuitting) {
        event.preventDefault();
        this.mainWindow.hide();
      }
    });
  }

  createBotWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    
    // Create floating bot window
    this.botWindow = new BrowserWindow({
      width: 300,
      height: 400,
      x: width - 320,
      y: height - 420,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
      },
      frame: false,
      alwaysOnTop: true,
      skipTaskbar: true,
      resizable: false,
      transparent: true,
      show: false
    });

    this.botWindow.loadFile('src/renderer/bot.html');

    // Make bot window draggable
    this.botWindow.setIgnoreMouseEvents(false);
  }

  createTray() {
    // Create system tray icon
    this.tray = new Tray(path.join(__dirname, '../assets/icon.png'));
    
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'Show Bot',
        click: () => {
          if (this.botWindow) {
            this.botWindow.show();
          }
        }
      },
      {
        label: 'Hide Bot',
        click: () => {
          if (this.botWindow) {
            this.botWindow.hide();
          }
        }
      },
      {
        label: 'Settings',
        click: () => {
          if (this.mainWindow) {
            this.mainWindow.show();
          }
        }
      },
      { type: 'separator' },
      {
        label: 'Quit',
        click: () => {
          this.isQuitting = true;
          app.quit();
        }
      }
    ]);

    this.tray.setContextMenu(contextMenu);
    this.tray.setToolTip('Desktop Floating Bots');

    // Double click tray to show/hide bot
    this.tray.on('double-click', () => {
      if (this.botWindow) {
        if (this.botWindow.isVisible()) {
          this.botWindow.hide();
        } else {
          this.botWindow.show();
        }
      }
    });
  }

  setupIPC() {
    // IPC handlers for communication between main and renderer processes
    ipcMain.handle('get-settings', () => {
      return store.get('settings', {
        botName: 'Assistant',
        alwaysOnTop: true,
        autoStart: false,
        theme: 'light',
        apiKey: ''
      });
    });

    ipcMain.handle('save-settings', (event, settings) => {
      store.set('settings', settings);
      
      // Update AI service with new API key
      if (settings.apiKey) {
        aiService.setApiKey(settings.apiKey);
      }
      
      return true;
    });

    ipcMain.handle('toggle-bot-visibility', () => {
      if (this.botWindow) {
        if (this.botWindow.isVisible()) {
          this.botWindow.hide();
          return false;
        } else {
          this.botWindow.show();
          return true;
        }
      }
      return false;
    });

    ipcMain.handle('send-message', async (event, message) => {
      try {
        // Get conversation history from store (optional)
        const history = store.get('conversationHistory', []);
        
        // Send message to AI service
        const response = await aiService.sendMessage(message, history);
        
        // Optionally save conversation history
        const newHistory = [
          ...history,
          { role: 'user', content: message },
          { role: 'assistant', content: response }
        ];
        
        // Keep only last 10 exchanges to prevent storage bloat
        const trimmedHistory = newHistory.slice(-20);
        store.set('conversationHistory', trimmedHistory);
        
        return response;
      } catch (error) {
        console.error('Error processing message:', error);
        return 'Sorry, I encountered an error processing your message. Please try again.';
      }
    });

    ipcMain.handle('clear-conversation', () => {
      store.delete('conversationHistory');
      return true;
    });

    ipcMain.handle('get-ai-status', () => {
      return {
        configured: aiService.isConfigured(),
        model: aiService.model
      };
    });
  }

  initialize() {
    // Initialize the application
    this.createMainWindow();
    this.createBotWindow();
    this.createTray();
    this.setupIPC();

    // Load existing settings and configure AI service
    const settings = store.get('settings', {});
    if (settings.apiKey) {
      aiService.setApiKey(settings.apiKey);
    }

    // Show bot window by default
    setTimeout(() => {
      if (this.botWindow) {
        this.botWindow.show();
      }
    }, 1000);
  }
}

// App event handlers
app.whenReady().then(() => {
  const bot = new DesktopFloatingBot();
  bot.initialize();
});

app.on('window-all-closed', () => {
  // Don't quit the app when all windows are closed on macOS
  if (process.platform !== 'darwin') {
    // Keep running in background via system tray
  }
});

app.on('activate', () => {
  // Re-create windows if needed on macOS
  if (BrowserWindow.getAllWindows().length === 0) {
    const bot = new DesktopFloatingBot();
    bot.initialize();
  }
});

// Prevent multiple instances
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    // Someone tried to run a second instance, focus our window instead
    const windows = BrowserWindow.getAllWindows();
    if (windows.length > 0) {
      const mainWindow = windows.find(w => w.webContents.getURL().includes('main.html'));
      if (mainWindow) {
        if (mainWindow.isMinimized()) mainWindow.restore();
        mainWindow.focus();
      }
    }
  });
}