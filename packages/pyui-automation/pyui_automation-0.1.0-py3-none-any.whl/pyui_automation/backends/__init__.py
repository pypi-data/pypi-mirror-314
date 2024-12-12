import platform
from typing import Optional

from .base import BaseBackend
from .windows import WindowsBackend
from .linux import LinuxBackend
from .macos import MacOSBackend


def get_backend() -> Optional[BaseBackend]:
    """Get the appropriate backend for the current platform"""
    system = platform.system().lower()
    
    if system == 'windows':
        return WindowsBackend()
    elif system == 'linux':
        return LinuxBackend()
    elif system == 'darwin':
        return MacOSBackend()
    else:
        raise NotImplementedError(f"Platform {system} is not supported")
