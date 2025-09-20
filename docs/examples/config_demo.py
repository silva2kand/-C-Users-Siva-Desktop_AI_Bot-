#!/usr/bin/env python3
"""
Example: Configuration Customization
Shows how to customize bot behavior through configuration
"""

import sys
import os
from unittest.mock import patch

# Add src to path for examples
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.bot import Bot
from src.config import Config


def demo_default_config():
    """Demo with default configuration"""
    print("=== Default Configuration ===")
    print(f"Bot Name: {Config.BOT_NAME}")
    print(f"Personality: {Config.BOT_PERSONALITY}")
    print(f"Window Size: {Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
    print(f"Transparency: {Config.TRANSPARENCY}")
    print(f"Always on Top: {Config.ALWAYS_ON_TOP}")
    print()
    
    bot = Bot()
    response = bot.get_response("hello")
    print(f"Default bot response: {response}")
    print()


def demo_custom_config():
    """Demo with custom configuration using environment variables"""
    print("=== Custom Configuration ===")
    
    # Simulate custom environment variables
    custom_env = {
        "BOT_NAME": "CustomAssistant",
        "BOT_PERSONALITY": "technical_expert",
        "WINDOW_WIDTH": "400",
        "WINDOW_HEIGHT": "300",
        "TRANSPARENCY": "0.8",
        "ALWAYS_ON_TOP": "false"
    }
    
    with patch.dict(os.environ, custom_env):
        # Reload configuration to pick up changes
        from importlib import reload
        import src.config
        reload(src.config)
        
        print(f"Bot Name: {src.config.Config.BOT_NAME}")
        print(f"Personality: {src.config.Config.BOT_PERSONALITY}")
        print(f"Window Size: {src.config.Config.WINDOW_WIDTH}x{src.config.Config.WINDOW_HEIGHT}")
        print(f"Transparency: {src.config.Config.TRANSPARENCY}")
        print(f"Always on Top: {src.config.Config.ALWAYS_ON_TOP}")
        print()
        
        # Create bot with custom config
        custom_bot = Bot()
        response = custom_bot.get_response("hello")
        print(f"Custom bot response: {response}")
        print()


def demo_api_key_config():
    """Demo API key configuration (simulated)"""
    print("=== API Key Configuration ===")
    
    # Simulate having an API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "demo-key-12345"}):
        # Reload configuration
        from importlib import reload
        import src.config
        reload(src.config)
        
        is_valid = src.config.Config.validate()
        print(f"API Key provided: {'Yes' if src.config.Config.OPENAI_API_KEY else 'No'}")
        print(f"Configuration valid: {is_valid}")
        print("Note: This is a demo key - real API integration would require a valid OpenAI key")
        print()


def main():
    print("=== Configuration Customization Example ===\n")
    
    demo_default_config()
    demo_custom_config()
    demo_api_key_config()
    
    print("=== Configuration Tips ===")
    print("1. Set environment variables before running the application")
    print("2. Use .env file for persistent configuration")
    print("3. API key enables OpenAI responses, otherwise mock responses are used")
    print("4. Window settings can be adjusted for different screen sizes")
    print("5. Transparency and always-on-top help with desktop integration")


if __name__ == "__main__":
    main()