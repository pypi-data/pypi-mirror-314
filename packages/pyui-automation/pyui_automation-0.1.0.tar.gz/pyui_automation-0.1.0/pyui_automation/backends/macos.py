import sys
from typing import Optional, List, Tuple, Any
import numpy as np
from PIL import Image

from .base import BaseBackend

if sys.platform == 'darwin':
    import Quartz
    from AppKit import NSWorkspace, NSScreen
    from Foundation import NSObject, NSPoint
    import objc
    from Cocoa import *

class MacOSBackend(BaseBackend):
    """macOS-specific implementation using Apple Accessibility API"""

    def __init__(self):
        if sys.platform != 'darwin':
            raise RuntimeError("MacOSBackend can only be used on macOS systems")
        self.ax = objc.ObjCClass('AXUIElement')
        self.system = self.ax.systemWide()

    def find_element(self, by: str, value: str) -> Optional[Any]:
        """Find a UI element using Apple Accessibility API"""
        app = self._get_frontmost_application()
        if not app:
            return None
        return self._find_element_recursive(app, by, value)

    def find_elements(self, by: str, value: str) -> List[Any]:
        """Find all matching UI elements"""
        app = self._get_frontmost_application()
        if not app:
            return []
        elements = []
        self._find_elements_recursive(app, by, value, elements)
        return elements

    def get_active_window(self) -> Optional[Any]:
        """Get the currently active window"""
        app = self._get_frontmost_application()
        if app:
            windows = self._get_attribute(app, "AXWindows")
            if windows and len(windows) > 0:
                return windows[0]
        return None

    def take_screenshot(self, filepath: str) -> bool:
        """Take a screenshot using Quartz"""
        try:
            # Get the main screen
            screen = NSScreen.mainScreen()
            rect = screen.frame()
            
            # Create CGImage
            image = Quartz.CGWindowListCreateImage(
                rect,
                Quartz.kCGWindowListOptionOnScreenOnly,
                Quartz.kCGNullWindowID,
                Quartz.kCGWindowImageDefault
            )
            
            # Convert to PIL Image
            width = Quartz.CGImageGetWidth(image)
            height = Quartz.CGImageGetHeight(image)
            bytesperrow = Quartz.CGImageGetBytesPerRow(image)
            
            # Create PIL Image
            pil_image = Image.frombytes(
                'RGBA',
                (width, height),
                Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image)),
                'raw',
                'BGRA'
            )
            
            # Save image
            pil_image.save(filepath)
            return True
        except Exception:
            return False

    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        screen = NSScreen.mainScreen()
        rect = screen.frame()
        return (int(rect.size.width), int(rect.size.height))

    def _get_frontmost_application(self) -> Optional[Any]:
        """Get the frontmost application"""
        workspace = NSWorkspace.sharedWorkspace()
        frontmost_app = workspace.frontmostApplication()
        if frontmost_app:
            pid = frontmost_app.processIdentifier()
            return self.ax.applicationElementForPID_(pid)
        return None

    def _find_element_recursive(self, element: Any, by: str, value: str) -> Optional[Any]:
        """Recursively search for an element"""
        if self._matches_criteria(element, by, value):
            return element

        children = self._get_attribute(element, "AXChildren")
        if children:
            for child in children:
                result = self._find_element_recursive(child, by, value)
                if result:
                    return result
        return None

    def _find_elements_recursive(self, element: Any, by: str, value: str, results: List[Any]):
        """Recursively search for all matching elements"""
        if self._matches_criteria(element, by, value):
            results.append(element)

        children = self._get_attribute(element, "AXChildren")
        if children:
            for child in children:
                self._find_elements_recursive(child, by, value, results)

    def _matches_criteria(self, element: Any, by: str, value: str) -> bool:
        """Check if element matches search criteria"""
        try:
            if by == "role":
                return self._get_attribute(element, "AXRole") == value
            elif by == "title":
                return self._get_attribute(element, "AXTitle") == value
            elif by == "description":
                return self._get_attribute(element, "AXDescription") == value
            elif by == "identifier":
                return self._get_attribute(element, "AXIdentifier") == value
        except Exception:
            pass
        return False

    def _get_attribute(self, element: Any, attribute: str) -> Any:
        """Get an accessibility attribute from an element"""
        try:
            return element.attributeValue_(attribute)
        except Exception:
            return None
