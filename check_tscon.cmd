@echo off
echo Checking if tscon and query user are available...
echo.

echo 1. Looking for tscon.exe:
where tscon 2>nul
if %ERRORLEVEL% neq 0 (
    echo    tscon.exe NOT found in PATH.
    if exist "%SystemRoot%\System32\tscon.exe" (
        echo    But found at %SystemRoot%\System32\tscon.exe
    ) else (
        echo    Not found in System32 either. tscon may not be available on this edition.
    )
) else (
    echo    tscon.exe found.
)
echo.

echo 2. Running "query user" (current sessions):
query user 2>nul
if %ERRORLEVEL% neq 0 (
    echo    "query user" failed or not available.
) else (
    echo    "query user" works. Third column above is the session ID needed for tscon.
)
echo.

echo 3. Session ID for %USERNAME%:
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME% 2^>nul') do (
    echo    Session ID: %%s
    goto :done
)
echo    Could not get session ID (are you in an RDP session?)
:done
echo.
echo If both tscon and query user work, the tscon-to-console command should work.
pause
