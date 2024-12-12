import subprocess
import time
import psutil
import platform
from typing import Optional, Dict, List
import os

class Application:
    """Class for managing desktop applications"""

    def __init__(self, path: str = None, process: psutil.Process = None):
        self.path = path
        self._process = process
        self.platform = platform.system().lower()
        self._window_handle = None
        self._backend = None
        
        # Initialize platform-specific backend
        if self.platform == 'windows':
            from .backends.windows import WindowsBackend
            self._backend = WindowsBackend()
        elif self.platform == 'linux':
            from .backends.linux import LinuxBackend
            self._backend = LinuxBackend()
        elif self.platform == 'darwin':
            from .backends.macos import MacOSBackend
            self._backend = MacOSBackend()

    @property
    def pid(self) -> Optional[int]:
        """Get process ID"""
        return self._process.pid if self._process else None

    @property
    def process(self) -> Optional[psutil.Process]:
        """Get process object"""
        return self._process

    @process.setter
    def process(self, value: psutil.Process):
        """Set process object"""
        self._process = value

    def kill(self):
        """Force kill the application"""
        if self._process:
            self._process.kill()

    @classmethod
    def launch(cls, path: str, args: List[str] = None, cwd: str = None,
               env: Dict[str, str] = None) -> 'Application':
        """Launch a new application"""
        if args is None:
            args = []
        
        try:
            process = subprocess.Popen(
                [path] + args,
                cwd=cwd,
                env=env or os.environ,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True if platform.system().lower() == 'windows' else False
            )
            
            # Wait briefly for process to start
            time.sleep(1.0)  # Increased wait time
            
            # Verify process exists and is running
            if process.poll() is not None:
                raise RuntimeError(f"Process failed to start (exit code: {process.poll()})")
            
            try:
                proc = psutil.Process(process.pid)
                if not proc.is_running():
                    raise RuntimeError("Process started but is not running")
                app = cls(path=path, process=proc)
                # Wait for window to be available
                start_time = time.time()
                while time.time() - start_time < 10:  # Wait up to 10 seconds
                    if app._backend and app._backend.get_window_handle(proc.pid):
                        return app
                    time.sleep(0.5)
                return app
            except psutil.NoSuchProcess:
                raise RuntimeError(f"Process PID not found (pid={process.pid})")
            
        except Exception as e:
            raise RuntimeError(f"Failed to launch application: {str(e)}")

    @classmethod
    def attach(cls, pid_or_name: str) -> Optional['Application']:
        """Attach to an existing application process"""
        # Try to attach by PID first
        try:
            pid = int(pid_or_name)
            try:
                process = psutil.Process(pid)
                return cls(path=process.exe(), process=process)
            except psutil.NoSuchProcess:
                raise ValueError(f"No process found with PID {pid}")
            except psutil.AccessDenied:
                raise ValueError(f"Access denied to process with PID {pid}")
        except ValueError as e:
            # If ValueError was raised by our code, re-raise it
            if "No process found" in str(e) or "Access denied" in str(e):
                raise
            # Otherwise, it's from int() conversion - try to attach by name
            for proc in psutil.process_iter(['name', 'exe']):
                try:
                    if proc.info['name'] == pid_or_name or \
                       (proc.info['exe'] and os.path.basename(proc.info['exe']) == pid_or_name):
                        return cls(path=proc.info['exe'], process=proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            raise ValueError(f"No process found with name {pid_or_name}")

    def terminate(self, timeout: int = 5):
        """Terminate the application"""
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=timeout)
            except psutil.TimeoutExpired:
                self._process.kill()

    def is_running(self) -> bool:
        """Check if the application is running"""
        if self._process:
            return self._process.is_running()
        return False

    def get_memory_usage(self) -> float:
        """Get application memory usage in MB"""
        if self._process:
            return self._process.memory_info().rss / (1024 * 1024)
        return 0.0

    def get_cpu_usage(self) -> float:
        """Get application CPU usage percentage"""
        if self._process:
            return self._process.cpu_percent(interval=0.1)
        return 0.0

    def get_child_processes(self) -> List[psutil.Process]:
        """Get list of child processes"""
        if self._process:
            return self._process.children(recursive=True)
        return []

    def wait_for_window(self, title: str, timeout: float = 10.0) -> Optional[object]:
        """Wait for window with title to appear"""
        if not self._backend:
            return None
            
        start_time = time.time()
        while time.time() - start_time < timeout:
            window = self._backend.find_window(title)
            if window:
                self._window_handle = window.CurrentNativeWindowHandle
                return window
            time.sleep(0.1)
        return None

    def get_window(self, title: str) -> Optional[object]:
        """Get window by title"""
        if not self._backend:
            return None
            
        window = self._backend.find_window(title)
        if window:
            self._window_handle = window.CurrentNativeWindowHandle
        return window

    def get_main_window(self) -> Optional[object]:
        """Get main window of application"""
        if not self._backend:
            return None
            
        window = self._backend.get_active_window()
        if window:
            self._window_handle = window.CurrentNativeWindowHandle
        return window

    def get_window_handles(self) -> List[int]:
        """Get all window handles for application"""
        if not self._backend:
            return []
        return self._backend.get_window_handles()

    def get_active_window(self) -> Optional[object]:
        """Get currently active window"""
        if not self._backend:
            return None
            
        window = self._backend.get_active_window()
        if window:
            self._window_handle = window.CurrentNativeWindowHandle
        return window
