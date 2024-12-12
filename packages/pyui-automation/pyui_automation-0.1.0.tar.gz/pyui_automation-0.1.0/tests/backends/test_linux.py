import pytest
from unittest.mock import MagicMock, patch
import sys
import numpy as np
from PIL import Image
import platform

# Skip all Linux tests if not on Linux
pytestmark = pytest.mark.skipif(
    platform.system() != "Linux",
    reason="Linux-specific tests can only run on Linux"
)

# Mock Linux-specific modules
class MockXlib:
    def __init__(self):
        self.Display = MagicMock()
        self.X = MagicMock()

mock_xlib = MockXlib()
mock_display = MagicMock()
mock_x = MagicMock()

# Set up the mock modules
sys.modules['Xlib'] = mock_xlib
sys.modules['Xlib.display'] = MagicMock(Display=mock_display)
sys.modules['Xlib.X'] = mock_x
sys.modules['pyatspi'] = MagicMock()

# Now import LinuxBackend after mocking the dependencies
from pyui_automation.backends.linux import LinuxBackend

@pytest.fixture
def mock_window():
    window = MagicMock()
    window.get_geometry.return_value = MagicMock(
        width=1920,
        height=1080,
        x=0,
        y=0
    )
    window.get_attributes.return_value = MagicMock(
        map_state=1,  # IsViewable
        x=0,
        y=0,
        width=1920,
        height=1080
    )
    window.get_wm_name.return_value = "Test Window"
    window.get_wm_class.return_value = ("test_class", "Test_Class")
    return window

@pytest.fixture
def mock_screen(mock_window):
    screen = MagicMock()
    screen.root = mock_window
    screen.width_in_pixels = 1920
    screen.height_in_pixels = 1080
    return screen

@pytest.fixture
def mock_display_instance(mock_screen, mock_window):
    display = MagicMock()
    display.screen.return_value = mock_screen
    display.get_input_focus.return_value = mock_window
    display.create_resource_object.return_value = mock_window
    
    # Set up image data for screenshots
    image = MagicMock()
    image.data = b'\x00' * (1920 * 1080 * 4)
    mock_window.get_image.return_value = image
    
    return display

@pytest.fixture
def backend(mock_display_instance):
    # Configure the Display mock to return our mock display instance
    mock_display.return_value = mock_display_instance
    return LinuxBackend()

def test_init_success(mock_display_instance):
    """Test successful initialization on Linux"""
    backend = LinuxBackend()
    assert backend._display is mock_display_instance

def test_find_element(backend, mock_window):
    """Test finding a UI element"""
    element = backend.find_element("name", "Test Window")
    assert element is not None
    assert element.get_wm_name() == "Test Window"

def test_find_elements(backend, mock_window):
    """Test finding multiple UI elements"""
    elements = backend.find_elements("name", "Test Window")
    assert len(elements) > 0
    assert elements[0].get_wm_name() == "Test Window"

def test_get_active_window(backend, mock_window):
    """Test getting active window"""
    window = backend.get_active_window()
    assert window is not None
    assert window.get_wm_name() == "Test Window"

def test_take_screenshot(backend):
    """Test taking screenshot"""
    screenshot = backend.take_screenshot()
    assert isinstance(screenshot, np.ndarray)
    assert screenshot.shape == (1080, 1920, 4)

def test_get_screen_size(backend):
    """Test getting screen size"""
    width, height = backend.get_screen_size()
    assert width == 1920
    assert height == 1080

def test_matches_criteria(backend, mock_window):
    """Test element criteria matching"""
    assert backend._matches_criteria(mock_window, "name", "Test Window")
    assert backend._matches_criteria(mock_window, "class", "test_class")
    assert not backend._matches_criteria(mock_window, "name", "Wrong Window")

def test_cleanup(backend, mock_display_instance):
    """Test cleanup"""
    backend.__del__()
    mock_display_instance.close.assert_called_once()
