import cv2
import numpy as np
from PIL import Image
import logging

try:
    from paddleocr import PaddleOCR
    HAS_PADDLE = True
except ImportError:
    HAS_PADDLE = False
    logging.warning("PaddleOCR not available. OCR functionality will be limited.")

class OCREngine:
    def __init__(self):
        self._paddle_ocr = None
        if HAS_PADDLE:
            try:
                self._paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
            except Exception as e:
                logging.error(f"Failed to initialize PaddleOCR: {e}")

    def recognize_text(self, image_path, preprocess=False):
        """Recognize text in an image"""
        if not HAS_PADDLE or self._paddle_ocr is None:
            raise RuntimeError("PaddleOCR not available")

        if isinstance(image_path, str):
            image = Image.open(image_path)
            image = np.array(image)
        else:
            image = image_path
            
        if preprocess:
            image = self._preprocess_image(image)

        result = self._paddle_ocr.ocr(image, cls=True)
        if not result or not result[0]:
            return ""
            
        return " ".join(line[1][0] for line in result[0])

    def _preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilation = cv2.dilate(thresh, kernel, iterations=1)

        return dilation

    def read_text_from_element(self, element, preprocess=False):
        """Read text from a UI element"""
        image = element.capture()
        return self.recognize_text(image, preprocess=preprocess)

    def find_text_location(self, element, text, confidence_threshold=0.5):
        """Find location of text within element"""
        if not HAS_PADDLE or self._paddle_ocr is None:
            raise RuntimeError("PaddleOCR not available")

        image = element.capture()
        result = self._paddle_ocr.ocr(image, cls=True)
        
        if not result or not result[0]:
            return None

        element_x, element_y = element.get_location()
        
        for line in result[0]:
            bbox, (detected_text, confidence) = line
            if detected_text == text and confidence >= confidence_threshold:
                # Calculate center point of the bounding box
                x1, y1 = bbox[0]
                x2, y2 = bbox[2]
                center_x = (x1 + x2) / 2 + element_x
                center_y = (y1 + y2) / 2 + element_y
                return (int(center_x), int(center_y))
        
        return None

    def get_all_text(self, element, confidence_threshold=0.5):
        """Get all text from element with positions"""
        if not HAS_PADDLE or self._paddle_ocr is None:
            raise RuntimeError("PaddleOCR not available")

        image = element.capture()
        result = self._paddle_ocr.ocr(image, cls=True)
        
        if not result or not result[0]:
            return []

        element_x, element_y = element.get_location()
        texts = []
        
        for line in result[0]:
            bbox, (text, confidence) = line
            if confidence >= confidence_threshold:
                x1, y1 = bbox[0]
                x2, y2 = bbox[2]
                center_x = int((x1 + x2) / 2 + element_x)
                center_y = int((y1 + y2) / 2 + element_y)
                texts.append({
                    'text': text,
                    'confidence': confidence,
                    'position': (center_x, center_y)
                })
        
        return texts

    def verify_text_presence(self, element, text, confidence_threshold=0.5):
        """Verify presence of text in element"""
        return self.find_text_location(element, text, confidence_threshold) is not None
