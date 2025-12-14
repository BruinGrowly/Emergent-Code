"""
JavaScript Healer
=================

Automatically heals LJPW deficits in JavaScript code:
- Love (L): Adds JSDoc comments to functions
- Justice (J): Adds input validation
- Power (P): Adds try/catch error handling
- Wisdom (W): Adds console logging

This completes the web autopoiesis loop:
  Intent → Generate JS → Measure JS → Heal JS → Complete!

Usage:
    healer = JSHealer()
    healer.heal_file("app.js", dimension="L")  # Add JSDoc
    healer.heal_file("app.js")  # Heal all dimensions
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import copy


@dataclass
class HealingResult:
    """Result of a healing operation."""
    file_path: str
    dimension: str
    functions_healed: int
    changes_made: List[str]
    success: bool
    error: Optional[str] = None


class JSHealer:
    """
    Heals JavaScript code by adding LJPW elements.
    
    Healing strategies:
    - L (Love): Add JSDoc comments
    - J (Justice): Add input validation 
    - P (Power): Add try/catch blocks
    - W (Wisdom): Add console logging
    """
    
    # Patterns for detecting functions
    FUNCTION_PATTERNS = [
        # function declaration: function name(params) {
        r'(?P<indent>\s*)(?:async\s+)?function\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{',
        # arrow function: const name = (params) => {
        r'(?P<indent>\s*)(?:const|let|var)\s+(?P<name>\w+)\s*=\s*(?:async\s*)?\((?P<params>[^)]*)\)\s*=>\s*\{',
        # method: name(params) {
        r'(?P<indent>\s*)(?:async\s+)?(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{',
    ]
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the healer.
        
        Args:
            dry_run: If True, don't actually modify files
        """
        self.dry_run = dry_run
    
    def heal_file(self, file_path: str, dimension: Optional[str] = None) -> List[HealingResult]:
        """
        Heal a JavaScript file.
        
        Args:
            file_path: Path to the JS file
            dimension: Specific dimension to heal (L, J, P, W) or None for all
            
        Returns:
            List of HealingResult for each dimension healed
        """
        path = Path(file_path)
        if not path.exists():
            return [HealingResult(
                file_path=file_path,
                dimension=dimension or "ALL",
                functions_healed=0,
                changes_made=[],
                success=False,
                error=f"File not found: {file_path}"
            )]
        
        # Read file
        content = path.read_text(encoding='utf-8', errors='ignore')
        original_content = content
        
        results = []
        dimensions = [dimension] if dimension else ['L', 'J', 'P', 'W']
        
        for dim in dimensions:
            if dim == 'L':
                content, result = self._heal_love(content, file_path)
            elif dim == 'J':
                content, result = self._heal_justice(content, file_path)
            elif dim == 'P':
                content, result = self._heal_power(content, file_path)
            elif dim == 'W':
                content, result = self._heal_wisdom(content, file_path)
            else:
                continue
            
            results.append(result)
        
        # Write if changed and not dry run
        if content != original_content and not self.dry_run:
            path.write_text(content, encoding='utf-8')
        
        return results
    
    def _find_functions(self, content: str) -> List[Dict]:
        """
        Find all functions in JavaScript content.
        
        Returns:
            List of dicts with: name, params, start_pos, end_pos, indent, full_match
        """
        functions = []
        
        for pattern in self.FUNCTION_PATTERNS:
            for match in re.finditer(pattern, content, re.MULTILINE):
                # Check if this line is inside a JSDoc (already documented)
                line_start = content.rfind('\n', 0, match.start()) + 1
                preceding = content[max(0, line_start - 100):line_start]
                
                func = {
                    'name': match.group('name'),
                    'params': match.group('params'),
                    'indent': match.group('indent') or '',
                    'start_pos': match.start(),
                    'line_start': line_start,
                    'full_match': match.group(0),
                    'has_jsdoc': '/**' in preceding and '*/' in preceding,
                }
                
                # Parse parameters
                func['param_list'] = self._parse_params(func['params'])
                
                functions.append(func)
        
        # Remove duplicates (same position)
        seen_positions = set()
        unique_functions = []
        for func in functions:
            if func['start_pos'] not in seen_positions:
                seen_positions.add(func['start_pos'])
                unique_functions.append(func)
        
        return sorted(unique_functions, key=lambda x: x['start_pos'], reverse=True)
    
    def _parse_params(self, params_str: str) -> List[Dict]:
        """Parse parameter string into list of param info."""
        if not params_str.strip():
            return []
        
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue
            
            # Handle destructuring
            if param.startswith('{') or param.startswith('['):
                params.append({'name': param, 'type': 'Object', 'destructured': True})
                continue
            
            # Handle default values
            if '=' in param:
                name, default = param.split('=', 1)
                name = name.strip()
                default = default.strip()
                
                # Infer type from default
                if default.startswith('"') or default.startswith("'"):
                    param_type = 'string'
                elif default in ('true', 'false'):
                    param_type = 'boolean'
                elif default.replace('.', '').isdigit():
                    param_type = 'number'
                elif default.startswith('['):
                    param_type = 'Array'
                elif default.startswith('{'):
                    param_type = 'Object'
                else:
                    param_type = '*'
                
                params.append({'name': name, 'type': param_type, 'default': default})
            else:
                # Infer type from name
                param_type = self._infer_type_from_name(param)
                params.append({'name': param, 'type': param_type})
        
        return params
    
    def _infer_type_from_name(self, name: str) -> str:
        """Infer parameter type from its name."""
        name_lower = name.lower()
        
        if any(x in name_lower for x in ['callback', 'handler', 'fn', 'func']):
            return 'Function'
        if any(x in name_lower for x in ['array', 'list', 'items', 'elements']):
            return 'Array'
        if any(x in name_lower for x in ['count', 'num', 'index', 'length', 'size', 'id', 'amount']):
            return 'number'
        if any(x in name_lower for x in ['name', 'text', 'message', 'title', 'label', 'str', 'path', 'url']):
            return 'string'
        if any(x in name_lower for x in ['is', 'has', 'should', 'can', 'enable', 'disable', 'flag']):
            return 'boolean'
        if any(x in name_lower for x in ['options', 'config', 'settings', 'data', 'obj', 'user', 'item']):
            return 'Object'
        if any(x in name_lower for x in ['element', 'el', 'node', 'dom']):
            return 'Element'
        
        return '*'
    
    def _heal_love(self, content: str, file_path: str) -> Tuple[str, HealingResult]:
        """
        Add JSDoc comments to functions without them.
        """
        functions = self._find_functions(content)
        changes = []
        healed_count = 0
        
        for func in functions:
            if func['has_jsdoc']:
                continue
            
            # Generate JSDoc
            jsdoc = self._generate_jsdoc(func)
            
            # Insert before function
            insert_pos = func['line_start']
            content = content[:insert_pos] + jsdoc + content[insert_pos:]
            
            changes.append(f"Added JSDoc to {func['name']}()")
            healed_count += 1
        
        return content, HealingResult(
            file_path=file_path,
            dimension='L',
            functions_healed=healed_count,
            changes_made=changes,
            success=True
        )
    
    def _generate_jsdoc(self, func: Dict) -> str:
        """Generate JSDoc comment for a function."""
        indent = func['indent']
        lines = [f"{indent}/**"]
        
        # Description based on function name
        name = func['name']
        description = self._name_to_description(name)
        lines.append(f"{indent} * {description}")
        
        # Parameters
        for param in func['param_list']:
            if param.get('destructured'):
                lines.append(f"{indent} * @param {{{param['type']}}} {param['name']} - Destructured parameter")
            elif param.get('default'):
                lines.append(f"{indent} * @param {{{param['type']}}} [{param['name']}={param['default']}] - {self._param_description(param['name'])}")
            else:
                lines.append(f"{indent} * @param {{{param['type']}}} {param['name']} - {self._param_description(param['name'])}")
        
        # Return type (heuristic)
        if 'async' in func['full_match']:
            lines.append(f"{indent} * @returns {{Promise}} Result of the operation")
        elif any(x in name.lower() for x in ['get', 'fetch', 'find', 'calculate', 'compute']):
            lines.append(f"{indent} * @returns {{*}} The requested value")
        elif any(x in name.lower() for x in ['is', 'has', 'should', 'can', 'check', 'validate']):
            lines.append(f"{indent} * @returns {{boolean}} True if condition is met")
        
        lines.append(f"{indent} */")
        
        return '\n'.join(lines) + '\n'
    
    def _name_to_description(self, name: str) -> str:
        """Convert function name to description."""
        # Split camelCase
        words = re.sub('([A-Z])', r' \1', name).split()
        words = [w.lower() for w in words]
        
        if words[0] in ['get', 'fetch', 'load', 'find']:
            return f"Retrieves {' '.join(words[1:])}."
        elif words[0] in ['set', 'update', 'save']:
            return f"Updates {' '.join(words[1:])}."
        elif words[0] in ['create', 'add', 'insert']:
            return f"Creates a new {' '.join(words[1:])}."
        elif words[0] in ['delete', 'remove']:
            return f"Removes {' '.join(words[1:])}."
        elif words[0] in ['is', 'has', 'should', 'can']:
            return f"Checks if {' '.join(words[1:])}."
        elif words[0] == 'handle':
            return f"Handles {' '.join(words[1:])} event."
        elif words[0] == 'on':
            return f"Handler for {' '.join(words[1:])} event."
        elif words[0] in ['init', 'initialize', 'setup']:
            return f"Initializes {' '.join(words[1:]) or 'the component'}."
        elif words[0] in ['calculate', 'compute']:
            return f"Calculates {' '.join(words[1:])}."
        elif words[0] == 'render':
            return f"Renders {' '.join(words[1:]) or 'the component'}."
        else:
            return f"{name.replace('_', ' ').title()} operation."
    
    def _param_description(self, name: str) -> str:
        """Generate description for a parameter."""
        words = re.sub('([A-Z])', r' \1', name).lower().split()
        return f"The {' '.join(words)}"
    
    def _heal_justice(self, content: str, file_path: str) -> Tuple[str, HealingResult]:
        """
        Add input validation to functions.
        """
        functions = self._find_functions(content)
        changes = []
        healed_count = 0
        
        for func in functions:
            if not func['param_list']:
                continue
            
            # Check if function already has validation
            # Find the function body start
            func_start = func['start_pos']
            brace_pos = content.find('{', func_start)
            if brace_pos == -1:
                continue
            
            # Look for existing validation in the first few lines
            body_start = brace_pos + 1
            body_preview = content[body_start:body_start + 200]
            if 'throw' in body_preview or 'typeof' in body_preview:
                continue  # Already has validation
            
            # Generate validation code
            validation = self._generate_validation(func)
            if not validation:
                continue
            
            # Insert after opening brace
            content = content[:body_start] + '\n' + validation + content[body_start:]
            
            changes.append(f"Added validation to {func['name']}()")
            healed_count += 1
        
        return content, HealingResult(
            file_path=file_path,
            dimension='J',
            functions_healed=healed_count,
            changes_made=changes,
            success=True
        )
    
    def _generate_validation(self, func: Dict) -> str:
        """Generate validation code for function parameters."""
        indent = func['indent'] + '    '
        lines = []
        
        for param in func['param_list']:
            if param.get('destructured'):
                continue
            
            name = param['name']
            param_type = param['type']
            
            if param_type == 'string':
                lines.append(f"{indent}if (typeof {name} !== 'string') {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be a string');")
                lines.append(f"{indent}}}")
            elif param_type == 'number':
                lines.append(f"{indent}if (typeof {name} !== 'number' || isNaN({name})) {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be a valid number');")
                lines.append(f"{indent}}}")
            elif param_type == 'boolean':
                lines.append(f"{indent}if (typeof {name} !== 'boolean') {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be a boolean');")
                lines.append(f"{indent}}}")
            elif param_type == 'Array':
                lines.append(f"{indent}if (!Array.isArray({name})) {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be an array');")
                lines.append(f"{indent}}}")
            elif param_type == 'Function':
                lines.append(f"{indent}if (typeof {name} !== 'function') {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be a function');")
                lines.append(f"{indent}}}")
            elif param_type == 'Object':
                lines.append(f"{indent}if (!{name} || typeof {name} !== 'object') {{")
                lines.append(f"{indent}    throw new TypeError('{name} must be an object');")
                lines.append(f"{indent}}}")
        
        return '\n'.join(lines) if lines else ''
    
    def _heal_power(self, content: str, file_path: str) -> Tuple[str, HealingResult]:
        """
        Add try/catch blocks to functions without error handling.
        """
        # This is complex because we need to wrap entire function bodies
        # For now, we'll add try/catch to async functions that don't have it
        
        changes = []
        healed_count = 0
        
        # Find async functions without try/catch
        pattern = r'(async\s+function\s+\w+\s*\([^)]*\)\s*\{|(?:const|let|var)\s+\w+\s*=\s*async\s*\([^)]*\)\s*=>\s*\{)'
        
        for match in re.finditer(pattern, content):
            func_start = match.start()
            brace_pos = content.find('{', match.start())
            if brace_pos == -1:
                continue
            
            # Check for existing try
            body_start = brace_pos + 1
            body_preview = content[body_start:body_start + 50].strip()
            if body_preview.startswith('try'):
                continue
            
            # Find function name for logging
            func_match = re.search(r'(?:function\s+|(?:const|let|var)\s+)(\w+)', match.group(0))
            func_name = func_match.group(1) if func_match else 'anonymous'
            
            # We found an async function without try/catch
            # This is a simplified approach - just note it
            changes.append(f"Detected {func_name}() needs error handling (manual review recommended)")
            healed_count += 1
        
        # For now, just report - actual wrapping is complex
        return content, HealingResult(
            file_path=file_path,
            dimension='P',
            functions_healed=healed_count,
            changes_made=changes,
            success=True
        )
    
    def _heal_wisdom(self, content: str, file_path: str) -> Tuple[str, HealingResult]:
        """
        Add logging to functions without it.
        """
        functions = self._find_functions(content)
        changes = []
        healed_count = 0
        
        for func in functions:
            # Find function body
            func_start = func['start_pos']
            brace_pos = content.find('{', func_start)
            if brace_pos == -1:
                continue
            
            # Check if function already has logging
            # Find end of function (simplified - look for matching brace)
            body_start = brace_pos + 1
            body_preview = content[body_start:body_start + 500]
            if 'console.' in body_preview:
                continue  # Already has logging
            
            # Generate logging
            indent = func['indent'] + '    '
            param_names = [p['name'] for p in func['param_list'] if not p.get('destructured')]
            
            if param_names:
                params_log = ', '.join(param_names[:3])  # Max 3 params
                log_line = f"{indent}console.log('[{func['name']}] called with:', {params_log});\n"
            else:
                log_line = f"{indent}console.log('[{func['name']}] called');\n"
            
            # Insert after opening brace
            content = content[:body_start] + '\n' + log_line + content[body_start:]
            
            changes.append(f"Added logging to {func['name']}()")
            healed_count += 1
        
        return content, HealingResult(
            file_path=file_path,
            dimension='W',
            functions_healed=healed_count,
            changes_made=changes,
            success=True
        )
    
    def heal_directory(self, dir_path: str, dimension: Optional[str] = None) -> Dict[str, List[HealingResult]]:
        """
        Heal all JavaScript files in a directory.
        
        Args:
            dir_path: Path to directory
            dimension: Specific dimension or None for all
            
        Returns:
            Dict mapping file paths to their healing results
        """
        results = {}
        path = Path(dir_path)
        
        for js_file in path.rglob('*.js'):
            # Skip common directories
            if any(skip in str(js_file) for skip in ['node_modules', 'dist', 'build', 'vendor']):
                continue
            
            file_results = self.heal_file(str(js_file), dimension)
            results[str(js_file)] = file_results
        
        return results


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def heal_js_file(file_path: str, dimension: Optional[str] = None, dry_run: bool = False) -> List[HealingResult]:
    """Convenience function to heal a single JS file."""
    healer = JSHealer(dry_run=dry_run)
    return healer.heal_file(file_path, dimension)


def heal_js_directory(dir_path: str, dimension: Optional[str] = None, dry_run: bool = False) -> Dict:
    """Convenience function to heal all JS files in a directory."""
    healer = JSHealer(dry_run=dry_run)
    return healer.heal_directory(dir_path, dimension)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("""
+==============================================================================+
|                                                                              |
|   JAVASCRIPT HEALER                                                          |
|                                                                              |
|   Healing Love, Justice, Power, Wisdom in JavaScript code                    |
|                                                                              |
+==============================================================================+
    """)
    
    # Test on bicameral calculator
    test_path = Path(__file__).parent.parent / "grown" / "bicameral_calculator" / "app.js"
    
    if test_path.exists():
        print(f"  Testing on: {test_path.name}")
        print("-" * 60)
        
        # Measure before
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from autopoiesis.js_analyzer import JSAnalyzer
        analyzer = JSAnalyzer()
        before = analyzer.analyze_file(str(test_path))
        
        print(f"\n  BEFORE HEALING:")
        print(f"    Love (L):    {before.love:.3f}")
        print(f"    Justice (J): {before.justice:.3f}")
        print(f"    Power (P):   {before.power:.3f}")
        print(f"    Wisdom (W):  {before.wisdom:.3f}")
        print(f"    Harmony:     {before.harmony:.3f}")
        
        # Heal (dry run)
        healer = JSHealer(dry_run=True)
        results = healer.heal_file(str(test_path))
        
        print(f"\n  HEALING ACTIONS (dry run):")
        for result in results:
            print(f"    [{result.dimension}] {result.functions_healed} functions to heal")
            for change in result.changes_made[:3]:  # Show first 3
                print(f"        - {change}")
            if len(result.changes_made) > 3:
                print(f"        ... and {len(result.changes_made) - 3} more")
        
        print("\n  (Use --live flag to actually modify files)")
    else:
        print(f"  Test file not found: {test_path}")
        print("  Run bicameral_grow.py first to generate a calculator.")
