from .base import UIElement

class Button(UIElement):
    """Button element class"""
    
    def is_pressed(self) -> bool:
        """Check if button is pressed"""
        return self.get_property('pressed')

    def wait_until_enabled(self, timeout: float = None) -> bool:
        """Wait until button is enabled"""
        return self._session.waits.wait_until(
            lambda: self.is_enabled(),
            timeout=timeout,
            message="Button not enabled"
        )

    def wait_until_clickable(self, timeout: float = None) -> bool:
        """Wait until button is clickable"""
        return self._session.waits.wait_until(
            lambda: self.is_displayed() and self.is_enabled(),
            timeout=timeout,
            message="Button not clickable"
        )

    def safe_click(self, timeout: float = None) -> bool:
        """Safely click button after waiting for it to be clickable"""
        if self.wait_until_clickable(timeout):
            self.click()
            return True
        return False
