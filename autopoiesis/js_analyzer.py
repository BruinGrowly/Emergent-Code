"""
JavaScript LJPW Analyzer
========================

Analyzes JavaScript code for Love, Justice, Power, and Wisdom dimensions.

This closes the autopoiesis feedback loop for web applications:
  Intent → Generate JS → Measure JS LJPW → Heal → Complete

LJPW Mapping for JavaScript:
  L (Love):    JSDoc comments, descriptive names, user-friendly messages
  J (Justice): Input validation, type checks, assertions
  P (Power):   try/catch blocks, error handling, defensive coding
  W (Wisdom):  Console logging, modular structure, const/let discipline
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import math


@dataclass
class JSFunction:
    """Represents a parsed JavaScript function with LJPW metrics."""
    name: str
    start_line: int
    end_line: int
    body: str
    
    # Raw metrics
    has_jsdoc: bool = False
    jsdoc_lines: int = 0
    has_validation: bool = False
    validation_count: int = 0
    has_try_catch: bool = False
    try_catch_count: int = 0
    has_logging: bool = False
    logging_count: int = 0
    
    # Computed LJPW
    love: float = 0.0
    justice: float = 0.0
    power: float = 0.0
    wisdom: float = 0.0
    harmony: float = 0.0


@dataclass
class JSFileAnalysis:
    """Analysis results for a single JavaScript file."""
    path: str
    functions: List[JSFunction] = field(default_factory=list)
    
    # Aggregated metrics
    total_lines: int = 0
    total_functions: int = 0
    
    # File-level LJPW
    love: float = 0.0
    justice: float = 0.0
    power: float = 0.0
    wisdom: float = 0.0
    harmony: float = 0.0
    
    # Deficit flags
    L_deficit: bool = False
    J_deficit: bool = False
    P_deficit: bool = False
    W_deficit: bool = False


class JSAnalyzer:
    """
    Analyzes JavaScript code for LJPW dimensions.
    
    Uses regex-based parsing which is more robust for JavaScript than AST
    since JS has many syntax variations and edge cases.
    """
    
    # Thresholds for dimension adequacy
    LOVE_THRESHOLD = 0.3     # 30% of functions should have JSDoc
    JUSTICE_THRESHOLD = 0.3  # 30% should have validation
    POWER_THRESHOLD = 0.3    # 30% should have error handling
    WISDOM_THRESHOLD = 0.3   # 30% should have logging
    
    # Patterns for detection
    PATTERNS = {
        # Function declarations
        'function_declaration': r'function\s+(\w+)\s*\([^)]*\)\s*\{',
        'arrow_function': r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{?',
        'method': r'(\w+)\s*\([^)]*\)\s*\{',
        'class_method': r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{',
        
        # JSDoc (Love)
        'jsdoc': r'/\*\*[\s\S]*?\*/',
        'jsdoc_param': r'@param\s+',
        'jsdoc_returns': r'@returns?\s+',
        'jsdoc_description': r'/\*\*\s*\n?\s*\*\s*[A-Z]',
        
        # Inline comments (Love)
        'inline_comment': r'//\s*[A-Z]',
        
        # Validation (Justice)
        'typeof_check': r'typeof\s+\w+\s*[!=]==?\s*',
        'instanceof_check': r'\w+\s+instanceof\s+\w+',
        'null_check': r'\w+\s*[!=]==?\s*null',
        'undefined_check': r'\w+\s*[!=]==?\s*undefined',
        'optional_chaining': r'\w+\?\.\w+',
        'throw_error': r'throw\s+(?:new\s+)?(?:Error|TypeError|RangeError)',
        'param_validation': r'if\s*\(\s*!?\w+\s*\)',
        
        # Error handling (Power)
        'try_block': r'\btry\s*\{',
        'catch_block': r'\bcatch\s*\([^)]*\)\s*\{',
        'finally_block': r'\bfinally\s*\{',
        'error_callback': r'\.catch\s*\(',
        'null_coalescing': r'\?\?',
        'or_fallback': r'\|\|\s*[\'"\d\[\{]',
        
        # Logging (Wisdom)
        'console_log': r'console\.log\s*\(',
        'console_warn': r'console\.warn\s*\(',
        'console_error': r'console\.error\s*\(',
        'console_info': r'console\.info\s*\(',
        'console_debug': r'console\.debug\s*\(',
        
        # Structure (Wisdom)
        'const_declaration': r'\bconst\s+\w+\s*=',
        'let_declaration': r'\blet\s+\w+\s*=',
        'class_declaration': r'\bclass\s+\w+',
        'export_declaration': r'\bexport\s+(?:default\s+)?(?:const|let|function|class)',
        'import_declaration': r'\bimport\s+',
    }
    
    def __init__(self):
        # Pre-compile patterns
        self.compiled = {
            name: re.compile(pattern, re.MULTILINE)
            for name, pattern in self.PATTERNS.items()
        }
    
    def analyze_file(self, file_path: str) -> JSFileAnalysis:
        """
        Analyze a single JavaScript file.
        
        Args:
            file_path: Path to the .js file
            
        Returns:
            JSFileAnalysis with all metrics
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix not in ['.js', '.jsx', '.ts', '.tsx', '.mjs']:
            raise ValueError(f"Not a JavaScript file: {file_path}")
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        
        analysis = JSFileAnalysis(
            path=str(path),
            total_lines=len(lines)
        )
        
        # Extract and analyze functions
        functions = self._extract_functions(content)
        
        for func in functions:
            self._analyze_function(func, content)
            analysis.functions.append(func)
        
        analysis.total_functions = len(functions)
        
        # If no functions found, analyze the file as a whole
        if len(functions) == 0:
            whole_file_func = JSFunction(
                name='__module__',
                start_line=1,
                end_line=len(lines),
                body=content
            )
            self._analyze_function(whole_file_func, content)
            analysis.functions.append(whole_file_func)
            analysis.total_functions = 1
        
        # Aggregate to file level
        self._aggregate_file_metrics(analysis)
        
        return analysis
    
    def _extract_functions(self, content: str) -> List[JSFunction]:
        """Extract function definitions from JavaScript content."""
        functions = []
        lines = content.split('\n')
        
        # Track JSDoc comments to associate with following functions
        jsdoc_positions = []
        for match in self.compiled['jsdoc'].finditer(content):
            end_pos = match.end()
            # Find line number
            line_num = content[:end_pos].count('\n')
            jsdoc_positions.append((line_num, match.group()))
        
        # Find function declarations
        for pattern_name in ['function_declaration', 'arrow_function']:
            for match in self.compiled[pattern_name].finditer(content):
                start_pos = match.start()
                line_num = content[:start_pos].count('\n')
                func_name = match.group(1)
                
                # Find matching closing brace (simplified)
                body_start = match.end() - 1  # Position of opening brace
                body = self._extract_function_body(content, body_start)
                end_line = line_num + body.count('\n')
                
                # Check for preceding JSDoc
                has_jsdoc = False
                jsdoc_lines = 0
                for jsdoc_line, jsdoc_text in jsdoc_positions:
                    if jsdoc_line == line_num - 1 or jsdoc_line == line_num - jsdoc_text.count('\n') - 1:
                        has_jsdoc = True
                        jsdoc_lines = jsdoc_text.count('\n') + 1
                        break
                
                func = JSFunction(
                    name=func_name,
                    start_line=line_num + 1,
                    end_line=end_line + 1,
                    body=body,
                    has_jsdoc=has_jsdoc,
                    jsdoc_lines=jsdoc_lines
                )
                functions.append(func)
        
        return functions
    
    def _extract_function_body(self, content: str, start_pos: int) -> str:
        """Extract function body by matching braces."""
        if start_pos >= len(content) or content[start_pos] != '{':
            # Arrow function without braces
            # Find end of statement
            end = content.find(';', start_pos)
            if end == -1:
                end = content.find('\n', start_pos)
            if end == -1:
                end = len(content)
            return content[start_pos:end]
        
        depth = 0
        end_pos = start_pos
        
        for i, char in enumerate(content[start_pos:], start_pos):
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end_pos = i + 1
                    break
        
        return content[start_pos:end_pos]
    
    def _analyze_function(self, func: JSFunction, full_content: str):
        """Analyze a function for LJPW metrics."""
        body = func.body
        body_lines = body.count('\n') + 1
        
        # === LOVE (Documentation) ===
        # Already have has_jsdoc from extraction
        inline_comments = len(self.compiled['inline_comment'].findall(body))
        
        love_score = 0.0
        if func.has_jsdoc:
            love_score += 0.5
            # Bonus for @param and @returns
            if self.compiled['jsdoc_param'].search(body) or '@param' in full_content[:full_content.find(body)]:
                love_score += 0.2
            if self.compiled['jsdoc_returns'].search(body) or '@return' in full_content[:full_content.find(body)]:
                love_score += 0.2
        
        # Inline comments add to love
        comment_ratio = inline_comments / max(body_lines, 1)
        love_score += min(0.3, comment_ratio)
        
        func.love = min(1.0, love_score)
        
        # === JUSTICE (Validation) ===
        validation_patterns = [
            'typeof_check', 'instanceof_check', 'null_check', 
            'undefined_check', 'throw_error', 'param_validation'
        ]
        
        validation_count = 0
        for pattern in validation_patterns:
            validation_count += len(self.compiled[pattern].findall(body))
        
        func.validation_count = validation_count
        func.has_validation = validation_count > 0
        
        # Score based on validation density
        validation_ratio = validation_count / max(body_lines / 10, 1)
        func.justice = min(1.0, validation_ratio * 0.5 + (0.5 if validation_count > 0 else 0))
        
        # === POWER (Error Handling) ===
        error_patterns = [
            'try_block', 'catch_block', 'error_callback',
            'null_coalescing', 'or_fallback'
        ]
        
        error_count = 0
        for pattern in error_patterns:
            error_count += len(self.compiled[pattern].findall(body))
        
        func.try_catch_count = error_count
        func.has_try_catch = error_count > 0
        
        # Optional chaining is defensive coding
        optional_chain_count = len(self.compiled['optional_chaining'].findall(body))
        error_count += optional_chain_count
        
        # Score based on error handling presence
        func.power = min(1.0, 0.3 + (0.5 if func.has_try_catch else 0) + (optional_chain_count * 0.05))
        
        # === WISDOM (Logging, Structure) ===
        logging_patterns = [
            'console_log', 'console_warn', 'console_error',
            'console_info', 'console_debug'
        ]
        
        logging_count = 0
        for pattern in logging_patterns:
            logging_count += len(self.compiled[pattern].findall(body))
        
        func.logging_count = logging_count
        func.has_logging = logging_count > 0
        
        # Const discipline
        const_count = len(self.compiled['const_declaration'].findall(body))
        let_count = len(self.compiled['let_declaration'].findall(body))
        total_vars = const_count + let_count
        const_ratio = const_count / max(total_vars, 1)
        
        # Wisdom score
        wisdom_score = 0.3  # Base
        if func.has_logging:
            wisdom_score += 0.3
        wisdom_score += const_ratio * 0.2
        if body_lines > 5:  # Not a one-liner
            wisdom_score += 0.2
        
        func.wisdom = min(1.0, wisdom_score)
        
        # === HARMONY ===
        # Geometric mean of dimensions
        func.harmony = (func.love * func.justice * func.power * func.wisdom) ** 0.25
    
    def _aggregate_file_metrics(self, analysis: JSFileAnalysis):
        """Aggregate function metrics to file level."""
        if not analysis.functions:
            return
        
        # Weight by function size (approximate)
        total_weight = 0
        weighted_L = 0
        weighted_J = 0
        weighted_P = 0
        weighted_W = 0
        
        for func in analysis.functions:
            weight = func.end_line - func.start_line + 1
            total_weight += weight
            weighted_L += func.love * weight
            weighted_J += func.justice * weight
            weighted_P += func.power * weight
            weighted_W += func.wisdom * weight
        
        if total_weight > 0:
            analysis.love = weighted_L / total_weight
            analysis.justice = weighted_J / total_weight
            analysis.power = weighted_P / total_weight
            analysis.wisdom = weighted_W / total_weight
        
        # Harmony is geometric mean
        analysis.harmony = (
            analysis.love * analysis.justice * 
            analysis.power * analysis.wisdom
        ) ** 0.25
        
        # Deficit flags
        analysis.L_deficit = analysis.love < self.LOVE_THRESHOLD
        analysis.J_deficit = analysis.justice < self.JUSTICE_THRESHOLD
        analysis.P_deficit = analysis.power < self.POWER_THRESHOLD
        analysis.W_deficit = analysis.wisdom < self.WISDOM_THRESHOLD
    
    def analyze_directory(self, dir_path: str) -> Dict[str, JSFileAnalysis]:
        """
        Analyze all JavaScript files in a directory.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            Dict mapping file paths to their analyses
        """
        path = Path(dir_path)
        results = {}
        
        for js_file in path.rglob('*.js'):
            # Skip node_modules and common build directories
            if 'node_modules' in str(js_file) or 'dist' in str(js_file):
                continue
            try:
                analysis = self.analyze_file(str(js_file))
                results[str(js_file)] = analysis
            except Exception as e:
                print(f"  Warning: Could not analyze {js_file}: {e}")
        
        return results


def analyze_js_file(file_path: str) -> JSFileAnalysis:
    """Convenience function to analyze a single JS file."""
    analyzer = JSAnalyzer()
    return analyzer.analyze_file(file_path)


def analyze_js_directory(dir_path: str) -> Dict[str, JSFileAnalysis]:
    """Convenience function to analyze a directory of JS files."""
    analyzer = JSAnalyzer()
    return analyzer.analyze_directory(dir_path)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("""
+==============================================================================+
|                                                                              |
|   JAVASCRIPT LJPW ANALYZER                                                   |
|                                                                              |
|   Measuring Love, Justice, Power, Wisdom in JavaScript code                  |
|                                                                              |
+==============================================================================+
    """)
    
    # Test on the bicameral calculator we grew
    test_path = Path(__file__).parent.parent / "grown" / "bicameral_calculator" / "app.js"
    
    if test_path.exists():
        print(f"  Analyzing: {test_path}")
        print("-" * 60)
        
        analyzer = JSAnalyzer()
        result = analyzer.analyze_file(str(test_path))
        
        print(f"\n  File: {result.path}")
        print(f"  Lines: {result.total_lines}")
        print(f"  Functions: {result.total_functions}")
        
        print(f"\n  LJPW Metrics:")
        print(f"    Love (L):    {result.love:.3f} {'[DEFICIT]' if result.L_deficit else ''}")
        print(f"    Justice (J): {result.justice:.3f} {'[DEFICIT]' if result.J_deficit else ''}")
        print(f"    Power (P):   {result.power:.3f} {'[DEFICIT]' if result.P_deficit else ''}")
        print(f"    Wisdom (W):  {result.wisdom:.3f} {'[DEFICIT]' if result.W_deficit else ''}")
        print(f"    Harmony:     {result.harmony:.3f}")
        
        if result.functions:
            print(f"\n  Function Breakdown:")
            for func in result.functions[:5]:  # Show first 5
                print(f"    {func.name}: L={func.love:.2f} J={func.justice:.2f} P={func.power:.2f} W={func.wisdom:.2f} H={func.harmony:.2f}")
    else:
        print(f"  Test file not found: {test_path}")
        print("  Run bicameral_grow.py first to generate a calculator.")
