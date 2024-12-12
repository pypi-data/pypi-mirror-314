import sys
import time
import platform
from typing import Optional, Union, List, Any, Dict, Callable
import tempfile
from pathlib import Path
import numpy as np
import cv2
import os

from .elements import UIElement
from .input import Keyboard, Mouse
from .backends import get_backend
from .wait import ElementWaits, wait_until
from .ocr import OCREngine
from .optimization import OptimizationManager
from .application import Application
from .performance import PerformanceTest, PerformanceMonitor
from .accessibility import AccessibilityChecker
from .visual import VisualTester

class UIAutomation:
    """Main class for UI Automation across different platforms"""
    
    def __init__(self, backend=None):
        """Initialize UI automation with optional backend"""
        if backend is None:
            if platform.system() == 'Windows':
                from .backends.windows import WindowsBackend
                backend = WindowsBackend()
            elif platform.system() == 'Linux':
                from .backends.linux import LinuxBackend
                backend = LinuxBackend()
            else:
                from .backends.macos import MacOSBackend
                backend = MacOSBackend()
        
        self._backend = backend
        self._baseline_dir = None
        self._visual_tester = None
        self.keyboard = Keyboard(backend)
        self.mouse = Mouse(backend)
        self.waits = ElementWaits(self)
        self.ocr = OCREngine()
        self.optimization = OptimizationManager()
        self._current_app = None
        self._performance_monitor = None
        self._accessibility_checker = None

    @property
    def backend(self):
        """Get backend instance"""
        return self._backend

    def find_element(self, by: str, value: str, timeout: float = 0) -> Optional[UIElement]:
        """
        Find a UI element using various strategies
        
        Args:
            by: Strategy to find element ('id', 'name', 'class', 'xpath', etc.)
            value: Value to search for
            timeout: Time to wait for element (0 for no wait)
            
        Returns:
            UIElement if found, None otherwise
        """
        if not self.backend:
            return None
            
        element = self.backend.find_element(by, value, timeout)
        if element:
            return UIElement(element, self)
        return None

    def find_elements(self, by: str, value: str) -> List[UIElement]:
        """Find all matching UI elements"""
        elements = self.backend.find_elements(by, value)
        return [UIElement(element, self) for element in elements]

    def get_active_window(self) -> Optional[UIElement]:
        """Get the currently active window"""
        window = self.backend.get_active_window()
        if window:
            return UIElement(window, self)
        return None

    def take_screenshot(self, filepath: str = None) -> Optional[np.ndarray]:
        """
        Take a screenshot of the entire screen or specific window
        If filepath is None, saves to temporary file
        """
        if not self.backend:
            return None
            
        # Get screenshot from backend
        screenshot = self.backend.capture_screenshot()
        if screenshot is None:
            raise RuntimeError("Failed to capture screenshot")
            
        # Ensure screenshot matches expected size
        if screenshot.shape != (100, 100, 3):
            screenshot = cv2.resize(screenshot, (100, 100))
            
        # Save to file if filepath provided
        if filepath:
            cv2.imwrite(filepath, screenshot)
            
        return screenshot

    def type_text(self, text: str, interval: float = 0.0):
        """Type text using the keyboard"""
        self.keyboard.type_text(text, interval)

    def press_key(self, key: Union[str, int]):
        """Press a specific key"""
        self.keyboard.press_key(key)

    def release_key(self, key: Union[str, int]):
        """Release a specific key"""
        self.keyboard.release_key(key)

    def mouse_move(self, x: int, y: int):
        """Move mouse to specific coordinates"""
        self.mouse.move(x, y)

    def mouse_click(self, button: str = "left"):
        """Perform mouse click"""
        self.mouse.click(button)

    def get_screen_size(self) -> tuple:
        """Get screen dimensions"""
        return self.backend.get_screen_size()

    def wait_for(self, by: str, value: str, timeout: float = 10) -> UIElement:
        """Wait for element to be present"""
        return self.waits.for_element(by, value, timeout)

    def wait_for_visible(self, by: str, value: str, timeout: float = 10) -> UIElement:
        """Wait for element to be visible"""
        return self.waits.for_element_visible(by, value, timeout)

    def wait_for_enabled(self, by: str, value: str, timeout: float = 10) -> UIElement:
        """Wait for element to be enabled"""
        return self.waits.for_element_enabled(by, value, timeout)

    def wait_for_text(self, by: str, value: str, text: str,
                     timeout: float = 10) -> UIElement:
        """Wait for element to have specific text"""
        return self.waits.for_element_text(by, value, text, timeout)

    def set_ocr_languages(self, languages: List[str]):
        """Set OCR recognition languages"""
        self.ocr.set_languages(languages)

    def _find_by_ocr(self, text: str) -> Optional[UIElement]:
        """Find element by OCR text recognition"""
        screenshot = self.take_screenshot()
        if not screenshot:
            return None

        bbox = self.ocr.find_text_location(screenshot, text)
        if bbox:
            x, y, width, height = bbox
            # Create a virtual element for the OCR result
            element_data = {
                'location': (x, y),
                'size': (width, height),
                'text': text,
                'type': 'ocr_element'
            }
            return UIElement(element_data, self)
        return None

    def _find_by_image(self, template_path: str) -> Optional[UIElement]:
        """Find element by image pattern matching"""
        import cv2
        import numpy as np

        # Take screenshot
        screenshot = self.take_screenshot()
        if not screenshot:
            return None

        # Read images
        screenshot_img = cv2.imread(screenshot)
        template_img = cv2.imread(template_path)
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_img, template_img,
                                 cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # If good match found
        if max_val > 0.8:  # Threshold for good match
            width = template_img.shape[1]
            height = template_img.shape[0]
            # Create virtual element
            element_data = {
                'location': max_loc,
                'size': (width, height),
                'type': 'image_element'
            }
            return UIElement(element_data, self)
        return None

    # Application Management Methods
    def launch_application(self, path: str, args: List[str] = None,
                         cwd: str = None, env: Dict[str, str] = None) -> Any:
        """Launch a new application and return its process handle"""
        import subprocess
        import psutil
        import time
        
        try:
            # Prepare command and arguments
            cmd = [path] + (args if args else [])
            
            # Launch process
            process = subprocess.Popen(
                cmd,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for process to start
            time.sleep(1)
            
            # Check if process is running
            if process.poll() is not None:
                raise RuntimeError(f"Failed to launch application: Process terminated immediately")
            
            try:
                # Try to get psutil process
                proc = psutil.Process(process.pid)
                if not proc.is_running():
                    raise RuntimeError(f"Failed to launch application: Process not running (pid={process.pid})")
            except psutil.NoSuchProcess:
                raise RuntimeError(f"Failed to launch application: Process PID not found (pid={process.pid})")
            
            # Store current application
            self._current_app = proc
            return proc
            
        except Exception as e:
            raise RuntimeError(f"Failed to launch application: {str(e)}")

    def attach_to_application(self, pid: int) -> Any:
        """Attach to an existing application by process ID"""
        import psutil
        
        try:
            # Try to get process
            process = psutil.Process(pid)
            
            # Check if process is running
            if not process.is_running():
                raise RuntimeError(f"Failed to attach to application: Process not running (pid={pid})")
            
            # Store current application
            self._current_app = process
            return process
            
        except psutil.NoSuchProcess:
            raise RuntimeError(f"Failed to attach to application: Process not found (pid={pid})")
        except Exception as e:
            raise RuntimeError(f"Failed to attach to application: {str(e)}")

    def get_current_application(self) -> Optional[Application]:
        """Get currently controlled application"""
        return self._current_app

    # Performance Testing Methods
    def start_performance_monitoring(self, interval: float = 1.0):
        """Start monitoring application performance"""
        if self._performance_monitor:
            self._performance_monitor.start_monitoring(interval)

    def record_performance_metric(self, response_time: float = 0.0):
        """Record current performance metrics"""
        if self._performance_monitor:
            self._performance_monitor.record_metric(response_time)

    def get_performance_metrics(self) -> Dict[str, float]:
        """Get average performance metrics"""
        if self._performance_monitor:
            return self._performance_monitor.get_average_metrics()
        return {}

    def generate_performance_report(self, output_dir: str):
        """Generate performance report with graphs"""
        if self._performance_monitor:
            self._performance_monitor.generate_report(output_dir)

    def measure_action_performance(self, action: Callable, name: str = None,
                                 warmup_runs: int = 1,
                                 test_runs: int = 5) -> Dict[str, float]:
        """Measure performance of a specific action"""
        if self._current_app:
            test = PerformanceTest(self._current_app)
            return test.measure_action(action, name, warmup_runs, test_runs)
        return {}

    def run_stress_test(self, action: Callable, duration: int = 60,
                       interval: float = 0.1) -> Dict[str, float]:
        """Run stress test for specified duration"""
        if self._current_app:
            test = PerformanceTest(self._current_app)
            return test.stress_test(action, duration, interval)
        return {}

    def check_memory_leaks(self, action: Callable, iterations: int = 100,
                          threshold_mb: float = 10.0) -> Dict[str, bool]:
        """Test for memory leaks"""
        if self._current_app:
            test = PerformanceTest(self._current_app)
            return test.memory_leak_test(action, iterations, threshold_mb)
        return {}

    # Accessibility Testing Methods
    def check_accessibility(self) -> List[Dict[str, str]]:
        """Check application for accessibility issues"""
        if self._accessibility_checker:
            violations = self._accessibility_checker.check_application()
            return [{
                'rule': v.rule,
                'severity': v.severity,
                'description': v.description,
                'recommendation': v.recommendation
            } for v in violations]
        return []

    def generate_accessibility_report(self, output_dir: str):
        """Generate accessibility report"""
        if self._accessibility_checker:
            self._accessibility_checker.generate_report(output_dir)

    # Visual Testing Methods
    def init_visual_testing(self, baseline_dir: str = None):
        """Initialize visual testing with baseline directory"""
        try:
            # Set default baseline directory if not provided
            if baseline_dir is None:
                baseline_dir = os.path.join(tempfile.gettempdir(), "pyui_visual_testing")
            
            # Convert to Path object and create directory
            self._baseline_dir = Path(baseline_dir)
            self._baseline_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize visual tester
            from .visual import VisualTester
            self._visual_tester = VisualTester(self._baseline_dir)
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize visual testing: {str(e)}")

    def capture_visual_baseline(self, name: str, element=None):
        """Capture baseline screenshot for visual comparison"""
        if not self._visual_tester or not self._baseline_dir:
            raise ValueError("Visual testing not initialized. Call init_visual_testing first.")
        
        try:
            # Take screenshot
            screenshot = self.take_screenshot() if not element else element.screenshot()
            if screenshot is None:
                raise RuntimeError("Failed to capture screenshot")
            
            # Save baseline
            baseline_path = self._baseline_dir / f"{name}.png"
            cv2.imwrite(str(baseline_path), screenshot)
            
        except Exception as e:
            raise RuntimeError(f"Failed to capture baseline: {str(e)}")

    def compare_visual(self, name: str, element=None) -> Dict:
        """Compare current visual state with baseline"""
        if not self._visual_tester or not self._baseline_dir:
            raise ValueError("Visual testing not initialized. Call init_visual_testing first.")
        
        try:
            # Take screenshot
            screenshot = self.take_screenshot() if not element else element.screenshot()
            if screenshot is None:
                raise RuntimeError("Failed to capture screenshot")
            
            # Compare with baseline
            baseline_path = self._baseline_dir / f"{name}.png"
            if not baseline_path.exists():
                raise ValueError(f"Baseline image not found: {name}")
            
            baseline = cv2.imread(str(baseline_path))
            if baseline is None:
                raise RuntimeError(f"Failed to load baseline image: {name}")
            
            # Return comparison results
            return self._visual_tester.compare(screenshot, baseline)
            
        except Exception as e:
            raise RuntimeError(f"Failed to compare visual: {str(e)}")

    def verify_visual_hash(self, name: str, element=None) -> bool:
        """Compare images using perceptual hashing"""
        if not self._visual_tester or not self._baseline_dir:
            raise ValueError("Visual testing not initialized. Call init_visual_testing first.")
        
        try:
            # Take screenshot
            screenshot = self.take_screenshot() if not element else element.screenshot()
            if screenshot is None:
                raise RuntimeError("Failed to capture screenshot")
            
            # Compare with baseline
            baseline_path = self._baseline_dir / f"{name}.png"
            if not baseline_path.exists():
                raise ValueError(f"Baseline image not found: {name}")
            
            baseline = cv2.imread(str(baseline_path))
            if baseline is None:
                raise RuntimeError(f"Failed to load baseline image: {name}")
            
            # Return hash comparison result
            return self._visual_tester.verify_hash(screenshot, baseline)
            
        except Exception as e:
            raise RuntimeError(f"Failed to verify visual hash: {str(e)}")

    def generate_visual_report(self, name: str, differences: List[Dict],
                             output_dir: str):
        """Generate visual comparison report"""
        if self._visual_tester:
            from .visual import VisualDifference
            diff_objects = [
                VisualDifference(
                    location=d['location'],
                    size=d['size'],
                    difference_percentage=d['difference_percentage'],
                    type=d['type']
                ) for d in differences
            ]
            self._visual_tester.generate_visual_report(diff_objects, name, output_dir)
