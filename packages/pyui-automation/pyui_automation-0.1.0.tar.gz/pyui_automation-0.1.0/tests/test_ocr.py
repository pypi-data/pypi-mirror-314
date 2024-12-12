import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from typing import List, Tuple

# Mock PIL.Image
pil_mock = MagicMock()
class MockImage:
    @staticmethod
    def fromarray(arr):
        return arr
        
    @staticmethod
    def open(fp):
        # Return a mock image that can be converted to numpy array
        mock_img = MagicMock()
        mock_img.__array__ = lambda: np.zeros((100, 100, 3), dtype=np.uint8)
        return mock_img

# Add the open method directly to the mock module
pil_mock.open = MockImage.open
pil_mock.Image = MockImage

# Mock PaddleOCR
paddle_mock = MagicMock()
class MockPaddleOCR:
    def __init__(self, use_angle_cls=True, lang='en', show_log=False):
        pass
        
    def ocr(self, image, cls=True):
        # Return format: [[[bbox, (text, confidence)], ...]]
        return [[
            [[[0, 0], [100, 0], [100, 30], [0, 30]], ("Sample Text 1", 0.95)],
            [[[0, 40], [100, 40], [100, 70], [0, 70]], ("Sample Text 2", 0.92)]
        ]]

paddle_mock.PaddleOCR = MockPaddleOCR

# Create patch objects
patches = {
    'PIL.Image': patch.dict('sys.modules', {'PIL.Image': pil_mock}),
    'paddleocr': patch.dict('sys.modules', {'paddleocr': paddle_mock})
}

@pytest.fixture
def mock_element():
    """Create a mock UI element for testing"""
    element = MagicMock()
    element.capture.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    element.get_location.return_value = (0, 0)
    return element

@pytest.fixture
def ocr_engine():
    """Create OCREngine instance with mocked PaddleOCR"""
    with patches['PIL.Image'], patches['paddleocr']:
        from pyui_automation.ocr import OCREngine
        global HAS_PADDLE
        HAS_PADDLE = True  # Force PaddleOCR availability
        engine = OCREngine()
        engine._paddle_ocr = MockPaddleOCR()  # Directly set the mock instance
        yield engine

def test_read_text_from_element(ocr_engine, mock_element):
    """Test reading text from UI element"""
    text = ocr_engine.read_text_from_element(mock_element)
    assert text == "Sample Text 1 Sample Text 2"

def test_find_text_location(ocr_engine, mock_element):
    """Test finding text location"""
    location = ocr_engine.find_text_location(mock_element, "Sample Text 1")
    assert location == (50, 15)  # Center point of first bbox

def test_get_all_text(ocr_engine, mock_element):
    """Test getting all text from element"""
    texts = ocr_engine.get_all_text(mock_element)
    assert len(texts) == 2
    assert texts[0] == {
        'text': 'Sample Text 1',
        'confidence': 0.95,
        'position': (50, 15)  # Center of first bbox
    }
    assert texts[1] == {
        'text': 'Sample Text 2',
        'confidence': 0.92,
        'position': (50, 55)  # Center of second bbox
    }

def test_recognize_text(ocr_engine):
    """Test recognizing text from image array"""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    text = ocr_engine.recognize_text(image)
    assert text == "Sample Text 1 Sample Text 2"

def test_recognize_text_with_preprocessing(ocr_engine):
    """Test text recognition with preprocessing"""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    text = ocr_engine.recognize_text(image, preprocess=True)
    assert text == "Sample Text 1 Sample Text 2"

def test_paddle_ocr_not_available():
    """Test behavior when PaddleOCR is not available"""
    with patches['PIL.Image'], patches['paddleocr']:
        # Import and reload to ensure fresh state
        import pyui_automation.ocr
        import sys
        if 'pyui_automation.ocr' in sys.modules:
            del sys.modules['pyui_automation.ocr']
        import pyui_automation.ocr
        
        # Set PaddleOCR as not available
        pyui_automation.ocr.HAS_PADDLE = False
        
        # Create engine and verify it raises error
        engine = pyui_automation.ocr.OCREngine()
        with pytest.raises(RuntimeError, match="PaddleOCR not available"):
            engine.recognize_text(np.zeros((100, 100, 3), dtype=np.uint8))
