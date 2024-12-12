from typing import Optional
from .base import UIElement

class Input(UIElement):
    """Input element class"""
    
    @property
    def value(self) -> str:
        """Get input value"""
        return self.get_property('value')

    @value.setter
    def value(self, text: str) -> None:
        """Set input value"""
        self.clear()
        self.send_keys(text)

    def clear(self) -> None:
        """Clear input value"""
        self._element.clear()

    def append(self, text: str) -> None:
        """Append text to current value"""
        self.send_keys(text)

    def focus(self) -> None:
        """Set focus to input"""
        self.click()

    def select_all(self) -> None:
        """Select all text in input"""
        self.focus()
        self._session.keyboard.select_all()

    def copy(self) -> None:
        """Copy selected text"""
        self._session.keyboard.copy()

    def paste(self) -> None:
        """Paste text"""
        self._session.keyboard.paste()

    def wait_until_value_is(self, expected_value: str, timeout: float = None) -> bool:
        """Wait until input has expected value"""
        return self._session.waits.wait_until(
            lambda: self.value == expected_value,
            timeout=timeout,
            message=f"Input value not equal to '{expected_value}'"
        )
