import pytest
import platform
from unittest.mock import MagicMock, patch
import sys
import numpy as np
from PIL import Image
from pyui_automation.backends.macos import MacOSBackend

# Skip all macOS tests if not on macOS
pytestmark = pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="macOS-specific tests can only run on macOS"
)

# Mock macOS-specific modules
mock_objc = MagicMock()
mock_objc.ObjCClass = MagicMock(return_value=MagicMock())

mock_quartz = MagicMock()
mock_quartz.kCGWindowListOptionOnScreenOnly = 1
mock_quartz.kCGNullWindowID = 0
mock_quartz.kCGWindowImageDefault = 0
mock_quartz.CGWindowListCreateImage = MagicMock(return_value=MagicMock())
mock_quartz.CGImageGetWidth = MagicMock(return_value=1920)
mock_quartz.CGImageGetHeight = MagicMock(return_value=1080)
mock_quartz.CGImageGetBytesPerRow = MagicMock(return_value=1920 * 4)
mock_quartz.CGImageGetDataProvider = MagicMock()
mock_quartz.CGDataProviderCopyData = MagicMock(return_value=b'\x00' * (1920 * 1080 * 4))

mock_nsworkspace = MagicMock()
mock_nsscreen = MagicMock()
mock_nsobject = MagicMock()
mock_nspoint = MagicMock()

mock_appkit = MagicMock()
mock_appkit.NSWorkspace = mock_nsworkspace
mock_appkit.NSScreen = mock_nsscreen

mock_foundation = MagicMock()
mock_foundation.NSObject = mock_nsobject
mock_foundation.NSPoint = mock_nspoint

mock_cocoa = MagicMock()

# Mock the macOS modules
sys.modules['objc'] = mock_objc
sys.modules['Quartz'] = mock_quartz
sys.modules['AppKit'] = mock_appkit
sys.modules['Foundation'] = mock_foundation
sys.modules['Cocoa'] = mock_cocoa

@pytest.fixture
def mock_ax():
    ax = MagicMock()
    ax.systemWide = MagicMock()
    ax.systemWide.return_value = MagicMock()
    return ax

@pytest.fixture
def mock_element():
    element = MagicMock()
    element.AXRole = "AXButton"
    element.AXTitle = "Test Button"
    element.AXEnabled = True
    element.AXPosition = (0, 0)
    element.AXSize = (100, 50)
    return element

@pytest.fixture
def mock_workspace():
    workspace = MagicMock()
    workspace.frontmostApplication.return_value = MagicMock()
    return workspace

@pytest.fixture
def backend(mock_ax, monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'darwin')
    mock_objc.ObjCClass.return_value = mock_ax
    return MacOSBackend()

def test_find_element(backend, mock_element):
    """Test finding a UI element"""
    backend.system.AXFocusedUIElement.return_value = mock_element
    element = backend.find_element("role", "AXButton")
    assert element is not None
    assert element.AXRole == "AXButton"

def test_find_elements(backend, mock_element):
    """Test finding multiple UI elements"""
    backend.system.AXFocusedUIElement.return_value = mock_element
    elements = backend.find_elements("role", "AXButton")
    assert len(elements) > 0
    assert elements[0].AXRole == "AXButton"

def test_get_active_window(backend, mock_element):
    """Test getting active window"""
    backend.system.AXFocusedWindow.return_value = mock_element
    window = backend.get_active_window()
    assert window is not None
    assert window.AXRole == "AXButton"

def test_take_screenshot(backend):
    """Test taking screenshot"""
    screenshot = backend.take_screenshot()
    assert isinstance(screenshot, np.ndarray)
    assert screenshot.shape == (1080, 1920, 4)

def test_get_screen_size(backend):
    """Test getting screen size"""
    size = backend.get_screen_size()
    assert isinstance(size, tuple)
    assert len(size) == 2
    assert size == (1920, 1080)

def test_get_frontmost_application(backend, mock_workspace):
    """Test getting frontmost application"""
    app = backend._get_frontmost_application()
    assert app is not None

def test_matches_criteria(backend, mock_element):
    """Test element criteria matching"""
    assert backend._matches_criteria(mock_element, "role", "AXButton")
    assert backend._matches_criteria(mock_element, "name", "Test Button")
    assert not backend._matches_criteria(mock_element, "role", "AXWindow")

def test_get_attribute(backend, mock_element):
    """Test getting element attribute"""
    value = backend._get_attribute(mock_element, "AXRole")
    assert value == "AXButton"
    value = backend._get_attribute(mock_element, "NonExistentAttribute")
    assert value is None
