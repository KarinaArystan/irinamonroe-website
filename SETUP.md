# VS Code Live Server Setup

## Quick Start

1. **Install Live Server Extension**
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X on Mac)
   - Search for "Live Server" by Ritwick Dey
   - Click Install

2. **Open Your Project**
   - In VS Code: File → Open Folder
   - Select: `/irinamonroe.com/new-site/`

3. **Start Live Server**
   - Right-click on `src/index.html`
   - Select "Open with Live Server"
   - Your site opens at http://127.0.0.1:5500/src/

## How It Works

- **Auto-refresh**: Saves in VS Code instantly update the browser
- **Edit any file**: HTML, CSS, or JS changes appear immediately
- **Port**: Usually runs on port 5500 (configurable)

## Tips

- Keep browser and VS Code side by side
- Use Cmd+S to save and see instant changes
- Browser console (F12) shows any JavaScript errors
- Live Server status appears in VS Code's bottom status bar

## File Locations

- **Edit these files:**
  - `src/index.html` - Main HTML
  - `src/styles.css` - All styles
  - `src/script.js` - JavaScript

- **Images go in:**
  - `assets/images/hero/`
  - `assets/images/backgrounds/`
  - `assets/images/profile/`

## Stopping Live Server

- Click "Port: 5500" in VS Code status bar
- Or right-click in HTML file → "Stop Live Server"