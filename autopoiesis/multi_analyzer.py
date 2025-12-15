"""
Multi-Language LJPW Analyzer
============================

Unified analyzer that supports multiple programming languages:
- Python (.py) - via CodeAnalyzer
- JavaScript (.js, .jsx, .ts, .tsx, .mjs) - via JSAnalyzer
- HTML (.html) - structural analysis
- CSS (.css) - design token analysis

This enables full-cycle autopoiesis for multi-language projects.
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# Handle imports for both module and standalone usage
try:
    from .analyzer import CodeAnalyzer
    from .js_analyzer import JSAnalyzer, JSFileAnalysis
except ImportError:
    # Running as standalone script
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from autopoiesis.analyzer import CodeAnalyzer
    from autopoiesis.js_analyzer import JSAnalyzer, JSFileAnalysis


class FileType(Enum):
    """Supported file types."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    HTML = "html"
    CSS = "css"
    UNKNOWN = "unknown"


@dataclass
class UnifiedFileAnalysis:
    """Unified analysis result for any file type."""
    path: str
    file_type: FileType
    
    # LJPW metrics
    love: float = 0.0
    justice: float = 0.0
    power: float = 0.0
    wisdom: float = 0.0
    harmony: float = 0.0
    
    # Counts
    total_lines: int = 0
    total_functions: int = 0
    
    # Deficits
    L_deficit: bool = False
    J_deficit: bool = False
    P_deficit: bool = False
    W_deficit: bool = False
    
    @property
    def dominant_deficit(self) -> Optional[str]:
        """Return the weakest dimension."""
        dims = {'L': self.love, 'J': self.justice, 'P': self.power, 'W': self.wisdom}
        return min(dims, key=dims.get)


@dataclass
class MultiLanguageReport:
    """Report for a multi-language project."""
    path: str
    
    # Per-language breakdowns
    python_files: List[UnifiedFileAnalysis] = field(default_factory=list)
    javascript_files: List[UnifiedFileAnalysis] = field(default_factory=list)
    html_files: List[UnifiedFileAnalysis] = field(default_factory=list)
    css_files: List[UnifiedFileAnalysis] = field(default_factory=list)
    
    # Aggregated LJPW
    love: float = 0.0
    justice: float = 0.0
    power: float = 0.0
    wisdom: float = 0.0
    harmony: float = 0.0
    
    # Totals
    total_files: int = 0
    total_lines: int = 0
    
    # Language distribution
    @property
    def language_distribution(self) -> Dict[str, int]:
        return {
            'python': len(self.python_files),
            'javascript': len(self.javascript_files),
            'html': len(self.html_files),
            'css': len(self.css_files),
        }


class MultiLanguageAnalyzer:
    """
    Unified analyzer for multi-language projects.
    
    Detects file types and routes to appropriate analyzers.
    Aggregates results into a unified LJPW report.
    """
    
    # File extension to type mapping
    EXTENSION_MAP = {
        '.py': FileType.PYTHON,
        '.js': FileType.JAVASCRIPT,
        '.jsx': FileType.JAVASCRIPT,
        '.ts': FileType.JAVASCRIPT,
        '.tsx': FileType.JAVASCRIPT,
        '.mjs': FileType.JAVASCRIPT,
        '.html': FileType.HTML,
        '.htm': FileType.HTML,
        '.css': FileType.CSS,
    }
    
    # Directories to skip
    SKIP_DIRS = {'node_modules', 'dist', 'build', '__pycache__', '.git', 'venv', 'env'}
    
    def __init__(self):
        self.python_analyzer = CodeAnalyzer()
        self.js_analyzer = JSAnalyzer()
    
    def detect_file_type(self, path: str) -> FileType:
        # Auto-healed: Input validation for detect_file_type
        if path is not None and not isinstance(path, str):
            raise TypeError(f'path must be str, got {type(path).__name__}')
        """Detect file type from extension."""
        ext = Path(path).suffix.lower()
        return self.EXTENSION_MAP.get(ext, FileType.UNKNOWN)
    
    def analyze_file(self, file_path: str) -> Optional[UnifiedFileAnalysis]:
        # Auto-healed: Input validation for analyze_file
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(f'file_path must be str, got {type(file_path).__name__}')
        """
        Analyze a single file, routing to appropriate analyzer.
        
        Args:
            file_path: Path to file
            
        Returns:
            UnifiedFileAnalysis or None if unsupported
        """
        path = Path(file_path)
        file_type = self.detect_file_type(str(path))
        
        if file_type == FileType.PYTHON:
            return self._analyze_python(str(path))
        elif file_type == FileType.JAVASCRIPT:
            return self._analyze_javascript(str(path))
        elif file_type == FileType.HTML:
            return self._analyze_html(str(path))
        elif file_type == FileType.CSS:
            return self._analyze_css(str(path))
        else:
            return None
    
    def _analyze_python(self, path: str) -> UnifiedFileAnalysis:
        """Analyze Python file."""
        try:
            result = self.python_analyzer.analyze_file(path)
            if result is None:
                return UnifiedFileAnalysis(path=path, file_type=FileType.PYTHON)
            
            ljpw = result.ljpw
            return UnifiedFileAnalysis(
                path=path,
                file_type=FileType.PYTHON,
                love=ljpw.get('L', 0),
                justice=ljpw.get('J', 0),
                power=ljpw.get('P', 0),
                wisdom=ljpw.get('W', 0),
                harmony=result.harmony,
                total_lines=result.lines,
                total_functions=len(result.functions),
                L_deficit=result.deficit == 'L',
                J_deficit=result.deficit == 'J',
                P_deficit=result.deficit == 'P',
                W_deficit=result.deficit == 'W',
            )
        except Exception as e:
            print(f"  Warning: Could not analyze Python file {path}: {e}")
            return UnifiedFileAnalysis(path=path, file_type=FileType.PYTHON)
    
    def _analyze_javascript(self, path: str) -> UnifiedFileAnalysis:
        """Analyze JavaScript file."""
        try:
            result = self.js_analyzer.analyze_file(path)
            
            return UnifiedFileAnalysis(
                path=path,
                file_type=FileType.JAVASCRIPT,
                love=result.love,
                justice=result.justice,
                power=result.power,
                wisdom=result.wisdom,
                harmony=result.harmony,
                total_lines=result.total_lines,
                total_functions=result.total_functions,
                L_deficit=result.L_deficit,
                J_deficit=result.J_deficit,
                P_deficit=result.P_deficit,
                W_deficit=result.W_deficit,
            )
        except Exception as e:
            print(f"  Warning: Could not analyze JS file {path}: {e}")
            return UnifiedFileAnalysis(path=path, file_type=FileType.JAVASCRIPT)
    
    def _analyze_html(self, path: str) -> UnifiedFileAnalysis:
        """
        Analyze HTML file.
        
        LJPW in HTML:
        - Love: Semantic elements, alt text, aria labels
        - Justice: Valid structure, proper nesting
        - Power: Error handling scripts, fallbacks
        - Wisdom: Meta tags, structured data
        """
        try:
            content = Path(path).read_text(encoding='utf-8', errors='ignore')
            lines = content.count('\n') + 1
            
            import re
            
            # Love indicators
            semantic_tags = len(re.findall(r'<(header|footer|nav|main|article|section|aside)', content))
            alt_text = len(re.findall(r'alt=["\'][^"\']+["\']', content))
            aria_labels = len(re.findall(r'aria-', content))
            love = min(1.0, (semantic_tags * 0.1 + alt_text * 0.1 + aria_labels * 0.05))
            
            # Justice indicators
            has_doctype = '<!DOCTYPE' in content.upper()
            has_lang = 'lang=' in content
            has_charset = 'charset' in content.lower()
            justice = 0.3 + (0.2 if has_doctype else 0) + (0.2 if has_lang else 0) + (0.3 if has_charset else 0)
            
            # Power indicators
            has_noscript = '<noscript>' in content.lower()
            has_error_handling = 'onerror' in content.lower()
            power = 0.3 + (0.3 if has_noscript else 0) + (0.3 if has_error_handling else 0)
            
            # Wisdom indicators
            has_meta = len(re.findall(r'<meta\s', content))
            has_title = '<title>' in content.lower()
            has_description = 'description' in content.lower()
            wisdom = min(1.0, 0.2 + has_meta * 0.1 + (0.3 if has_title else 0) + (0.2 if has_description else 0))
            
            harmony = (love * justice * power * wisdom) ** 0.25
            
            return UnifiedFileAnalysis(
                path=path,
                file_type=FileType.HTML,
                love=love,
                justice=justice,
                power=power,
                wisdom=wisdom,
                harmony=harmony,
                total_lines=lines,
                L_deficit=love < 0.3,
                J_deficit=justice < 0.3,
                P_deficit=power < 0.3,
                W_deficit=wisdom < 0.3,
            )
        except Exception as e:
            print(f"  Warning: Could not analyze HTML file {path}: {e}")
            return UnifiedFileAnalysis(path=path, file_type=FileType.HTML)
    
    def _analyze_css(self, path: str) -> UnifiedFileAnalysis:
        """
        Analyze CSS file.
        
        LJPW in CSS:
        - Love: Comments, readable formatting
        - Justice: Consistent naming, design tokens
        - Power: Fallbacks, vendor prefixes
        - Wisdom: Custom properties, organized sections
        """
        try:
            content = Path(path).read_text(encoding='utf-8', errors='ignore')
            lines = content.count('\n') + 1
            
            import re
            
            # Love indicators
            comments = len(re.findall(r'/\*[\s\S]*?\*/', content))
            love = min(1.0, 0.2 + comments * 0.1)
            
            # Justice indicators
            has_root = ':root' in content
            custom_props = len(re.findall(r'--[\w-]+:', content))
            justice = 0.2 + (0.3 if has_root else 0) + min(0.5, custom_props * 0.05)
            
            # Power indicators
            fallbacks = len(re.findall(r';\s*[\w-]+:', content))  # Multiple declarations
            vendor_prefixes = len(re.findall(r'-webkit-|-moz-|-ms-', content))
            power = 0.3 + min(0.4, fallbacks * 0.01) + min(0.3, vendor_prefixes * 0.05)
            
            # Wisdom indicators
            media_queries = len(re.findall(r'@media', content))
            section_comments = len(re.findall(r'/\*\s*={3,}', content))
            wisdom = 0.2 + min(0.4, media_queries * 0.1) + min(0.4, section_comments * 0.1)
            
            harmony = (love * justice * power * wisdom) ** 0.25
            
            return UnifiedFileAnalysis(
                path=path,
                file_type=FileType.CSS,
                love=love,
                justice=justice,
                power=power,
                wisdom=wisdom,
                harmony=harmony,
                total_lines=lines,
                L_deficit=love < 0.3,
                J_deficit=justice < 0.3,
                P_deficit=power < 0.3,
                W_deficit=wisdom < 0.3,
            )
        except Exception as e:
            print(f"  Warning: Could not analyze CSS file {path}: {e}")
            return UnifiedFileAnalysis(path=path, file_type=FileType.CSS)
    
    def analyze_directory(self, dir_path: str) -> MultiLanguageReport:
        # Auto-healed: Input validation for analyze_directory
        if dir_path is not None and not isinstance(dir_path, str):
            raise TypeError(f'dir_path must be str, got {type(dir_path).__name__}')
        """
        Analyze all supported files in a directory.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            MultiLanguageReport with aggregated metrics
        """
        path = Path(dir_path)
        report = MultiLanguageReport(path=str(path))
        
        for file_path in path.rglob('*'):
            # Skip directories in skip list
            if any(skip in str(file_path) for skip in self.SKIP_DIRS):
                continue
            
            if file_path.is_file():
                file_type = self.detect_file_type(str(file_path))
                
                if file_type != FileType.UNKNOWN:
                    analysis = self.analyze_file(str(file_path))
                    if analysis:
                        if file_type == FileType.PYTHON:
                            report.python_files.append(analysis)
                        elif file_type == FileType.JAVASCRIPT:
                            report.javascript_files.append(analysis)
                        elif file_type == FileType.HTML:
                            report.html_files.append(analysis)
                        elif file_type == FileType.CSS:
                            report.css_files.append(analysis)
        
        # Aggregate metrics
        self._aggregate_report(report)
        
        return report
    
    def _aggregate_report(self, report: MultiLanguageReport):
        """Aggregate file-level metrics to report level."""
        all_files = (
            report.python_files + 
            report.javascript_files + 
            report.html_files + 
            report.css_files
        )
        
        if not all_files:
            return
        
        report.total_files = len(all_files)
        report.total_lines = sum(f.total_lines for f in all_files)
        
        # Weight by lines
        total_weight = sum(f.total_lines for f in all_files) or 1
        
        weighted_L = sum(f.love * f.total_lines for f in all_files)
        weighted_J = sum(f.justice * f.total_lines for f in all_files)
        weighted_P = sum(f.power * f.total_lines for f in all_files)
        weighted_W = sum(f.wisdom * f.total_lines for f in all_files)
        
        report.love = weighted_L / total_weight
        report.justice = weighted_J / total_weight
        report.power = weighted_P / total_weight
        report.wisdom = weighted_W / total_weight
        report.harmony = (report.love * report.justice * report.power * report.wisdom) ** 0.25


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("""
+==============================================================================+
|                                                                              |
|   MULTI-LANGUAGE LJPW ANALYZER                                               |
|                                                                              |
|   Analyzing Python, JavaScript, HTML, and CSS                                |
|                                                                              |
+==============================================================================+
    """)
    
    analyzer = MultiLanguageAnalyzer()
    
    # Test on bicameral calculator
    test_path = Path(__file__).parent.parent / "grown" / "bicameral_calculator"
    
    if test_path.exists():
        print(f"  Analyzing: {test_path}")
        print("-" * 60)
        
        report = analyzer.analyze_directory(str(test_path))
        
        print(f"\n  Total Files: {report.total_files}")
        print(f"  Total Lines: {report.total_lines}")
        print(f"\n  Language Distribution:")
        for lang, count in report.language_distribution.items():
            if count > 0:
                print(f"    {lang}: {count} files")
        
        print(f"\n  Aggregated LJPW:")
        print(f"    Love (L):    {report.love:.3f}")
        print(f"    Justice (J): {report.justice:.3f}")
        print(f"    Power (P):   {report.power:.3f}")
        print(f"    Wisdom (W):  {report.wisdom:.3f}")
        print(f"    Harmony:     {report.harmony:.3f}")
        
        print(f"\n  Per-File Breakdown:")
        for f in report.javascript_files:
            print(f"    [JS]   {Path(f.path).name}: L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f}")
        for f in report.html_files:
            print(f"    [HTML] {Path(f.path).name}: L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f}")
        for f in report.css_files:
            print(f"    [CSS]  {Path(f.path).name}: L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f}")
    else:
        print(f"  Test path not found: {test_path}")
