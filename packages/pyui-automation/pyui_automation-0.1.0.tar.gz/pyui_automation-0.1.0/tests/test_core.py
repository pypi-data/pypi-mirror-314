import pytest
from unittest.mock import MagicMock, patch
from pyui_automation import UIAutomation
from pyui_automation.input import Mouse, Keyboard
import time
import numpy as np
from PIL import Image
import platform
import comtypes.client
import comtypes.gen.UIAutomationClient as UIAutomationClient
import unittest
from pathlib import Path
import tempfile
import psutil


@pytest.fixture
def mock_uiautomation():
    """Mock the UIAutomation COM interface"""
    mock_uia = MagicMock(spec=UIAutomationClient.IUIAutomation)
    mock_root = MagicMock()
    mock_uia.GetRootElement.return_value = mock_root
    
    # Mock element
    mock_element = MagicMock()
    mock_element.CurrentName = "test-button"
    mock_element.CurrentAutomationId = "test-id"
    mock_element.GetCurrentPropertyValue.return_value = "test-value"
    mock_element.CurrentIsEnabled = True
    mock_element.CurrentIsOffscreen = False
    mock_element.CurrentBoundingRectangle = (0, 0, 100, 30)
    
    # Set up search conditions
    mock_condition = MagicMock()
    mock_uia.CreatePropertyCondition.return_value = mock_condition
    mock_root.FindFirst.return_value = mock_element
    mock_root.FindAll.return_value = [mock_element]
    
    return mock_uia


@pytest.fixture
def mock_element():
    """Create a mock element with all required methods and properties"""
    element = MagicMock()
    element.get_attribute.side_effect = lambda name: {
        "AutomationId": "test-id",
        "Name": "test-button"
    }.get(name)
    element.get_property.return_value = "test-value"
    element.text = "test text"
    element.location = {'x': 10, 'y': 20}
    element.size = {'width': 100, 'height': 30}
    element.is_enabled.return_value = True
    element.is_displayed.return_value = True
    element.click = MagicMock()
    element.send_keys = MagicMock()
    return element


@pytest.fixture
def mock_windows_backend(mock_uiautomation, mock_element):
    """Create mock Windows backend"""
    with patch('comtypes.client.CreateObject', return_value=mock_uiautomation):
        with patch('pyui_automation.backends.windows.WindowsBackend') as mock_backend:
            instance = mock_backend.return_value
            instance.automation = mock_uiautomation
            instance.root = mock_uiautomation.GetRootElement()
            
            # Set up backend methods
            instance.find_element.return_value = mock_element
            instance.find_elements.return_value = [mock_element]
            instance.capture_screenshot.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
            instance.type_text.return_value = True
            instance.click.return_value = True
            instance.get_active_window.return_value = mock_element
            instance.press_key.return_value = True
            instance.move_mouse.return_value = True
            instance.mouse_down.return_value = True
            instance.mouse_up.return_value = True
            
            yield instance


@pytest.fixture
def mock_visual_tester():
    """Create mock visual tester"""
    tester = MagicMock()
    tester.baseline_dir = None
    tester.save_baseline = MagicMock()
    tester.compare = MagicMock(return_value={'match': True, 'similarity': 1.0, 'differences': []})
    tester.verify_hash = MagicMock(return_value=True)
    return tester


@pytest.fixture
def ui_automation(mock_windows_backend, mock_visual_tester):
    """Create UIAutomation instance with mock backend"""
    with patch('platform.system', return_value='Windows'):
        # Create automation with mock backend
        automation = UIAutomation(backend=mock_windows_backend)
        automation._visual_tester = mock_visual_tester
        return automation


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary directory for testing"""
    return tmp_path


def test_find_element(ui_automation):
    """Test finding an element"""
    # Mock the backend's find_element method
    mock_element = MagicMock()
    mock_element.get_attribute.side_effect = lambda x: {
        "AutomationId": "test-id",
        "Name": "test-button"
    }[x]
    ui_automation._backend.find_element.return_value = mock_element

    # Test with default timeout
    element = ui_automation.find_element(by="id", value="test-id")
    assert element is not None
    assert element.get_attribute("AutomationId") == "test-id"
    assert element.get_attribute("Name") == "test-button"
    ui_automation._backend.find_element.assert_called_once_with("id", "test-id", 10.0)  # Default timeout


def test_find_element_with_timeout(ui_automation):
    """Test finding an element with timeout"""
    element = ui_automation.find_element(by="name", value="test-button", timeout=5)
    assert element is not None
    ui_automation._backend.find_element.assert_called_once_with("name", "test-button", 5)


def test_take_screenshot(ui_automation, temp_dir):
    """Test taking a screenshot"""
    screenshot = ui_automation.take_screenshot()
    assert screenshot is not None
    assert isinstance(screenshot, np.ndarray)
    assert screenshot.shape == (100, 100, 3)


def test_keyboard_input(ui_automation):
    """Test keyboard input"""
    # Test type_text with default interval
    assert ui_automation.keyboard.type_text("test") is True
    ui_automation._backend.type_text.assert_called_once_with("test", 0.0)

    # Reset mock and test with custom interval
    ui_automation._backend.type_text.reset_mock()
    assert ui_automation.keyboard.type_text("test", interval=0.1) is True
    ui_automation._backend.type_text.assert_called_once_with("test", 0.1)

    # Test press_key
    ui_automation._backend.press_key.return_value = True
    assert ui_automation.keyboard.press_key("enter") is True
    ui_automation._backend.press_key.assert_called_once_with("enter")


def test_mouse_click(ui_automation):
    """Test mouse click"""
    # Test left click
    assert ui_automation.mouse.click(100, 200) is True
    ui_automation._backend.click.assert_called_once_with(100, 200, "left")

    # Reset mock and test right click
    ui_automation._backend.click.reset_mock()
    assert ui_automation.mouse.click(100, 200, "right") is True
    ui_automation._backend.click.assert_called_once_with(100, 200, "right")

    # Test move
    ui_automation._backend.move_mouse.return_value = True
    assert ui_automation.mouse.move(300, 400) is True
    ui_automation._backend.move_mouse.assert_called_once_with(300, 400)

    # Test drag
    ui_automation._backend.move_mouse.reset_mock()
    ui_automation._backend.mouse_down.return_value = True
    ui_automation._backend.mouse_up.return_value = True
    assert ui_automation.mouse.drag(100, 200, 300, 400) is True
    ui_automation._backend.move_mouse.assert_any_call(100, 200)
    ui_automation._backend.move_mouse.assert_any_call(300, 400)
    ui_automation._backend.mouse_down.assert_called_once_with("left")
    ui_automation._backend.mouse_up.assert_called_once_with("left")


def test_wait_until(ui_automation):
    """Test wait until condition"""
    condition = lambda: True
    result = ui_automation.waits.wait_until(condition, timeout=1)
    assert result is True


def test_init_visual_testing(ui_automation, temp_dir):
    """Test initializing visual testing"""
    ui_automation.init_visual_testing(temp_dir)
    assert ui_automation._visual_tester is not None
    assert ui_automation._visual_tester.baseline_dir == temp_dir


def test_capture_visual_baseline(ui_automation, temp_dir):
    """Test capturing visual baseline"""
    ui_automation.init_visual_testing(temp_dir)
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)  # Mock screenshot
    ui_automation._backend.capture_screenshot.return_value = screenshot
    
    # Mock visual tester methods
    ui_automation.visual_tester.capture_baseline = MagicMock()
    ui_automation.capture_visual_baseline("test_baseline")
    ui_automation.visual_tester.capture_baseline.assert_called_once_with("test_baseline", screenshot)


def test_compare_visual(ui_automation, temp_dir):
    """Test visual comparison"""
    ui_automation.init_visual_testing(temp_dir)
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)  # Mock screenshot
    ui_automation._backend.capture_screenshot.return_value = screenshot
    
    # Mock visual tester methods
    ui_automation.visual_tester.compare = MagicMock(return_value={'match': True})
    result = ui_automation.compare_visual("test_compare")
    ui_automation.visual_tester.compare.assert_called_once_with("test_compare", screenshot)
    assert result['match'] is True


def test_verify_visual_hash(ui_automation, temp_dir):
    """Test visual hash verification"""
    ui_automation.init_visual_testing(temp_dir)
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)  # Mock screenshot
    ui_automation._backend.capture_screenshot.return_value = screenshot
    
    # Mock visual tester methods
    ui_automation.visual_tester.verify_hash = MagicMock(return_value=True)
    result = ui_automation.verify_visual_hash("test_hash")
    ui_automation.visual_tester.verify_hash.assert_called_once_with("test_hash", screenshot)
    assert result is True


@patch('subprocess.Popen')
@patch('psutil.Process')
def test_launch_application(mock_process, mock_popen, ui_automation):
    """Test application launch"""
    # Mock subprocess.Popen
    mock_popen_instance = MagicMock()
    mock_popen_instance.pid = 12345
    mock_popen_instance.poll.return_value = None
    mock_popen.return_value = mock_popen_instance
    
    # Mock psutil.Process to use same PID
    mock_psutil_instance = MagicMock()
    mock_psutil_instance.is_running.return_value = True
    mock_process.return_value = mock_psutil_instance
    
    app = ui_automation.launch_application("notepad.exe")
    assert app is not None
    mock_popen.assert_called_once()
    # Verify psutil.Process was called with the PID from Popen
    mock_process.assert_called_once_with(mock_popen_instance.pid)


@patch('psutil.Process')
def test_attach_to_application(mock_process, ui_automation):
    """Test attaching to application"""
    # Mock psutil process
    mock_proc = MagicMock()
    mock_proc.pid = 12345
    mock_proc.is_running.return_value = True
    mock_process.return_value = mock_proc
    
    app = ui_automation.attach_to_application(12345)
    assert app is not None
    mock_process.assert_called_once_with(12345)
