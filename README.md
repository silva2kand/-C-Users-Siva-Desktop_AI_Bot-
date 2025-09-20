# Desktop Floating Bots

An AI-powered desktop assistant that floats on your screen, ready to help with various tasks.

## Features

- 🎯 **Floating Interface**: Always-accessible bot that floats on your desktop
- 🤖 **AI-Powered**: Integrated with OpenAI for intelligent responses
- ⚙️ **Customizable**: Configurable settings for behavior and appearance
- 🎨 **Modern UI**: Clean, intuitive interface with smooth animations
- 🔧 **System Integration**: System tray integration and hotkeys
- 💬 **Real-time Chat**: Instant messaging with AI assistant
- 🌙 **Theme Support**: Light and dark themes
- 🚀 **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/silva2kand/-C-Users-Siva-Desktop_AI_Bot-.git
   cd -C-Users-Siva-Desktop_AI_Bot-
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure your OpenAI API key:
   - Run the application: `npm start`
   - Open settings and enter your OpenAI API key
   - Save settings

## Usage

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Platform-specific builds
```bash
npm run build-win    # Windows
npm run build-mac    # macOS
npm run build-linux  # Linux
```

## Configuration

The bot can be configured through the settings interface:

- **Bot Name**: Customize your assistant's name
- **Always on Top**: Keep bot window above other applications
- **Auto Start**: Launch with system startup
- **Theme**: Choose between light, dark, or auto themes
- **API Key**: Configure OpenAI integration

## Architecture

```
src/
├── main.js              # Main Electron process
├── renderer/            # UI components
│   ├── bot.html        # Bot chat interface
│   └── main.html       # Settings interface
├── scripts/            # Frontend JavaScript
│   ├── bot.js          # Bot interface logic
│   └── main.js         # Settings interface logic
└── styles/             # CSS stylesheets
    ├── bot.css         # Bot interface styles
    └── main.css        # Settings interface styles
```

## Features Overview

### Core Components
- **Main Process** (`src/main.js`): Handles window management, system integration
- **Bot Interface** (`src/renderer/bot.html`): Floating chat interface
- **Settings Interface** (`src/renderer/main.html`): Configuration panel
- **IPC Communication**: Secure communication between processes

### Key Features
- Floating, draggable bot window
- System tray integration with context menu
- Persistent settings storage
- AI message processing
- Modern, responsive UI

## Development

### Project Structure
- Built with Electron for cross-platform desktop apps
- Modern JavaScript with ES6+ features
- CSS3 with animations and gradients
- IPC (Inter-Process Communication) for secure data flow

### Adding Features
1. **New UI Components**: Add to `src/renderer/`
2. **Styling**: Update CSS files in `src/styles/`
3. **Logic**: Extend JavaScript files in `src/scripts/`
4. **Main Process**: Modify `src/main.js` for system integration

## Testing

```bash
npm test
```

## Packaging

The application uses electron-builder for packaging:

```bash
npm run package
```

Output will be in the `dist/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Voice commands integration
- [ ] Plugin system for custom AI models
- [ ] Multi-bot support
- [ ] Advanced customization options
- [ ] Cloud sync for settings
- [ ] Mobile companion app

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review existing issues for solutions

---

**Note**: This project requires an OpenAI API key for AI functionality. Get yours at [OpenAI's website](https://openai.com/api/).
