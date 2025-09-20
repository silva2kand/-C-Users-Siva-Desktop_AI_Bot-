"""
Main application entry point for Desktop Floating Bots
"""

import sys
import argparse
from typing import Optional

from .config import Config
from .bot import Bot
from .ui import FloatingBotWindow, SystemTrayIcon


class FloatingBotsApp:
    """Main application class"""

    def __init__(self):
        self.bot: Optional[Bot] = None
        self.ui: Optional[FloatingBotWindow] = None
        self.tray: Optional[SystemTrayIcon] = None

    def initialize(self):
        """Initialize the application"""
        print("Initializing Desktop Floating Bots...")

        # Validate configuration
        config_valid = Config.validate()
        if not config_valid:
            print("Note: Some features may be limited due to missing configuration.")

        # Create bot instance
        self.bot = Bot()
        print(f"Created bot: {self.bot.name}")

        # Create UI
        self.ui = FloatingBotWindow(self.bot, on_close=self.shutdown)
        print("Created floating bot window")

        # Create system tray icon
        self.tray = SystemTrayIcon(self.ui)
        if self.tray.icon:
            self.tray.run()
            print("System tray icon initialized")

        print("Application initialized successfully!")

    def run(self):
        """Run the application"""
        if not self.ui:
            raise RuntimeError("Application not initialized")

        print("Starting Desktop Floating Bots...")
        try:
            self.ui.run()
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.shutdown()

    def shutdown(self):
        """Shutdown the application"""
        print("Shutting down Desktop Floating Bots...")
        if self.tray and self.tray.icon:
            self.tray.icon.stop()
        if self.ui:
            self.ui.root.quit()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Desktop Floating Bots")
    parser.add_argument("--version", action="version", version="1.0.0")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument(
        "--no-tray", action="store_true", help="Disable system tray icon"
    )

    args = parser.parse_args()

    try:
        app = FloatingBotsApp()
        app.initialize()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
