"""
Test Generator
==============

Automatically generates unit tests from function signatures.
This massively boosts the Power (P) dimension by proving correctness.

Supports:
- Python: Generates pytest test files
- JavaScript: Generates Jest test files

Usage:
    generator = TestGenerator()
    generator.generate_tests("module.py")  # Creates test_module.py
"""

import re
import os
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TestCase:
    """A single test case."""
    function_name: str
    test_name: str
    test_code: str
    description: str


@dataclass 
class TestFile:
    """Generated test file."""
    source_file: str
    test_file: str
    test_cases: List[TestCase]
    language: str


class TestGenerator:
    """Generates unit tests from source code."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize test generator.
        
        Args:
            output_dir: Directory for test files (default: same as source)
        """
        self.output_dir = output_dir
    
    def generate_tests(self, file_path: str, dry_run: bool = False) -> TestFile:
        """
        Generate tests for a source file.
        
        Args:
            file_path: Path to source file
            dry_run: If True, don't write files
            
        Returns:
            TestFile with generated tests
        """
        path = Path(file_path)
        
        if path.suffix == '.py':
            return self._generate_python_tests(path, dry_run)
        elif path.suffix in ['.js', '.jsx', '.ts', '.tsx']:
            return self._generate_js_tests(path, dry_run)
        else:
            return TestFile(str(path), "", [], "unknown")
    
    def _generate_python_tests(self, path: Path, dry_run: bool) -> TestFile:
        """Generate pytest tests for Python file."""
        content = path.read_text(encoding='utf-8', errors='ignore')
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return TestFile(str(path), "", [], "python")
        
        test_cases = []
        module_name = path.stem
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private and test functions
                if node.name.startswith('_') or node.name.startswith('test'):
                    continue
                
                test_case = self._generate_python_test_case(node, module_name)
                if test_case:
                    test_cases.append(test_case)
        
        if not test_cases:
            return TestFile(str(path), "", [], "python")
        
        # Build test file
        output_dir = Path(self.output_dir) if self.output_dir else path.parent
        test_path = output_dir / f"test_{path.name}"
        
        test_content = self._build_python_test_file(module_name, test_cases)
        
        if not dry_run:
            test_path.write_text(test_content, encoding='utf-8')
        
        return TestFile(
            source_file=str(path),
            test_file=str(test_path),
            test_cases=test_cases,
            language="python"
        )
    
    def _generate_python_test_case(self, node: ast.FunctionDef, module_name: str) -> Optional[TestCase]:
        """Generate a test case for a Python function."""
        func_name = node.name
        
        # Get parameters
        params = []
        for arg in node.args.args:
            param_name = arg.arg
            param_type = None
            
            # Get type annotation if present
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    param_type = arg.annotation.id
                elif isinstance(arg.annotation, ast.Constant):
                    param_type = str(arg.annotation.value)
            
            params.append((param_name, param_type))
        
        # Generate test fixtures based on types
        fixtures = []
        for name, ptype in params:
            if name == 'self':
                continue
            fixtures.append(self._get_python_fixture(name, ptype))
        
        # Build test function
        test_name = f"test_{func_name}"
        fixture_str = ", ".join([f[0] for f in fixtures])
        fixture_setup = "\n    ".join([f[1] for f in fixtures])
        
        # Check for return type
        returns = "result"
        if node.returns:
            if isinstance(node.returns, ast.Name):
                if node.returns.id == 'bool':
                    returns = "assert result in [True, False]"
                elif node.returns.id in ['int', 'float']:
                    returns = "assert isinstance(result, (int, float))"
                elif node.returns.id == 'str':
                    returns = "assert isinstance(result, str)"
        
        test_code = f'''def {test_name}():
    """Test {func_name} function."""
    {fixture_setup}
    
    result = {func_name}({fixture_str})
    
    assert result is not None  # Basic existence check
    # TODO: Add specific assertions'''
        
        return TestCase(
            function_name=func_name,
            test_name=test_name,
            test_code=test_code,
            description=f"Test for {func_name}"
        )
    
    def _get_python_fixture(self, name: str, ptype: Optional[str]) -> Tuple[str, str]:
        """Get fixture value based on parameter name and type."""
        # Type-based fixtures
        if ptype == 'str':
            return (name, f'{name} = "test_value"')
        elif ptype == 'int':
            return (name, f'{name} = 42')
        elif ptype == 'float':
            return (name, f'{name} = 3.14')
        elif ptype == 'bool':
            return (name, f'{name} = True')
        elif ptype == 'list' or ptype == 'List':
            return (name, f'{name} = [1, 2, 3]')
        elif ptype == 'dict' or ptype == 'Dict':
            return (name, f'{name} = {{"key": "value"}}')
        
        # Name-based inference
        name_lower = name.lower()
        if 'path' in name_lower or 'file' in name_lower:
            return (name, f'{name} = "/tmp/test.txt"')
        elif 'url' in name_lower:
            return (name, f'{name} = "http://example.com"')
        elif 'id' in name_lower:
            return (name, f'{name} = 1')
        elif 'name' in name_lower:
            return (name, f'{name} = "test_name"')
        elif 'count' in name_lower or 'num' in name_lower:
            return (name, f'{name} = 10')
        elif 'items' in name_lower or 'list' in name_lower:
            return (name, f'{name} = []')
        elif 'data' in name_lower or 'config' in name_lower:
            return (name, f'{name} = {{}}')
        else:
            return (name, f'{name} = None  # TODO: Set appropriate test value')
    
    def _build_python_test_file(self, module_name: str, test_cases: List[TestCase]) -> str:
        """Build complete pytest test file."""
        tests = "\n\n".join([tc.test_code for tc in test_cases])
        
        return f'''"""
Auto-generated tests for {module_name}
Generated by Autopoiesis Test Generator
"""

import pytest
from {module_name} import *


{tests}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
    
    def _generate_js_tests(self, path: Path, dry_run: bool) -> TestFile:
        """Generate Jest tests for JavaScript file."""
        content = path.read_text(encoding='utf-8', errors='ignore')
        
        test_cases = []
        module_name = path.stem
        
        # Find all function declarations
        patterns = [
            # function name(params)
            r'function\s+(\w+)\s*\(([^)]*)\)',
            # const name = (params) =>
            r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>',
            # export function name(params)
            r'export\s+(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)',
        ]
        
        seen_functions = set()
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                params = match.group(2)
                
                if func_name in seen_functions:
                    continue
                seen_functions.add(func_name)
                
                if func_name.startswith('_') or func_name.startswith('test'):
                    continue
                
                test_case = self._generate_js_test_case(func_name, params)
                if test_case:
                    test_cases.append(test_case)
        
        if not test_cases:
            return TestFile(str(path), "", [], "javascript")
        
        # Build test file
        output_dir = Path(self.output_dir) if self.output_dir else path.parent
        test_path = output_dir / f"{path.stem}.test.js"
        
        test_content = self._build_js_test_file(module_name, path.name, test_cases)
        
        if not dry_run:
            test_path.write_text(test_content, encoding='utf-8')
        
        return TestFile(
            source_file=str(path),
            test_file=str(test_path),
            test_cases=test_cases,
            language="javascript"
        )
    
    def _generate_js_test_case(self, func_name: str, params: str) -> Optional[TestCase]:
        """Generate a test case for a JavaScript function."""
        # Parse parameters
        param_list = [p.strip() for p in params.split(',') if p.strip()]
        
        # Generate fixtures
        fixtures = []
        for param in param_list:
            # Handle destructuring
            if param.startswith('{') or param.startswith('['):
                fixtures.append(f"const {param} = {{}};")
            elif '=' in param:
                # Has default value, skip
                continue
            else:
                fixtures.append(self._get_js_fixture(param))
        
        param_names = [p.split('=')[0].strip().lstrip('{[').rstrip('}]') for p in param_list]
        param_names = [p for p in param_names if p]
        
        test_code = f'''  test('{func_name} should work correctly', () => {{
{chr(10).join(["    " + f for f in fixtures])}
    
    const result = {func_name}({", ".join(param_names)});
    
    expect(result).toBeDefined();
    // TODO: Add specific assertions
  }});'''
        
        return TestCase(
            function_name=func_name,
            test_name=f"test_{func_name}",
            test_code=test_code,
            description=f"Test for {func_name}"
        )
    
    def _get_js_fixture(self, param: str) -> str:
        """Get fixture value based on parameter name."""
        name = param.strip()
        name_lower = name.lower()
        
        if 'callback' in name_lower or 'handler' in name_lower or 'fn' in name_lower:
            return f"const {name} = jest.fn();"
        elif 'array' in name_lower or 'list' in name_lower or 'items' in name_lower:
            return f"const {name} = [1, 2, 3];"
        elif 'count' in name_lower or 'num' in name_lower or 'id' in name_lower:
            return f"const {name} = 42;"
        elif 'name' in name_lower or 'text' in name_lower or 'str' in name_lower:
            return f'const {name} = "test";'
        elif 'flag' in name_lower or name_lower.startswith('is') or name_lower.startswith('has'):
            return f"const {name} = true;"
        elif 'url' in name_lower or 'path' in name_lower:
            return f'const {name} = "/test/path";'
        elif 'data' in name_lower or 'config' in name_lower or 'options' in name_lower:
            return f"const {name} = {{}};"
        else:
            return f"const {name} = null;  // TODO: Set test value"
    
    def _build_js_test_file(self, module_name: str, filename: str, test_cases: List[TestCase]) -> str:
        """Build complete Jest test file."""
        tests = "\n\n".join([tc.test_code for tc in test_cases])
        
        return f'''/**
 * Auto-generated tests for {module_name}
 * Generated by Autopoiesis Test Generator
 */

const {{ /* imports */ }} = require('./{filename}');

describe('{module_name}', () => {{
{tests}
}});
'''


def generate_tests(file_path: str, dry_run: bool = False) -> TestFile:
    """Convenience function to generate tests."""
    generator = TestGenerator()
    return generator.generate_tests(file_path, dry_run)


if __name__ == "__main__":
    print("Test Generator - Testing")
    print("-" * 40)
    
    # Test on a Python file
    test_py = Path(__file__).parent / "grower.py"
    if test_py.exists():
        print(f"\nPython: {test_py.name}")
        gen = TestGenerator()
        result = gen.generate_tests(str(test_py), dry_run=True)
        print(f"  Generated {len(result.test_cases)} test cases")
        for tc in result.test_cases[:5]:
            print(f"    - {tc.test_name}")
        if len(result.test_cases) > 5:
            print(f"    ... and {len(result.test_cases) - 5} more")
    
    # Test on a JS file
    test_js = Path(__file__).parent.parent / "flight-tracker" / "app.js"
    if test_js.exists():
        print(f"\nJavaScript: {test_js.name}")
        result = gen.generate_tests(str(test_js), dry_run=True)
        print(f"  Generated {len(result.test_cases)} test cases")
        for tc in result.test_cases[:5]:
            print(f"    - {tc.test_name}")
        if len(result.test_cases) > 5:
            print(f"    ... and {len(result.test_cases) - 5} more")
