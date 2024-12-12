from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Any


class BaseBackend(ABC):
    """Base class for platform-specific backends"""

    @abstractmethod
    def find_element(self, by: str, value: str) -> Optional[Any]:
        """
        Find a single UI element
        
        Supported strategies:
        - id: Element ID or automation ID
        - name: Element name or title
        - class: Element class name
        - role/control_type: Element role or control type
        - xpath: XPath expression
        - css: CSS selector
        - text: Element text content
        - partial_text: Partial text content
        - ocr_text: Text found using OCR
        - image: Image pattern matching
        """
        pass

    @abstractmethod
    def find_elements(self, by: str, value: str) -> List[Any]:
        """Find multiple UI elements using the same strategies as find_element"""
        pass

    @abstractmethod
    def get_active_window(self) -> Optional[Any]:
        """Get the currently active window"""
        pass

    @abstractmethod
    def take_screenshot(self, filepath: str) -> bool:
        """Take a screenshot"""
        pass

    @abstractmethod
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        pass

    def find_element_by_id(self, id: str) -> Optional[Any]:
        """Find element by ID"""
        return self.find_element("id", id)

    def find_element_by_name(self, name: str) -> Optional[Any]:
        """Find element by name"""
        return self.find_element("name", name)

    def find_element_by_class(self, class_name: str) -> Optional[Any]:
        """Find element by class name"""
        return self.find_element("class", class_name)

    def find_element_by_role(self, role: str) -> Optional[Any]:
        """Find element by role/control type"""
        return self.find_element("role", role)

    def find_element_by_xpath(self, xpath: str) -> Optional[Any]:
        """Find element by XPath"""
        return self.find_element("xpath", xpath)

    def find_element_by_css(self, css: str) -> Optional[Any]:
        """Find element by CSS selector"""
        return self.find_element("css", css)

    def find_element_by_text(self, text: str) -> Optional[Any]:
        """Find element by exact text content"""
        return self.find_element("text", text)

    def find_element_by_partial_text(self, text: str) -> Optional[Any]:
        """Find element by partial text content"""
        return self.find_element("partial_text", text)

    def find_element_by_ocr(self, text: str) -> Optional[Any]:
        """Find element by OCR text recognition"""
        return self.find_element("ocr_text", text)

    def find_element_by_image(self, image_path: str) -> Optional[Any]:
        """Find element by image pattern matching"""
        return self.find_element("image", image_path)
