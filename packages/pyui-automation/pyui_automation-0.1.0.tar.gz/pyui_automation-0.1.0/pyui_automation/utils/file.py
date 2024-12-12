import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List

def ensure_dir(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_dir() -> Path:
    """Get temporary directory"""
    return Path(tempfile.gettempdir())

def get_temp_file(suffix: str = '') -> Path:
    """Get temporary file path"""
    return Path(tempfile.mktemp(suffix=suffix))

def safe_remove(path: Path) -> bool:
    """Safely remove file or directory"""
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return True
    except Exception:
        return False

def list_files(directory: Path, pattern: str = '*') -> List[Path]:
    """List files in directory matching pattern"""
    return list(directory.glob(pattern))

def copy_file(src: Path, dst: Path, overwrite: bool = False) -> bool:
    """Copy file with error handling"""
    try:
        if dst.exists() and not overwrite:
            return False
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False

def move_file(src: Path, dst: Path, overwrite: bool = False) -> bool:
    """Move file with error handling"""
    try:
        if dst.exists() and not overwrite:
            return False
        shutil.move(src, dst)
        return True
    except Exception:
        return False

def get_file_size(path: Path) -> Optional[int]:
    """Get file size in bytes"""
    try:
        return path.stat().st_size
    except Exception:
        return None

def is_file_empty(path: Path) -> bool:
    """Check if file is empty"""
    size = get_file_size(path)
    return size == 0 if size is not None else True
