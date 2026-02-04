@echo off
echo Moving your RDP session to console - RDP will close when this finishes.
echo Your desktop, bot, and Hubstaff keep running on the VPS.
echo.
timeout /t 3
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do tscon.exe %%s /dest:console