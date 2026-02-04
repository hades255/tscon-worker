"""
Auto-bot: randomly emits mouse and keyboard events based on the active window.
Configure variables in config.py.
"""

import ctypes
import os
import random
import subprocess
import time
from ctypes import wintypes

import psutil
import win32gui

import config
from mouse_test import (
    move_mouse_absolute,
    click_mouse,
    move_mouse_absolute_sendinput,
    click_mouse_sendinput,
)

# EnumWindows via ctypes (avoids pywin32 callback error on some systems)
user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def random_delay():
    """Sleep a random duration between DELAY_MIN_SEC and DELAY_MAX_SEC."""
    time.sleep(random.uniform(config.DELAY_MIN_SEC, config.DELAY_MAX_SEC))


# State for EnumWindows ctypes callback (callback cannot use closure)
_find_window_target = None
_find_window_hwnd = [None]  # mutable so callback can set


def _enum_windows_cb(hwnd, lparam):
    """C callback for EnumWindows: find window whose process name matches _find_window_target."""
    global _find_window_hwnd
    if _find_window_target is None:
        return True
    if not win32gui.IsWindowVisible(hwnd) or not win32gui.GetWindowText(hwnd):
        return True
    try:
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        proc = psutil.Process(pid.value)
        if proc.name().lower() == _find_window_target:
            _find_window_hwnd[0] = hwnd
            return False  # stop enumeration
    except (psutil.Error, OSError):
        pass
    return True


def find_and_activate_window(process_name):
    """Find a top-level window whose process name matches (case-insensitive) and activate it. Returns True if found and activated."""
    global _find_window_target, _find_window_hwnd
    target = process_name.strip().lower()
    if not target:
        return False
    _find_window_target = target
    _find_window_hwnd[0] = None
    enum_proc = WNDENUMPROC(_enum_windows_cb)
    if not user32.EnumWindows(enum_proc, 0):
        pass  # enumeration stopped (found) or error
    _find_window_target = None
    hwnd = _find_window_hwnd[0]
    if hwnd is None:
        return False
    try:
        win32gui.ShowWindow(hwnd, 9)  # SW_RESTORE if minimized
        win32gui.SetForegroundWindow(hwnd)
    except win32gui.error:
        return False
    return True


def do_idle_action():
    """When not running: activate IDLE_TARGET_PROCESS, move mouse to top-right of that window, left-click."""
    print("doing idle action...")
    find_and_activate_window(config.IDLE_TARGET_PROCESS)
    random_delay()
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, _bottom = win32gui.GetWindowRect(hwnd)
        x = right - config.IDLE_TOP_RIGHT_OFFSET_X
        y = top + config.IDLE_TOP_RIGHT_OFFSET_Y
        move_mouse_absolute(x, y)
    else:
        # fallback: screen top-left
        x = config.IDLE_TOP_LEFT_OFFSET_X
        y = config.IDLE_TOP_LEFT_OFFSET_Y
        move_mouse_absolute(x, y)
    random_delay()
    click_mouse()
    random_delay()


def run_tscon_to_console():
    """
    Move current RDP session to console (so it stays active after RDP disconnect).
    Runs: query user %USERNAME% to get session ID, then tscon <id> /dest:console.
    Returns True if tscon was run, False if skipped or failed. RDP client will disconnect.
    """
    try:
        username = os.environ.get("USERNAME", "").strip()
        if not username:
            return False
        out = subprocess.run(
            ["query", "user", username],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
            if hasattr(subprocess, "CREATE_NO_WINDOW")
            else 0,
        )
        # query user can return exit code 1 even when stdout has valid session list
        if not (out.stdout and out.stdout.strip()):
            return False
        lines = out.stdout.strip().splitlines()
        if len(lines) < 2:
            return False
        # Skip header; first data line, 3rd column is session ID
        parts = lines[1].split()
        if len(parts) < 3:
            return False
        session_id = parts[2]
        tscon_exe = os.path.join(
            os.environ.get("SystemRoot", "C:\\Windows"), "System32", "tscon.exe"
        )
        if not os.path.isfile(tscon_exe):
            return False
        subprocess.run(
            [tscon_exe, session_id, "/dest:console"],
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
            if hasattr(subprocess, "CREATE_NO_WINDOW")
            else 0,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, IndexError):
        return False


def log(msg):
    """Print and append to a log file (so you can check after reconnecting)."""
    print(msg)
    try:
        with open(os.path.join(os.path.dirname(__file__) or ".", "idle_test_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    except OSError:
        pass


def main():
    time.sleep(3)
    log("Calling run_tscon_to_console()...")
    run_tscon_to_console()
    # Session may need a few seconds to settle after tscon before it accepts input
    log("Waiting 5s for session to settle after tscon...")
    time.sleep(5)

    # Use SendInput instead of mouse_event after tscon (mouse_event often has no effect in console session)
    log("Moving mouse to (300, 300) via SendInput...")
    move_mouse_absolute_sendinput(300, 300)
    random_delay()
    log("Clicking via SendInput...")
    click_mouse_sendinput()
    random_delay()
    log("Done.")


if __name__ == "__main__":
    main()
