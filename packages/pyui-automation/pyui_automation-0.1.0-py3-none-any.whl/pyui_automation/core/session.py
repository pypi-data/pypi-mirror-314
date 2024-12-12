from typing import Optional, List
import numpy as np
import subprocess
import psutil
import os
from pathlib import Path

from .config import AutomationConfig
from .factory import BackendFactory, ComponentFactory
from ..elements import UIElement
from ..wait import ElementWaits
from ..backends.base import BaseBackend

class AutomationSession:
    """Main session class for UI Automation"""
    
    def __init__(self, backend: Optional[BaseBackend] = None):
        """Initialize automation session"""
        self.config = AutomationConfig()
        
        # Initialize backend
        self._backend = backend or BackendFactory.create_backend()
        
        # Initialize components
        factory = ComponentFactory()
        self.keyboard = factory.create_keyboard(self._backend)
        self.mouse = factory.create_mouse(self._backend)
        self.ocr = factory.create_ocr_engine()
        self.waits = ElementWaits(self)
        self._visual_tester = None
        
    @property
    def backend(self) -> BaseBackend:
        """Get backend instance"""
        return self._backend

    def find_element(self, by: str, value: str, timeout: float = None) -> Optional[UIElement]:
        """Find UI element using specified strategy"""
        if timeout is None:
            timeout = self.config.timeout
            
        element = self.backend.find_element(by, value, timeout)
        return UIElement(element, self) if element else None

    def find_elements(self, by: str, value: str) -> List[UIElement]:
        """Find all matching UI elements"""
        elements = self.backend.find_elements(by, value)
        return [UIElement(element, self) for element in elements]

    def get_active_window(self) -> Optional[UIElement]:
        """Get currently active window"""
        window = self.backend.get_active_window()
        return UIElement(window, self) if window else None

    def take_screenshot(self, filepath: Optional[str] = None) -> Optional[np.ndarray]:
        """Take screenshot of entire screen"""
        return self.backend.capture_screenshot(filepath)

    @property
    def visual_tester(self):
        """Get or create visual tester"""
        if self._visual_tester is None:
            self._visual_tester = ComponentFactory.create_visual_tester()
        return self._visual_tester

    def init_visual_testing(self, baseline_dir: str):
        """Initialize visual testing with specified baseline directory"""
        self._visual_tester = ComponentFactory.create_visual_tester(baseline_dir)

    def capture_visual_baseline(self, name: str, element: Optional[UIElement] = None):
        """Capture baseline image for visual comparison"""
        if element:
            image = element.capture_screenshot()
        else:
            image = self.take_screenshot()
        self.visual_tester.capture_baseline(name, image)

    def compare_visual(self, name: str, element: Optional[UIElement] = None) -> bool:
        """Compare current visual state with baseline"""
        if element:
            image = element.capture_screenshot()
        else:
            image = self.take_screenshot()
        return self.visual_tester.compare(name, image)

    def verify_visual_hash(self, name: str, element: Optional[UIElement] = None) -> bool:
        """Verify visual state using perceptual hash"""
        if element:
            image = element.capture_screenshot()
        else:
            image = self.take_screenshot()
        return self.visual_tester.verify_hash(name, image)

    def launch_application(self, executable_path: str, args: Optional[List[str]] = None) -> Optional[UIElement]:
        """Launch application and return its main window"""
        try:
            # Start the process
            process = subprocess.Popen(
                [executable_path] + (args or []),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for the process to start
            psutil.Process(process.pid).wait(timeout=self.config.timeout)
            
            # Find the main window
            return self.find_element("process", str(process.pid), timeout=self.config.timeout)
            
        except (subprocess.SubprocessError, psutil.TimeoutExpired) as e:
            raise RuntimeError(f"Failed to launch application: {str(e)}")

    def attach_to_application(self, process_id: int) -> Optional[UIElement]:
        """Attach to existing application and return its main window"""
        try:
            # Verify process exists
            process = psutil.Process(process_id)
            if not process.is_running():
                raise RuntimeError(f"Process {process_id} is not running")
                
            # Find the main window
            return self.find_element("process", str(process_id), timeout=self.config.timeout)
            
        except psutil.NoSuchProcess:
            raise RuntimeError(f"Process {process_id} not found")
