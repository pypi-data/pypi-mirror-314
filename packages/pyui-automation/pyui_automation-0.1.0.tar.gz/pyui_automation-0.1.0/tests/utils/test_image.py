import pytest
import numpy as np
import cv2
from pathlib import Path
import tempfile
from pyui_automation.utils.image import (
    load_image, save_image, resize_image, compare_images,
    find_template, highlight_region, crop_image
)

@pytest.fixture
def test_image():
    """Create test image"""
    return np.zeros((100, 100, 3), dtype=np.uint8)

@pytest.fixture
def temp_image_path():
    """Create temporary path for image"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        return Path(f.name)

def test_save_load_image(test_image, temp_image_path):
    """Test saving and loading image"""
    assert save_image(test_image, str(temp_image_path))
    loaded = load_image(str(temp_image_path))
    assert np.array_equal(test_image, loaded)
    temp_image_path.unlink()

def test_load_invalid_image():
    """Test loading invalid image"""
    assert load_image('nonexistent.png') is None

def test_resize_image(test_image):
    """Test image resizing"""
    resized = resize_image(test_image, width=50)
    assert resized.shape == (50, 50, 3)
    
    resized = resize_image(test_image, height=50)
    assert resized.shape == (50, 50, 3)

def test_compare_images():
    """Test image comparison"""
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    img3 = np.ones((100, 100, 3), dtype=np.uint8)
    
    assert compare_images(img1, img2)
    assert not compare_images(img1, img3)
    assert not compare_images(img1, np.zeros((50, 50, 3)))

def test_find_template():
    """Test template matching"""
    # Create a test image (100x100) with a distinctive pattern
    image = np.zeros((100, 100), dtype=np.uint8)  # Black background
    # Create a distinctive pattern - a white cross with a dot
    image[20:40, 28:32] = 255  # Vertical line (4 pixels wide)
    image[28:32, 20:40] = 255  # Horizontal line (4 pixels wide)
    image[29:31, 29:31] = 0    # Black dot in center

    # Create the template - same pattern but smaller
    template = np.zeros((20, 20), dtype=np.uint8)  # Black background
    template[4:16, 8:12] = 255  # Vertical line (4 pixels wide)
    template[8:12, 4:16] = 255  # Horizontal line (4 pixels wide)
    template[9:11, 9:11] = 0    # Black dot in center

    # Debug: Print unique values and shapes
    print("\nImage shape:", image.shape)
    print("Image unique values:", np.unique(image))
    print("Template shape:", template.shape)
    print("Template unique values:", np.unique(template))

    # Debug: Print template pattern
    print("\nTemplate pattern:")
    print(template)

    # Debug: Print relevant part of image around expected match
    print("\nImage pattern around center:")
    center_y, center_x = 30, 30
    h, w = template.shape
    roi = image[center_y-h//2:center_y+h//2, center_x-w//2:center_x+w//2]
    print(roi)

    # Find template matches with a lower threshold
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    print("\nMatching scores around center:")
    print(result[center_y-5:center_y+5, center_x-5:center_x+5])
    print("Max matching score:", np.max(result))

    locations = find_template(image, template, threshold=0.6)

    # Should find exactly one match at the center of the cross
    assert len(locations) == 1
    x, y = locations[0]
    # Check if the match is near the center of the cross (30, 30)
    assert abs(x - 30) <= 2 and abs(y - 30) <= 2

    # Test with no matches (using a threshold that's too high)
    locations = find_template(image, template, threshold=0.99)
    assert len(locations) == 0

def test_highlight_region(test_image):
    """Test region highlighting"""
    highlighted = highlight_region(test_image, 10, 10, 20, 20)
    assert not np.array_equal(test_image, highlighted)
    assert highlighted[10, 10:30, 1].any()  # Green channel should have some non-zero values

def test_crop_image(test_image):
    """Test image cropping"""
    cropped = crop_image(test_image, 10, 10, 20, 20)
    assert cropped.shape == (20, 20, 3)
