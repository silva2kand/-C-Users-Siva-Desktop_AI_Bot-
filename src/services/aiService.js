const axios = require('axios');

class AIService {
  constructor() {
    this.apiKey = null;
    this.baseURL = 'https://api.openai.com/v1';
    this.model = 'gpt-3.5-turbo';
    this.maxTokens = 150;
    this.temperature = 0.7;
  }

  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }

  isConfigured() {
    return this.apiKey && this.apiKey.startsWith('sk-') && this.apiKey.length > 20;
  }

  async sendMessage(message, conversationHistory = []) {
    if (!this.isConfigured()) {
      return this.getFallbackResponse(message);
    }

    try {
      const messages = [
        {
          role: 'system',
          content: 'You are a helpful desktop assistant. Keep responses concise and helpful. You can help with tasks, answer questions, and provide information.'
        },
        ...conversationHistory,
        {
          role: 'user',
          content: message
        }
      ];

      const response = await axios.post(
        `${this.baseURL}/chat/completions`,
        {
          model: this.model,
          messages: messages,
          max_tokens: this.maxTokens,
          temperature: this.temperature,
          top_p: 1,
          frequency_penalty: 0,
          presence_penalty: 0
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          timeout: 30000 // 30 second timeout
        }
      );

      if (response.data && response.data.choices && response.data.choices.length > 0) {
        return response.data.choices[0].message.content.trim();
      } else {
        return 'I received an unexpected response format. Please try again.';
      }

    } catch (error) {
      console.error('AI Service Error:', error);
      return this.handleError(error);
    }
  }

  getFallbackResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Simple pattern matching for common queries
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      return 'Hello! I\'m your desktop assistant. To enable AI responses, please configure your OpenAI API key in settings.';
    }
    
    if (lowerMessage.includes('time')) {
      return `The current time is ${new Date().toLocaleTimeString()}.`;
    }
    
    if (lowerMessage.includes('date')) {
      return `Today is ${new Date().toLocaleDateString()}.`;
    }
    
    if (lowerMessage.includes('weather')) {
      return 'I can\'t check the weather without an API key. Please configure your OpenAI API key in settings to enable full AI capabilities.';
    }
    
    if (lowerMessage.includes('help')) {
      return 'I can help you with various tasks once you configure your OpenAI API key in settings. Right-click the system tray icon and select "Settings" to get started.';
    }
    
    if (lowerMessage.includes('settings') || lowerMessage.includes('config')) {
      return 'To access settings, right-click on the system tray icon and select "Settings". There you can configure your API key and other preferences.';
    }
    
    // Default response
    return `I understand you said: "${message}". To provide intelligent responses, please configure your OpenAI API key in the settings. For now, I can help with basic queries about time, date, and settings.`;
  }

  handleError(error) {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data;
      
      switch (status) {
      case 401:
        return 'Invalid API key. Please check your OpenAI API key in settings.';
      case 429:
        return 'Rate limit exceeded. Please wait a moment and try again.';
      case 500:
        return 'OpenAI service is temporarily unavailable. Please try again later.';
      case 503:
        return 'OpenAI service is overloaded. Please try again in a few moments.';
      default:
        if (data && data.error && data.error.message) {
          return `AI service error: ${data.error.message}`;
        }
        return `AI service returned an error (${status}). Please try again.`;
      }
    } else if (error.request) {
      // Network error
      return 'Unable to connect to AI service. Please check your internet connection.';
    } else {
      // Other error
      return 'An unexpected error occurred. Please try again.';
    }
  }

  // Method to validate API key format
  static validateApiKey(apiKey) {
    if (!apiKey || typeof apiKey !== 'string') {
      return false;
    }
    
    return apiKey.startsWith('sk-') && apiKey.length > 20;
  }

  // Method to get available models (for future enhancement)
  async getAvailableModels() {
    if (!this.isConfigured()) {
      return ['gpt-3.5-turbo']; // Default model
    }

    try {
      const response = await axios.get(`${this.baseURL}/models`, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      });

      return response.data.data
        .filter(model => model.id.includes('gpt'))
        .map(model => model.id)
        .sort();
    } catch (error) {
      console.error('Error fetching models:', error);
      return ['gpt-3.5-turbo', 'gpt-4'];
    }
  }

  // Method to estimate token usage
  estimateTokens(text) {
    // Rough estimation: 1 token ≈ 4 characters for English text
    return Math.ceil(text.length / 4);
  }

  // Method to truncate conversation history to stay within token limits
  truncateHistory(history, maxTokens = 3000) {
    let totalTokens = 0;
    const truncatedHistory = [];

    // Start from the most recent messages and work backwards
    for (let i = history.length - 1; i >= 0; i--) {
      const messageTokens = this.estimateTokens(history[i].content);
      
      if (totalTokens + messageTokens > maxTokens) {
        break;
      }
      
      totalTokens += messageTokens;
      truncatedHistory.unshift(history[i]);
    }

    return truncatedHistory;
  }
}

module.exports = AIService;