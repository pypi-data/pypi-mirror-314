import os
import sys
import pytest
from unittest.mock import MagicMock
from pathlib import Path
from PIL import Image
import numpy as np

from pyui_automation import UIAutomation
from pyui_automation.elements import UIElement
from pyui_automation.accessibility import AccessibilityChecker
from pyui_automation.application import Application
from pyui_automation.performance import PerformanceMonitor


# Create a mock module for os
class MockOS:
    def __init__(self):
        # Copy all attributes from the real os module
        for attr in dir(os):
            if not attr.startswith('__'):
                setattr(self, attr, getattr(os, attr))
        # Add mock getuid
        self.getuid = MagicMock(return_value=1000)

# Replace os module with our mock for tests
@pytest.fixture(autouse=True)
def mock_os_module():
    real_os = sys.modules['os']
    mock_os = MockOS()
    sys.modules['os'] = mock_os
    yield
    sys.modules['os'] = real_os


@pytest.fixture
def mock_element():
    """Create a mock UI element for testing"""
    element = MagicMock(spec=UIElement)
    element.id = 'test-id'
    element.name = 'test-button'
    element.class_name = 'button'
    element.location = (100, 100)
    element.size = (50, 30)
    element.text = 'Click me'
    element.enabled = True
    element.visible = True
    element.get_attribute.return_value = 'test-value'
    element.is_enabled.return_value = True
    element.is_displayed.return_value = True
    element.is_keyboard_accessible.return_value = True
    element.get_location.return_value = (100, 100)
    element.get_size.return_value = (50, 30)
    element.capture.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    return element


@pytest.fixture
def mock_backend():
    """Mock backend for testing"""
    backend = MagicMock()
    backend.find_element.return_value = mock_element()
    backend.find_elements.return_value = [mock_element()]
    backend.get_active_window.return_value = mock_element()
    backend.capture_element.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    backend.get_element_attribute.return_value = 'test-value'
    backend.get_window_handles.return_value = ['window1', 'window2']
    backend.get_main_window.return_value = mock_element()
    backend.wait_for_window.return_value = True
    backend.take_screenshot.return_value = "screenshot.png"
    return backend


@pytest.fixture
def ui_automation(mock_backend):
    """Create UIAutomation instance with mocked backend"""
    automation = UIAutomation()
    automation._backend = mock_backend
    return automation


@pytest.fixture
def mock_process():
    """Create a mock process for testing"""
    process = MagicMock()
    process.pid = 12345
    process.name.return_value = 'test_app.exe'
    process.is_running.return_value = True
    process.cpu_percent.return_value = 5.0
    process.memory_info.return_value = MagicMock(rss=1024*1024*100)  # 100MB
    process.terminate = MagicMock()
    process.kill = MagicMock()
    process.exe.return_value = "test_app.exe"
    return process


@pytest.fixture
def mock_application(mock_process, mock_backend):
    """Create a mock application for testing"""
    with patch('platform.system', return_value='Windows'):
        app = Application('test_app.exe')
        app._process = mock_process
        app._backend = mock_backend
        app.pid = mock_process.pid
        return app


@pytest.fixture
def accessibility_checker(ui_automation):
    """Create AccessibilityChecker instance"""
    checker = AccessibilityChecker(ui_automation)
    checker._is_image_element = MagicMock(return_value=True)
    checker._get_element_color = MagicMock(side_effect=[(0, 0, 0), (255, 255, 255)])
    return checker


@pytest.fixture
def mock_performance_data():
    """Create mock performance data"""
    return {
        'cpu_usage': [5.0, 6.0, 4.0],
        'memory_usage': [100*1024*1024, 110*1024*1024, 95*1024*1024],
        'duration': 1.5,
        'timestamps': [0.0, 0.5, 1.0]
    }


@pytest.fixture
def performance_monitor(mock_application):
    """Create PerformanceMonitor instance"""
    monitor = PerformanceMonitor(mock_application)
    monitor._start_time = 0
    monitor._metrics = []
    return monitor


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files"""
    return tmp_path
