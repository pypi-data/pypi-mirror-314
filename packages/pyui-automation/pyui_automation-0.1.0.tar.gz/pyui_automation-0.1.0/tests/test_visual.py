import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from PIL import Image
from pyui_automation.visual import VisualMatcher, VisualDifference
import cv2
from pathlib import Path
from pyui_automation.visual import VisualTester

@pytest.fixture
def mock_element():
    """Create a mock UI element for testing"""
    from unittest.mock import MagicMock
    import numpy as np
    
    element = MagicMock()
    element.capture_screenshot = MagicMock(return_value=np.zeros((100, 100, 3), dtype=np.uint8))
    return element


@pytest.fixture
def visual_matcher(mock_element):
    """Create VisualMatcher instance with mock element"""
    matcher = VisualMatcher(mock_element)
    return matcher


@pytest.fixture
def visual_tester(tmp_path):
    return VisualTester(tmp_path)


@pytest.fixture
def sample_images():
    # Create two similar images for testing
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Draw different shapes on images
    cv2.circle(img1, (50, 50), 20, (255, 255, 255), -1)
    cv2.circle(img2, (50, 50), 20, (255, 255, 255), -1)
    cv2.rectangle(img2, (70, 70), (90, 90), (255, 255, 255), -1)  # Additional shape in img2
    
    return img1, img2


def test_compare_images(visual_matcher):
    """Test comparing two images"""
    # Create two similar but slightly different test images
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2[10:20, 10:20] = 255  # Add a white square to create a difference
    
    difference = visual_matcher.compare_images(img1, img2)
    assert isinstance(difference, float)
    assert 0 <= difference <= 1


def test_find_element(visual_matcher, temp_dir):
    """Test finding element by image"""
    template_path = temp_dir / "template.png"
    Image.fromarray(np.zeros((50, 50, 3), dtype=np.uint8)).save(str(template_path))
    
    element = visual_matcher.find_element(str(template_path))
    assert element is not None


def test_wait_for_image(visual_matcher):
    """Test waiting for image to appear"""
    template = np.zeros((50, 50, 3), dtype=np.uint8)
    
    result = visual_matcher.wait_for_image(template, timeout=1)
    assert result is True


def test_verify_visual_state(visual_matcher):
    """Test verifying visual state against baseline"""
    baseline = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Create current image with a clear difference
    current = np.zeros((100, 100, 3), dtype=np.uint8)
    current[10:30, 10:30] = 255  # Create a larger white square
    
    # Mock the capture_screenshot to return our test image
    visual_matcher.automation.capture_screenshot = MagicMock(return_value=current)
    
    differences = visual_matcher.verify_visual_state(baseline)
    assert isinstance(differences, list)
    assert len(differences) > 0
    assert all(isinstance(d, VisualDifference) for d in differences)
    
    # Verify the difference was detected in the correct location
    diff = differences[0]
    assert diff.location == (10, 10)
    assert diff.size == (20, 20)
    assert diff.type == 'changed'


def test_capture_baseline(visual_matcher, temp_dir):
    """Test capturing baseline image"""
    baseline_path = temp_dir / "baseline.png"
    
    visual_matcher.capture_baseline(str(baseline_path))
    assert baseline_path.exists()


def test_highlight_differences(visual_matcher):
    """Test highlighting differences between images"""
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2[10:20, 10:20] = 255  # Create a difference
    
    diff_image = visual_matcher.highlight_differences(img1, img2)
    assert isinstance(diff_image, np.ndarray)
    assert diff_image.shape == (100, 100, 3)


def test_generate_diff_report(visual_matcher, temp_dir):
    """Test generating visual difference report"""
    baseline = np.zeros((100, 100, 3), dtype=np.uint8)
    current = np.zeros((100, 100, 3), dtype=np.uint8)
    current[10:20, 10:20] = 255  # Create a difference
    
    report_path = temp_dir / "visual_diff_report.html"
    visual_matcher.generate_diff_report(baseline, str(report_path))
    
    assert report_path.exists()


def test_image_similarity_threshold(visual_matcher):
    """Test image similarity threshold settings"""
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2[10:20, 10:20] = 255  # Create a difference
    
    threshold = visual_matcher.image_similarity_threshold(img1, img2)
    assert isinstance(threshold, float)
    assert 0 <= threshold <= 1


def test_region_of_interest(visual_matcher):
    """Test comparing specific regions of interest"""
    # Create test image with a region of interest
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[10:60, 10:60] = 255  # Add white square in ROI
    
    # Create template matching the ROI
    template = np.ones((50, 50, 3), dtype=np.uint8) * 255
    
    roi = (10, 10, 50, 50)  # x, y, width, height
    result = visual_matcher.compare_region(roi, template)
    assert isinstance(result, float)
    assert result >= visual_matcher.similarity_threshold


def test_multiple_template_matching(visual_matcher):
    """Test finding multiple instances of a template"""
    template = np.zeros((20, 20, 3), dtype=np.uint8)
    
    matches = visual_matcher.find_all_matches(template)
    assert isinstance(matches, list)
    assert all(isinstance(m, tuple) for m in matches)


def test_visual_tester_init(tmp_path):
    """Test VisualTester initialization"""
    tester = VisualTester(tmp_path)
    assert isinstance(tester.baseline_dir, Path)
    assert tester.baseline_dir.exists()


def test_compare_identical_images(visual_tester):
    """Test comparing identical images"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = visual_tester.compare(img, img)
    
    assert result['match'] is True
    assert result['similarity'] == 1.0
    assert len(result['differences']) == 0


def test_compare_different_images(visual_tester, sample_images):
    """Test comparing different images"""
    img1, img2 = sample_images
    result = visual_tester.compare(img1, img2)
    
    assert result['match'] is False
    assert result['similarity'] < 1.0
    assert len(result['differences']) > 0


def test_compare_different_sizes(visual_tester):
    """Test comparing images of different sizes"""
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((200, 200, 3), dtype=np.uint8)
    
    with pytest.raises(ValueError):
        visual_tester.compare(img1, img2)


def test_verify_hash_identical_images(visual_tester):
    """Test hash verification with identical images"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.circle(img, (50, 50), 20, (255, 255, 255), -1)
    
    assert visual_tester.verify_hash(img, img) is True


def test_verify_hash_similar_images(visual_tester):
    """Test hash verification with similar images"""
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Draw similar but slightly different shapes
    cv2.circle(img1, (50, 50), 20, (255, 255, 255), -1)
    cv2.circle(img2, (51, 51), 20, (255, 255, 255), -1)  # Slightly offset
    
    assert visual_tester.verify_hash(img1, img2) is True  # Should still match due to hash tolerance


def test_verify_hash_different_images(visual_tester, sample_images):
    """Test hash verification with different images"""
    img1, img2 = sample_images
    assert visual_tester.verify_hash(img1, img2) is False


def test_calculate_phash(visual_tester):
    """Test perceptual hash calculation"""
    img = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(img, (50, 50), 20, 255, -1)
    
    hash_result = visual_tester._calculate_phash(img)
    assert isinstance(hash_result, np.ndarray)
    assert hash_result.shape == (8, 8)  # Should be 8x8 binary hash
