import platform
import os
from typing import Optional, Type

from ..backends.base import BaseBackend
from ..backends.windows import WindowsBackend
from ..backends.linux import LinuxBackend
from ..backends.macos import MacOSBackend

class BackendFactory:
    """Factory class for creating automation backends"""
    
    @staticmethod
    def create_backend(backend_type: Optional[str] = None) -> BaseBackend:
        """Create and return appropriate backend instance"""
        if backend_type is None:
            backend_type = platform.system().lower()

        backend_map = {
            'windows': WindowsBackend,
            'linux': LinuxBackend,
            'darwin': MacOSBackend,
            'macos': MacOSBackend,
        }

        backend_class = backend_map.get(backend_type.lower())
        if not backend_class:
            raise ValueError(f"Unsupported platform: {backend_type}")

        return backend_class()

class ComponentFactory:
    """Factory for creating various automation components"""
    
    @staticmethod
    def create_keyboard(backend: BaseBackend):
        """Create keyboard controller"""
        from ..input import Keyboard
        return Keyboard(backend)

    @staticmethod
    def create_mouse(backend: BaseBackend):
        """Create mouse controller"""
        from ..input import Mouse
        return Mouse(backend)

    @staticmethod
    def create_ocr_engine():
        """Create OCR engine"""
        from ..ocr import OCREngine
        return OCREngine()

    @staticmethod
    def create_visual_tester(baseline_dir: Optional[str] = None):
        """Create visual testing component"""
        from ..visual import VisualTester
        if baseline_dir is None:
            baseline_dir = os.path.join(os.getcwd(), 'visual_baseline')
            os.makedirs(baseline_dir, exist_ok=True)
        return VisualTester(baseline_dir)
