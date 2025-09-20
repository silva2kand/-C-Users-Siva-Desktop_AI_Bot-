"""
Configuration module for Desktop Floating Bots
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application"""

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Bot Configuration
    BOT_NAME: str = os.getenv("BOT_NAME", "FloatingBot")
    BOT_PERSONALITY: str = os.getenv("BOT_PERSONALITY", "helpful_assistant")
    UPDATE_INTERVAL: int = int(os.getenv("UPDATE_INTERVAL", "1000"))

    # UI Configuration
    WINDOW_WIDTH: int = int(os.getenv("WINDOW_WIDTH", "300"))
    WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "200"))
    TRANSPARENCY: float = float(os.getenv("TRANSPARENCY", "0.9"))
    ALWAYS_ON_TOP: bool = os.getenv("ALWAYS_ON_TOP", "true").lower() == "true"

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set. Bot will use mock responses.")
            return False
        return True
