import cv2
import numpy as np
from PIL import Image
import imagehash
from typing import Dict, List, Tuple, Optional, Any
import json
from pathlib import Path
import time
from dataclasses import dataclass


@dataclass
class VisualDifference:
    location: Tuple[int, int]
    size: Tuple[int, int]
    difference_percentage: float
    type: str  # 'added', 'removed', 'changed'
    element: Any = None


class VisualMatcher:
    """Class for visual element matching and comparison"""

    def __init__(self, automation):
        self.automation = automation
        self.similarity_threshold = 0.95

    def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare two images and return similarity score"""
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate similarity score using structural similarity index
        score = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]
        return float(score)

    def find_element(self, template_path: str) -> Optional[Any]:
        """Find element matching the template image"""
        template = cv2.imread(template_path)
        if template is None:
            raise ValueError(f"Could not load template image: {template_path}")
        
        screen = self.automation.capture_screenshot()
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= self.similarity_threshold:
            return self.automation.get_element_at(max_loc)
        return None

    def wait_for_image(self, template: np.ndarray, timeout: int = 10) -> bool:
        """Wait for image to appear on screen"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            screen = self.automation.capture_screenshot()
            if self.compare_images(template, screen) >= self.similarity_threshold:
                return True
            time.sleep(0.5)
        return False

    def verify_visual_state(self, baseline: np.ndarray) -> List[VisualDifference]:
        """Verify current visual state against baseline"""
        current = self.automation.capture_screenshot()
        if current is None:
            return []
            
        # Ensure images are same size
        if current.shape != baseline.shape:
            current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))
            
        # Convert to grayscale
        gray1 = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        differences = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > 100:  # Filter out small differences
                diff_percentage = area / (baseline.shape[0] * baseline.shape[1])
                differences.append(VisualDifference(
                    location=(x, y),
                    size=(w, h),
                    difference_percentage=diff_percentage,
                    type='changed'
                ))
                
        return differences

    def capture_baseline(self, baseline_path: str):
        """Capture baseline screenshot"""
        screen = self.automation.capture_screenshot()
        cv2.imwrite(baseline_path, screen)

    def highlight_differences(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """Create image highlighting differences between two images"""
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        diff = cv2.absdiff(img1, img2)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Create colored mask for differences
        diff_highlight = img1.copy()
        diff_highlight[thresh > 0] = [0, 0, 255]  # Red color for differences
        
        return diff_highlight

    def generate_diff_report(self, baseline: np.ndarray, report_path: str):
        """Generate visual difference report"""
        current = self.automation.capture_screenshot()
        differences = self.verify_visual_state(baseline)
        
        # Create report with highlighted differences
        diff_image = self.highlight_differences(baseline, current)
        
        # Save difference image
        cv2.imwrite(str(Path(report_path).with_suffix('.diff.png')), diff_image)
        
        # Generate HTML report
        html_content = f"""
        <html>
        <head><title>Visual Difference Report</title></head>
        <body>
            <h1>Visual Difference Report</h1>
            <h2>Found {len(differences)} differences</h2>
            <div>
                <h3>Difference Image</h3>
                <img src="{Path(report_path).with_suffix('.diff.png').name}" />
            </div>
            <div>
                <h3>Differences Details</h3>
                <ul>
                    {''.join(f'<li>Difference at {d.location}: {d.difference_percentage:.2f}% different</li>' for d in differences)}
                </ul>
            </div>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)

    def compare_region(self, roi: Tuple[int, int, int, int], template: np.ndarray) -> float:
        """Compare specific region of interest with template
        
        Args:
            roi: Region of interest as (x, y, width, height)
            template: Template image to compare against
            
        Returns:
            Similarity score between 0 and 1
        """
        screen = self.automation.capture_screenshot()
        if screen is None:
            return 0.0
            
        # Extract region of interest
        x, y, w, h = roi
        roi_img = screen[y:y+h, x:x+w]
        
        # Resize template if needed
        if template.shape[:2] != (h, w):
            template = cv2.resize(template, (w, h))
            
        return self.compare_images(roi_img, template)

    def find_multiple_matches(self, template: np.ndarray, threshold: float = None) -> List[Tuple[int, int]]:
        """Find all instances of template in screenshot
        
        Args:
            template: Template image to find
            threshold: Optional override for similarity threshold
            
        Returns:
            List of (x, y) coordinates where template was found
        """
        if threshold is None:
            threshold = self.similarity_threshold
            
        screen = self.automation.capture_screenshot()
        if screen is None:
            return []
            
        # Perform template matching
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        
        # Convert to list of coordinates
        matches = list(zip(*locations[::-1]))
        return matches

    def find_all_matches(self, template: np.ndarray, threshold: float = None) -> List[Tuple[int, int]]:
        """Find all instances of template in screen"""
        if threshold is None:
            threshold = self.similarity_threshold
            
        screen = self.automation.capture_screenshot()
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        
        return list(zip(locations[1], locations[0]))  # Convert to (x, y) coordinates

    def image_similarity_threshold(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate similarity threshold between two images
        
        Args:
            img1: First image
            img2: Second image
            
        Returns:
            Similarity threshold value between 0 and 1
        """
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate MSE (Mean Squared Error)
        mse = np.mean((gray1 - gray2) ** 2)
        
        # Convert MSE to similarity score (0 to 1)
        # Using exponential decay: similarity = e^(-mse/constant)
        # The constant controls how quickly similarity drops with increasing MSE
        constant = 10000  # Adjust this value to control sensitivity
        similarity = np.exp(-mse/constant)
        
        return float(similarity)


class VisualTester:
    """Visual testing functionality"""

    def __init__(self, baseline_dir: Path):
        """Initialize visual tester with baseline directory"""
        if not isinstance(baseline_dir, Path):
            baseline_dir = Path(baseline_dir)
        self.baseline_dir = baseline_dir
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def compare(self, current: np.ndarray, baseline: np.ndarray) -> Dict:
        """Compare current screenshot with baseline"""
        try:
            # Ensure images are same size
            if current.shape != baseline.shape:
                raise ValueError("Image sizes do not match")
            
            # Calculate difference
            diff = cv2.absdiff(current, baseline)
            
            # Calculate difference metrics
            mse = np.mean((diff) ** 2)
            similarity = 1 - (mse / 255)
            
            # Find regions with differences
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Get difference regions
            differences = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                if area > 100:  # Filter out small differences
                    differences.append({
                        'location': (x, y),
                        'size': (w, h),
                        'area': area
                    })
            
            return {
                'similarity': float(similarity),  # Convert to float for serialization
                'differences': differences,
                'match': len(differences) == 0
            }
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise RuntimeError(f"Failed to compare images: {str(e)}")

    def verify_hash(self, current: np.ndarray, baseline: np.ndarray) -> bool:
        """Compare images using perceptual hashing"""
        try:
            # Convert images to grayscale
            current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
            
            # Calculate perceptual hashes
            current_hash = self._calculate_phash(current_gray)
            baseline_hash = self._calculate_phash(baseline_gray)
            
            # Convert boolean arrays to uint8 for hamming distance calculation
            current_bits = current_hash.astype(np.uint8)
            baseline_bits = baseline_hash.astype(np.uint8)
            
            # Calculate hamming distance (number of differing bits)
            hash_diff = np.sum(current_bits != baseline_bits)
            
            # Return True if images are similar enough (threshold can be adjusted)
            # Convert numpy bool to Python bool
            return bool(hash_diff < 20)  # Increased threshold for better tolerance
            
        except Exception as e:
            raise RuntimeError(f"Failed to verify image hash: {str(e)}")

    def _calculate_phash(self, image: np.ndarray) -> np.ndarray:
        """Calculate perceptual hash for image"""
        try:
            # Resize image to 32x32
            image = cv2.resize(image, (32, 32))
            
            # Convert to float and compute DCT
            dct = cv2.dct(np.float32(image))
            
            # Keep only top-left 8x8 (low frequency) coefficients
            dct = dct[:8, :8]
            
            # Calculate median value
            median = np.median(dct)
            
            # Convert to binary hash (boolean array)
            # Normalize DCT coefficients for better hash stability
            dct_normalized = dct / (np.abs(dct).max() + 1e-8)  # Add small epsilon to avoid division by zero
            return dct_normalized > np.median(dct_normalized)
            
        except Exception as e:
            raise RuntimeError(f"Failed to calculate image hash: {str(e)}")
