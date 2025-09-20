# Deployment Guide

This guide covers how to build, package, and deploy the Desktop Floating Bots application.

## Prerequisites

- Node.js 16+ 
- npm or yarn
- Git

## Development Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/silva2kand/-C-Users-Siva-Desktop_AI_Bot-.git
   cd -C-Users-Siva-Desktop_AI_Bot-
   npm install
   ```

2. **Development Mode**
   ```bash
   npm run dev
   ```

3. **Testing**
   ```bash
   npm test
   npm run lint
   ```

## Building for Production

### Local Build

1. **Build for current platform:**
   ```bash
   npm run build
   ```

2. **Platform-specific builds:**
   ```bash
   npm run build-win     # Windows
   npm run build-mac     # macOS  
   npm run build-linux   # Linux
   ```

3. **Output location:**
   Built applications will be in the `dist/` directory.

### Cross-Platform Building

For building on different platforms:

**Windows (from any OS):**
```bash
npm install --save-dev electron-builder
npx electron-builder --win
```

**macOS (requires macOS):**
```bash
npx electron-builder --mac
```

**Linux (from any OS):**
```bash
npx electron-builder --linux
```

## Distribution

### GitHub Releases (Automated)

The project includes GitHub Actions for automated building and releasing:

1. **Tag a release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Run tests and linting
   - Build for Windows, macOS, and Linux
   - Create a GitHub release with binaries

### Manual Distribution

1. **Build all platforms:**
   ```bash
   npm run build-win
   npm run build-mac  
   npm run build-linux
   ```

2. **Package files are created in `dist/`:**
   - Windows: `.exe` installer and portable `.exe`
   - macOS: `.dmg` installer and `.app` bundle
   - Linux: `.AppImage`, `.deb`, and `.tar.gz`

## Installation for End Users

### Windows
1. Download the `.exe` installer from releases
2. Run the installer
3. Launch from Start Menu or desktop shortcut

### macOS
1. Download the `.dmg` file from releases
2. Open the DMG and drag the app to Applications
3. Launch from Applications folder

### Linux
1. Download the `.AppImage` file from releases
2. Make it executable: `chmod +x Desktop-Floating-Bots.AppImage`
3. Run the AppImage directly

## Configuration

### API Key Setup
1. Launch the application
2. Open settings (right-click system tray → Settings)
3. Enter your OpenAI API key
4. Save settings

### Auto-start Setup
- Enable "Auto Start with System" in settings
- On Windows: Creates registry entry
- On macOS: Creates login item
- On Linux: Creates autostart desktop entry

## Troubleshooting

### Common Issues

**Application won't start:**
- Check Node.js version (16+ required)
- Verify all dependencies installed: `npm install`
- Check antivirus software isn't blocking

**Bot not responding:**
- Verify OpenAI API key is valid
- Check internet connection
- Look at developer console (Ctrl+Shift+I) for errors

**Build failures:**
- Clean build: `rm -rf node_modules dist && npm install`
- Update electron-builder: `npm update electron-builder`
- Check platform-specific requirements

### Platform-Specific Issues

**Windows:**
- May require Visual Studio Build Tools for native modules
- Windows Defender might flag the app initially

**macOS:**
- App might be blocked by Gatekeeper (right-click → Open)
- Code signing required for distribution

**Linux:**
- May need to install additional dependencies for Electron
- Different distributions may have different requirements

## Advanced Deployment

### Code Signing

**Windows:**
```bash
# Set environment variables
export CSC_LINK=path/to/certificate.p12
export CSC_KEY_PASSWORD=certificate_password
npm run build-win
```

**macOS:**
```bash
# Set environment variables  
export CSC_LINK=path/to/certificate.p12
export CSC_KEY_PASSWORD=certificate_password
export APPLE_ID=your_apple_id
export APPLE_ID_PASS=app_specific_password
npm run build-mac
```

### Custom Distribution

1. **Modify electron-builder config in package.json**
2. **Add custom scripts for your deployment process**
3. **Configure update servers if needed**

### Enterprise Deployment

1. **Create MSI packages for Windows:**
   ```bash
   npx electron-builder --win --publish=never
   ```

2. **Create custom installers with company branding**
3. **Set up internal update servers**
4. **Configure group policies for automatic deployment**

## Monitoring and Updates

### Update Mechanism
- electron-updater can be integrated for automatic updates
- Configure update server in main.js
- Users will be notified of available updates

### Analytics
- Add analytics service integration if needed
- Monitor usage patterns and crash reports
- Track feature adoption

## Security Considerations

1. **API Key Storage**: Keys are stored encrypted using electron-store
2. **Auto-updates**: Only download from trusted sources
3. **Permissions**: App requests minimal system permissions
4. **Network**: All external requests go through HTTPS

## Support

For deployment issues:
1. Check the GitHub Issues page
2. Review build logs in GitHub Actions
3. Test locally before deploying
4. Verify all environment variables are set correctly