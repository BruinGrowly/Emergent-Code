"""
SPDX-License-Identifier: MIT
Harmonizer Integration Module

This module provides a unified interface to the LJPW harmonizer,
attempting to load the real Python Code Harmonizer if available,
or falling back to a mock implementation for testing.

To use the real harmonizer:
1. Clone the Python-Code-Harmonizer repository into this project root
2. Ensure it's named: Python-Code-Harmonizer/ or Python-Code-Harmonizer-main/
3. The harmonizer should have: harmonizer/main.py with PythonCodeHarmonizer class
"""

import sys
import os
from pathlib import Path

# Try to find and load the real harmonizer
project_root = Path(__file__).parent
# Support both directory names for flexibility
harmonizer_path = project_root / 'Python-Code-Harmonizer'
if not harmonizer_path.exists():
    harmonizer_path = project_root / 'Python-Code-Harmonizer-main'

HARMONIZER_AVAILABLE = False
PythonCodeHarmonizer = None

if harmonizer_path.exists():
    sys.path.insert(0, str(harmonizer_path))
    try:
        from harmonizer.main import PythonCodeHarmonizer as RealHarmonizer

        class StringHarmonizer(RealHarmonizer):
            """Wrapper for the real harmonizer that can analyze string content."""
            def analyze_file_content(self, content: str) -> dict:
                tree = self._parse_code_to_ast(content, "string")
                if tree is None:
                    return {}
                return self._analyze_all_functions(tree)

        PythonCodeHarmonizer = StringHarmonizer
        HARMONIZER_AVAILABLE = True
        print("[OK] Real Python Code Harmonizer loaded successfully.")

    except ImportError as e:
        print(f"[WARNING] Failed to load real harmonizer: {e}")
        print("[INFO] Falling back to Mock Harmonizer.")
        HARMONIZER_AVAILABLE = False
else:
    print("[INFO] Python-Code-Harmonizer-main not found.")
    print(f"[INFO] Expected location: {harmonizer_path}")
    print("[INFO] Using Mock Harmonizer.")
    HARMONIZER_AVAILABLE = False


# Mock Harmonizer Implementation
if not HARMONIZER_AVAILABLE:
    class MockIceComponent:
        """Mock ICE component with LJPW coordinates."""
        def __init__(self, l, j, p, w):
            self.coordinates = type('Coords', (), {
                'love': l,
                'justice': j,
                'power': p,
                'wisdom': w
            })()

    class MockIceResult:
        """Mock ICE result structure."""
        def __init__(self, l, j, p, w):
            self.ice_components = {
                'intent': MockIceComponent(l, j, p, w)
            }

    class PythonCodeHarmonizer:
        """
        Mock harmonizer for testing when real harmonizer is unavailable.

        Returns zero profiles for all code to enable testing of composition
        logic without real LJPW analysis.
        """
        def __init__(self, quiet=True):
            self.quiet = quiet
            if not quiet:
                print("[MOCK] Using Mock Harmonizer - all LJPW values will be 0.0")

        def analyze_file_content(self, content):
            """
            Analyze code content and return LJPW profile.

            Mock implementation returns zeros for all dimensions.
            This allows testing composition logic independently of analysis.
            """
            # Extract function name for proper response structure
            import re
            match = re.search(r"def\s+(\w+)\(", content)
            func_name = match.group(1) if match else "unknown"

            # Return zero profile (real harmonizer will provide actual values)
            return {
                func_name: {
                    'ice_result': {
                        'ice_components': {
                            'intent': MockIceComponent(0.0, 0.0, 0.0, 0.0)
                        }
                    }
                }
            }


# Export the harmonizer class and availability flag
__all__ = ['PythonCodeHarmonizer', 'HARMONIZER_AVAILABLE']


# Usage example:
# from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE
#
# harmonizer = PythonCodeHarmonizer()
# if HARMONIZER_AVAILABLE:
#     # Using real harmonizer - get actual LJPW profiles
#     profile = harmonizer.analyze_file_content(code)
# else:
#     # Using mock - composition logic still works with zero profiles
#     profile = harmonizer.analyze_file_content(code)
