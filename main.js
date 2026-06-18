const { app, BrowserWindow, powerSaveBlocker } = require('electron');
const path = require('path');

let win = null;
let blockerId = null;

function createWindow() {
  win = new BrowserWindow({
    fullscreen: true,
    frame: false,
    backgroundColor: '#000000',
    show: false,
    title: 'Caffeinatrix',
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.setMenuBarVisibility(false);
  win.loadFile('index.html');
  win.once('ready-to-show', () => win.show());
  win.on('closed', () => { win = null; });

  // Keys are handled at the window level, not globally, so nothing is
  // intercepted system-wide while the app runs in the background.
  win.webContents.on('before-input-event', (event, input) => {
    if (input.type !== 'keyDown') return;
    const key = (input.key || '').toLowerCase();
    const quit = key === 'escape' || (key === 'q' && (input.meta || input.control));
    if (quit) {
      event.preventDefault();
      app.quit();
    } else if (key === 'f') {
      event.preventDefault();
      win.setFullScreen(!win.isFullScreen());
    }
  });
}

app.whenReady().then(() => {
  // 'prevent-display-sleep' keeps the screen on so the rain stays visible.
  // (Use 'prevent-app-suspension' instead if you ever want the display to
  // sleep while only the system stays awake.)
  blockerId = powerSaveBlocker.start('prevent-display-sleep');
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => app.quit());

app.on('will-quit', () => {
  if (blockerId !== null && powerSaveBlocker.isStarted(blockerId)) {
    powerSaveBlocker.stop(blockerId);
  }
});
