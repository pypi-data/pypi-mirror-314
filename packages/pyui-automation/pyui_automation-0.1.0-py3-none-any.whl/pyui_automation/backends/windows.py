import os
from typing import Optional, Any, List, Tuple
import win32gui
import win32con
import win32api
from PIL import Image
import numpy as np
import comtypes.client
import comtypes.gen.UIAutomationClient as UIAutomationClient
import win32ui
import time
import win32process

# Import or generate UI Automation type library
try:
    from comtypes.gen.UIAutomationClient import *
except ImportError:
    # Generate the required wrapper module
    dll_path = os.path.join(os.environ['SystemRoot'], 'System32', 'UIAutomationCore.dll')
    comtypes.client.GetModule(dll_path)
    from comtypes.gen.UIAutomationClient import *


from .base import BaseBackend


class WindowsBackend(BaseBackend):
    """Windows-specific implementation using UI Automation"""

    def __init__(self):
        try:
            # Register the COM server first
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"UIAutomationClient.CUIAutomation")
                winreg.CloseKey(key)
            except WindowsError:
                # If the key doesn't exist, register the COM server
                os.system('regsvr32 /s %SystemRoot%\\System32\\UIAutomationCore.dll')
            
            # Create UI Automation client using proper interface
            self.automation = comtypes.client.CreateObject(
                "UIAutomationClient.CUIAutomation",
                interface=UIAutomationClient.IUIAutomation
            )
            self.root = self.automation.GetRootElement()
            self._init_patterns()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Windows UI Automation: {str(e)}")

    def _init_patterns(self):
        """Initialize commonly used UI Automation patterns"""
        self.value_pattern = None
        self.invoke_pattern = None
        self.window_pattern = None
        self.transform_pattern = None

    def find_element(self, by: str, value: str, timeout: float = 0) -> Optional[Any]:
        """Find a UI element using Windows UI Automation"""
        try:
            condition = self._create_condition(by, value)
            if not condition:
                return None
                
            if timeout > 0:
                start_time = time.time()
                while time.time() - start_time < timeout:
                    element = self.root.FindFirst(UIAutomationClient.TreeScope_Descendants, condition)
                    if element:
                        return element
                    time.sleep(0.1)
                return None
            
            return self.root.FindFirst(UIAutomationClient.TreeScope_Descendants, condition)
        except Exception as e:
            return None

    def find_elements(self, by: str, value: str) -> List[Any]:
        """Find all matching UI elements"""
        try:
            condition = self._create_condition(by, value)
            if condition:
                return list(self.root.FindAll(UIAutomationClient.TreeScope_Children | UIAutomationClient.TreeScope_Descendants, condition))
        except Exception as e:
            print(f"Error finding elements: {str(e)}")
        return []

    def _create_condition(self, by: str, value: str) -> Optional[Any]:
        """Create search condition based on search strategy"""
        try:
            if by == "id":
                return self.automation.CreatePropertyCondition(
                    UIAutomationClient.UIA_AutomationIdPropertyId, value)
            elif by == "name":
                return self.automation.CreatePropertyCondition(
                    UIAutomationClient.UIA_NamePropertyId, value)
            elif by == "class":
                return self.automation.CreatePropertyCondition(
                    UIAutomationClient.UIA_ClassNamePropertyId, value)
            elif by == "type":
                return self.automation.CreatePropertyCondition(
                    UIAutomationClient.UIA_ControlTypePropertyId, value)
            return None
        except Exception:
            return None

    def get_active_window(self) -> Optional[Any]:
        """Get the currently active window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                return self.automation.ElementFromHandle(hwnd)
        except Exception as e:
            print(f"Error getting active window: {str(e)}")
        return None

    def get_window_handles(self) -> List[int]:
        """Get all window handles"""
        try:
            handles = []
            def enum_windows(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    handles.append(hwnd)
                return True
            win32gui.EnumWindows(enum_windows, None)
            return handles
        except Exception as e:
            print(f"Error getting window handles: {str(e)}")
            return []

    def click(self, x: int, y: int, button: str = "left"):
        """Perform mouse click at coordinates"""
        try:
            # Move cursor to position
            win32api.SetCursorPos((x, y))
            time.sleep(0.1)  # Small delay for cursor movement
            
            # Map button names to win32 constants
            button_map = {
                "left": (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
                "right": (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
                "middle": (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP)
            }
            
            if button not in button_map:
                raise ValueError(f"Invalid button: {button}")
                
            down_event, up_event = button_map[button]
            
            # Perform click
            win32api.mouse_event(down_event, x, y, 0, 0)
            time.sleep(0.1)  # Small delay between down and up
            win32api.mouse_event(up_event, x, y, 0, 0)
            return True
        except Exception as e:
            print(f"Error performing click: {str(e)}")
            return False

    def type_text(self, text: str, interval: float = 0.0) -> bool:
        """Type text using Windows API"""
        try:
            for char in text:
                vk = win32api.VkKeyScan(char)
                if vk == -1:
                    continue
                    
                # Handle shift state
                if vk >> 8:  # If shift state is set
                    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                
                # Press and release the key
                win32api.keybd_event(vk & 0xFF, 0, 0, 0)
                win32api.keybd_event(vk & 0xFF, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                # Release shift if it was pressed
                if vk >> 8:
                    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                if interval > 0:
                    time.sleep(interval)
            return True
        except Exception as e:
            print(f"Error typing text: {str(e)}")
            return False

    def get_window_handle(self, pid: int = None) -> Optional[int]:
        """Get window handle for process"""
        def callback(hwnd, handles):
            if win32gui.IsWindowVisible(hwnd):
                _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                if pid is None or process_id == pid:
                    handles.append(hwnd)
            return True

        handles = []
        win32gui.EnumWindows(callback, handles)
        return handles[0] if handles else None

    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        try:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            return (width, height)
        except Exception as e:
            print(f"Error getting screen size: {str(e)}")
            return (0, 0)

    def take_screenshot(self, filepath: str) -> bool:
        """Take a screenshot and save to file"""
        try:
            # Get screen dimensions
            width, height = self.get_screen_size()
            
            # Create device context and bitmap
            hdesktop = win32gui.GetDesktopWindow()
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
            
            # Convert to PIL Image and save
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            
            im.save(filepath)
            
            # Cleanup
            mem_dc.DeleteDC()
            win32gui.DeleteObject(screenshot.GetHandle())
            
            return True
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return False

    def capture_screenshot(self) -> Optional[np.ndarray]:
        """Capture screenshot as numpy array"""
        try:
            # Get screen dimensions
            width, height = self.get_screen_size()
            
            # Create device context and bitmap
            hdesktop = win32gui.GetDesktopWindow()
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
            
            # Convert to numpy array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            
            # Cleanup
            mem_dc.DeleteDC()
            win32gui.DeleteObject(screenshot.GetHandle())
            
            return img[..., :3]  # Remove alpha channel
        except Exception as e:
            print(f"Error capturing screenshot: {str(e)}")
            return None

    def find_window(self, title: str) -> Optional[Any]:
        """Find window by title"""
        try:
            condition = self.automation.CreatePropertyCondition(
                UIAutomationClient.UIA_NamePropertyId, title
            )
            return self.root.FindFirst(UIAutomationClient.TreeScope_Children | UIAutomationClient.TreeScope_Descendants, condition)
        except Exception as e:
            print(f"Error finding window: {str(e)}")
            return None

    def get_window_title(self, window: Any) -> Optional[str]:
        """Get window title"""
        try:
            return window.CurrentName
        except Exception as e:
            print(f"Error getting window title: {str(e)}")
            return None

    def wait_for_window(self, title: str, timeout: int = 30) -> Optional[Any]:
        """Wait for window with given title to appear"""
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                window = self.find_window(title)
                if window:
                    return window
                time.sleep(0.5)
        except Exception as e:
            print(f"Error waiting for window: {str(e)}")
        return None

    def get_element_attributes(self, element: Any) -> dict:
        """Get element attributes"""
        try:
            return {
                'name': element.CurrentName,
                'id': element.CurrentAutomationId,
                'class_name': element.CurrentClassName,
                'control_type': element.CurrentControlType,
                'is_enabled': element.CurrentIsEnabled,
                'is_offscreen': element.CurrentIsOffscreen,
                'bounding_rectangle': element.CurrentBoundingRectangle
            }
        except Exception as e:
            print(f"Error getting element attributes: {str(e)}")
            return {}
