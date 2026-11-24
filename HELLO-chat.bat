@echo off
rem Double-click to start HELLO chat on Windows. The admin screen opens in your browser.
cd /d "%~dp0"
py hello_chat.py --open
pause
