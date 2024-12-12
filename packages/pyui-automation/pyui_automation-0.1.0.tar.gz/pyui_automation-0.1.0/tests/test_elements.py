import pytest
from unittest.mock import MagicMock, patch
from pyui_automation.elements import UIElement

@pytest.fixture
def mock_automation():
    automation = MagicMock()
    automation.mouse = MagicMock()
    automation.keyboard = MagicMock()
    return automation

@pytest.fixture
def mock_element_with_current():
    element = MagicMock()
    # Set default attribute values
    element.text = "test_text"
    element.location = {'x': 10, 'y': 20}
    element.size = {'width': 100, 'height': 100}
    element.is_enabled.return_value = True
    element.is_displayed.return_value = True
    element.get_attribute.return_value = "test_value"
    element.get_property.return_value = "test_property"
    return element

@pytest.fixture
def mock_element_with_get():
    element = MagicMock()
    # Set up method return values
    element.get_attribute.return_value = "test_value"
    element.get_property.return_value = "test_value"
    element.text = "test text"
    element.location = {'x': 30, 'y': 40}
    element.size = {'width': 50, 'height': 60}
    element.is_enabled.return_value = True
    element.is_displayed.return_value = True
    return element

def test_text_with_get_text(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.text == "test text"

def test_text_without_text(mock_automation):
    element = MagicMock()
    element.text = ""
    ui_element = UIElement(element, mock_automation)
    assert ui_element.text == ""

def test_location_with_get_location(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.location == {'x': 30, 'y': 40}

def test_location_without_location(mock_automation):
    element = MagicMock()
    element.location = {'x': 0, 'y': 0}
    ui_element = UIElement(element, mock_automation)
    assert ui_element.location == {'x': 0, 'y': 0}

def test_size_with_get_size(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.size == {'width': 50, 'height': 60}

def test_size_without_size(mock_automation):
    element = MagicMock()
    element.size = {'width': 0, 'height': 0}
    ui_element = UIElement(element, mock_automation)
    assert ui_element.size == {'width': 0, 'height': 0}

def test_is_enabled_with_current(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    assert ui_element.is_enabled()

def test_is_enabled_with_get(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.is_enabled()
    mock_element_with_get.is_enabled.assert_called_once()

def test_is_enabled_without_enabled(mock_automation):
    element = MagicMock()
    element.is_enabled.return_value = False
    ui_element = UIElement(element, mock_automation)
    assert not ui_element.is_enabled()

def test_is_displayed_with_current(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    assert ui_element.is_displayed()

def test_is_displayed_with_get(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.is_displayed()
    mock_element_with_get.is_displayed.assert_called_once()

def test_is_displayed_without_displayed(mock_automation):
    element = MagicMock()
    element.is_displayed.return_value = False
    ui_element = UIElement(element, mock_automation)
    assert not ui_element.is_displayed()

def test_click(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    ui_element.click()
    mock_element_with_current.click.assert_called_once()

def test_right_click(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    ui_element.right_click()
    mock_automation.mouse.right_click.assert_called_once_with(10, 20)

def test_double_click(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    ui_element.double_click()
    mock_automation.mouse.double_click.assert_called_once_with(10, 20)

def test_hover(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    ui_element.hover()
    mock_automation.mouse.move_to.assert_called_once_with(10, 20)

def test_send_keys(mock_element_with_current, mock_automation):
    ui_element = UIElement(mock_element_with_current, mock_automation)
    ui_element.send_keys("test")
    mock_element_with_current.send_keys.assert_called_once_with("test")

def test_get_attribute_with_attribute(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.get_attribute("test_attr") == "test_value"
    mock_element_with_get.get_attribute.assert_called_once_with("test_attr")

def test_get_attribute_without_attribute(mock_automation):
    element = MagicMock()
    element.get_attribute.return_value = None
    ui_element = UIElement(element, mock_automation)
    assert ui_element.get_attribute("test_attr") is None

def test_get_property_with_property(mock_element_with_get, mock_automation):
    ui_element = UIElement(mock_element_with_get, mock_automation)
    assert ui_element.get_property("test_prop") == "test_value"
    mock_element_with_get.get_property.assert_called_once_with("test_prop")

def test_get_property_without_property(mock_automation):
    element = MagicMock()
    element.get_property.return_value = None
    ui_element = UIElement(element, mock_automation)
    assert ui_element.get_property("test_prop") is None
