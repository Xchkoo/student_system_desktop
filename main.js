const {app, BrowserWindow} = require('electron')

function createWindow(){
    var spawn = require('child_process').spawn;
    run = spawn('python3.8', ['run.py']); 
    const win = new BrowserWindow({
        width: 1440,
        height: 900,
    })

    win.loadURL('http://127.0.0.1:8080')
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', function(){
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

app.on('window-all-closed', function(){
    if (process.platform !== 'darwin' ) app.quit()
})