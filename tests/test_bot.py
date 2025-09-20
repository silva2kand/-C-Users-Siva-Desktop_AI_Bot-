"""
Test bot module
"""

import pytest
from unittest.mock import Mock, patch
from src.bot import Bot


class TestBot:
    """Test cases for bot module"""

    def test_bot_initialization(self):
        """Test bot initialization"""
        bot = Bot(name="TestBot", personality="test_personality")
        assert bot.name == "TestBot"
        assert bot.personality == "test_personality"
        assert bot.conversation_history == []

    def test_bot_default_initialization(self):
        """Test bot initialization with defaults"""
        bot = Bot()
        assert bot.name == "FloatingBot"  # From config default
        assert bot.personality == "helpful_assistant"  # From config default
        assert bot.conversation_history == []

    def test_mock_response_hello(self):
        """Test mock response for hello message"""
        bot = Bot()
        response = bot.get_response("hello")
        assert isinstance(response, str)
        assert len(response) > 0
        assert any(word in response.lower() for word in ["hello", "hi", "hey"])

    def test_mock_response_help(self):
        """Test mock response for help message"""
        bot = Bot()
        response = bot.get_response("help")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_mock_response_goodbye(self):
        """Test mock response for goodbye message"""
        bot = Bot()
        response = bot.get_response("goodbye")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_mock_response_time(self):
        """Test mock response for time query"""
        bot = Bot()
        response = bot.get_response("what time is it")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_mock_response_general(self):
        """Test mock response for general message"""
        bot = Bot()
        response = bot.get_response("This is a random message")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_reset_conversation(self):
        """Test conversation reset"""
        bot = Bot()
        # Add some conversation history
        bot.conversation_history.append({"role": "user", "content": "test"})
        bot.conversation_history.append({"role": "assistant", "content": "response"})

        assert len(bot.conversation_history) == 2

        bot.reset_conversation()
        assert len(bot.conversation_history) == 0

    def test_get_status(self):
        """Test status retrieval"""
        bot = Bot(name="TestBot", personality="test")
        status = bot.get_status()

        assert isinstance(status, dict)
        assert status["name"] == "TestBot"
        assert status["personality"] == "test"
        assert status["conversation_length"] == 0
        assert "openai_available" in status

    def test_error_handling(self):
        """Test error handling in get_response"""
        bot = Bot()

        # Simulate error by mocking the _get_mock_response method to raise exception
        with patch.object(
            bot, "_get_mock_response", side_effect=Exception("Test error")
        ):
            response = bot.get_response("test")
            assert "error" in response.lower()

    @patch("src.bot.OPENAI_AVAILABLE", True)
    @patch("src.bot.Config.OPENAI_API_KEY", "test-key")
    def test_openai_initialization(self):
        """Test OpenAI client initialization when available"""
        with patch("src.bot.openai") as mock_openai:
            bot = Bot()
            assert bot.openai_client is not None

    @patch("src.bot.OPENAI_AVAILABLE", False)
    def test_no_openai_initialization(self):
        """Test behavior when OpenAI is not available"""
        bot = Bot()
        assert bot.openai_client is None

    def test_conversation_history_management(self):
        """Test conversation history is properly managed"""
        bot = Bot()

        # Simulate adding conversation history
        for i in range(10):
            bot.conversation_history.append({"role": "user", "content": f"message {i}"})
            bot.conversation_history.append(
                {"role": "assistant", "content": f"response {i}"}
            )

        assert len(bot.conversation_history) == 20

        # Test that status reflects the correct length
        status = bot.get_status()
        assert status["conversation_length"] == 20
