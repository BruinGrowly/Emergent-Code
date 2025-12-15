"""
Autopoiesis Analyzer Module
============================

Deep AST-based code analysis to identify deficits in LJPW dimensions.

Consolidated from:
- experiments/deep_autopoiesis.py (DeepCodeAnalyzer)
- experiments/true_autopoiesis.py (CodeAnalyzer)

Key capabilities:
- AST parsing for structural analysis
- Function signature extraction with types
- Validation pattern detection
- LJPW dimension scoring via SemanticResonanceAnalyzer
- System-level aggregation
"""

import ast
import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

# Import LJPW analyzer
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer


@dataclass
class FunctionAnalysis:
    """Deep analysis of a single function."""
    name: str
    lineno: int
    params: List[Dict[str, Any]]
    returns: Optional[str]
    has_docstring: bool
    has_validation: bool
    has_error_handling: bool
    complexity: int  # cyclomatic complexity estimate
    calls_made: List[str]
    body_lines: int


@dataclass
class FileAnalysis:
    """Complete analysis of a Python file."""
    path: str
    functions: List[FunctionAnalysis]
    classes: List[Dict]
    imports: List[str]
    has_logging: bool
    ljpw: Dict[str, float]
    deficit: str
    harmony: float
    
    @property
    def needs_love(self) -> bool:
        """Check if file has Love deficit."""
        return self.deficit == 'L' or self.ljpw.get('L', 0) < 0.7
    
    @property
    def needs_justice(self) -> bool:
        """Check if file has Justice deficit."""
        return self.deficit == 'J' or self.ljpw.get('J', 0) < 0.7
    
    @property
    def needs_power(self) -> bool:
        """Check if file has Power deficit."""
        return self.deficit == 'P' or self.ljpw.get('P', 0) < 0.7
    
    @property
    def needs_wisdom(self) -> bool:
        """Check if file has Wisdom deficit."""
        return self.deficit == 'W' or self.ljpw.get('W', 0) < 0.7
    
    @property
    def is_autopoietic(self) -> bool:
        """Check if file meets autopoietic threshold (L > 0.7, H > 0.6)."""
        return self.ljpw.get('L', 0) > 0.7 and self.harmony > 0.6


@dataclass
class SystemAnalysis:
    """System-level analysis aggregating multiple files."""
    path: str
    files: List[FileAnalysis]
    total_functions: int = 0
    total_classes: int = 0
    
    # Aggregated LJPW
    system_ljpw: Dict[str, float] = field(default_factory=dict)
    system_harmony: float = 0.0
    deficit_distribution: Dict[str, int] = field(default_factory=dict)
    
    @property
    def is_autopoietic(self) -> bool:
        """Check if system meets autopoietic threshold."""
        return self.system_ljpw.get('L', 0) > 0.7 and self.system_harmony > 0.6
    
    def calculate_system_metrics(self):
        """Aggregate metrics from all files."""
        if not self.files:
            return
        
        # Sum up totals
        self.total_functions = sum(len(f.functions) for f in self.files)
        self.total_classes = sum(len(f.classes) for f in self.files)
        
        # Aggregate LJPW (weighted average by file complexity)
        total_weight = 0
        aggregated = {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}
        
        for f in self.files:
            weight = len(f.functions) + len(f.classes) + 1
            total_weight += weight
            for dim in 'LJPW':
                aggregated[dim] += f.ljpw.get(dim, 0) * weight
        
        if total_weight > 0:
            for dim in 'LJPW':
                self.system_ljpw[dim] = aggregated[dim] / total_weight
        
        # Calculate system harmony as geometric mean
        if all(self.system_ljpw.get(d, 0) > 0 for d in 'LJPW'):
            product = 1.0
            for d in 'LJPW':
                product *= self.system_ljpw[d]
            self.system_harmony = product ** 0.25
        else:
            # If any dimension is 0, use average instead
            self.system_harmony = sum(self.system_ljpw.values()) / 4
        
        # Count deficits
        self.deficit_distribution = {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        for f in self.files:
            if f.deficit in self.deficit_distribution:
                self.deficit_distribution[f.deficit] += 1


class CodeAnalyzer:
    """
    Deep code analyzer using AST parsing and LJPW measurement.
    
    Performs comprehensive analysis at:
    - Function level (params, validation, complexity)
    - File level (LJPW scores, deficits)
    - System level (aggregated harmony)
    """
    
    def __init__(self):
        self.semantic_analyzer = SemanticResonanceAnalyzer()
    
    def analyze_file(self, filepath: str) -> Optional[FileAnalysis]:
        """
        Perform comprehensive analysis of a Python file.
        
        Args:
            filepath: Path to Python file
            
        Returns:
            FileAnalysis with all metrics, or None if parse failed
        """
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get LJPW metrics from semantic analyzer
        try:
            report = self.semantic_analyzer.analyze_code(content, os.path.basename(filepath))
            ljpw = {
                'L': report['final_ljpw'][0],
                'J': report['final_ljpw'][1],
                'P': report['final_ljpw'][2],
                'W': report['final_ljpw'][3],
            }
            deficit = report['deficit_dimension']
            harmony = report['harmony_final']
        except Exception:
            # Default if analyzer fails
            ljpw = {'L': 0.5, 'J': 0.5, 'P': 0.5, 'W': 0.5}
            deficit = 'L'
            harmony = 0.5
        
        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return None
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_analysis = self._analyze_function(node, content)
                functions.append(func_analysis)
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'has_docstring': ast.get_docstring(node) is not None,
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                else:
                    imports.append(node.module or '')
        
        return FileAnalysis(
            path=filepath,
            functions=functions,
            classes=classes,
            imports=imports,
            has_logging='logging' in ' '.join(imports),
            ljpw=ljpw,
            deficit=deficit,
            harmony=harmony
        )
    
    def analyze_directory(self, dirpath: str, recursive: bool = True) -> SystemAnalysis:
        # Auto-healed: Input validation for analyze_directory
        if dirpath is not None and not isinstance(dirpath, str):
            raise TypeError(f'dirpath must be str, got {type(dirpath).__name__}')
        """
        Analyze all Python files in a directory.
        
        Args:
            dirpath: Path to directory
            recursive: Whether to search subdirectories
            
        Returns:
            SystemAnalysis with aggregated metrics
        """
        files = []
        path = Path(dirpath)
        
        pattern = '**/*.py' if recursive else '*.py'
        for py_file in path.glob(pattern):
            # Skip __pycache__ and test files
            if '__pycache__' in str(py_file):
                continue
            if py_file.name.startswith('test_'):
                continue
                
            analysis = self.analyze_file(str(py_file))
            if analysis:
                files.append(analysis)
        
        system = SystemAnalysis(path=dirpath, files=files)
        system.calculate_system_metrics()
        
        return system
    
    def _analyze_function(self, node: ast.FunctionDef, content: str) -> FunctionAnalysis:
        """Deep analysis of a single function."""
        # Extract parameters with types
        params = []
        for arg in node.args.args:
            param = {'name': arg.arg, 'type': None, 'has_default': False}
            if arg.annotation:
                try:
                    param['type'] = ast.unparse(arg.annotation)
                except Exception:
                    pass
            params.append(param)
        
        # Mark defaults
        defaults = node.args.defaults
        for i, default in enumerate(reversed(defaults)):
            if i < len(params):
                params[-(i+1)]['has_default'] = True
        
        # Get return type
        returns = None
        if node.returns:
            try:
                returns = ast.unparse(node.returns)
            except Exception:
                pass
        
        # Check for validation patterns
        has_validation = False
        has_error_handling = False
        calls_made = []
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, ast.Assert):
                has_validation = True
            elif isinstance(child, ast.Raise):
                has_validation = True
            elif isinstance(child, ast.Try):
                has_error_handling = True
            elif isinstance(child, ast.If):
                complexity += 1
                # Check if it's input validation
                try:
                    if_test = ast.unparse(child.test)
                    if any(p['name'] in if_test for p in params):
                        if 'None' in if_test or 'isinstance' in if_test or 'not ' in if_test:
                            has_validation = True
                except Exception:
                    pass
            elif isinstance(child, (ast.For, ast.While)):
                complexity += 1
            elif isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls_made.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls_made.append(child.func.attr)
        
        # Count body lines
        body_lines = len(node.body) if node.body else 0
        
        return FunctionAnalysis(
            name=node.name,
            lineno=node.lineno,
            params=params,
            returns=returns,
            has_docstring=ast.get_docstring(node) is not None,
            has_validation=has_validation,
            has_error_handling=has_error_handling,
            complexity=complexity,
            calls_made=calls_made,
            body_lines=body_lines
        )
    
    def get_functions_needing_healing(self, file_analysis: FileAnalysis) -> Dict[str, List[FunctionAnalysis]]:
        """
        Identify functions that need healing in each dimension.
        
        Returns:
            Dict mapping dimension to list of functions needing that type of healing
        """
        needs_healing = {
            'L': [],  # Love: needs docstrings
            'J': [],  # Justice: needs validation
            'P': [],  # Power: complex, needs optimization
            'W': [],  # Wisdom: needs logging/observability
        }
        
        for func in file_analysis.functions:
            # Skip private methods except __init__
            if func.name.startswith('_') and func.name != '__init__':
                continue
            
            # Love: missing docstrings
            if not func.has_docstring:
                needs_healing['L'].append(func)
            
            # Justice: missing validation on functions with params
            if not func.has_validation and len([p for p in func.params if p['name'] != 'self']) > 0:
                needs_healing['J'].append(func)
            
            # Power: high complexity without error handling
            if func.complexity > 3 and not func.has_error_handling:
                needs_healing['P'].append(func)
            
            # Wisdom: public functions without logging
            if func.body_lines > 3 and 'log' not in ' '.join(func.calls_made).lower():
                needs_healing['W'].append(func)
        
        return needs_healing
