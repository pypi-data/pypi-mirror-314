from typing import Dict, Any, Optional
from pathlib import Path

class AutomationConfig:
    """Configuration class for UI Automation"""
    
    def __init__(self):
        self._config: Dict[str, Any] = {
            'screenshot_dir': None,
            'timeout': 10,
            'retry_interval': 0.5,
            'screenshot_on_error': True,
            'log_level': 'INFO',
        }

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)

    @property
    def screenshot_dir(self) -> Optional[Path]:
        """Get screenshot directory"""
        dir_path = self._config.get('screenshot_dir')
        return Path(dir_path) if dir_path else None

    @screenshot_dir.setter
    def screenshot_dir(self, path: str) -> None:
        """Set screenshot directory"""
        self._config['screenshot_dir'] = path

    @property
    def timeout(self) -> float:
        """Get default timeout"""
        return float(self._config.get('timeout', 10))

    @timeout.setter
    def timeout(self, value: float) -> None:
        """Set default timeout"""
        self._config['timeout'] = float(value)

    @property
    def retry_interval(self) -> float:
        """Get retry interval"""
        return float(self._config.get('retry_interval', 0.5))

    @retry_interval.setter
    def retry_interval(self, value: float) -> None:
        """Set retry interval"""
        self._config['retry_interval'] = float(value)
