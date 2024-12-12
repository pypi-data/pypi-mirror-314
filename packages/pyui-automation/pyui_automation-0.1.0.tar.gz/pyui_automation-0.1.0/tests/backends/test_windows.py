import pytest
from unittest.mock import MagicMock, patch, PropertyMock
import win32gui
import win32con
import win32api
import win32ui
import numpy as np
from PIL import Image
import comtypes.client
from pyui_automation.backends.windows import WindowsBackend


@pytest.fixture
def mock_automation():
    automation = MagicMock()
    automation.GetRootElement.return_value = MagicMock()
    return automation


@pytest.fixture
def mock_element():
    """Create mock element with required properties"""
    mock = MagicMock()
    type(mock).CurrentName = PropertyMock(return_value="Test Element")
    type(mock).CurrentAutomationId = PropertyMock(return_value="test_id")
    type(mock).CurrentClassName = PropertyMock(return_value="TestClass")
    type(mock).CurrentControlType = PropertyMock(return_value=50000)
    type(mock).CurrentIsEnabled = PropertyMock(return_value=True)
    type(mock).CurrentIsOffscreen = PropertyMock(return_value=False)
    type(mock).CurrentBoundingRectangle = PropertyMock(return_value=(0, 0, 100, 100))
    return mock


@pytest.fixture
def backend(mock_automation):
    with patch('comtypes.client.CreateObject', return_value=mock_automation):
        return WindowsBackend()


def test_init_success(mock_automation):
    """Test successful initialization"""
    with patch('comtypes.client.CreateObject', return_value=mock_automation):
        backend = WindowsBackend()
        assert backend.automation == mock_automation
        assert backend.root == mock_automation.GetRootElement.return_value


def test_init_failure():
    """Test initialization failure"""
    with patch('comtypes.client.CreateObject', side_effect=Exception("Test error")):
        with pytest.raises(RuntimeError) as exc:
            WindowsBackend()
        assert "Failed to initialize Windows UI Automation" in str(exc.value)


def test_find_element(backend, mock_element):
    """Test finding a single element"""
    # Test successful find
    condition = MagicMock()
    backend.automation.CreatePropertyCondition.return_value = condition
    backend.root.FindFirst.return_value = mock_element

    element = backend.find_element("id", "test_id")
    assert element == mock_element
    backend.automation.CreatePropertyCondition.assert_called_once()

    # Test with timeout
    backend.root.FindFirst.side_effect = [None, None, mock_element]
    with patch('time.sleep'):  # Mock sleep to speed up test
        element = backend.find_element("id", "test_id", timeout=1)
        assert element == mock_element

    # Test not found
    backend.root.FindFirst.return_value = None
    element = backend.find_element("id", "nonexistent")
    assert element is None

    # Test exception handling
    backend.root.FindFirst.side_effect = Exception("Test error")
    element = backend.find_element("id", "test_id")
    assert element is None


def test_find_elements(backend, mock_element):
    """Test finding multiple elements"""
    # Test successful find
    condition = MagicMock()
    backend.automation.CreatePropertyCondition.return_value = condition
    backend.root.FindAll.return_value = [mock_element, mock_element]

    elements = backend.find_elements("class", "TestClass")
    assert len(elements) == 2
    assert all(e == mock_element for e in elements)

    # Test no elements found
    backend.root.FindAll.return_value = []
    elements = backend.find_elements("class", "NonexistentClass")
    assert elements == []

    # Test exception handling
    backend.root.FindAll.side_effect = Exception("Test error")
    elements = backend.find_elements("class", "TestClass")
    assert elements == []


def test_create_condition(backend):
    """Test condition creation for different search strategies"""
    # Test all supported strategies
    for by, value in [
        ("id", "test_id"),
        ("name", "Test Name"),
        ("class", "TestClass"),
        ("type", "button")
    ]:
        condition = backend._create_condition(by, value)
        assert condition == backend.automation.CreatePropertyCondition.return_value
        backend.automation.CreatePropertyCondition.assert_called()

    # Test invalid strategy
    condition = backend._create_condition("invalid", "value")
    assert condition is None

    # Test exception handling
    backend.automation.CreatePropertyCondition.side_effect = Exception("Test error")
    condition = backend._create_condition("id", "test_id")
    assert condition is None


def test_get_active_window(backend, mock_element):
    """Test getting active window"""
    with patch('win32gui.GetForegroundWindow', return_value=12345):
        backend.automation.ElementFromHandle.return_value = mock_element
        window = backend.get_active_window()
        assert window == mock_element

    # Test no active window
    with patch('win32gui.GetForegroundWindow', return_value=0):
        window = backend.get_active_window()
        assert window is None

    # Test exception handling
    with patch('win32gui.GetForegroundWindow', side_effect=Exception("Test error")):
        window = backend.get_active_window()
        assert window is None


def test_get_window_handles(backend):
    """Test getting window handles"""
    def mock_enum_windows(callback, extra):
        for hwnd in [12345, 67890]:
            callback(hwnd, extra)

    with patch('win32gui.EnumWindows', side_effect=mock_enum_windows), \
         patch('win32gui.IsWindowVisible', return_value=True):
        handles = backend.get_window_handles()
        assert handles == [12345, 67890]

    # Test exception handling
    with patch('win32gui.EnumWindows', side_effect=Exception("Test error")):
        handles = backend.get_window_handles()
        assert handles == []


def test_click(backend):
    """Test mouse click functionality"""
    with patch('win32api.SetCursorPos') as mock_set_pos, \
         patch('win32api.mouse_event') as mock_mouse_event, \
         patch('time.sleep'):
        
        # Test left click
        assert backend.click(100, 200, "left") is True
        mock_set_pos.assert_called_with((100, 200))
        assert mock_mouse_event.call_count == 2  # down and up events

        # Test right click
        assert backend.click(100, 200, "right") is True
        mock_mouse_event.assert_called()

        # Test invalid button
        assert backend.click(100, 200, "invalid") is False

        # Test exception handling
        mock_set_pos.side_effect = Exception("Test error")
        assert backend.click(100, 200) is False


def test_type_text(backend):
    """Test text typing functionality"""
    with patch('win32api.VkKeyScan', return_value=65), \
         patch('win32api.keybd_event') as mock_keybd_event, \
         patch('time.sleep'):
        
        # Test basic typing
        assert backend.type_text("test") is True
        assert mock_keybd_event.call_count == 8  # 4 chars * (down + up)

        # Test with interval
        assert backend.type_text("test", interval=0.1) is True

        # Test with shift character
        with patch('win32api.VkKeyScan', return_value=(65 | (1 << 8))):
            assert backend.type_text("A") is True
            assert mock_keybd_event.call_count >= 4  # shift down, key down, key up, shift up

        # Test invalid character
        with patch('win32api.VkKeyScan', return_value=-1):
            assert backend.type_text("☺") is True  # Should skip invalid char

        # Test exception handling
        mock_keybd_event.side_effect = Exception("Test error")
        assert backend.type_text("test") is False


def test_get_screen_size(backend):
    """Test screen size retrieval"""
    with patch('win32api.GetSystemMetrics', side_effect=[1920, 1080]):
        size = backend.get_screen_size()
        assert size == (1920, 1080)

    # Test exception handling
    with patch('win32api.GetSystemMetrics', side_effect=Exception("Test error")):
        size = backend.get_screen_size()
        assert size == (0, 0)


def test_find_window(backend, mock_element):
    """Test finding window by title"""
    condition = MagicMock()
    backend.automation.CreatePropertyCondition.return_value = condition
    backend.root.FindFirst.return_value = mock_element

    # Test successful find
    window = backend.find_window("Test Window")
    assert window == mock_element
    backend.automation.CreatePropertyCondition.assert_called_once()

    # Test window not found
    backend.root.FindFirst.return_value = None
    window = backend.find_window("Nonexistent Window")
    assert window is None

    # Test exception handling
    backend.root.FindFirst.side_effect = Exception("Test error")
    window = backend.find_window("Test Window")
    assert window is None


def test_get_window_title(backend, mock_element):
    """Test getting window title"""
    # Test successful get
    type(mock_element).CurrentName = PropertyMock(return_value="Test Element")
    title = backend.get_window_title(mock_element)
    assert title == "Test Element"

    # Test exception handling
    mock = MagicMock()
    type(mock).CurrentName = PropertyMock(side_effect=Exception("No title"))
    title = backend.get_window_title(mock)
    assert title is None


def test_wait_for_window(backend, mock_element):
    """Test waiting for window"""
    with patch('time.sleep'):
        # Test successful wait
        backend.find_window = MagicMock(side_effect=[None, None, mock_element])
        window = backend.wait_for_window("Test Window", timeout=1)
        assert window == mock_element

        # Test timeout
        backend.find_window = MagicMock(return_value=None)
        window = backend.wait_for_window("Nonexistent Window", timeout=1)
        assert window is None

        # Test exception handling
        backend.find_window.side_effect = Exception("Test error")
        window = backend.wait_for_window("Test Window", timeout=1)
        assert window is None


def test_get_element_attributes(backend, mock_element):
    """Test getting element attributes"""
    # Test successful get
    attrs = backend.get_element_attributes(mock_element)
    assert attrs == {
        'name': "Test Element",
        'id': "test_id",
        'class_name': "TestClass",
        'control_type': 50000,
        'is_enabled': True,
        'is_offscreen': False,
        'bounding_rectangle': (0, 0, 100, 100)
    }

    # Test exception handling by creating a mock that raises AttributeError
    mock = MagicMock()
    type(mock).CurrentName = PropertyMock(side_effect=Exception("No name"))
    type(mock).CurrentAutomationId = PropertyMock(side_effect=Exception("No id"))
    type(mock).CurrentClassName = PropertyMock(side_effect=Exception("No class"))
    type(mock).CurrentControlType = PropertyMock(side_effect=Exception("No type"))
    type(mock).CurrentIsEnabled = PropertyMock(side_effect=Exception("Not enabled"))
    type(mock).CurrentIsOffscreen = PropertyMock(side_effect=Exception("Not offscreen"))
    type(mock).CurrentBoundingRectangle = PropertyMock(side_effect=Exception("No bounds"))

    attrs = backend.get_element_attributes(mock)
    assert attrs == {}
