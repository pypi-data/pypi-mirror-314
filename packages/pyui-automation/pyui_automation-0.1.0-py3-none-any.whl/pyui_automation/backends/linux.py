import sys
from typing import Optional, List, Tuple, Any
import numpy as np
from PIL import Image

from .base import BaseBackend

if sys.platform == 'linux':
    import pyatspi
    from Xlib import display, X


class LinuxBackend(BaseBackend):
    """Linux-specific implementation using AT-SPI2"""

    def __init__(self):
        if sys.platform != 'linux':
            raise RuntimeError("LinuxBackend can only be used on Linux systems")
        self.display = display.Display()
        self.screen = self.display.screen()
        self.registry = pyatspi.Registry
        self.registry.start()

    def find_element(self, by: str, value: str) -> Optional[Any]:
        """Find a UI element using AT-SPI2"""
        desktop = self.registry.getDesktop(0)
        return self._find_element_recursive(desktop, by, value)

    def find_elements(self, by: str, value: str) -> List[Any]:
        """Find all matching UI elements"""
        desktop = self.registry.getDesktop(0)
        elements = []
        self._find_elements_recursive(desktop, by, value, elements)
        return elements

    def get_active_window(self) -> Optional[Any]:
        """Get the currently active window"""
        desktop = self.registry.getDesktop(0)
        for app in desktop:
            if app.getState().contains(pyatspi.STATE_ACTIVE):
                return app
        return None

    def take_screenshot(self, filepath: str) -> bool:
        """Take a screenshot using X11"""
        try:
            root = self.display.screen().root
            geom = root.get_geometry()
            raw = root.get_image(0, 0, geom.width, geom.height, X.ZPixmap, 0xffffffff)
            image = Image.frombytes("RGB", (geom.width, geom.height), raw.data, "raw", "BGRX")
            image.save(filepath)
            return True
        except Exception:
            return False

    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        root = self.display.screen().root
        geom = root.get_geometry()
        return (geom.width, geom.height)

    def _find_element_recursive(self, element: Any, by: str, value: str) -> Optional[Any]:
        """Recursively search for an element"""
        if self._matches_criteria(element, by, value):
            return element

        for i in range(element.childCount):
            child = element.getChildAtIndex(i)
            result = self._find_element_recursive(child, by, value)
            if result:
                return result
        return None

    def _find_elements_recursive(self, element: Any, by: str, value: str, results: List[Any]):
        """Recursively search for all matching elements"""
        if self._matches_criteria(element, by, value):
            results.append(element)

        for i in range(element.childCount):
            child = element.getChildAtIndex(i)
            self._find_elements_recursive(child, by, value, results)

    def _matches_criteria(self, element: Any, by: str, value: str) -> bool:
        """Check if element matches search criteria"""
        try:
            if by == "name":
                return element.name == value
            elif by == "role":
                return element.getRole() == getattr(pyatspi, value.upper())
            elif by == "id":
                return str(element.id) == value
            elif by == "description":
                return element.description == value
        except Exception:
            pass
        return False

    def __del__(self):
        """Cleanup AT-SPI2 registry"""
        try:
            self.registry.stop()
        except Exception:
            pass
