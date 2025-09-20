#!/usr/bin/env python3
"""
Example: Basic Bot Usage
Demonstrates creating and using a bot instance directly
"""

import sys
import os

# Add src to path for examples
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.bot import Bot
from src.config import Config


def main():
    print("=== Basic Bot Usage Example ===\n")
    
    # Create a bot instance
    bot = Bot(name="ExampleBot", personality="friendly_helper")
    print(f"Created bot: {bot.name}")
    print(f"Personality: {bot.personality}")
    print()
    
    # Test different types of conversations
    test_conversations = [
        "Hello, how are you?",
        "Can you help me with something?",
        "What time is it?",
        "Tell me about the weather",
        "What's your name?",
        "Goodbye!"
    ]
    
    print("Starting conversation:")
    print("-" * 40)
    
    for message in test_conversations:
        print(f"You: {message}")
        response = bot.get_response(message)
        print(f"Bot: {response}")
        print()
    
    # Show bot status
    print("Bot Status:")
    print("-" * 40)
    status = bot.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()