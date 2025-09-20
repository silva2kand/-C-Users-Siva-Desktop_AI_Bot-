"""
Integration tests for the main application
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.main import FloatingBotsApp


class TestFloatingBotsApp:
    """Test cases for main application"""

    @patch("src.main.FloatingBotWindow")
    @patch("src.main.SystemTrayIcon")
    @patch("src.main.Bot")
    def test_app_initialization(self, mock_bot, mock_tray, mock_ui):
        """Test application initialization"""
        # Setup mocks
        mock_bot_instance = Mock()
        mock_bot.return_value = mock_bot_instance
        mock_bot_instance.name = "TestBot"

        mock_ui_instance = Mock()
        mock_ui.return_value = mock_ui_instance

        mock_tray_instance = Mock()
        mock_tray_instance.icon = Mock()
        mock_tray.return_value = mock_tray_instance

        # Test initialization
        app = FloatingBotsApp()
        app.initialize()

        assert app.bot is not None
        assert app.ui is not None
        assert app.tray is not None

        # Verify mocks were called
        mock_bot.assert_called_once()
        mock_ui.assert_called_once()
        mock_tray.assert_called_once()

    @patch("src.main.FloatingBotWindow")
    @patch("src.main.SystemTrayIcon")
    @patch("src.main.Bot")
    def test_app_run(self, mock_bot, mock_tray, mock_ui):
        """Test application run method"""
        # Setup mocks
        mock_ui_instance = Mock()
        mock_ui.return_value = mock_ui_instance

        mock_tray_instance = Mock()
        mock_tray_instance.icon = Mock()
        mock_tray.return_value = mock_tray_instance

        # Test run
        app = FloatingBotsApp()
        app.initialize()

        # Mock the UI run method to avoid actually starting GUI
        mock_ui_instance.run = Mock()
        app.run()

        mock_ui_instance.run.assert_called_once()

    def test_app_run_without_initialization(self):
        """Test app run fails without initialization"""
        app = FloatingBotsApp()

        with pytest.raises(RuntimeError, match="Application not initialized"):
            app.run()

    @patch("src.main.FloatingBotWindow")
    @patch("src.main.SystemTrayIcon")
    @patch("src.main.Bot")
    def test_app_shutdown(self, mock_bot, mock_tray, mock_ui):
        """Test application shutdown"""
        # Setup mocks
        mock_ui_instance = Mock()
        mock_ui_instance.root = Mock()
        mock_ui.return_value = mock_ui_instance

        mock_tray_instance = Mock()
        mock_tray_instance.icon = Mock()
        mock_tray.return_value = mock_tray_instance

        # Test shutdown
        app = FloatingBotsApp()
        app.initialize()
        app.shutdown()

        # Verify shutdown methods were called
        mock_tray_instance.icon.stop.assert_called_once()
        mock_ui_instance.root.quit.assert_called_once()

    @patch("src.main.FloatingBotsApp")
    @patch("sys.argv", ["main.py", "--version"])
    def test_main_version_argument(self, mock_app):
        """Test main function with version argument"""
        from src.main import main

        with pytest.raises(SystemExit):
            main()

    @patch("src.main.FloatingBotsApp")
    @patch("sys.argv", ["main.py"])
    def test_main_normal_execution(self, mock_app_class):
        """Test main function normal execution"""
        from src.main import main

        # Setup mock
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        main()

        # Verify app methods were called
        mock_app.initialize.assert_called_once()
        mock_app.run.assert_called_once()

    @patch("src.main.FloatingBotsApp")
    @patch("sys.argv", ["main.py"])
    def test_main_exception_handling(self, mock_app_class):
        """Test main function exception handling"""
        from src.main import main

        # Setup mock to raise exception
        mock_app = Mock()
        mock_app.initialize.side_effect = Exception("Test error")
        mock_app_class.return_value = mock_app

        with pytest.raises(SystemExit):
            main()


class TestIntegration:
    """Integration tests for full application flow"""

    @patch("tkinter.Tk")
    @patch("src.main.SystemTrayIcon")
    def test_full_application_flow(self, mock_tray, mock_tk):
        """Test full application initialization and basic flow"""
        # Mock Tkinter to avoid GUI
        mock_root = Mock()
        mock_tk.return_value = mock_root

        # Mock tray icon
        mock_tray_instance = Mock()
        mock_tray_instance.icon = None  # Simulate no system tray
        mock_tray.return_value = mock_tray_instance

        # Test full flow
        app = FloatingBotsApp()
        app.initialize()

        # Verify components are created
        assert app.bot is not None
        assert app.ui is not None
        assert app.tray is not None

        # Test bot functionality
        response = app.bot.get_response("hello")
        assert isinstance(response, str)
        assert len(response) > 0

        # Test status
        status = app.bot.get_status()
        assert isinstance(status, dict)
        assert "name" in status
