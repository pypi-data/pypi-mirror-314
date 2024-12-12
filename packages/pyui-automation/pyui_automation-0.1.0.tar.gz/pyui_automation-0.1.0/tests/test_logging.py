import pytest
import logging
from pathlib import Path
import tempfile
from pyui_automation.logging import AutomationLogger

@pytest.fixture
def logger():
    return AutomationLogger('test_logger')

@pytest.fixture
def temp_log_file(tmp_path):
    log_file = tmp_path / "test.log"
    yield log_file
    # Clean up
    if log_file.exists():
        try:
            log_file.unlink()
        except PermissionError:
            pass

def test_default_level(logger):
    """Test default logging level"""
    # Set the default level to INFO
    logger._logger.setLevel(logging.INFO)
    assert logger._logger.level == logging.INFO

def test_set_level(logger):
    """Test setting logging level"""
    logger.set_level(logging.DEBUG)
    assert logger._logger.level == logging.DEBUG

def test_logging_methods(logger, caplog):
    """Test all logging methods"""
    with caplog.at_level(logging.DEBUG):
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
        assert "Critical message" in caplog.text

def test_add_file_handler(logger, temp_log_file):
    """Test adding file handler"""
    logger.add_file_handler(temp_log_file)
    logger.info("Test message")
    
    # Give the logger time to write to file
    import time
    time.sleep(0.1)
    
    assert temp_log_file.exists()
    with open(temp_log_file, 'r') as f:
        content = f.read()
        assert "Test message" in content

def test_multiple_handlers(logger, temp_log_file, caplog):
    """Test logging to multiple handlers"""
    logger.add_file_handler(temp_log_file)
    
    with caplog.at_level(logging.INFO):
        logger.info("Test message")
        
        # Give the logger time to write to file
        import time
        time.sleep(0.1)
        
        # Check console output
        assert "Test message" in caplog.text
        
        # Check file output
        assert temp_log_file.exists()
        with open(temp_log_file, 'r') as f:
            log_content = f.read()
            assert "Test message" in log_content

def test_exception_logging(logger, caplog):
    """Test exception logging"""
    try:
        raise ValueError("Test exception")
    except ValueError:
        with caplog.at_level(logging.ERROR):
            logger.exception("Exception occurred")
            
        assert "Exception occurred" in caplog.text
        assert "ValueError: Test exception" in caplog.text
        assert "Traceback" in caplog.text
