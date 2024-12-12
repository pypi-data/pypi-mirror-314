import pytest
from pyui_automation.utils.validation import (
    validate_type, validate_not_none, validate_string_not_empty,
    validate_number_range, validate_regex, validate_callable,
    validate_iterable, validate_all, validate_any
)

def test_validate_type():
    """Test type validation"""
    assert validate_type("test", str)
    assert validate_type(123, (int, float))
    assert not validate_type("test", int)

def test_validate_not_none():
    """Test None validation"""
    assert validate_not_none("test")
    assert validate_not_none(0)
    assert not validate_not_none(None)

def test_validate_string_not_empty():
    """Test string emptiness validation"""
    assert validate_string_not_empty("test")
    assert not validate_string_not_empty("")
    assert not validate_string_not_empty("   ")
    assert not validate_string_not_empty(None)

def test_validate_number_range():
    """Test number range validation"""
    assert validate_number_range(5, min_value=0, max_value=10)
    assert validate_number_range(5, min_value=5)
    assert validate_number_range(5, max_value=5)
    assert not validate_number_range(5, min_value=6)
    assert not validate_number_range(5, max_value=4)

def test_validate_regex():
    """Test regex validation"""
    assert validate_regex("test123", r"^[a-z]+\d+$")
    assert not validate_regex("test", r"^\d+$")
    assert not validate_regex("test", "[")  # Invalid regex

def test_validate_callable():
    """Test callable validation"""
    def test_func():
        pass
    
    assert validate_callable(test_func)
    assert validate_callable(lambda x: x)
    assert not validate_callable("not callable")

def test_validate_iterable():
    """Test iterable validation"""
    assert validate_iterable([1, 2, 3])
    assert validate_iterable("test")
    assert validate_iterable(range(5))
    assert not validate_iterable(123)

def test_validate_all():
    """Test multiple validators (all must pass)"""
    validators = [
        lambda x: isinstance(x, str),
        lambda x: len(x) > 3,
        lambda x: x.startswith('test')
    ]
    
    assert validate_all(validators, "test123")
    assert not validate_all(validators, "te")
    assert not validate_all(validators, "long123")

def test_validate_any():
    """Test multiple validators (any must pass)"""
    validators = [
        lambda x: isinstance(x, int),
        lambda x: isinstance(x, str)
    ]
    
    assert validate_any(validators, 123)
    assert validate_any(validators, "test")
    assert not validate_any(validators, [1, 2, 3])
