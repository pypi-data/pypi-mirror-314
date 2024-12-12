import time
from typing import Union
import platform

if platform.system() == 'Windows':
    import win32api
    import win32con
elif platform.system() == 'Linux':
    from Xlib import X, display
    from Xlib.ext.xtest import fake_input
else:  # macOS
    from Quartz import *


class Mouse:
    """Mouse input handler"""
    
    def __init__(self, backend):
        self._backend = backend

    def click(self, x: int, y: int, button: str = "left") -> bool:
        """Click at coordinates"""
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Coordinates must be numbers")
        if not isinstance(button, str):
            raise ValueError("Button must be a string")
        if button not in ["left", "right", "middle"]:
            raise ValueError("Invalid button type. Must be 'left', 'right', or 'middle'")
        return self._backend.click(int(x), int(y), button)

    def double_click(self, x: int, y: int, button: str = "left") -> bool:
        """Double click at coordinates"""
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Coordinates must be numbers")
        if not isinstance(button, str):
            raise ValueError("Button must be a string")
        if button not in ["left", "right", "middle"]:
            raise ValueError("Invalid button type. Must be 'left', 'right', or 'middle'")
        
        success = self._backend.click(int(x), int(y), button)
        if not success:
            return False
        time.sleep(0.1)  # Small delay between clicks
        return self._backend.click(int(x), int(y), button)

    def move(self, x: int, y: int) -> bool:
        """Move mouse to coordinates"""
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Coordinates must be numbers")
        return self._backend.move_mouse(int(x), int(y))

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, button: str = "left") -> bool:
        """Drag from start to end coordinates"""
        if not all(isinstance(coord, (int, float)) for coord in [start_x, start_y, end_x, end_y]):
            raise ValueError("Coordinates must be numbers")
        if not isinstance(button, str):
            raise ValueError("Button must be a string")
        if button not in ["left", "right", "middle"]:
            raise ValueError("Invalid button type. Must be 'left', 'right', or 'middle'")
        
        # Move to start position
        if not self._backend.move_mouse(int(start_x), int(start_y)):
            return False
        time.sleep(0.1)
        
        # Press button
        if not self._backend.mouse_down(button):
            return False
        time.sleep(0.1)
        
        # Move to end position
        if not self._backend.move_mouse(int(end_x), int(end_y)):
            self._backend.mouse_up(button)  # Release button if move fails
            return False
        time.sleep(0.1)
        
        # Release button
        return self._backend.mouse_up(button)


class Keyboard:
    """Keyboard input handler"""
    
    def __init__(self, backend):
        self._backend = backend

    def type_text(self, text: str, interval: float = 0.0) -> bool:
        """Type text with optional interval between keystrokes"""
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not text:
            return True
        return self._backend.type_text(text, interval)

    def press_key(self, key: str) -> bool:
        """Press a single key"""
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        if not key:
            return True
        return self._backend.press_key(key)

    def release_key(self, key: str) -> bool:
        """Release a single key"""
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        if not key:
            return True
        return self._backend.release_key(key)

    def press_keys(self, *keys: str) -> bool:
        """Press multiple keys simultaneously"""
        if not keys:
            return True
        if not all(isinstance(k, str) for k in keys):
            raise ValueError("All keys must be strings")
        return self._backend.press_keys(*keys)

    def release_keys(self, *keys: str) -> bool:
        """Release multiple keys simultaneously"""
        if not keys:
            return True
        if not all(isinstance(k, str) for k in keys):
            raise ValueError("All keys must be strings")
        return self._backend.release_keys(*keys)

    def send_keys(self, keys: str) -> bool:
        """Send a sequence of keys with special key support"""
        if not isinstance(keys, str):
            raise ValueError("Keys must be a string")
        if not keys:
            return True
        return self._backend.send_keys(keys)


class Backend:
    """Cross-platform keyboard and mouse input handling"""

    def __init__(self):
        self.platform = platform.system().lower()
        if self.platform == 'linux':
            self.display = display.Display()

    def type_text(self, text: str, interval: float = 0.0) -> bool:
        """Type text with optional interval between keystrokes"""
        for char in text:
            self.press_key(char)
            self.release_key(char)
            if interval > 0:
                time.sleep(interval)
        return True

    def press_key(self, key: str) -> bool:
        """Press a key"""
        if self.platform == 'windows':
            win32api.keybd_event(self._get_vk_code(key), 0, 0, 0)
        elif self.platform == 'linux':
            keycode = self.display.keysym_to_keycode(ord(key))
            fake_input(self.display, X.KeyPress, keycode)
            self.display.sync()
        else:  # macOS
            event = CGEventCreateKeyboardEvent(None, ord(key), True)
            CGEventPost(kCGHIDEventTap, event)
        return True

    def release_key(self, key: str) -> bool:
        """Release a key"""
        if self.platform == 'windows':
            win32api.keybd_event(self._get_vk_code(key), 0, win32con.KEYEVENTF_KEYUP, 0)
        elif self.platform == 'linux':
            keycode = self.display.keysym_to_keycode(ord(key))
            fake_input(self.display, X.KeyRelease, keycode)
            self.display.sync()
        else:  # macOS
            event = CGEventCreateKeyboardEvent(None, ord(key), False)
            CGEventPost(kCGHIDEventTap, event)
        return True

    def _get_vk_code(self, key: str) -> int:
        """Convert character to virtual key code (Windows-specific)"""
        return ord(key.upper())

    def click(self, x: int, y: int, button: str = "left") -> bool:
        """Click at coordinates"""
        if self.platform == 'windows':
            button_map = {
                "left": win32con.MOUSEEVENTF_LEFTDOWN,
                "right": win32con.MOUSEEVENTF_RIGHTDOWN,
                "middle": win32con.MOUSEEVENTF_MIDDLEDOWN
            }
            button_up_map = {
                "left": win32con.MOUSEEVENTF_LEFTUP,
                "right": win32con.MOUSEEVENTF_RIGHTUP,
                "middle": win32con.MOUSEEVENTF_MIDDLEUP
            }
            win32api.mouse_event(button_map[button], 0, 0, 0, 0)
            win32api.mouse_event(button_up_map[button], 0, 0, 0, 0)
        elif self.platform == 'linux':
            button_map = {
                "left": X.Button1,
                "right": X.Button3,
                "middle": X.Button2
            }
            fake_input(self.display, X.ButtonPress, button_map[button])
            self.display.sync()
            fake_input(self.display, X.ButtonRelease, button_map[button])
            self.display.sync()
        else:  # macOS
            button_map = {
                "left": kCGMouseButtonLeft,
                "right": kCGMouseButtonRight,
                "middle": kCGMouseButtonCenter
            }
            pos = CGEventGetLocation(CGEventCreate(None))
            clickDown = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseDown, pos, button_map[button])
            clickUp = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseUp, pos, button_map[button])
            CGEventPost(kCGHIDEventTap, clickDown)
            CGEventPost(kCGHIDEventTap, clickUp)
        return True

    def press_keys(self, *keys: str) -> bool:
        """Press multiple keys simultaneously"""
        for key in keys:
            self.press_key(key)
        return True

    def release_keys(self, *keys: str) -> bool:
        """Release multiple keys simultaneously"""
        for key in reversed(keys):
            self.release_key(key)
        return True

    def send_keys(self, keys: str) -> bool:
        """Send a sequence of keys with special key support"""
        for key in keys:
            self.press_key(key)
            self.release_key(key)
        return True

    def move_mouse(self, x: int, y: int) -> bool:
        """Move mouse to coordinates"""
        if self.platform == 'windows':
            win32api.SetCursorPos((x, y))
        elif self.platform == 'linux':
            fake_input(self.display, X.MotionNotify, x, y)
            self.display.sync()
        else:  # macOS
            pos = CGEventGetLocation(CGEventCreate(None))
            move = CGEventCreateMouseEvent(
                None, kCGEventMouseMoved, (x, y), 0)
            CGEventPost(kCGHIDEventTap, move)
        return True

    def mouse_down(self, button: str) -> bool:
        """Press mouse button"""
        if self.platform == 'windows':
            button_map = {
                "left": win32con.MOUSEEVENTF_LEFTDOWN,
                "right": win32con.MOUSEEVENTF_RIGHTDOWN,
                "middle": win32con.MOUSEEVENTF_MIDDLEDOWN
            }
            win32api.mouse_event(button_map[button], 0, 0, 0, 0)
        elif self.platform == 'linux':
            button_map = {
                "left": X.Button1,
                "right": X.Button3,
                "middle": X.Button2
            }
            fake_input(self.display, X.ButtonPress, button_map[button])
            self.display.sync()
        else:  # macOS
            button_map = {
                "left": kCGMouseButtonLeft,
                "right": kCGMouseButtonRight,
                "middle": kCGMouseButtonCenter
            }
            pos = CGEventGetLocation(CGEventCreate(None))
            clickDown = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseDown, pos, button_map[button])
            CGEventPost(kCGHIDEventTap, clickDown)
        return True

    def mouse_up(self, button: str) -> bool:
        """Release mouse button"""
        if self.platform == 'windows':
            button_map = {
                "left": win32con.MOUSEEVENTF_LEFTUP,
                "right": win32con.MOUSEEVENTF_RIGHTUP,
                "middle": win32con.MOUSEEVENTF_MIDDLEUP
            }
            win32api.mouse_event(button_map[button], 0, 0, 0, 0)
        elif self.platform == 'linux':
            button_map = {
                "left": X.Button1,
                "right": X.Button3,
                "middle": X.Button2
            }
            fake_input(self.display, X.ButtonRelease, button_map[button])
            self.display.sync()
        else:  # macOS
            button_map = {
                "left": kCGMouseButtonLeft,
                "right": kCGMouseButtonRight,
                "middle": kCGMouseButtonCenter
            }
            pos = CGEventGetLocation(CGEventCreate(None))
            clickUp = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseUp, pos, button_map[button])
            CGEventPost(kCGHIDEventTap, clickUp)
        return True


def main():
    backend = Backend()
    mouse = Mouse(backend)
    keyboard = Keyboard(backend)

    mouse.click(100, 100)
    keyboard.type_text("Hello, World!")


if __name__ == "__main__":
    main()
