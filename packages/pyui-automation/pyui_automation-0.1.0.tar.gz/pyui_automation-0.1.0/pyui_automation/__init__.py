from .core.session import AutomationSession as UIAutomation
from .elements import UIElement, Button, Window, Input
from .utils import *
from .logging import logger
from .exceptions import *
from .di import container

__version__ = "0.1.0"
__all__ = [
    'UIAutomation',
    'UIElement',
    'Button',
    'Window',
    'Input',
    'logger',
    'container'
]
