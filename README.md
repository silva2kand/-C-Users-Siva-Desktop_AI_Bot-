# Desktop Floating Bots

A desktop application featuring floating AI-powered bots that provide interactive assistance.

## Features

- 🤖 AI-powered floating bots
- 🎨 Customizable appearance and behavior
- 💬 Interactive chat interface
- ⚙️ Configurable settings
- 🔒 Secure API key management
- 🧪 Comprehensive testing suite
- 🚀 CI/CD pipeline integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/silva2kand/-C-Users-Siva-Desktop_AI_Bot-.git
cd -C-Users-Siva-Desktop_AI_Bot-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and preferences
```

4. Run the application:
```bash
python -m src.main
```

## Development

### Running Tests
```bash
pytest tests/ -v --cov=src
```

### Code Formatting
```bash
black src/ tests/
flake8 src/ tests/
```

### Building
```bash
python setup.py build
```

## Configuration

See `.env.example` for available configuration options.

## License

MIT License
