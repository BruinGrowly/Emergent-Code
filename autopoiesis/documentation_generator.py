"""
Documentation Generator

Automatically generates documentation from code analysis:
- README files from module structure
- API documentation from docstrings
- LJPW health reports
"""

import os
import ast
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class DocSection:
    """A section of documentation."""
    title: str
    content: str
    level: int = 2


class DocumentationGenerator:
    """
    Generates documentation from codebase analysis.
    """
    
    def __init__(self, target_path: str = "."):
        """Initialize documentation generator."""
        self.target_path = Path(target_path).resolve()
    
    def generate_readme(self, output_path: Optional[str] = None) -> str:
        """
        Generate a README.md for the codebase.
        
        Args:
            output_path: Where to write (default: don't write, just return)
            
        Returns:
            Generated markdown content
        """
        sections = []
        
        # Title
        project_name = self.target_path.name
        sections.append(f"# {project_name}\n")
        
        # Description from existing README or generate
        existing_readme = self.target_path / "README.md"
        if existing_readme.exists():
            content = existing_readme.read_text(encoding='utf-8', errors='ignore')
            # Extract first paragraph
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#'):
                    sections.append(line + "\n")
                    break
        else:
            sections.append("Auto-generated documentation.\n")
        
        # Structure
        sections.append("\n## Project Structure\n\n```\n")
        sections.append(self._generate_tree())
        sections.append("```\n")
        
        # Modules
        sections.append("\n## Modules\n")
        sections.append(self._generate_module_docs())
        
        # LJPW Health
        sections.append("\n## Health Metrics\n")
        sections.append(self._generate_health_section())
        
        # Generated timestamp
        sections.append(f"\n---\n*Generated: {datetime.now().isoformat()}*\n")
        
        result = '\n'.join(sections)
        
        if output_path:
            Path(output_path).write_text(result, encoding='utf-8')
        
        return result
    
    def _generate_tree(self, max_depth: int = 2) -> str:
        """Generate directory tree."""
        lines = []
        
        def walk(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules', 'venv']:
                    continue
                
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{item.name}")
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    walk(item, prefix + extension, depth + 1)
        
        walk(self.target_path)
        return '\n'.join(lines[:30])  # Limit output
    
    def _generate_module_docs(self) -> str:
        """Generate documentation for Python modules."""
        docs = []
        
        for py_file in sorted(self.target_path.rglob('*.py'))[:20]:
            if '__pycache__' in str(py_file):
                continue
            
            rel_path = py_file.relative_to(self.target_path)
            module_doc = self._extract_module_doc(py_file)
            
            if module_doc:
                docs.append(f"\n### {rel_path}\n\n{module_doc}\n")
        
        return '\n'.join(docs) if docs else "No modules documented yet.\n"
    
    def _extract_module_doc(self, file_path: Path) -> Optional[str]:
        """Extract docstring from Python module."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
            
            docstring = ast.get_docstring(tree)
            if docstring:
                # First line only
                return docstring.split('\n')[0]
        except Exception:
            pass
        return None
    
    def _generate_health_section(self) -> str:
        """Generate LJPW health section."""
        try:
            from autopoiesis.system import SystemHarmonyMeasurer
            measurer = SystemHarmonyMeasurer()
            report = measurer.measure(str(self.target_path))
            
            return f"""
| Dimension | Score |
|-----------|-------|
| **Harmony** | {report.harmony:.3f} |
| Love | {report.love:.3f} |
| Justice | {report.justice:.3f} |
| Power | {report.power:.3f} |
| Wisdom | {report.wisdom:.3f} |

*Phase: {report.phase.value}*
"""
        except Exception as e:
            return f"Unable to measure: {e}\n"
    
    def generate_api_docs(self, module_path: str) -> str:
        """
        Generate API documentation for a module.
        
        Args:
            module_path: Path to Python module
            
        Returns:
            Markdown API documentation
        """
        path = Path(module_path)
        if not path.exists():
            return f"Module not found: {module_path}"
        
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
        except Exception as e:
            return f"Parse error: {e}"
        
        docs = [f"# API: {path.stem}\n"]
        
        # Module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            docs.append(f"{module_doc}\n")
        
        # Classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_doc = ast.get_docstring(node)
                docs.append(f"\n## Class: {node.name}\n")
                if class_doc:
                    docs.append(f"{class_doc}\n")
                
                # Methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_doc = ast.get_docstring(item)
                        docs.append(f"\n### {item.name}()\n")
                        if method_doc:
                            docs.append(f"{method_doc}\n")
        
        return '\n'.join(docs)


if __name__ == "__main__":
    gen = DocumentationGenerator(".")
    print("Documentation Generator - Test")
    print()
    
    # Generate README preview
    readme = gen.generate_readme()
    print("Generated README preview:")
    print("-" * 40)
    print(readme[:1000])
    print("...")
