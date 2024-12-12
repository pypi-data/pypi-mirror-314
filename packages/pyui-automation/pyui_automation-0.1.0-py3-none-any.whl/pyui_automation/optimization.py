import platform
import os
import multiprocessing
from typing import Optional, Dict, Any
import json
import threading
from pathlib import Path


class OptimizationManager:
    """Manages platform-specific optimizations and caching"""

    def __init__(self):
        self.platform = platform.system().lower()
        self.cache_dir = self._get_cache_dir()
        self.element_cache = {}
        self.cache_lock = threading.Lock()
        self._load_cached_data()
        self._configure_platform_optimizations()

    def _get_cache_dir(self) -> Path:
        """Get platform-specific cache directory"""
        if self.platform == 'windows':
            base_dir = os.getenv('LOCALAPPDATA')
        elif self.platform == 'darwin':
            base_dir = os.path.expanduser('~/Library/Caches')
        else:  # Linux
            base_dir = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        
        cache_dir = Path(base_dir) / 'pyui_automation'
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _configure_platform_optimizations(self):
        """Configure platform-specific optimizations"""
        self.optimizations = {
            'use_multiprocessing': multiprocessing.cpu_count() > 1,
            'cache_enabled': True,
            'threading_enabled': True
        }

        if self.platform == 'windows':
            self._configure_windows_optimizations()
        elif self.platform == 'darwin':
            self._configure_macos_optimizations()
        else:  # Linux
            self._configure_linux_optimizations()

    def _configure_windows_optimizations(self):
        """Windows-specific optimizations"""
        import ctypes
        
        # Enable process priority
        try:
            ctypes.windll.kernel32.SetPriorityClass(
                ctypes.windll.kernel32.GetCurrentProcess(),
                0x00008000  # ABOVE_NORMAL_PRIORITY_CLASS
            )
        except Exception:
            pass

        # Enable Windows-specific optimizations
        self.optimizations.update({
            'use_ui_automation_com': True,
            'use_win32_hooks': True,
            'enable_dpi_awareness': True
        })

    def _configure_macos_optimizations(self):
        """macOS-specific optimizations"""
        self.optimizations.update({
            'use_quartz_events': True,
            'enable_accessibility': True,
            'use_native_screenshot': True
        })

    def _configure_linux_optimizations(self):
        """Linux-specific optimizations"""
        self.optimizations.update({
            'use_xdotool': True,
            'enable_compositing': True,
            'use_atspi_cache': True
        })

    def cache_element(self, element_id: str, data: Dict[str, Any],
                     ttl: Optional[int] = 300):
        """Cache element data with optional TTL (in seconds)"""
        with self.cache_lock:
            self.element_cache[element_id] = {
                'data': data,
                'timestamp': time.time(),
                'ttl': ttl
            }
            self._save_cached_data()

    def get_cached_element(self, element_id: str) -> Optional[Dict[str, Any]]:
        """Get cached element data if not expired"""
        with self.cache_lock:
            if element_id in self.element_cache:
                cache_entry = self.element_cache[element_id]
                if cache_entry['ttl'] is None or \
                   time.time() - cache_entry['timestamp'] < cache_entry['ttl']:
                    return cache_entry['data']
                del self.element_cache[element_id]
        return None

    def clear_cache(self):
        """Clear all cached data"""
        with self.cache_lock:
            self.element_cache.clear()
            self._save_cached_data()

    def _load_cached_data(self):
        """Load cached data from disk"""
        cache_file = self.cache_dir / 'element_cache.json'
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    self.element_cache = json.load(f)
        except Exception:
            self.element_cache = {}

    def _save_cached_data(self):
        """Save cached data to disk"""
        cache_file = self.cache_dir / 'element_cache.json'
        try:
            with open(cache_file, 'w') as f:
                json.dump(self.element_cache, f)
        except Exception:
            pass

    def get_optimization(self, key: str) -> Any:
        """Get optimization setting value"""
        return self.optimizations.get(key)

    def set_optimization(self, key: str, value: Any):
        """Set optimization setting value"""
        self.optimizations[key] = value
