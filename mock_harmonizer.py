"""
SPDX-License-Identifier: MIT
Mock Harmonizer for Testing

Provides a simple mock implementation of the Python Code Harmonizer
for testing composition logic without real LJPW analysis.
"""

class MockIceComponent:
    def __init__(self, l, j, p, w):
        self.coordinates = type('Coords', (), {'love': l, 'justice': j, 'power': p, 'wisdom': w})()

class MockIceResult:
    def __init__(self, l, j, p, w):
        self.ice_components = {'intent': MockIceComponent(l, j, p, w)}

class PythonCodeHarmonizer:
    def __init__(self, quiet=True):
        pass

    def analyze_file_content(self, content):
        # Simple heuristic based on content to return a profile
        l, j, p, w = 0, 0, 0, 0
        if "def main_simple" in content:
            p = 0.9
            j = 0.1
            l = 0.1
            w = 0.1
        elif "def main_robust" in content:
            p = 0.5
            j = 0.9
            l = 0.9
            w = 0.9
        elif "Justice" in content:
            j = 0.9
            p = 0.5
            w = 0.5
        
        if "Wisdom" in content:
            w = 0.9
        
        if "Love" in content:
            l = 0.9
            
        # Specific overrides for known components if needed
        if "def main_simple" in content:
            p = 0.9
            j = 0.1
            l = 0.1
            w = 0.1
        elif "def main_robust" in content:
            p = 0.5
            j = 0.9
            l = 0.9
            w = 0.9
            
        # Return structure matching what master_grower expects:
        # report[func_name]['ice_result']['ice_components']['intent'].coordinates
        
        # We need to extract the function name to make the key
        import re
        match = re.search(r"def\s+(\w+)\(", content)
        func_name = match.group(1) if match else "unknown"
        
        return {
            func_name: {
                'ice_result': {
                    'ice_components': {
                        'intent': MockIceComponent(l, j, p, w)
                    }
                }
            }
        }
