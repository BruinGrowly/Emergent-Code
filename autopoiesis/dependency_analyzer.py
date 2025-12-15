"""
Dependency Analyzer

Analyzes import relationships in a codebase to understand
module dependencies and coupling.
"""

import re
import os
import logging
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class ModuleNode:
    """A module in the dependency graph."""
    path: str
    imports: Set[str] = field(default_factory=set)
    imported_by: Set[str] = field(default_factory=set)
    
    @property
    def coupling(self) -> int:
        """Total coupling (imports + imported_by)."""
        return len(self.imports) + len(self.imported_by)


@dataclass
class DependencyGraph:
    """Complete dependency graph of a codebase."""
    modules: Dict[str, ModuleNode] = field(default_factory=dict)
    
    @property
    def total_modules(self) -> int:
        return len(self.modules)
    
    @property
    def total_edges(self) -> int:
        return sum(len(m.imports) for m in self.modules.values())
    
    @property
    def most_coupled(self) -> List[str]:
        """Get modules with highest coupling."""
        sorted_modules = sorted(
            self.modules.values(),
            key=lambda m: m.coupling,
            reverse=True
        )
        return [m.path for m in sorted_modules[:5]]


class DependencyAnalyzer:
    """
    Analyzes import relationships in Python and JavaScript codebases.
    """
    
    # Python import patterns
    PYTHON_PATTERNS = [
        r'^import\s+([\w.]+)',                    # import module
        r'^from\s+([\w.]+)\s+import',             # from module import
    ]
    
    # JavaScript/TypeScript import patterns
    JS_PATTERNS = [
        r'import\s+.*?\s+from\s+[\'"]([^\'"]+)', # import X from 'Y'
        r'require\s*\(\s*[\'"]([^\'"]+)',         # require('X')
        r'import\s*\(\s*[\'"]([^\'"]+)',          # dynamic import
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        # Auto-healed: Input validation for __init__
        if config is not None and not isinstance(config, dict):
            raise TypeError(f'config must be a dict')
        """Initialize dependency analyzer."""
        self.config = config or {}
    
    def analyze(self, root_path: str) -> DependencyGraph:
        # Auto-healed: Input validation for analyze
        if root_path is not None and not isinstance(root_path, str):
            raise TypeError(f'root_path must be str, got {type(root_path).__name__}')
        """
        Analyze all dependencies in a codebase.
        
        Args:
            root_path: Root directory to analyze
            
        Returns:
            DependencyGraph with all modules and their relationships
        """
        root = Path(root_path).resolve()
        graph = DependencyGraph()
        
        # Analyze Python files
        for py_file in root.rglob('*.py'):
            if self._should_skip(py_file):
                continue
            rel_path = str(py_file.relative_to(root))
            imports = self._extract_python_imports(py_file)
            
            if rel_path not in graph.modules:
                graph.modules[rel_path] = ModuleNode(path=rel_path)
            graph.modules[rel_path].imports.update(imports)
        
        # Analyze JavaScript files
        for js_ext in ['*.js', '*.jsx', '*.ts', '*.tsx']:
            for js_file in root.rglob(js_ext):
                if self._should_skip(js_file):
                    continue
                rel_path = str(js_file.relative_to(root))
                imports = self._extract_js_imports(js_file)
                
                if rel_path not in graph.modules:
                    graph.modules[rel_path] = ModuleNode(path=rel_path)
                graph.modules[rel_path].imports.update(imports)
        
        # Build reverse relationships
        for module_path, module in graph.modules.items():
            for imported in module.imports:
                # Try to find the actual file
                for ext in ['', '.py', '.js', '.ts', '.tsx', '.jsx']:
                    candidate = imported.replace('.', '/') + ext
                    if candidate in graph.modules:
                        graph.modules[candidate].imported_by.add(module_path)
                        break
        
        return graph
    
    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped."""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
        return any(skip in str(path) for skip in skip_dirs)
    
    def _extract_python_imports(self, file_path: Path) -> Set[str]:
        """Extract imports from Python file."""
        imports = set()
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern in self.PYTHON_PATTERNS:
                for match in re.finditer(pattern, content, re.MULTILINE):
                    module = match.group(1)
                    # Get top-level module
                    imports.add(module.split('.')[0])
        except Exception:
            pass
        
        return imports
    
    def _extract_js_imports(self, file_path: Path) -> Set[str]:
        """Extract imports from JavaScript/TypeScript file."""
        imports = set()
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern in self.JS_PATTERNS:
                for match in re.finditer(pattern, content):
                    import_path = match.group(1)
                    # Clean up path
                    if import_path.startswith('.'):
                        imports.add(import_path)
                    else:
                        imports.add(import_path.split('/')[0])
        except Exception:
            pass
        
        return imports
    
    def get_summary(self, root_path: str) -> Dict[str, Any]:
        # Auto-healed: Input validation for get_summary
        if root_path is not None and not isinstance(root_path, str):
            raise TypeError(f'root_path must be str, got {type(root_path).__name__}')
        """Get a summary of dependencies."""
        graph = self.analyze(root_path)
        
        return {
            "total_modules": graph.total_modules,
            "total_imports": graph.total_edges,
            "avg_coupling": graph.total_edges / max(graph.total_modules, 1),
            "most_coupled": graph.most_coupled
        }


if __name__ == "__main__":
    analyzer = DependencyAnalyzer()
    print("Dependency Analyzer - Testing")
    
    summary = analyzer.get_summary(".")
    print(f"Modules: {summary['total_modules']}")
    print(f"Total imports: {summary['total_imports']}")
    print(f"Avg coupling: {summary['avg_coupling']:.2f}")
    print(f"Most coupled: {summary['most_coupled'][:3]}")
