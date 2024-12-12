import pytest
from unittest.mock import MagicMock, patch
from pyui_automation.application import Application
import platform
import psutil
import comtypes.client
import comtypes.gen.UIAutomationClient as UIAutomationClient


@pytest.fixture
def mock_uiautomation():
    """Mock the UIAutomation COM interface"""
    mock_uia = MagicMock(spec=UIAutomationClient.IUIAutomation)
    mock_root = MagicMock()
    mock_uia.GetRootElement.return_value = mock_root
    
    # Mock element
    mock_element = MagicMock()
    mock_element.CurrentName = "Test Window"
    mock_element.CurrentAutomationId = "test-window"
    mock_element.GetCurrentPropertyValue.return_value = "test-value"
    mock_element.CurrentIsEnabled = True
    mock_element.CurrentIsOffscreen = False
    mock_element.CurrentBoundingRectangle = (0, 0, 800, 600)
    mock_element.CurrentNativeWindowHandle = 12345
    
    # Set up search conditions
    mock_condition = MagicMock()
    mock_uia.CreatePropertyCondition.return_value = mock_condition
    mock_root.FindFirst.return_value = mock_element
    mock_root.FindAll.return_value = [mock_element]
    
    return mock_uia


@pytest.fixture
def mock_windows_backend(mock_uiautomation):
    """Create mock Windows backend"""
    with patch('comtypes.client.CreateObject', return_value=mock_uiautomation) as mock_create:
        with patch('pyui_automation.backends.windows.WindowsBackend') as mock_backend:
            instance = mock_backend.return_value
            instance.automation = mock_uiautomation
            instance.root = mock_uiautomation.GetRootElement()
            
            # Set up backend methods
            instance.find_window.return_value = instance.root.FindFirst.return_value
            instance.get_window.return_value = instance.root.FindFirst.return_value
            instance.get_window_title.return_value = "Test Window"
            instance.get_active_window.return_value = instance.root.FindFirst.return_value
            instance.get_main_window.return_value = instance.root.FindFirst.return_value
            instance.get_window_handles.return_value = [12345, 12346]
            
            yield instance


@pytest.fixture
def mock_process():
    """Create a mock process"""
    process = MagicMock(spec=psutil.Process)
    process.pid = 12345
    process.name.return_value = "test_app.exe"
    process.cpu_percent.return_value = 5.0
    process.memory_info.return_value = MagicMock(rss=1024*1024*100)  # 100MB
    process.is_running.return_value = True
    process.children.return_value = []
    return process


@pytest.fixture
def mock_application(mock_process, mock_windows_backend):
    """Create Application instance with mock process"""
    with patch('platform.system', return_value='Windows'), \
         patch('psutil.Process', return_value=mock_process):
        app = Application(process=mock_process)
        app._backend = mock_windows_backend
        return app


def test_terminate_application(mock_application):
    """Test terminating application"""
    mock_application.terminate()
    assert mock_application.process.terminate.called


def test_kill_application(mock_application):
    """Test force killing application"""
    mock_application.kill()
    assert mock_application.process.kill.called


def test_wait_for_window(mock_application):
    """Test waiting for window"""
    # Set up mock window
    mock_window = MagicMock()
    mock_window.CurrentNativeWindowHandle = 12345
    mock_application._backend.find_window.return_value = mock_window
    
    # Test successful window wait
    window = mock_application.wait_for_window("Test Window", timeout=1)
    assert window is not None
    assert window.CurrentNativeWindowHandle == 12345
    mock_application._backend.find_window.assert_called_with("Test Window")
    
    # Test timeout
    mock_application._backend.find_window.return_value = None
    window = mock_application.wait_for_window("NonExistent", timeout=0.1)
    assert window is None


def test_get_window(mock_application):
    """Test getting window by title"""
    # Set up mock window
    mock_window = MagicMock()
    mock_window.CurrentNativeWindowHandle = 12345
    mock_application._backend.find_window.return_value = mock_window
    
    # Test successful window get
    window = mock_application.get_window("Test Window")
    assert window is not None
    assert window.CurrentNativeWindowHandle == 12345
    mock_application._backend.find_window.assert_called_with("Test Window")
    
    # Test window not found
    mock_application._backend.find_window.return_value = None
    window = mock_application.get_window("NonExistent")
    assert window is None


def test_get_main_window(mock_application):
    """Test getting main window"""
    # Set up mock window
    mock_window = MagicMock()
    mock_window.CurrentNativeWindowHandle = 12345
    mock_application._backend.get_active_window.return_value = mock_window
    
    # Test successful main window get
    window = mock_application.get_main_window()
    assert window is not None
    assert window.CurrentNativeWindowHandle == 12345
    mock_application._backend.get_active_window.assert_called_once()
    
    # Test no main window
    mock_application._backend.get_active_window.return_value = None
    window = mock_application.get_main_window()
    assert window is None


def test_get_window_handles(mock_application):
    """Test getting window handles"""
    handles = mock_application.get_window_handles()
    assert handles == [12345, 12346]
    assert mock_application._backend.get_window_handles.called


def test_get_active_window(mock_application):
    """Test getting active window"""
    window = mock_application.get_active_window()
    assert window is not None
    assert window.CurrentNativeWindowHandle == 12345
    assert mock_application._backend.get_active_window.called


def test_is_running(mock_application):
    """Test checking if application is running"""
    assert mock_application.is_running() is True
    mock_application.process.is_running.assert_called_once()


def test_get_cpu_usage(mock_application):
    """Test getting CPU usage"""
    cpu_usage = mock_application.get_cpu_usage()
    assert cpu_usage == 5.0
    mock_application.process.cpu_percent.assert_called_once()


def test_get_memory_usage(mock_application):
    """Test getting memory usage"""
    memory_usage = mock_application.get_memory_usage()
    assert memory_usage == 100  # 100MB
    mock_application.process.memory_info.assert_called_once()
