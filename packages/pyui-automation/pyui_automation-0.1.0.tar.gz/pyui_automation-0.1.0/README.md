# PyUI Automation

A powerful, cross-platform Python library for desktop UI testing and automation with advanced features including visual testing, performance monitoring, and accessibility checking.

## Features

- 🖥️ Cross-Platform Support (Windows, Linux, macOS)
- 🔍 Multiple Element Finding Strategies
- 🖱️ Advanced Input Simulation
- 📸 Visual Testing and Comparison
- ⚡ Performance Monitoring and Testing
- ♿ Accessibility Testing
- 🔄 Application Management
- 📊 Comprehensive Reporting

## Quick Start

```python
from pyui_automation import UIAutomation

# Initialize automation
ui = UIAutomation()

# Find and interact with elements
button = ui.find_element(by="name", value="Submit")
button.click()

# Visual testing
ui.take_screenshot("before.png")
button.click()
ui.take_screenshot("after.png")
ui.compare_images("before.png", "after.png", threshold=0.95)

# OCR capabilities
text = ui.recognize_text("screenshot.png")
print(f"Found text: {text}")

# Performance monitoring
with ui.measure_performance() as perf:
    button.click()
print(f"Click took: {perf.duration}ms")

# Accessibility testing
violations = ui.check_accessibility(button)
for v in violations:
    print(f"Violation: {v.description}")
```

## Installation

```bash
# Install required dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Examples

### Finding Elements

```python
# Find by name
element = ui.find_element(by="name", value="Submit")

# Find by ID
element = ui.find_element(by="id", value="submit-button")

# Find by class name
element = ui.find_element(by="class", value="btn-primary")

# Find with timeout
element = ui.find_element(by="name", value="Submit", timeout=10)

# Find multiple elements
elements = ui.find_elements(by="class", value="list-item")
```

### Mouse and Keyboard Input

```python
# Mouse actions
ui.click(x=100, y=200)
ui.double_click(x=100, y=200)
ui.right_click(x=100, y=200)
ui.drag_and_drop(start_x=100, start_y=200, end_x=300, end_y=400)

# Keyboard input
ui.type_text("Hello World")
ui.press_key("enter")
ui.press_keys(["ctrl", "c"])
```

### Visual Testing

```python
# Basic screenshot comparison
ui.take_screenshot("baseline.png")
# ... perform actions ...
ui.take_screenshot("current.png")
diff = ui.compare_images("baseline.png", "current.png")
assert diff.similarity > 0.95

# Region-based comparison
region = (100, 100, 200, 200)  # x, y, width, height
ui.take_screenshot("region.png", region=region)

# With masking
mask = ui.create_mask()
mask.add_region((100, 100, 200, 200))
diff = ui.compare_images("baseline.png", "current.png", mask=mask)
```

### OCR and Text Recognition

```python
# Basic text recognition
text = ui.recognize_text("screenshot.png")

# With region
region = (100, 100, 200, 200)
text = ui.recognize_text("screenshot.png", region=region)

# With confidence threshold
text = ui.recognize_text("screenshot.png", confidence=0.8)

# Find text location
locations = ui.find_text("Submit", "screenshot.png")
for x, y in locations:
    print(f"Found 'Submit' at ({x}, {y})")
```

### Performance Testing

```python
# Basic performance measurement
with ui.measure_performance() as perf:
    button.click()
print(f"Operation took: {perf.duration}ms")

# Custom metrics
with ui.measure_performance() as perf:
    perf.start_metric("database")
    # ... database operations ...
    perf.end_metric("database")
    
    perf.start_metric("rendering")
    # ... rendering operations ...
    perf.end_metric("rendering")

print(f"Database: {perf.get_metric('database')}ms")
print(f"Rendering: {perf.get_metric('rendering')}ms")
```

### Accessibility Testing

```python
# Check single element
violations = ui.check_accessibility(button)

# Check entire window
window = ui.get_active_window()
violations = ui.check_accessibility(window, recursive=True)

# With custom rules
rules = {
    "contrast": {"min_ratio": 4.5},
    "text_size": {"min_size": 12}
}
violations = ui.check_accessibility(button, rules=rules)
```

## Code Coverage

```
---------- coverage: platform win32, python 3.12.0-final-0 -----------
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
pyui_automation/__init__.py                8      0   100%
pyui_automation/accessibility.py         136      8    94%
pyui_automation/application.py           138     62    55%
pyui_automation/backends/__init__.py      14      7    50%
pyui_automation/backends/base.py          33      0   100%
pyui_automation/backends/linux.py         75     58    23%
pyui_automation/backends/macos.py         94     76    19%
pyui_automation/backends/windows.py      218     56    74%
pyui_automation/core.py                  246    246     0%
pyui_automation/core/__init__.py           5      0   100%
pyui_automation/core/config.py            28      0   100%
pyui_automation/core/factory.py           37      2    95%
pyui_automation/core/session.py           74     13    82%
pyui_automation/core/utils.py             36     24    33%
pyui_automation/di.py                     29      0   100%
pyui_automation/elements.py               83     83     0%
pyui_automation/elements/__init__.py       5      0   100%
pyui_automation/elements/base.py          40      3    92%
pyui_automation/elements/button.py        13      0   100%
pyui_automation/elements/input.py         25     11    56%
pyui_automation/elements/window.py        25      0   100%
pyui_automation/exceptions.py             11      0   100%
pyui_automation/input.py                 202    106    48%
pyui_automation/logging.py                39      0   100%
pyui_automation/ocr.py                    79     15    81%
pyui_automation/optimization.py           75     75     0%
pyui_automation/performance.py           142     45    68%
pyui_automation/utils/__init__.py          4      0   100%
pyui_automation/utils/file.py             47     33    30%
pyui_automation/utils/image.py           101     36    64%
pyui_automation/utils/validation.py       31      0   100%
pyui_automation/visual.py                168     25    85%
pyui_automation/wait.py                   44     23    48%
----------------------------------------------------------
TOTAL                                   2305   1007    56%
```

### Coverage Highlights

🟢 **High Coverage (90-100%)**
- Core Components: `exceptions.py`, `logging.py`, `validation.py`, `di.py`
- Base Classes: `backends/base.py`, `elements/button.py`, `elements/window.py`
- Configuration: `core/config.py`, `core/factory.py`
- Accessibility Testing: `accessibility.py` (94%)

🟡 **Medium Coverage (50-89%)**
- Visual Testing: `visual.py` (85%)
- Core Session: `core/session.py` (82%)
- OCR: `ocr.py` (81%)
- Windows Backend: `backends/windows.py` (74%)
- Performance: `performance.py` (68%)
- Image Utils: `utils/image.py` (64%)
- Input Elements: `elements/input.py` (56%)
- Application: `application.py` (55%)

🔴 **Low Coverage (<50%)**
- Core Implementation: `core.py` (0%)
- Elements Base: `elements.py` (0%)
- Optimization: `optimization.py` (0%)
- Platform Backends: `linux.py` (23%), `macos.py` (19%)
- File Utils: `utils/file.py` (30%)
- Core Utils: `core/utils.py` (33%)
- Input Handling: `input.py` (48%), `wait.py` (48%)

### Areas for Improvement
1. Core Implementation (`core.py`, `elements.py`): Need comprehensive test coverage
2. Platform Backends: Improve Linux and macOS testing
3. Input Handling: Add more test cases for input simulation and wait conditions
4. Optimization: Implement test suite for performance optimization module

## Project Structure

```
pyui_automation/
├── core/
│   ├── config.py      # Configuration management
│   ├── factory.py     # Component factories
│   ├── session.py     # Main automation session
│   └── utils.py       # Core utilities
├── elements/
│   ├── base.py        # Base element class
│   ├── window.py      # Window element
│   └── controls/      # UI control elements
├── backends/
│   ├── windows.py     # Windows implementation
│   ├── linux.py       # Linux implementation
│   └── macos.py       # macOS implementation
└── utils/
    ├── image.py       # Image processing
    ├── ocr.py         # Text recognition
    └── performance.py # Performance monitoring
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyui_automation

# Run specific test module
pytest tests/test_visual.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_visual or test_ocr"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure coverage
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
