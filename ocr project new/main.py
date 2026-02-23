"""
Auto-bot: randomly emits mouse and keyboard events based on the active window.
Configure variables in config.py.
"""

import ctypes
import os
import random
import subprocess
import sys
import time
from ctypes import wintypes
from datetime import datetime, timedelta

import keyboard
import psutil
import win32gui
import win32process

import actions as config
from image_processor import get_active_window_info
from result_in_json import (
    move_mouse_absolute,
    smooth_move,
    click_mouse,
    right_click_mouse,
    scroll_up,
    scroll_down,
)

# EnumWindows via ctypes (avoids pywin32 callback error on some systems)
user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_cursor_pos():
    """Return (x, y) of current cursor in screen coordinates."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def random_delay():
    """Sleep a random duration between DELAY_MIN_SEC and DELAY_MAX_SEC."""
    time.sleep(random.uniform(config.DELAY_MIN_SEC, config.DELAY_MAX_SEC))


def get_process_name():
    """Return exe name of foreground window, or empty string."""
    info = get_active_window_info()
    if info is None:
        return ""
    return info[2]  # exe_name


def get_all_process_names():
    """Return a sorted list of unique process names (exe names) from all running processes."""
    names = set()
    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info.get("name")
            if name:
                names.add(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            pass
    return sorted(names)


def get_window_process_names():
    """Return a list of (window_title, process_name) for visible windows with non-empty titles. Useful to find Hubstaff etc. by title."""
    result = []

    def enum_cb(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return True
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            result.append((title, proc.name()))
        except (psutil.Error, win32process.error):
            pass
        return True

    win32gui.EnumWindows(enum_cb, None)
    return result


def is_vs_code(exe_name):
    return exe_name and exe_name.lower() in [
        n.lower() for n in config.VS_CODE_PROCESS_NAMES
    ]


def is_chrome(exe_name):
    return exe_name and exe_name.lower() in [
        n.lower() for n in config.CHROME_PROCESS_NAMES
    ]


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
    # click_mouse()
    random_delay()


def do_click_left_or_right(click_left=False):
    """Random left or right click. If right, move left and left-click to close context menu."""
    if click_left or random.choice([True, False]):
        click_mouse()
    else:
        right_click_mouse()
        random_delay()
        x, y = get_cursor_pos()
        move_mouse_absolute(x - config.CONTEXT_MENU_OFFSET_LEFT_PX, y)
        random_delay()
        click_mouse()
        random_delay()
        click_mouse()
    random_delay()


def do_alt_tab():
    """Hold Alt, press Tab N times, release Alt (N = random in config range)."""
    n = random.randint(config.ALT_TAB_COUNT_MIN, config.ALT_TAB_COUNT_MAX)
    keyboard.press("alt")
    for _ in range(n):
        keyboard.press_and_release("tab")
        random_delay()
    keyboard.release("alt")
    random_delay()


def do_ctrl_tab():
    """Hold Ctrl, press Tab N times, release Ctrl (N = random in config range)."""
    n = random.randint(config.CTRL_TAB_COUNT_MIN, config.CTRL_TAB_COUNT_MAX)
    keyboard.press("ctrl")
    for _ in range(n):
        keyboard.press_and_release("tab")
        random_delay()
    keyboard.release("ctrl")
    random_delay()


def do_random_scroll():
    """Scroll up or down a random amount."""
    mult = random.randint(config.SCROLL_MULTIPLIER_MIN, config.SCROLL_MULTIPLIER_MAX)
    amount = config.SCROLL_DELTA_BASE * mult
    if random.choice([True, False]):
        scroll_up(amount)
    else:
        scroll_down(amount)
    random_delay()


def do_vs_code_cycle():
    """One cycle of actions for Visual Studio Code."""
    x1, y1, x2, y2 = config.VS_CODE_REGION
    start_x, start_y = get_cursor_pos()
    end_x = random.uniform(x1, x2)
    end_y = random.uniform(y1, y2)
    duration = random.uniform(
        config.SMOOTH_MOVE_DURATION_MIN, config.SMOOTH_MOVE_DURATION_MAX
    )
    random_delay()
    if random.choice([True, False]):
        smooth_move(
            start_x,
            start_y,
            end_x,
            end_y,
            duration=duration,
            steps=config.SMOOTH_MOVE_STEPS,
        )
        random_delay()
    if random.choice([True, False]):
        do_random_scroll()
    if random.choice([True, False]):
        do_click_left_or_right()
    do_click_left_or_right(click_left=True)

    # Open the VS Code file quick open (Ctrl+P), select a file name from config.VS_CODE_FILE_NAMES,
    # type it, and press Enter to open the file.
    if random.choice([True, False]):
        keyboard.press_and_release("ctrl+p")
        random_delay()
        file_name = random.choice(config.VS_CODE_FILE_NAMES)
        keyboard.write(file_name, delay=config.TYPING_DELAY_PER_CHAR)
        random_delay()
        keyboard.press_and_release("enter")
        random_delay()
        keyboard.press_and_release("escape")
        random_delay()

    if random.choice([True, False]):
        for _ in range(random.randint(0, 20)):
            keyboard.press_and_release("down")
            random_delay()
    else:
        for _ in range(random.randint(0, 20)):
            keyboard.press_and_release("up")
            random_delay()

    keyboard.press_and_release("end")
    random_delay()
    keyboard.press_and_release("enter")
    random_delay()

    if not config.VS_CODE_TEXTS:
        text = "print('test')"
    else:
        n_max = min(config.VS_CODE_TEXTS_LINES_MAX, len(config.VS_CODE_TEXTS))
        n = random.randint(config.VS_CODE_TEXTS_LINES_MIN, n_max)
        lines = random.choices(config.VS_CODE_TEXTS, k=n)
        text = "\n".join(lines)

    keyboard.write(text, delay=config.TYPING_DELAY_PER_CHAR)
    random_delay()

    if random.choice([True, False]):
        do_alt_tab()
    else:
        do_ctrl_tab()
    random_delay()


def do_chrome_cycle():
    """One cycle of actions for Google Chrome."""
    newPage = False

    if random.choice([True, False]):
        newPage = True
        keyboard.press_and_release("ctrl+t")
        random_delay()
        search = random.choice(config.CHROME_SEARCH_KEYWORDS)
        keyboard.write(search, delay=config.TYPING_DELAY_PER_CHAR)
        random_delay()
        keyboard.press_and_release("enter")
        random_delay()

    x1, y1, x2, y2 = config.CHROME_REGION
    start_x, start_y = get_cursor_pos()
    end_x = random.uniform(x1, x2)
    end_y = random.uniform(y1, y2)
    duration = random.uniform(
        config.SMOOTH_MOVE_DURATION_MIN, config.SMOOTH_MOVE_DURATION_MAX
    )
    random_delay()
    if random.choice([True, False]):
        smooth_move(
            start_x,
            start_y,
            end_x,
            end_y,
            duration=duration,
            steps=config.SMOOTH_MOVE_STEPS,
        )
        random_delay()

    if random.choice([True, False]):
        do_random_scroll()
    if random.choice([True, False]):
        do_click_left_or_right()
    do_click_left_or_right(click_left=True)

    if random.choice([True, False]):
        keyboard.press_and_release("alt+left")
        random_delay()

    if random.choice([True, False]):
        keyboard.press_and_release("alt+right")
        random_delay()

    for _ in range(random.randint(0, 20)):
        random_delay()

    if newPage:
        keyboard.press_and_release("ctrl+w")
        random_delay()

    if random.choice([True, False]):
        do_ctrl_tab()
    else:
        do_alt_tab()
    random_delay()


def do_others_cycle():
    """One cycle for other apps: only scroll and alt+tab."""
    do_random_scroll()
    do_alt_tab()
    random_delay()


# --- Run control state (toggled by TOGGLE_KEY) ---
_enabled = False
_enabled_since = None
_random_t_from = None
_random_t_to = None
# When time is over, do_idle_action() is called only once; reset when running again
_idle_action_done = True
# Override RUN_MINS from -m/--mins CLI arg (None = use config.RUN_MINS)
_run_mins_override = None


def _get_run_mins():
    """Return effective RUN_MINS (CLI override or config)."""
    return _run_mins_override if _run_mins_override is not None else config.RUN_MINS


def _parse_time(s):
    """Parse 'HH:MM' or 'H:MM' to datetime.time."""
    return datetime.strptime(s.strip(), "%H:%M").time()


def _time_plus_minutes(t, delta_minutes):
    """Return time t plus delta_minutes (may wrap across midnight)."""
    dt = datetime.combine(datetime.now().date(), t) + timedelta(minutes=delta_minutes)
    return dt.time()


def _random_time_around(config_time_str, plus_minus_minutes):
    """Return a random time within ± plus_minus_minutes of the config time."""
    t = _parse_time(config_time_str)
    delta = random.uniform(-plus_minus_minutes, plus_minus_minutes)
    return _time_plus_minutes(t, delta)


def _in_fixed_time_window():
    """True if current time is within (random) RUN_TIME_FROM..RUN_TIME_TO (handles overnight)."""
    now = datetime.now().time()
    t_from = (
        _random_t_from
        if _random_t_from is not None
        else _parse_time(config.RUN_TIME_FROM)
    )
    t_to = _random_t_to if _random_t_to is not None else _parse_time(config.RUN_TIME_TO)
    if t_from <= t_to:
        return t_from <= now <= t_to
    return now >= t_from or now <= t_to


def _should_run():
    """True if bot is on and within the active window for current mode."""
    global _enabled, _enabled_since
    if not _enabled:
        return False
    if config.RUN_MODE == "mins":
        run_mins = _get_run_mins()
        if _enabled_since is None:
            return True
        elapsed_min = (time.time() - _enabled_since) / 60.0
        if elapsed_min >= run_mins:
            _enabled = False
            _enabled_since = None
            print("Off ({} mins elapsed).".format(run_mins))
            return False
        return True
    if config.RUN_MODE == "fixed_time":
        return _in_fixed_time_window()
    return True


def _on_toggle_key():
    global _enabled, _enabled_since, _random_t_from, _random_t_to, _idle_action_done
    new_enabled = not _enabled
    if new_enabled:
        print(f"toggle in {config.START_DELAY_SEC} seconds...")
        time.sleep(config.START_DELAY_SEC)
        print("start:", datetime.now())
    _enabled = new_enabled
    if _enabled and config.RUN_MODE == "mins":
        _enabled_since = time.time()
        _random_t_from = _random_t_to = None
        _idle_action_done = (
            False  # reset so idle action runs once again after next time-over
        )
        print("m mode")
        # print("On (m mode, {}).".format(config.RUN_MINS))
    elif _enabled and config.RUN_MODE == "fixed_time":
        _enabled_since = None
        _random_t_from = _random_time_around(
            config.RUN_TIME_FROM, config.RUN_TIME_RANDOM_MINUTES
        )
        _random_t_to = _random_time_around(
            config.RUN_TIME_TO, config.RUN_TIME_RANDOM_MINUTES
        )
        _idle_action_done = (
            False  # reset so idle action runs once again after next time-over
        )
        print(
            "f mode"
            # "On (f {}–{}).".format(
            #     _random_t_from.strftime("%H:%M"), _random_t_to.strftime("%H:%M")
            # )
        )
    elif not _enabled:
        _enabled_since = None
        _random_t_from = _random_t_to = None
        print("Off.")

    if _enabled and getattr(config, "RUN_TSCON_AT_STARTUP", False):
        print(f"new session in {config.TSCON_DELAY_SEC} seconds...")
        time.sleep(config.TSCON_DELAY_SEC)
        if run_tscon_to_console():
            print("Session moved to console.")
        else:
            print("tscon skipped or failed.")


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


def main():
    global _idle_action_done
    print("Server is starting. Press {} to restart".format(config.TOGGLE_KEY))

    _hotkey = keyboard.add_hotkey(config.TOGGLE_KEY, _on_toggle_key)
    try:
        while True:
            if not _should_run():
                if not _idle_action_done:
                    print("idle:", datetime.now())
                    do_idle_action()
                    _idle_action_done = True
                time.sleep(0.5)
                continue
            exe = get_process_name()
            if is_vs_code(exe):
                do_vs_code_cycle()
            elif is_chrome(exe):
                do_chrome_cycle()
            else:
                do_others_cycle()
    except KeyboardInterrupt:
        print("\n...")
    finally:
        keyboard.remove_hotkey(_hotkey)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--list-processes", "-l"):
        print("All process names (exe):")
        for name in get_all_process_names():
            print(" ", name)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in ("--list-windows", "-w"):
        print("Visible windows (title -> process name):")
        for title, exe in sorted(get_window_process_names(), key=lambda x: x[1]):
            print(" ", exe, "->", title[:60] + ("..." if len(title) > 60 else ""))
        sys.exit(0)
    # -m / --mins: override RUN_MINS (only used when RUN_MODE == "mins")
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("-m", "--mins") and i + 1 < len(sys.argv):
            try:
                _run_mins_override = int(sys.argv[i + 1])
                if _run_mins_override <= 0:
                    _run_mins_override = None
            except ValueError:
                _run_mins_override = None
            i += 2
            continue
        i += 1
    if _run_mins_override is not None:
        print("RUN_MINS override: {} (from -m)".format(_run_mins_override))
    main()
