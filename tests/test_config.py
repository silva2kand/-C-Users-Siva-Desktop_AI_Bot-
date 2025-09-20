"""
Test configuration module
"""

import pytest
import os
from src.config import Config


class TestConfig:
    """Test cases for configuration module"""

    def test_default_values(self):
        """Test default configuration values"""
        assert Config.BOT_NAME == "FloatingBot"
        assert Config.BOT_PERSONALITY == "helpful_assistant"
        assert Config.UPDATE_INTERVAL == 1000
        assert Config.WINDOW_WIDTH == 300
        assert Config.WINDOW_HEIGHT == 200
        assert Config.TRANSPARENCY == 0.9
        assert Config.ALWAYS_ON_TOP is True

    def test_environment_override(self, monkeypatch):
        """Test environment variable override"""
        monkeypatch.setenv("BOT_NAME", "TestBot")
        monkeypatch.setenv("WINDOW_WIDTH", "400")
        monkeypatch.setenv("TRANSPARENCY", "0.8")

        # Reload config
        from importlib import reload
        import src.config

        reload(src.config)

        assert src.config.Config.BOT_NAME == "TestBot"
        assert src.config.Config.WINDOW_WIDTH == 400
        assert src.config.Config.TRANSPARENCY == 0.8

    def test_validate_with_api_key(self, monkeypatch):
        """Test validation with API key"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        # Reload config
        from importlib import reload
        import src.config

        reload(src.config)

        assert src.config.Config.validate() is True

    def test_validate_without_api_key(self, monkeypatch):
        """Test validation without API key"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        # Reload config
        from importlib import reload
        import src.config

        reload(src.config)

        assert src.config.Config.validate() is False
