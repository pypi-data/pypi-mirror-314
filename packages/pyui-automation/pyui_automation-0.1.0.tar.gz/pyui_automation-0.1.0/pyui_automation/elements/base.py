from typing import Optional, Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.session import AutomationSession

class UIElement:
    """Base class for UI elements"""
    
    def __init__(self, native_element: Any, session: 'AutomationSession'):
        self._element = native_element
        self._session = session

    @property
    def native_element(self) -> Any:
        """Get native element"""
        return self._element

    @property
    def session(self) -> 'AutomationSession':
        """Get automation session"""
        return self._session

    def get_attribute(self, name: str) -> Optional[str]:
        """Get element attribute"""
        return self._element.get_attribute(name)

    def get_property(self, name: str) -> Any:
        """Get element property"""
        return self._element.get_property(name)

    @property
    def text(self) -> str:
        """Get element text"""
        return self._element.text

    @property
    def location(self) -> Dict[str, int]:
        """Get element location"""
        return self._element.location

    @property
    def size(self) -> Dict[str, int]:
        """Get element size"""
        return self._element.size

    def is_displayed(self) -> bool:
        """Check if element is displayed"""
        return self._element.is_displayed()

    def is_enabled(self) -> bool:
        """Check if element is enabled"""
        return self._element.is_enabled()

    def click(self) -> None:
        """Click element"""
        self._element.click()

    def double_click(self) -> None:
        """Double click element"""
        self._session.mouse.double_click(self.location['x'], self.location['y'])

    def right_click(self) -> None:
        """Right click element"""
        self._session.mouse.right_click(self.location['x'], self.location['y'])

    def hover(self) -> None:
        """Hover over element"""
        self._session.mouse.move_to(self.location['x'], self.location['y'])

    def send_keys(self, *keys: str) -> None:
        """Send keys to element"""
        self._element.send_keys(*keys)
