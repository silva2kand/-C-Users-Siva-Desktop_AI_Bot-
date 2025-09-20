# Documentation

## Architecture

### Overview

The Desktop Floating Bots application is built with a modular architecture:

```
src/
├── __init__.py      # Package initialization
├── config.py        # Configuration management
├── bot.py          # AI bot logic and conversation handling  
├── ui.py           # Floating window UI and system tray
└── main.py         # Application entry point and orchestration
```

### Components

#### 1. Configuration (`config.py`)
- Manages environment variables and application settings
- Validates configuration at startup
- Supports OpenAI API key configuration
- Customizable UI settings (window size, transparency, etc.)

#### 2. Bot Logic (`bot.py`)
- Handles AI conversations and responses
- Supports both OpenAI API and mock responses
- Maintains conversation history
- Provides status information

#### 3. User Interface (`ui.py`)
- **FloatingBotWindow**: Main chat interface with tkinter
- **SystemTrayIcon**: System tray integration for easy access
- Floating, always-on-top window design
- Responsive chat interface with scrolling history

#### 4. Main Application (`main.py`)
- Application lifecycle management
- Component initialization and coordination
- Command-line argument handling
- Error handling and graceful shutdown

## Features

### Core Features
- 🤖 **AI-Powered Conversations**: Intelligent responses using OpenAI API or smart mock responses
- 🎨 **Floating UI**: Always-on-top window that doesn't interfere with work
- 💬 **Chat Interface**: Clean, scrollable chat history with timestamps
- ⚙️ **System Tray**: Quick access from system tray with show/hide functionality
- 🔧 **Configurable**: Customizable appearance, behavior, and AI personality

### Technical Features
- 🧪 **Comprehensive Testing**: Unit tests, integration tests, and test coverage
- 🚀 **CI/CD Pipeline**: Automated testing, linting, and building
- 📦 **Cross-Platform**: Works on Windows, macOS, and Linux
- 🔒 **Secure**: Proper API key management and error handling
- 🛠️ **Developer-Friendly**: Well-documented, modular code with linting

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | OpenAI API key for AI responses |
| `BOT_NAME` | FloatingBot | Name of the bot |
| `BOT_PERSONALITY` | helpful_assistant | Bot personality type |
| `UPDATE_INTERVAL` | 1000 | UI update interval (ms) |
| `WINDOW_WIDTH` | 300 | Window width in pixels |
| `WINDOW_HEIGHT` | 200 | Window height in pixels |
| `TRANSPARENCY` | 0.9 | Window transparency (0.0-1.0) |
| `ALWAYS_ON_TOP` | true | Keep window always on top |

### Usage Examples

#### Basic Usage
```bash
# Run with default settings
python -m src.main

# Show version
python -m src.main --version
```

#### With Custom Configuration
```bash
# Set environment variables
export OPENAI_API_KEY="your-api-key-here"
export BOT_NAME="MyAssistant"
export WINDOW_WIDTH="400"

# Run the application
python -m src.main
```

#### Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=src

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## API Integration

### OpenAI Integration

When an OpenAI API key is provided, the bot uses GPT-3.5-turbo for responses:

- Maintains conversation context (last 5 exchanges)
- Configurable bot personality through system messages
- Error handling with fallback to mock responses
- Rate limiting and token management

### Mock Responses

When OpenAI is unavailable, the bot provides intelligent mock responses:

- Keyword-based response matching
- Context-aware replies
- Time and date queries
- Helpful default responses

## Deployment

### Local Development
1. Clone the repository
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables
5. Run: `python -m src.main`

### Production Deployment
1. Package with: `python -m build`
2. Install from wheel: `pip install dist/*.whl`
3. Run with: `floating-bots`

### CI/CD Pipeline

The GitHub Actions pipeline includes:

- **Multi-Python Testing**: Tests on Python 3.8-3.11
- **Cross-Platform**: Ubuntu, Windows, macOS
- **Code Quality**: Linting with flake8, formatting with black
- **Security**: Vulnerability scanning with bandit
- **Build Artifacts**: Automatic package building
- **Coverage Reporting**: Test coverage tracking

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**
   - Install tkinter: `sudo apt-get install python3-tk` (Ubuntu/Debian)

2. **"OpenAI API key not found"**
   - Set `OPENAI_API_KEY` environment variable
   - Bot will use mock responses without API key

3. **Window not showing**
   - Check if system supports GUI
   - Ensure X11 forwarding if using SSH

4. **System tray not working**
   - Install pystray dependencies
   - Check desktop environment supports system tray

### Development Issues

1. **Tests failing on GUI**
   - Use xvfb for headless testing: `xvfb-run pytest`

2. **Import errors**
   - Ensure virtual environment is activated
   - Install in development mode: `pip install -e .`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Use black for code formatting
- Add tests for new features
- Update documentation as needed