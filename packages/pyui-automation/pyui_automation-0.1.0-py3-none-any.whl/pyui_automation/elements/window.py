from typing import Optional, List, Dict
from .base import UIElement

class Window(UIElement):
    """Window element class"""
    
    @property
    def title(self) -> str:
        """Get window title"""
        return self.get_property('title')

    def maximize(self) -> None:
        """Maximize window"""
        self._element.maximize()

    def minimize(self) -> None:
        """Minimize window"""
        self._element.minimize()

    def restore(self) -> None:
        """Restore window"""
        self._element.restore()

    def close(self) -> None:
        """Close window"""
        self._element.close()

    def move_to(self, x: int, y: int) -> None:
        """Move window to position"""
        self._element.move_to(x, y)

    def resize(self, width: int, height: int) -> None:
        """Resize window"""
        self._element.resize(width, height)

    def get_child_windows(self) -> List['Window']:
        """Get child windows"""
        children = self._element.get_child_windows()
        return [Window(child, self._session) for child in children]

    def get_process_id(self) -> int:
        """Get window process ID"""
        return self._element.get_process_id()

    def bring_to_front(self) -> None:
        """Bring window to front"""
        self._element.bring_to_front()
