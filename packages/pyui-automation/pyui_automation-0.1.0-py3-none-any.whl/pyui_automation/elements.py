from typing import Optional, Tuple, Dict


class UIElement:
    """Represents a UI element across different platforms"""

    def __init__(self, native_element, automation):
        self._element = native_element
        self._automation = automation

    @property
    def id(self) -> str:
        """Get element ID"""
        if hasattr(self._element, 'CurrentAutomationId'):
            return self._element.CurrentAutomationId
        return self._element.get_id() if hasattr(self._element, 'get_id') else None

    @property
    def text(self) -> str:
        """Get element text content"""
        if hasattr(self._element, 'CurrentValue'):
            return self._element.CurrentValue
        return self._element.get_text() if hasattr(self._element, 'get_text') else ''

    @property
    def name(self) -> str:
        """Get element name"""
        if hasattr(self._element, 'CurrentName'):
            return self._element.CurrentName
        return self._element.get_name() if hasattr(self._element, 'get_name') else ''

    @property
    def location(self) -> Tuple[int, int]:
        """Get element location (x, y coordinates)"""
        if hasattr(self._element, 'CurrentBoundingRectangle'):
            rect = self._element.CurrentBoundingRectangle
            return (rect[0], rect[1])
        if hasattr(self._element, 'get_location'):
            return self._element.get_location()
        return (0, 0)

    @property
    def size(self) -> Tuple[int, int]:
        """Get element size (width, height)"""
        if hasattr(self._element, 'CurrentBoundingRectangle'):
            rect = self._element.CurrentBoundingRectangle
            return (rect[2] - rect[0], rect[3] - rect[1])
        if hasattr(self._element, 'get_size'):
            return self._element.get_size()
        return (0, 0)

    @property
    def enabled(self) -> bool:
        """Check if element is enabled"""
        if hasattr(self._element, 'CurrentIsEnabled'):
            return self._element.CurrentIsEnabled
        return self._element.is_enabled() if hasattr(self._element, 'is_enabled') else False

    @property
    def visible(self) -> bool:
        """Check if element is visible"""
        if hasattr(self._element, 'CurrentIsOffscreen'):
            return not self._element.CurrentIsOffscreen
        return self._element.is_visible() if hasattr(self._element, 'is_visible') else False

    def click(self):
        """Click the element"""
        if self.visible and self.enabled:
            x, y = self._get_click_point()
            self._automation.mouse.move(x, y)
            self._automation.mouse.click()

    def double_click(self):
        """Double click the element"""
        if self.visible and self.enabled:
            x, y = self._get_click_point()
            self._automation.mouse.move(x, y)
            self._automation.mouse.double_click()

    def right_click(self):
        """Right click the element"""
        if self.visible and self.enabled:
            x, y = self._get_click_point()
            self._automation.mouse.move(x, y)
            self._automation.mouse.click(button='right')

    def type_text(self, text: str, interval: float = 0.0):
        """Type text into element"""
        if self.visible and self.enabled:
            self.click()  # Focus element first
            self._automation.keyboard.type_text(text, interval)

    def clear(self):
        """Clear element content"""
        if hasattr(self._element, 'clear'):
            self._element.clear()
        else:
            # Simulate clear using keyboard
            self.click()
            self._automation.keyboard.press('ctrl+a')
            self._automation.keyboard.press('delete')

    def get_attribute(self, name: str) -> Optional[str]:
        """Get element attribute value"""
        if hasattr(self._element, 'get_attribute'):
            return self._element.get_attribute(name)
        return None

    def get_property(self, name: str) -> Optional[str]:
        """Get element property value"""
        if hasattr(self._element, 'get_property'):
            return self._element.get_property(name)
        return None

    def _get_click_point(self) -> Tuple[int, int]:
        """Get coordinates for clicking element"""
        x, y = self.location
        width, height = self.size
        return (x + width // 2, y + height // 2)
