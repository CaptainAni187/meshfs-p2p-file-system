const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  mainWindow.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );

  if (isDev) {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }

  // --- Start Python Process with correct CWD ---
  const projectRoot = path.join(__dirname, '..', '..'); // Navigates from /public to project root
  const pythonExecutable = path.join(projectRoot, '.venv', 'bin', 'python');
  
  pythonProcess = spawn(pythonExecutable, ['-m', 'backend.cli'], {
    cwd: projectRoot // Set the working directory here
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
    data.toString().split('\n').forEach(line => {
      if (line.trim()) {
        try {
          const parsed = JSON.parse(line);
          mainWindow.webContents.send('from-python', parsed);
        } catch (error) {
          console.error('Error parsing JSON from Python:', error);
        }
      }
    });
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  mainWindow.on('closed', () => {
    if (pythonProcess) {
      pythonProcess.kill();
    }
    mainWindow = null;
  });
}

ipcMain.on('to-python', (event, arg) => {
  console.log('Received from UI, sending to Python:', arg);
  if (pythonProcess) {
    pythonProcess.stdin.write(JSON.stringify(arg) + '\n');
  }
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

