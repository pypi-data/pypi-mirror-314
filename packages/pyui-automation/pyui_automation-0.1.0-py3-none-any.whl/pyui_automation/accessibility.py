from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path
import time
import cv2
import numpy as np
from PIL import Image
import colour


@dataclass
class AccessibilityViolation:
    element: Any
    rule: str
    severity: str
    description: str
    recommendation: str


class AccessibilityChecker:
    """Check application accessibility compliance"""
    
    # Valid ARIA roles from WAI-ARIA specification
    VALID_ROLES = {
        "alert", "alertdialog", "application", "article", "banner", "button", 
        "checkbox", "columnheader", "combobox", "complementary", "contentinfo", 
        "dialog", "directory", "document", "form", "grid", "gridcell", "group", 
        "heading", "img", "link", "list", "listbox", "listitem", "main", "menu", 
        "menubar", "menuitem", "menuitemcheckbox", "menuitemradio", "navigation", 
        "note", "option", "presentation", "progressbar", "radio", "radiogroup", 
        "region", "row", "rowgroup", "rowheader", "scrollbar", "search", 
        "searchbox", "separator", "slider", "spinbutton", "status", "tab", 
        "tablist", "tabpanel", "textbox", "timer", "toolbar", "tooltip", "tree", 
        "treegrid", "treeitem"
    }
    
    # Interactive roles that should be keyboard accessible
    INTERACTIVE_ROLES = {
        "button", "checkbox", "combobox", "link", "menuitem", "menuitemcheckbox",
        "menuitemradio", "option", "radio", "slider", "spinbutton", "tab", 
        "textbox", "treeitem"
    }

    def __init__(self, automation=None):
        """Initialize accessibility checker
        
        Args:
            automation: Optional UIAutomation instance for automation-specific checks
        """
        self.automation = automation
        self.violations: List[AccessibilityViolation] = []

    def check_element(self, element: Any) -> None:
        """Check single element for accessibility issues"""
        # Check for alternative text on images
        if self._is_image_element(element) and not element.get_attribute("alt"):
            self.violations.append(AccessibilityViolation(
                element=element,
                rule="missing_alt_text",
                severity="high",
                description="Image element missing alternative text",
                recommendation="Add descriptive alt text to the image"
            ))

        # Check color contrast
        if self._has_text(element):
            try:
                fg_color = self._get_element_color(element, "color") or (0, 0, 0)
                bg_color = self._get_element_color(element, "background-color") or (255, 255, 255)
                
                contrast = self._calculate_contrast_ratio(fg_color, bg_color)
                if contrast < 4.5:  # WCAG AA standard
                    self.violations.append(AccessibilityViolation(
                        element=element,
                        rule="insufficient_contrast",
                        severity="high",
                        description=f"Insufficient color contrast ratio: {contrast:.1f}:1",
                        recommendation="Increase the color contrast to at least 4.5:1"
                    ))
            except Exception as e:
                # Log error but continue checking other aspects
                print(f"Error checking color contrast: {str(e)}")

        # Check keyboard accessibility
        if self._is_interactive(element) and not element.is_keyboard_accessible():
            self.violations.append(AccessibilityViolation(
                element=element,
                rule="not_keyboard_accessible",
                severity="high",
                description="Interactive element not keyboard accessible",
                recommendation="Ensure the element can be focused and activated with keyboard"
            ))

        # Check ARIA role validity
        if not self._has_valid_role(element):
            self.violations.append(AccessibilityViolation(
                element=element,
                rule="invalid_aria_role",
                severity="medium",
                description=f"Invalid ARIA role: {element.role}",
                recommendation="Use a valid ARIA role from the WAI-ARIA specification"
            ))

    def check_application(self, root_element: Any = None) -> List[AccessibilityViolation]:
        """Check entire application for accessibility issues"""
        self.violations.clear()
        if root_element is None and self.automation:
            root_element = self.automation.get_active_window()
        if root_element:
            elements = self._get_all_elements(root_element)
            for element in elements:
                self.check_element(element)
        return self.violations

    def generate_report(self, output_path: str) -> None:
        """Generate HTML accessibility report"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        violations_html = ""
        
        for v in self.violations:
            element_info = f"Element: {v.element.name if hasattr(v.element, 'name') else 'Unknown'}"
            if hasattr(v.element, 'role'):
                element_info += f" (Role: {v.element.role})"
                
            violations_html += f"""
            <div class="violation {v.severity}">
                <h3>{v.rule}</h3>
                <p><strong>{element_info}</strong></p>
                <p>{v.description}</p>
                <p><em>Recommendation: {v.recommendation}</em></p>
            </div>
            """

        html = f"""
        <html>
        <head>
            <title>Accessibility Report</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 2em;
                    line-height: 1.6;
                }}
                .violation {{
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 1em;
                    margin: 1em 0;
                }}
                .high {{ border-left: 5px solid #dc3545; }}
                .medium {{ border-left: 5px solid #ffc107; }}
                .low {{ border-left: 5px solid #17a2b8; }}
                h1, h2 {{ color: #333; }}
                h3 {{ margin-top: 0; color: #666; }}
            </style>
        </head>
        <body>
            <h1>Accessibility Report</h1>
            <p>Generated on: {timestamp}</p>
            <h2>Found {len(self.violations)} violations</h2>
            {violations_html}
        </body>
        </html>
        """
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    @staticmethod
    def _is_image_element(element: Any) -> bool:
        """Check if element is an image"""
        return element.role == "img" or element.get_attribute("role") == "img"

    @staticmethod
    def _has_text(element: Any) -> bool:
        """Check if element contains text"""
        try:
            if not hasattr(element, "text"):
                return False
            text = element.text
            if not isinstance(text, str):
                return False
            return bool(text.strip())
        except Exception:
            return False

    def _get_element_color(self, element: Any, property: str) -> Optional[Tuple[int, int, int]]:
        """Get element's color as RGB tuple"""
        try:
            # Try to get color from element attribute
            color_str = element.get_attribute(property)
            if not color_str:
                return None
                
            # Handle different color formats
            color_str = color_str.strip().lower()
            
            # Handle hex colors
            if color_str.startswith('#'):
                if len(color_str) == 4:  # Short form #RGB
                    r = int(color_str[1] + color_str[1], 16)
                    g = int(color_str[2] + color_str[2], 16)
                    b = int(color_str[3] + color_str[3], 16)
                elif len(color_str) == 7:  # Full form #RRGGBB
                    r = int(color_str[1:3], 16)
                    g = int(color_str[3:5], 16)
                    b = int(color_str[5:7], 16)
                else:
                    return None
                return (r, g, b)
            
            # Handle rgb/rgba colors
            if color_str.startswith('rgb'):
                values = color_str.split('(')[1].split(')')[0].split(',')
                if len(values) >= 3:
                    r = int(values[0].strip())
                    g = int(values[1].strip())
                    b = int(values[2].strip())
                    return (r, g, b)
            
            # Handle named colors
            named_colors = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                # Add more named colors as needed
            }
            if color_str in named_colors:
                return named_colors[color_str]
                
            return None
            
        except Exception as e:
            print(f"Error parsing color {property}: {str(e)}")
            return None

    def _calculate_contrast_ratio(self, fg_color: Tuple[int, int, int], 
                                bg_color: Tuple[int, int, int]) -> float:
        """Calculate color contrast ratio using WCAG algorithm"""
        try:
            # Convert colors to relative luminance
            fg_luminance = self._get_luminance(fg_color)
            bg_luminance = self._get_luminance(bg_color)
            
            # Calculate contrast ratio
            lighter = max(fg_luminance, bg_luminance)
            darker = min(fg_luminance, bg_luminance)
            
            # WCAG contrast ratio formula: (L1 + 0.05) / (L2 + 0.05)
            ratio = (lighter + 0.05) / (darker + 0.05)
            return float(ratio)  # Ensure we return a float
            
        except Exception as e:
            print(f"Error calculating contrast ratio: {str(e)}")
            return 0.0

    def _get_luminance(self, color: Tuple[int, int, int]) -> float:
        """Calculate relative luminance using WCAG formula"""
        try:
            # Normalize RGB values
            r, g, b = [x / 255.0 for x in color]
            
            # Convert to sRGB
            def to_srgb(c):
                if c <= 0.03928:
                    return c / 12.92
                return ((c + 0.055) / 1.055) ** 2.4
            
            r = to_srgb(r)
            g = to_srgb(g)
            b = to_srgb(b)
            
            # Calculate luminance using WCAG coefficients
            return float(0.2126 * r + 0.7152 * g + 0.0722 * b)
            
        except Exception as e:
            print(f"Error calculating luminance: {str(e)}")
            return 0.0

    @staticmethod
    def _is_interactive(element: Any) -> bool:
        """Check if element is interactive"""
        return element.role in AccessibilityChecker.INTERACTIVE_ROLES

    @staticmethod
    def _has_valid_role(element: Any) -> bool:
        """Check if element has valid ARIA role"""
        return element.role in AccessibilityChecker.VALID_ROLES

    def _get_all_elements(self, root_element: Any) -> List[Any]:
        """Get all elements in application"""
        return root_element.find_elements("*")
