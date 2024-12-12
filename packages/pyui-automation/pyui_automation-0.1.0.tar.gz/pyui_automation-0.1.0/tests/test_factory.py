import pytest
from unittest.mock import MagicMock, patch
import platform
import sys
from pyui_automation.core.factory import BackendFactory, ComponentFactory
from pyui_automation.backends.base import BaseBackend
from pyui_automation.input import Keyboard, Mouse
from pyui_automation.visual import VisualTester
import comtypes.client

try:
    from pyui_automation.ocr import OCREngine
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

def is_uiautomation_available():
    """Check if Windows UI Automation is available"""
    if sys.platform != 'win32':
        return False
    try:
        comtypes.client.CreateObject("UIAutomationClient.CUIAutomation")
        return True
    except:
        return False

@pytest.fixture
def mock_backend():
    return MagicMock(spec=BaseBackend)

@pytest.mark.skipif(sys.platform == 'darwin', reason="Test not applicable on macOS")
@pytest.mark.skipif(not is_uiautomation_available(), reason="Windows UI Automation not available")
def test_create_backend_for_current_platform():
    """Test creating backend for current platform"""
    backend = BackendFactory.create_backend()
    assert backend is not None

@pytest.mark.skipif(sys.platform == 'darwin', reason="Test not applicable on macOS")
@pytest.mark.skipif(not is_uiautomation_available(), reason="Windows UI Automation not available")
def test_create_backend_explicit():
    """Test creating backend with explicit type"""
    backend = BackendFactory.create_backend("windows")
    assert backend is not None

def test_create_backend_invalid():
    """Test creating backend with invalid type"""
    with pytest.raises(ValueError):
        BackendFactory.create_backend("invalid")

def test_create_keyboard(mock_backend):
    """Test creating keyboard controller"""
    keyboard = ComponentFactory.create_keyboard(mock_backend)
    assert isinstance(keyboard, Keyboard)

def test_create_mouse(mock_backend):
    """Test creating mouse controller"""
    mouse = ComponentFactory.create_mouse(mock_backend)
    assert isinstance(mouse, Mouse)

@pytest.mark.ocr
@pytest.mark.skipif(not HAS_OCR, reason="OCR dependencies not available")
def test_create_ocr_engine():
    """Test creating OCR engine"""
    ocr = ComponentFactory.create_ocr_engine()
    assert isinstance(ocr, OCREngine)

def test_create_visual_tester():
    """Test creating visual tester"""
    tester = ComponentFactory.create_visual_tester()
    assert isinstance(tester, VisualTester)
