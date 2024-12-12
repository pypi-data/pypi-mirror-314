import pytest
from unittest.mock import MagicMock
from pyui_automation.elements.window import Window
from pyui_automation.core.session import AutomationSession

@pytest.fixture
def mock_session():
    return MagicMock(spec=AutomationSession)

@pytest.fixture
def mock_native_element():
    element = MagicMock()
    element.get_property.return_value = "Test Window"
    element.maximize = MagicMock()
    element.minimize = MagicMock()
    element.restore = MagicMock()
    element.close = MagicMock()
    element.move_to = MagicMock()
    element.resize = MagicMock()
    element.get_child_windows.return_value = []
    element.get_process_id.return_value = 1234
    element.bring_to_front = MagicMock()
    return element

@pytest.fixture
def window(mock_session, mock_native_element):
    return Window(mock_native_element, mock_session)

def test_title(window, mock_native_element):
    """Test getting window title"""
    assert window.title == "Test Window"
    mock_native_element.get_property.assert_called_with('title')

def test_maximize(window, mock_native_element):
    """Test maximizing window"""
    window.maximize()
    mock_native_element.maximize.assert_called_once()

def test_minimize(window, mock_native_element):
    """Test minimizing window"""
    window.minimize()
    mock_native_element.minimize.assert_called_once()

def test_restore(window, mock_native_element):
    """Test restoring window"""
    window.restore()
    mock_native_element.restore.assert_called_once()

def test_close(window, mock_native_element):
    """Test closing window"""
    window.close()
    mock_native_element.close.assert_called_once()

def test_move_to(window, mock_native_element):
    """Test moving window"""
    window.move_to(100, 200)
    mock_native_element.move_to.assert_called_with(100, 200)

def test_resize(window, mock_native_element):
    """Test resizing window"""
    window.resize(800, 600)
    mock_native_element.resize.assert_called_with(800, 600)

def test_get_child_windows(window, mock_native_element):
    """Test getting child windows"""
    child_element = MagicMock()
    mock_native_element.get_child_windows.return_value = [child_element]
    
    children = window.get_child_windows()
    assert len(children) == 1
    assert isinstance(children[0], Window)
    mock_native_element.get_child_windows.assert_called_once()

def test_get_process_id(window, mock_native_element):
    """Test getting process ID"""
    assert window.get_process_id() == 1234
    mock_native_element.get_process_id.assert_called_once()

def test_bring_to_front(window, mock_native_element):
    """Test bringing window to front"""
    window.bring_to_front()
    mock_native_element.bring_to_front.assert_called_once()
