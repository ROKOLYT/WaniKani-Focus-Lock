import keyboard
from src.config import HOTKEYS_TO_SUPPRESS


def suppress_hotkeys() -> None:
    for hotkey in HOTKEYS_TO_SUPPRESS:
        keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
