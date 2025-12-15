"""
TypeScript Analyzer

Analyzes TypeScript code for LJPW dimensions.
Extends the JavaScript analyzer with TypeScript-specific patterns.
"""

import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TypeScriptAnalysisResult:
    """Result of TypeScript LJPW analysis."""
    file_path: str
    love: float
    justice: float
    power: float
    wisdom: float
    
    @property
    def harmony(self) -> float:
        """Geometric mean of LJPW dimensions."""
        if min(self.love, self.justice, self.power, self.wisdom) <= 0:
            return 0.0
        return (self.love * self.justice * self.power * self.wisdom) ** 0.25


class TypescriptAnalyzer:
    """
    Analyzes TypeScript code for LJPW harmony.
    
    Extends JavaScript analysis with TypeScript-specific patterns:
    - Love: TSDoc comments, interface descriptions
    - Justice: Type annotations, generics, strict mode
    - Power: Error types, try-catch with typed errors
    - Wisdom: Logging with types, debug statements
    """
    
    # TypeScript-specific patterns (extend JS patterns)
    LOVE_PATTERNS = [
        r'/\*\*[\s\S]*?\*/',      # TSDoc comments
        r'^\s*//.*',              # Single-line comments
        r'@param\s+\{[^}]+\}',    # JSDoc with types
        r'@returns?\s+\{[^}]+\}', # Return type docs
        r'@deprecated',           # Deprecation notices
        r'@example',              # Usage examples
    ]
    
    JUSTICE_PATTERNS = [
        r':\s*string\b',          # String type
        r':\s*number\b',          # Number type
        r':\s*boolean\b',         # Boolean type
        r':\s*\w+\[\]',           # Array type
        r'<\w+>',                 # Generics
        r'interface\s+\w+',       # Interface declaration
        r'type\s+\w+\s*=',        # Type alias
        r'readonly\s+',           # Readonly modifier
        r'private\s+',            # Access modifier
        r'public\s+',             # Access modifier
        r'protected\s+',          # Access modifier
        r'as\s+\w+',              # Type assertion
        r'\?\s*:',                # Optional property
        r'!\.',                   # Non-null assertion
    ]
    
    POWER_PATTERNS = [
        r'try\s*\{',              # Try block
        r'catch\s*\([^)]+:[^)]+\)', # Typed catch
        r'finally\s*\{',          # Finally block
        r'throw\s+new\s+\w+Error', # Typed error throw
        r'Promise<[^>]+>',        # Typed Promise
        r'async\s+function',      # Async function
        r'await\s+',              # Await usage
        r'\.catch\(',             # Promise catch
        r'Result<[^>]+>',         # Result type pattern
        r'Error\s*\|',            # Union with Error
    ]
    
    WISDOM_PATTERNS = [
        r'console\.(log|debug|info|warn|error)', # Logging
        r'logger\.\w+',           # Logger calls
        r'debug\s*\(',            # Debug calls
        r'@deprecated',           # Deprecation markers
        r'TODO:',                 # TODO comments
        r'FIXME:',                # FIXME comments
        r'NOTE:',                 # NOTE comments
        r'import.*debug',         # Debug imports
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        # Auto-healed: Input validation for __init__
        if config is not None and not isinstance(config, dict):
            raise TypeError(f'config must be a dict')
        """Initialize TypeScript analyzer."""
        self.config = config or {}
    
    def analyze_file(self, file_path: str) -> TypeScriptAnalysisResult:
        # Auto-healed: Input validation for analyze_file
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(f'file_path must be str, got {type(file_path).__name__}')
        """
        Analyze a TypeScript file for LJPW harmony.
        
        Args:
            file_path: Path to the .ts or .tsx file
            
        Returns:
            TypeScriptAnalysisResult with LJPW scores
        """
        path = Path(file_path)
        
        if not path.exists():
            return TypeScriptAnalysisResult(file_path, 0, 0, 0, 0)
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        
        # Count lines for normalization
        lines = len(content.split('\n'))
        if lines == 0:
            return TypeScriptAnalysisResult(file_path, 0, 0, 0, 0)
        
        # Calculate each dimension
        love = self._calculate_dimension(content, lines, self.LOVE_PATTERNS)
        justice = self._calculate_dimension(content, lines, self.JUSTICE_PATTERNS)
        power = self._calculate_dimension(content, lines, self.POWER_PATTERNS)
        wisdom = self._calculate_dimension(content, lines, self.WISDOM_PATTERNS)
        
        return TypeScriptAnalysisResult(
            file_path=file_path,
            love=min(1.0, love),
            justice=min(1.0, justice),
            power=min(1.0, power),
            wisdom=min(1.0, wisdom)
        )
    
    def _calculate_dimension(self, content: str, lines: int, patterns: List[str]) -> float:
        """Calculate score for a dimension based on pattern matches."""
        total_matches = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            total_matches += len(matches)
        
        # Normalize by lines of code
        density = total_matches / lines
        
        # Scale to 0-1 range (assume ~0.1 matches per line is excellent)
        return min(1.0, density * 10)
    
    def analyze_directory(self, dir_path: str) -> Dict[str, Any]:
        # Auto-healed: Input validation for analyze_directory
        if dir_path is not None and not isinstance(dir_path, str):
            raise TypeError(f'dir_path must be str, got {type(dir_path).__name__}')
        """
        Analyze all TypeScript files in a directory.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            Aggregated analysis results
        """
        path = Path(dir_path)
        results = []
        
        for ts_file in path.rglob('*.ts'):
            if 'node_modules' in str(ts_file):
                continue
            results.append(self.analyze_file(str(ts_file)))
        
        for tsx_file in path.rglob('*.tsx'):
            if 'node_modules' in str(tsx_file):
                continue
            results.append(self.analyze_file(str(tsx_file)))
        
        if not results:
            return {"files": 0, "harmony": 0}
        
        avg_love = sum(r.love for r in results) / len(results)
        avg_justice = sum(r.justice for r in results) / len(results)
        avg_power = sum(r.power for r in results) / len(results)
        avg_wisdom = sum(r.wisdom for r in results) / len(results)
        
        return {
            "files": len(results),
            "love": avg_love,
            "justice": avg_justice,
            "power": avg_power,
            "wisdom": avg_wisdom,
            "harmony": (avg_love * avg_justice * avg_power * avg_wisdom) ** 0.25 if min(avg_love, avg_justice, avg_power, avg_wisdom) > 0 else 0
        }


if __name__ == "__main__":
    analyzer = TypescriptAnalyzer()
    print("TypeScript Analyzer - Ready")
    print("Usage: analyzer.analyze_file('app.ts')")
