import cv2
import numpy as np
from typing import Tuple, Optional, List
from pathlib import Path

def load_image(path: str) -> Optional[np.ndarray]:
    """Load image from file"""
    try:
        return cv2.imread(str(path))
    except Exception:
        return None

def save_image(image: np.ndarray, path: str) -> bool:
    """Save image to file"""
    try:
        return cv2.imwrite(str(path), image)
    except Exception:
        return False

def resize_image(image: np.ndarray, width: int = None, height: int = None) -> np.ndarray:
    """Resize image maintaining aspect ratio"""
    if width is None and height is None:
        return image

    h, w = image.shape[:2]
    if width is None:
        aspect = height / h
        width = int(w * aspect)
    elif height is None:
        aspect = width / w
        height = int(h * aspect)

    return cv2.resize(image, (width, height))

def compare_images(img1: np.ndarray, img2: np.ndarray, threshold: float = 0.95) -> bool:
    """Compare two images for similarity"""
    if img1.shape != img2.shape:
        return False
        
    # Convert images to grayscale
    if len(img1.shape) == 3:
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    else:
        img1_gray = img1
        img2_gray = img2
        
    # Calculate mean squared error
    mse = np.mean((img1_gray - img2_gray) ** 2)
    similarity = 1 / (1 + mse)  # Convert MSE to similarity score (0 to 1)
    return similarity >= threshold

def find_template(image: np.ndarray, template: np.ndarray, threshold: float = 0.8) -> List[Tuple[int, int]]:
    """Find template in image using template matching"""
    # Convert images to grayscale
    if len(image.shape) == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    if len(template.shape) == 3:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        template_gray = template

    # Normalize images to improve matching
    image_gray = cv2.normalize(image_gray, None, 0, 255, cv2.NORM_MINMAX)
    template_gray = cv2.normalize(template_gray, None, 0, 255, cv2.NORM_MINMAX)

    # Perform template matching
    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    print("\nTemplate matching result:")
    print("Result shape:", result.shape)
    print("Max correlation:", np.max(result))
    print("Min correlation:", np.min(result))
    
    # Find locations where matching exceeds threshold
    locations = np.where(result >= threshold)
    points = list(zip(*locations[::-1]))  # Convert to (x,y) format
    print(f"Found {len(points)} points above threshold {threshold}")
    
    if not points:
        return []
    
    # Get template dimensions
    h, w = template.shape[:2]
    
    # Convert points to list of matches with scores
    matches = [(x, y, result[y, x]) for x, y in points]
    
    # Sort matches by score in descending order
    matches.sort(key=lambda x: x[2], reverse=True)
    print(f"Top match score: {matches[0][2]}")
    
    # Apply non-maximum suppression
    filtered_matches = []
    
    for x, y, score in matches:
        # Check if this point overlaps with any existing match
        overlap = False
        for fx, fy, _ in filtered_matches:
            # Calculate overlap using center points and template size
            if abs(x - fx) < w//2 and abs(y - fy) < h//2:
                overlap = True
                break
        
        if not overlap:
            filtered_matches.append((x, y, score))
            print(f"Added match at ({x}, {y}) with score {score}")
    
    # Return center points of top matches
    return [(x + w//2, y + h//2) for x, y, _ in filtered_matches]

def non_max_suppression(matches: List[Tuple[int, int]], template_shape: Tuple[int, int], overlap_thresh: float) -> List[Tuple[int, int]]:
    """Remove overlapping matches"""
    if not matches:
        return []
        
    # Convert matches to list of rectangles (x, y, w, h)
    boxes = [(x, y, template_shape[1], template_shape[0]) for x, y in matches]
    
    # Convert to numpy array
    boxes = np.array(boxes)
    
    # Get coordinates
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 0] + boxes[:, 2]
    y2 = boxes[:, 1] + boxes[:, 3]
    
    # Compute area
    area = (x2 - x1) * (y2 - y1)
    
    # Sort by bottom-right y-coordinate
    idxs = np.argsort(y2)
    
    pick = []
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        
        # Find intersection
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        # Compute intersection area
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        overlap = (w * h) / area[idxs[:last]]
        
        # Delete overlapping boxes
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
    
    return [(boxes[i][0], boxes[i][1]) for i in pick]

def highlight_region(image: np.ndarray, x: int, y: int, width: int, height: int,
                    color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
    """Draw rectangle around region of interest"""
    img_copy = image.copy()
    cv2.rectangle(img_copy, (x, y), (x + width, y + height), color, thickness)
    return img_copy

def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """Crop image to specified region"""
    return image[y:y+height, x:x+width]
