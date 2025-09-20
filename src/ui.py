"""
Floating UI module for desktop bot interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from typing import Optional, Callable

from .config import Config
from .bot import Bot


class FloatingBotWindow:
    """Floating window for bot interaction"""

    def __init__(self, bot: Bot, on_close: Optional[Callable] = None):
        self.bot = bot
        self.on_close = on_close
        self.message_queue = queue.Queue()

        # Create main window
        self.root = tk.Tk()
        self.root.title(f"{self.bot.name} - Floating Bot")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # Configure window properties
        self.root.attributes("-alpha", Config.TRANSPARENCY)
        if Config.ALWAYS_ON_TOP:
            self.root.attributes("-topmost", True)

        # Make window resizable but set minimum size
        self.root.minsize(250, 150)

        # Configure window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        self._setup_ui()
        self._position_window()

        # Start message processing
        self._process_queue()

    def _setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Bot name label
        name_label = ttk.Label(
            main_frame, text=f"🤖 {self.bot.name}", font=("Arial", 10, "bold")
        )
        name_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=8,
            width=30,
            state=tk.DISABLED,
            font=("Arial", 9),
        )
        self.chat_display.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5)
        )

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        input_frame.columnconfigure(0, weight=1)

        # Input entry
        self.input_entry = ttk.Entry(input_frame, font=("Arial", 9))
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.input_entry.bind("<Return>", self._on_send_message)

        # Send button
        send_button = ttk.Button(
            input_frame, text="Send", command=self._on_send_message
        )
        send_button.grid(row=0, column=1)

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))

        # Clear button
        clear_button = ttk.Button(
            control_frame, text="Clear", command=self._on_clear_chat
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 5))

        # Status button
        status_button = ttk.Button(
            control_frame, text="Status", command=self._on_show_status
        )
        status_button.pack(side=tk.LEFT, padx=(0, 5))

        # Hide button
        hide_button = ttk.Button(
            control_frame, text="Hide", command=self._on_hide_window
        )
        hide_button.pack(side=tk.RIGHT)

        # Add welcome message
        self._add_message(
            "Bot", f"Hello! I'm {self.bot.name}. How can I help you today?"
        )

        # Focus on input
        self.input_entry.focus()

    def _position_window(self):
        """Position window in the top-right corner"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        x = screen_width - window_width - 50
        y = 50

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def _on_send_message(self, event=None):
        """Handle sending a message"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        # Add user message to chat
        self._add_message("You", user_input)
        self.input_entry.delete(0, tk.END)

        # Get bot response in a separate thread
        threading.Thread(
            target=self._get_bot_response, args=(user_input,), daemon=True
        ).start()

    def _get_bot_response(self, user_input: str):
        """Get bot response in background thread"""
        try:
            response = self.bot.get_response(user_input)
            self.message_queue.put(("bot_response", response))
        except Exception as e:
            self.message_queue.put(("error", f"Error: {str(e)}"))

    def _add_message(self, sender: str, message: str):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)

        # Add timestamp
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M")

        # Format message
        if sender == "You":
            prefix = f"[{timestamp}] You: "
        else:
            prefix = f"[{timestamp}] {sender}: "

        self.chat_display.insert(tk.END, prefix + message + "\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _on_clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.bot.reset_conversation()
        self._add_message("Bot", "Chat cleared! How can I help you?")

    def _on_show_status(self):
        """Show bot status"""
        status = self.bot.get_status()
        status_text = f"""Bot Status:
Name: {status['name']}
Personality: {status['personality']}
Messages in conversation: {status['conversation_length']}
OpenAI Available: {'Yes' if status['openai_available'] else 'No (using mock responses)'}"""

        messagebox.showinfo("Bot Status", status_text)

    def _on_hide_window(self):
        """Hide the window"""
        self.root.withdraw()

    def _on_window_close(self):
        """Handle window close event"""
        if self.on_close:
            self.on_close()
        else:
            self.root.quit()

    def _process_queue(self):
        """Process messages from background threads"""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                if msg_type == "bot_response":
                    self._add_message("Bot", content)
                elif msg_type == "error":
                    self._add_message("System", content)
        except queue.Empty:
            pass

        # Schedule next check
        self.root.after(100, self._process_queue)

    def show(self):
        """Show the window"""
        self.root.deiconify()
        self.root.lift()
        self.input_entry.focus()

    def run(self):
        """Run the main window loop"""
        self.root.mainloop()


class SystemTrayIcon:
    """System tray icon for the floating bot"""

    def __init__(self, bot_window: FloatingBotWindow):
        self.bot_window = bot_window
        self.icon = None

        try:
            import pystray
            from PIL import Image, ImageDraw

            # Create a simple icon
            image = Image.new("RGB", (64, 64), color="blue")
            draw = ImageDraw.Draw(image)
            draw.ellipse([16, 16, 48, 48], fill="white")
            draw.text((28, 26), "B", fill="blue")

            # Create menu
            menu = pystray.Menu(
                pystray.MenuItem("Show Bot", self._show_bot),
                pystray.MenuItem("Hide Bot", self._hide_bot),
                pystray.MenuItem("-", None),
                pystray.MenuItem("Quit", self._quit),
            )

            self.icon = pystray.Icon("FloatingBot", image, menu=menu)

        except ImportError:
            print("pystray not available, system tray disabled")

    def _show_bot(self, icon=None, item=None):
        """Show bot window"""
        self.bot_window.show()

    def _hide_bot(self, icon=None, item=None):
        """Hide bot window"""
        self.bot_window._on_hide_window()

    def _quit(self, icon=None, item=None):
        """Quit application"""
        if self.icon:
            self.icon.stop()
        self.bot_window._on_window_close()

    def run(self):
        """Run system tray icon"""
        if self.icon:
            threading.Thread(target=self.icon.run, daemon=True).start()
