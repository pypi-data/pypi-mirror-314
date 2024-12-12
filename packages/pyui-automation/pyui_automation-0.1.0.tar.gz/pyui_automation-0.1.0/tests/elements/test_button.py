import pytest
from unittest.mock import MagicMock
from pyui_automation.elements.base import UIElement
from pyui_automation.elements.button import Button
from pyui_automation.core.session import AutomationSession

@pytest.fixture
def mock_session():
    session = MagicMock(spec=AutomationSession)
    session.waits = MagicMock()
    session.waits.wait_until = MagicMock(return_value=True)
    return session

@pytest.fixture
def mock_native_element():
    element = MagicMock()
    element.is_enabled.return_value = True
    element.is_displayed.return_value = True
    element.get_property.return_value = False
    return element

@pytest.fixture
def button(mock_session, mock_native_element):
    return Button(mock_native_element, mock_session)

def test_is_pressed(button, mock_native_element):
    """Test checking if button is pressed"""
    assert not button.is_pressed()
    mock_native_element.get_property.assert_called_with('pressed')

def test_wait_until_enabled(button, mock_session):
    """Test waiting for button to be enabled"""
    mock_session.waits.wait_until.return_value = True
    assert button.wait_until_enabled()
    mock_session.waits.wait_until.assert_called_once()

def test_wait_until_clickable(button, mock_session):
    """Test waiting for button to be clickable"""
    mock_session.waits.wait_until.return_value = True
    assert button.wait_until_clickable()
    mock_session.waits.wait_until.assert_called_once()

def test_safe_click_success(button):
    """Test safe click when button is clickable"""
    button.wait_until_clickable = MagicMock(return_value=True)
    button.click = MagicMock()
    
    assert button.safe_click()
    button.wait_until_clickable.assert_called_once()
    button.click.assert_called_once()

def test_safe_click_failure(button):
    """Test safe click when button is not clickable"""
    button.wait_until_clickable = MagicMock(return_value=False)
    button.click = MagicMock()
    
    assert not button.safe_click()
    button.wait_until_clickable.assert_called_once()
    button.click.assert_not_called()
