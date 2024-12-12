from typing import Any, Callable, Optional, Type, Union
import re

def validate_type(value: Any, expected_type: Union[Type, tuple]) -> bool:
    """Validate value type"""
    return isinstance(value, expected_type)

def validate_not_none(value: Any) -> bool:
    """Validate value is not None"""
    return value is not None

def validate_string_not_empty(value: str) -> bool:
    """Validate string is not empty"""
    return bool(value and value.strip())

def validate_number_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None,
                        max_value: Optional[Union[int, float]] = None) -> bool:
    """Validate number is within range"""
    if min_value is not None and value < min_value:
        return False
    if max_value is not None and value > max_value:
        return False
    return True

def validate_regex(value: str, pattern: str) -> bool:
    """Validate string matches regex pattern"""
    try:
        return bool(re.match(pattern, value))
    except re.error:
        return False

def validate_callable(value: Any) -> bool:
    """Validate value is callable"""
    return callable(value)

def validate_iterable(value: Any) -> bool:
    """Validate value is iterable"""
    try:
        iter(value)
        return True
    except TypeError:
        return False

def validate_all(validators: list[Callable[[Any], bool]], value: Any) -> bool:
    """Run multiple validators on value"""
    return all(validator(value) for validator in validators)

def validate_any(validators: list[Callable[[Any], bool]], value: Any) -> bool:
    """Run multiple validators on value, pass if any pass"""
    return any(validator(value) for validator in validators)
