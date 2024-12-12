import pytest
from unittest.mock import MagicMock
from pyui_automation.backends.base import BaseBackend
from typing import Optional, List, Tuple, Any

class ConcreteBackend(BaseBackend):
    """Concrete implementation of BaseBackend for testing"""
    def __init__(self):
        self._mock_find_element = MagicMock()
        self._mock_find_elements = MagicMock()
        self._mock_get_active_window = MagicMock()
        self._mock_take_screenshot = MagicMock()
        self._mock_get_screen_size = MagicMock()

    def find_element(self, by: str, value: str) -> Optional[Any]:
        return self._mock_find_element(by, value)

    def find_elements(self, by: str, value: str) -> List[Any]:
        return self._mock_find_elements(by, value)

    def get_active_window(self) -> Optional[Any]:
        return self._mock_get_active_window()

    def take_screenshot(self, filepath: str) -> bool:
        return self._mock_take_screenshot(filepath)

    def get_screen_size(self) -> Tuple[int, int]:
        return self._mock_get_screen_size()

@pytest.fixture
def backend():
    return ConcreteBackend()

def test_find_element_by_id(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_id("test_id")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("id", "test_id")

def test_find_element_by_name(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_name("test_name")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("name", "test_name")

def test_find_element_by_class(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_class("test_class")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("class", "test_class")

def test_find_element_by_role(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_role("button")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("role", "button")

def test_find_element_by_xpath(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_xpath("//button[@name='test']")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("xpath", "//button[@name='test']")

def test_find_element_by_css(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_css("#test-button")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("css", "#test-button")

def test_find_element_by_text(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_text("Click me")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("text", "Click me")

def test_find_element_by_partial_text(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_partial_text("Click")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("partial_text", "Click")

def test_find_element_by_ocr(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_ocr("Click me")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("ocr_text", "Click me")

def test_find_element_by_image(backend):
    backend._mock_find_element.return_value = "test_element"
    element = backend.find_element_by_image("button.png")
    assert element == "test_element"
    backend._mock_find_element.assert_called_once_with("image", "button.png")

def test_find_element_returns_none(backend):
    backend._mock_find_element.return_value = None
    element = backend.find_element_by_id("non_existent")
    assert element is None
    backend._mock_find_element.assert_called_once_with("id", "non_existent")

def test_get_active_window(backend):
    backend._mock_get_active_window.return_value = "active_window"
    window = backend.get_active_window()
    assert window == "active_window"
    backend._mock_get_active_window.assert_called_once()

def test_take_screenshot(backend):
    backend._mock_take_screenshot.return_value = True
    result = backend.take_screenshot("test.png")
    assert result is True
    backend._mock_take_screenshot.assert_called_once_with("test.png")

def test_get_screen_size(backend):
    backend._mock_get_screen_size.return_value = (1920, 1080)
    size = backend.get_screen_size()
    assert size == (1920, 1080)
    backend._mock_get_screen_size.assert_called_once()

def test_find_elements(backend):
    backend._mock_find_elements.return_value = ["element1", "element2"]
    elements = backend.find_elements("class", "test-class")
    assert elements == ["element1", "element2"]
    backend._mock_find_elements.assert_called_once_with("class", "test-class")

def test_find_elements_empty(backend):
    backend._mock_find_elements.return_value = []
    elements = backend.find_elements("id", "non-existent")
    assert elements == []
    backend._mock_find_elements.assert_called_once_with("id", "non-existent")

def test_abstract_find_element():
    class IncompleteBackend(BaseBackend):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteBackend()

def test_abstract_find_elements():
    class IncompleteBackend(BaseBackend):
        def find_element(self, by, value): pass
        def get_active_window(self): pass
        def take_screenshot(self, filepath): pass
        def get_screen_size(self): pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteBackend()

def test_abstract_get_active_window():
    class IncompleteBackend(BaseBackend):
        def find_element(self, by, value): pass
        def find_elements(self, by, value): pass
        def take_screenshot(self, filepath): pass
        def get_screen_size(self): pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteBackend()

def test_abstract_take_screenshot():
    class IncompleteBackend(BaseBackend):
        def find_element(self, by, value): pass
        def find_elements(self, by, value): pass
        def get_active_window(self): pass
        def get_screen_size(self): pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteBackend()

def test_abstract_get_screen_size():
    class IncompleteBackend(BaseBackend):
        def find_element(self, by, value): pass
        def find_elements(self, by, value): pass
        def get_active_window(self): pass
        def take_screenshot(self, filepath): pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteBackend()
