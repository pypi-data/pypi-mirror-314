import time
from typing import Callable, Optional, Any
from functools import partial


class WaitTimeout(Exception):
    """Exception raised when wait condition times out"""
    pass


def wait_until(condition: Callable[[], bool],
               timeout: float = 10,
               poll_frequency: float = 0.5,
               error_message: str = None) -> bool:
    """
    Wait until condition is true or timeout occurs
    
    Args:
        condition: Function that returns bool
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to check condition in seconds
        error_message: Custom error message for timeout
    
    Returns:
        True if condition was met, raises WaitTimeout otherwise
    """
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        if condition():
            return True
        time.sleep(poll_frequency)
    
    if error_message:
        raise WaitTimeout(error_message)
    raise WaitTimeout(f"Timed out after {timeout} seconds")


class ElementWaits:
    """Element wait conditions"""

    def __init__(self, automation):
        self.automation = automation

    def wait_until(self, condition: Callable[[], bool], timeout: float = 10) -> bool:
        """
        Wait until condition is true or timeout occurs
        
        Args:
            condition: Function that returns bool
            timeout: Maximum time to wait in seconds
        
        Returns:
            True if condition was met, raises WaitTimeout otherwise
        """
        return wait_until(condition, timeout)

    def for_element(self, by: str, value: str, timeout: float = 10) -> Any:
        """Wait for element to be present"""
        def condition():
            element = self.automation.find_element(by, value)
            return element is not None

        self.wait_until(condition, timeout,
                        error_message=f"Element not found with {by}={value}")
        return self.automation.find_element(by, value)

    def for_element_visible(self, element: Any, timeout: float = 10) -> bool:
        """Wait for element to be visible"""
        return self.wait_until(
            lambda: not element.is_offscreen,
            timeout,
            error_message="Element did not become visible"
        )

    def for_element_enabled(self, element: Any, timeout: float = 10) -> bool:
        """Wait for element to be enabled"""
        return self.wait_until(
            lambda: element.is_enabled,
            timeout,
            error_message="Element did not become enabled"
        )

    def for_element_property(self, element: Any, property_name: str,
                           expected_value: Any, timeout: float = 10) -> bool:
        """Wait for element property to have expected value"""
        return self.wait_until(
            lambda: element.get_property(property_name) == expected_value,
            timeout,
            error_message=f"Property {property_name} did not match expected value"
        )

    def for_element_pattern(self, element: Any, pattern_name: str,
                          timeout: float = 10) -> bool:
        """Wait for element to support pattern"""
        return self.wait_until(
            lambda: element.has_pattern(pattern_name),
            timeout,
            error_message=f"Element does not support pattern {pattern_name}"
        )

    def for_element_text(self, by: str, value: str, text: str,
                        timeout: float = 10) -> Any:
        """Wait for element to have specific text"""
        element = self.for_element(by, value, timeout)
        
        def condition():
            return element.text == text

        self.wait_until(condition, timeout,
                  error_message=f"Element text mismatch: {by}={value}")
        return element

    def for_element_contains_text(self, by: str, value: str, text: str,
                                timeout: float = 10) -> Any:
        """Wait for element to contain specific text"""
        element = self.for_element(by, value, timeout)
        
        def condition():
            return text in element.text

        self.wait_until(condition, timeout,
                  error_message=f"Element does not contain text: {by}={value}")
        return element
