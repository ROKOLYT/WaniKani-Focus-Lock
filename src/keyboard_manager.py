import sys
from src.config import HOTKEYS_TO_SUPPRESS

def suppress_hotkeys() -> None:
    if sys.platform != 'win32':
        print("Keyboard hotkey suppression is only supported on Windows. Skipping.")
        return
        
    try:
        import keyboard
        for hotkey in HOTKEYS_TO_SUPPRESS:
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
    except Exception as e:
        print(f"Warning: Failed to suppress hotkeys: {e}")
