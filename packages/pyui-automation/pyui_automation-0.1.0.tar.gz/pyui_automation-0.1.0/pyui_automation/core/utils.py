import time
from typing import Callable, Any, Optional
from pathlib import Path
import tempfile
import cv2
import numpy as np

def retry(attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Retry decorator for functions that may fail"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def ensure_dir(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_path(suffix: str = '') -> Path:
    """Get temporary file path"""
    temp_dir = Path(tempfile.gettempdir())
    return temp_dir / f"pyui_automation_{time.time()}{suffix}"

def save_image(image: np.ndarray, filepath: str) -> None:
    """Save image to file"""
    cv2.imwrite(str(filepath), image)

def load_image(filepath: str) -> Optional[np.ndarray]:
    """Load image from file"""
    try:
        return cv2.imread(str(filepath))
    except Exception:
        return None

def compare_images(img1: np.ndarray, img2: np.ndarray, threshold: float = 0.95) -> bool:
    """Compare two images for similarity"""
    if img1.shape != img2.shape:
        return False
    return cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)[0][0] >= threshold
