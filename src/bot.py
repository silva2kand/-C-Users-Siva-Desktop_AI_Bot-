"""
Bot logic module for handling AI interactions
"""

import random
from typing import Dict, Any

try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .config import Config


class Bot:
    """AI Bot class for handling conversations"""

    def __init__(self, name: str = None, personality: str = None):
        self.name = name or Config.BOT_NAME
        self.personality = personality or Config.BOT_PERSONALITY
        self.conversation_history = []

        # Initialize OpenAI if available and API key is set
        self.openai_client = None
        if OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            try:
                openai.api_key = Config.OPENAI_API_KEY
                self.openai_client = openai
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")

    def get_response(self, user_input: str) -> str:
        """Get AI response to user input"""
        try:
            if self.openai_client and Config.OPENAI_API_KEY:
                return self._get_openai_response(user_input)
            else:
                return self._get_mock_response(user_input)
        except Exception as e:
            print(f"Error getting bot response: {e}")
            return "Sorry, I encountered an error. Please try again."

    def _get_openai_response(self, user_input: str) -> str:
        """Get response from OpenAI API"""
        try:
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Prepare messages with system personality
            messages = [
                {
                    "role": "system",
                    "content": f"You are {self.name}, a {self.personality}. Keep responses concise and helpful.",
                }
            ]
            messages.extend(self.conversation_history[-5:])  # Keep last 5 exchanges

            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7,
            )

            bot_response = response.choices[0].message.content.strip()
            self.conversation_history.append(
                {"role": "assistant", "content": bot_response}
            )

            return bot_response
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_mock_response(user_input)

    def _get_mock_response(self, user_input: str) -> str:
        """Get mock response when OpenAI is not available"""
        user_input_lower = user_input.lower()

        # Simple keyword-based responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            responses = [
                f"Hello! I'm {self.name}, your floating desktop assistant!",
                "Hi there! How can I help you today?",
                "Hey! What can I do for you?",
            ]
        elif any(word in user_input_lower for word in ["help", "what", "how"]):
            responses = [
                "I'm here to help! You can ask me questions or just chat.",
                "I can assist with various tasks. What do you need help with?",
                "Feel free to ask me anything - I'm here to help!",
            ]
        elif any(word in user_input_lower for word in ["bye", "goodbye", "exit"]):
            responses = [
                "Goodbye! Thanks for chatting with me!",
                "See you later! Have a great day!",
                "Farewell! Come back anytime!",
            ]
        elif any(word in user_input_lower for word in ["time", "date"]):
            import datetime

            now = datetime.datetime.now()
            return f"It's currently {now.strftime('%H:%M on %B %d, %Y')}"
        elif any(word in user_input_lower for word in ["weather"]):
            responses = [
                "I don't have access to weather data right now, but you can check your local weather service!",
                "For weather updates, I'd recommend checking a weather app or website.",
            ]
        else:
            responses = [
                "That's interesting! Tell me more.",
                "I understand. What else would you like to discuss?",
                "Thanks for sharing that with me!",
                "Interesting point! Anything else on your mind?",
                f"As {self.name}, I find that fascinating!",
            ]

        return random.choice(responses)

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []

    def get_status(self) -> Dict[str, Any]:
        """Get bot status information"""
        return {
            "name": self.name,
            "personality": self.personality,
            "conversation_length": len(self.conversation_history),
            "openai_available": self.openai_client is not None,
        }
