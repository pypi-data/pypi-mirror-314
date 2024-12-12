import pytest
from pathlib import Path
from pyui_automation.core.config import AutomationConfig

@pytest.fixture
def config():
    return AutomationConfig()

def test_default_values(config):
    """Test default configuration values"""
    assert config.get('timeout') == 10
    assert config.get('retry_interval') == 0.5
    assert config.get('screenshot_on_error') is True
    assert config.get('log_level') == 'INFO'

def test_set_get_values(config):
    """Test setting and getting configuration values"""
    config.set('custom_key', 'custom_value')
    assert config.get('custom_key') == 'custom_value'
    assert config.get('non_existent', 'default') == 'default'

def test_screenshot_dir(config):
    """Test screenshot directory property"""
    test_path = str(Path('/test/path'))  # Convert to proper path for platform
    config.screenshot_dir = test_path
    assert isinstance(config.screenshot_dir, Path)
    assert str(config.screenshot_dir) == test_path

def test_timeout(config):
    """Test timeout property"""
    config.timeout = 20.5
    assert config.timeout == 20.5
    assert isinstance(config.timeout, float)

def test_retry_interval(config):
    """Test retry interval property"""
    config.retry_interval = 1.5
    assert config.retry_interval == 1.5
    assert isinstance(config.retry_interval, float)
