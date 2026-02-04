import win32gui
import win32process
import psutil
import time
from datetime import datetime

def get_active_window_info():
    """Returns (hwnd, window_title, exe_name, exe_path) of active window."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return None

    # Get window title
    window_title = win32gui.GetWindowText(hwnd)

    # Get process ID from hwnd
    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        proc = psutil.Process(pid)
        exe_name = proc.name()
        exe_path = proc.exe()
    except psutil.Error:
        exe_name = "Unknown"
        exe_path = "Unknown"

    return hwnd, window_title, exe_name, exe_path

def log_window_change(prev_hwnd):
    info = get_active_window_info()
    if info is None:
        return prev_hwnd

    hwnd, title, exe, path = info
    if hwnd != prev_hwnd:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"  ▶ Window Title: {title}")
        print(f"  ▶ Executable  : {exe}")
        print(f"  ▶ Path        : {path}")
        print("-" * 60)
        return hwnd
    return prev_hwnd

if __name__ == "__main__":
    print("Monitoring active window changes (click or Alt+Tab to switch)...\n")
    last_hwnd = None
    try:
        while True:
            last_hwnd = log_window_change(last_hwnd)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")
