@echo off
taskkill /F /IM chrome.exe >nul 2>&1

set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist %CHROME% set CHROME="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

start "" %CHROME% --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-debug"

timeout /t 2 >nul

start http://127.0.0.1:9222/json/version