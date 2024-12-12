class AutomationError(Exception):
    """Base exception for UI Automation"""
    pass

class ElementNotFoundError(AutomationError):
    """Raised when element is not found"""
    pass

class ElementStateError(AutomationError):
    """Raised when element is in invalid state"""
    pass

class TimeoutError(AutomationError):
    """Raised when operation times out"""
    pass

class BackendError(AutomationError):
    """Raised when backend operation fails"""
    pass

class ConfigurationError(AutomationError):
    """Raised when configuration is invalid"""
    pass

class ValidationError(AutomationError):
    """Raised when validation fails"""
    pass

class OCRError(AutomationError):
    """Raised when OCR operation fails"""
    pass

class VisualError(AutomationError):
    """Raised when visual operation fails"""
    pass

class InputError(AutomationError):
    """Raised when input operation fails"""
    pass

class WindowError(AutomationError):
    """Raised when window operation fails"""
    pass
