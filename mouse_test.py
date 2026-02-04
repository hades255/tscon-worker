import ctypes
import time

# Windows constants for mouse event types
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800

# Get screen resolution
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# --- SendInput (alternative to mouse_event; can work in console/tscon session) ---
INPUT_MOUSE = 0


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort),
    ]


class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", _INPUTunion)]


def move_mouse_absolute_sendinput(x, y):
    """Move mouse using SendInput (use in console/tscon session if mouse_event has no effect)."""
    nx = int(x * 65535 / screen_width)
    ny = int(y * 65535 / screen_height)
    mi = MOUSEINPUT(
        dx=nx,
        dy=ny,
        mouseData=0,
        dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        time=0,
        dwExtraInfo=None,
    )
    inp = INPUT(type=INPUT_MOUSE, union=_INPUTunion(mi=mi))
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def click_mouse_sendinput():
    """Left click using SendInput (use in console/tscon session if mouse_event has no effect)."""
    for dwFlags in (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP):
        mi = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=dwFlags, time=0, dwExtraInfo=None)
        inp = INPUT(type=INPUT_MOUSE, union=_INPUTunion(mi=mi))
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def move_mouse_absolute(x, y):
    """Move mouse to absolute position (0-65535 range)."""
    x = int(x * 65535 / screen_width)
    y = int(y * 65535 / screen_height)
    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x, y, 0, 0
    )


def click_mouse():
    """Simulate left mouse click."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def right_click_mouse():
    """Simulate right mouse click."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def scroll_up(amount=120):
    """Scroll up. Default Windows wheel delta is 120."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, amount, 0)


def scroll_down(amount=120):
    """Scroll down (negative delta)."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, -amount, 0)


def smooth_move(x1, y1, x2, y2, duration=1.0, steps=100):
    """Smooth mouse move from (x1, y1) to (x2, y2) in given duration."""
    for i in range(steps):
        t = i / steps
        xt = x1 + (x2 - x1) * t
        yt = y1 + (y2 - y1) * t
        move_mouse_absolute(xt, yt)
        time.sleep(duration / steps)


# Example usage
if __name__ == "__main__":
    print("Starting in 3 seconds...")
    time.sleep(3)

    start_x, start_y = 100, 100
    end_x, end_y = 600, 400

    # Move to start
    move_mouse_absolute(start_x, start_y)
    time.sleep(0.5)

    # Smooth move to destination
    smooth_move(start_x, start_y, end_x, end_y, duration=1.5)

    # Click at destination
    click_mouse()
    time.sleep(0.5)

    scroll_down(120 * 3)
    time.sleep(0.5)

    scroll_up()
    time.sleep(0.5)

    right_click_mouse()
    time.sleep(0.5)
