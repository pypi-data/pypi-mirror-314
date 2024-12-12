import pytest
from unittest.mock import MagicMock, patch
from pyui_automation.input import Mouse, Keyboard

# Mock backend for testing
@pytest.fixture
def mock_backend():
    backend = MagicMock()
    # Set default return values
    backend.click.return_value = True
    backend.move_mouse.return_value = True
    backend.mouse_down.return_value = True
    backend.mouse_up.return_value = True
    backend.type_text.return_value = True
    backend.press_key.return_value = True
    backend.release_key.return_value = True
    backend.press_keys.return_value = True
    backend.release_keys.return_value = True
    backend.send_keys.return_value = True
    return backend

# Mouse Tests
def test_click_valid_input(mock_backend):
    mouse = Mouse(mock_backend)
    assert mouse.click(100, 200, "left") is True
    mock_backend.click.assert_called_once_with(100, 200, "left")

def test_click_invalid_button(mock_backend):
    mouse = Mouse(mock_backend)
    with pytest.raises(ValueError, match="Invalid button type"):
        mouse.click(100, 200, "invalid")

def test_click_invalid_coordinates(mock_backend):
    mouse = Mouse(mock_backend)
    with pytest.raises(ValueError, match="Coordinates must be numbers"):
        mouse.click("invalid", 200)

def test_double_click_success(mock_backend):
    mouse = Mouse(mock_backend)
    assert mouse.double_click(100, 200) is True
    assert mock_backend.click.call_count == 2

def test_double_click_first_click_fails(mock_backend):
    mock_backend.click.side_effect = [False, True]
    mouse = Mouse(mock_backend)
    assert mouse.double_click(100, 200) is False
    assert mock_backend.click.call_count == 1

def test_move_valid_coordinates(mock_backend):
    mouse = Mouse(mock_backend)
    assert mouse.move(100, 200) is True
    mock_backend.move_mouse.assert_called_once_with(100, 200)

def test_move_invalid_coordinates(mock_backend):
    mouse = Mouse(mock_backend)
    with pytest.raises(ValueError, match="Coordinates must be numbers"):
        mouse.move("invalid", 200)

def test_drag_success(mock_backend):
    mouse = Mouse(mock_backend)
    assert mouse.drag(100, 200, 300, 400) is True
    mock_backend.move_mouse.assert_called_with(300, 400)
    mock_backend.mouse_down.assert_called_once()
    mock_backend.mouse_up.assert_called_once()

def test_drag_move_fails(mock_backend):
    mock_backend.move_mouse.side_effect = [True, False]
    mouse = Mouse(mock_backend)
    assert mouse.drag(100, 200, 300, 400) is False
    mock_backend.mouse_up.assert_called_once()  # Ensure cleanup

def test_drag_invalid_coordinates(mock_backend):
    mouse = Mouse(mock_backend)
    with pytest.raises(ValueError, match="Coordinates must be numbers"):
        mouse.drag("invalid", 200, 300, 400)

# Keyboard Tests
def test_type_text_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.type_text("Hello World") is True
    mock_backend.type_text.assert_called_once_with("Hello World", 0.0)

def test_type_text_with_interval(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.type_text("Test", 0.1) is True
    mock_backend.type_text.assert_called_once_with("Test", 0.1)

def test_type_text_empty_string(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.type_text("") is True
    mock_backend.type_text.assert_not_called()

def test_type_text_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="Text must be a string"):
        keyboard.type_text(123)

def test_press_key_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.press_key("a") is True
    mock_backend.press_key.assert_called_once_with("a")

def test_press_key_empty_string(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.press_key("") is True
    mock_backend.press_key.assert_not_called()

def test_press_key_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="Key must be a string"):
        keyboard.press_key(123)

def test_release_key_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.release_key("a") is True
    mock_backend.release_key.assert_called_once_with("a")

def test_release_key_empty_string(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.release_key("") is True
    mock_backend.release_key.assert_not_called()

def test_release_key_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="Key must be a string"):
        keyboard.release_key(123)

def test_press_keys_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    result = keyboard.press_keys("ctrl", "c")
    assert result is True
    mock_backend.press_keys.assert_called_once_with("ctrl", "c")

def test_press_keys_empty(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.press_keys() is True
    mock_backend.press_keys.assert_not_called()

def test_press_keys_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="All keys must be strings"):
        keyboard.press_keys("ctrl", 123)

def test_release_keys_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    result = keyboard.release_keys("ctrl", "c")
    assert result is True
    mock_backend.release_keys.assert_called_once_with("ctrl", "c")

def test_release_keys_empty(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.release_keys() is True
    mock_backend.release_keys.assert_not_called()

def test_release_keys_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="All keys must be strings"):
        keyboard.release_keys("ctrl", 123)

def test_send_keys_success(mock_backend):
    keyboard = Keyboard(mock_backend)
    result = keyboard.send_keys("{CTRL}c")
    assert result is True
    mock_backend.send_keys.assert_called_once_with("{CTRL}c")

def test_send_keys_empty(mock_backend):
    keyboard = Keyboard(mock_backend)
    assert keyboard.send_keys("") is True
    mock_backend.send_keys.assert_not_called()

def test_send_keys_invalid_input(mock_backend):
    keyboard = Keyboard(mock_backend)
    with pytest.raises(ValueError, match="Keys must be a string"):
        keyboard.send_keys(123)
