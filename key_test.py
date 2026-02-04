import keyboard
import time

# Wait 3 seconds before starting (to give you time to focus a text editor)
print("Click into your text editor, typing will start in 3 seconds...")
time.sleep(3)

# Type a sentence with real key events (like hardware)
keyboard.write("Hello, this is simulated typing via Python!", delay=0.1)

# You can also press individual keys like:
keyboard.press_and_release("enter")
keyboard.write("This is a new line.", delay=0.1)

keyboard.write(
    """
               import os
    import datetime
    import threading
    import Quartz
    from ._mouse_event import ButtonEvent, WheelEvent, MoveEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN

               """,
    delay=0.1,
)

# Combination keys:
keyboard.press_and_release("ctrl+a")  # select all
keyboard.press_and_release("backspace")  # delete all

keyboard.press_and_release("alt+tab")  # select all
time.sleep(3)
keyboard.press_and_release("alt+tab")  # select all

keyboard.write("Hello, this is simulated typing via Python!", delay=0.1)
