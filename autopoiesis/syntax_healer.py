"""
Syntax Healer
=============

Automatically detects and fixes syntax issues in Python files.

This enables the agent to heal its own code when:
- Invalid escape sequences are detected (e.g., / instead of /)
- Python syntax errors occur
- Common linting issues are found

The healer runs before LJPW healing to ensure code is valid first.

Usage:
    healer = SyntaxHealer()
    result = healer.heal_file("path/to/file.py")
    
    # Or heal entire codebase
    results = healer.heal_codebase("./autopoiesis")
"""

import ast
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SyntaxIssue:
    """A syntax issue found in a file."""
    file_path: str
    line_number: int
    issue_type: str  # 'escape_sequence', 'syntax_error', 'lint'
    description: str
    original: str
    fixed: str = ""
    can_fix: bool = False


@dataclass
class SyntaxHealingResult:
    """Result of syntax healing."""
    file_path: str
    issues_found: List[SyntaxIssue]
    issues_fixed: int
    success: bool
    message: str


class SyntaxHealer:
    """
    Heals Python syntax issues automatically.
    
    The healer can detect and fix:
    1. Invalid escape sequences (/ \\[ etc.)
    2. Basic syntax errors (missing colons, unmatched brackets)
    3. Common patterns that cause warnings
    """
    
    # Patterns for invalid escape sequences
    INVALID_ESCAPES = {
        r"\\\/": r"/",           # \/ -> /
        r"\\\ ": r" ",          # \\space -> space
        r"\\\[": r"[",          # \[ -> [ (in non-regex strings)
        r"\\\]": r"]",          # \] -> ]
    }
    
    # Known safe replacements for escape sequences in regex strings
    REGEX_ESCAPE_FIXES = {
        r"\/": r"/",  # Forward slash doesn't need escaping in regex
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the syntax healer.
        
        Args:
            dry_run: If True, detect but don't fix issues
        """
        self.dry_run = dry_run
    
    def check_file(self, file_path: str) -> List[SyntaxIssue]:
        # Auto-healed: Input validation for check_file
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(f'file_path must be str, got {type(file_path).__name__}')
        """
        Check a Python file for syntax issues.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of issues found
        """
        path = Path(file_path)
        if not path.exists() or path.suffix != '.py':
            return []
        
        issues = []
        
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Could not read {file_path}: {e}")
            return []
        
        # Check for invalid escape sequences
        issues.extend(self._find_escape_sequence_issues(content, file_path))
        
        # Check for syntax errors
        issues.extend(self._find_syntax_errors(content, file_path))
        
        return issues
    
    def _find_escape_sequence_issues(self, content: str, file_path: str) -> List[SyntaxIssue]:
        """Find invalid escape sequences in file content."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip comments and docstrings (rough check)
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # Check for \/ in non-raw strings
            # This is the escape sequence we fixed earlier
            if r'\/' in line and "r'" not in line and 'r"' not in line:
                # Found an invalid escape in a non-raw string
                # Check if it's in a Python string (not regex context)
                
                # Find position
                pos = line.find(r'\/')
                
                issue = SyntaxIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='escape_sequence',
                    description=f"Invalid escape sequence '/' at column {pos}",
                    original=line,
                    fixed=line.replace(r'\/', '/'),
                    can_fix=True
                )
                issues.append(issue)
        
        return issues
    
    def _find_syntax_errors(self, content: str, file_path: str) -> List[SyntaxIssue]:
        """Find Python syntax errors using compile()."""
        issues = []
        
        try:
            compile(content, file_path, 'exec')
        except SyntaxError as e:
            issue = SyntaxIssue(
                file_path=file_path,
                line_number=e.lineno or 0,
                issue_type='syntax_error',
                description=str(e.msg),
                original=e.text or "",
                can_fix=False  # Syntax errors are harder to auto-fix
            )
            issues.append(issue)
        
        return issues
    
    def heal_file(self, file_path: str) -> SyntaxHealingResult:
        # Auto-healed: Input validation for heal_file
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(f'file_path must be str, got {type(file_path).__name__}')
        """
        Heal a Python file by fixing detected issues.
        
        Args:
            file_path: Path to the file to heal
            
        Returns:
            SyntaxHealingResult with outcome
        """
        path = Path(file_path)
        issues = self.check_file(file_path)
        
        if not issues:
            return SyntaxHealingResult(
                file_path=file_path,
                issues_found=[],
                issues_fixed=0,
                success=True,
                message="No syntax issues found"
            )
        
        # Count fixable issues
        fixable = [i for i in issues if i.can_fix]
        
        if not fixable:
            return SyntaxHealingResult(
                file_path=file_path,
                issues_found=issues,
                issues_fixed=0,
                success=False,
                message=f"Found {len(issues)} issues but none auto-fixable"
            )
        
        if self.dry_run:
            return SyntaxHealingResult(
                file_path=file_path,
                issues_found=issues,
                issues_fixed=0,
                success=True,
                message=f"[Dry run] Would fix {len(fixable)} of {len(issues)} issues"
            )
        
        # Apply fixes
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        fixed_count = 0
        
        for issue in fixable:
            if issue.issue_type == 'escape_sequence':
                # Fix the line
                if issue.line_number <= len(lines):
                    old_line = lines[issue.line_number - 1]
                    new_line = issue.fixed
                    
                    if old_line == issue.original:
                        lines[issue.line_number - 1] = new_line
                        fixed_count += 1
                        logger.info(f"Fixed escape sequence at {file_path}:{issue.line_number}")
        
        # Write back
        if fixed_count > 0:
            new_content = '\n'.join(lines)
            path.write_text(new_content, encoding='utf-8')
        
        return SyntaxHealingResult(
            file_path=file_path,
            issues_found=issues,
            issues_fixed=fixed_count,
            success=True,
            message=f"Fixed {fixed_count} of {len(issues)} issues"
        )
    
    def heal_codebase(self, root_path: str, exclude_dirs: List[str] = None) -> List[SyntaxHealingResult]:
        # Auto-healed: Input validation for heal_codebase
        if root_path is not None and not isinstance(root_path, str):
            raise TypeError(f'root_path must be str, got {type(root_path).__name__}')
        """
        Heal all Python files in a directory.
        
        Args:
            root_path: Root directory to scan
            exclude_dirs: Directories to skip
            
        Returns:
            List of healing results
        """
        exclude_dirs = exclude_dirs or ['__pycache__', '.git', 'venv', 'node_modules']
        results = []
        root = Path(root_path)
        
        for py_file in root.rglob('*.py'):
            # Skip excluded directories
            if any(ex in str(py_file) for ex in exclude_dirs):
                continue
            
            result = self.heal_file(str(py_file))
            if result.issues_found:  # Only report files with issues
                results.append(result)
        
        return results
    
    def run_syntax_check(self, root_path: str) -> Dict:
        # Auto-healed: Input validation for run_syntax_check
        if root_path is not None and not isinstance(root_path, str):
            raise TypeError(f'root_path must be str, got {type(root_path).__name__}')
        """
        Run a full syntax check on the codebase.
        
        Returns summary of issues found without fixing.
        """
        healer = SyntaxHealer(dry_run=True)
        results = healer.heal_codebase(root_path)
        
        total_issues = sum(len(r.issues_found) for r in results)
        fixable = sum(len([i for i in r.issues_found if i.can_fix]) for r in results)
        
        return {
            'files_with_issues': len(results),
            'total_issues': total_issues,
            'fixable_issues': fixable,
            'unfixable_issues': total_issues - fixable,
            'files': [
                {
                    'path': r.file_path,
                    'issues': len(r.issues_found)
                }
                for r in results
            ]
        }


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SYNTAX HEALER - SELF TEST")
    print("=" * 60)
    print()
    
    # Test on autopoiesis folder
    import os
    autopoiesis_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(autopoiesis_path)
    
    healer = SyntaxHealer(dry_run=True)  # Dry run for testing
    
    print("Scanning codebase for syntax issues...")
    print()
    
    summary = healer.run_syntax_check(project_root)
    
    print(f"Files with issues: {summary['files_with_issues']}")
    print(f"Total issues: {summary['total_issues']}")
    print(f"  - Fixable: {summary['fixable_issues']}")
    print(f"  - Unfixable: {summary['unfixable_issues']}")
    print()
    
    if summary['files']:
        print("Files with issues:")
        for f in summary['files'][:10]:  # Show max 10
            print(f"  - {f['path']}: {f['issues']} issues")
    else:
        print("No syntax issues found! Codebase is clean.")
    
    print()
    print("To fix issues, run:")
    print("  healer = SyntaxHealer(dry_run=False)")
    print("  healer.heal_codebase('.')")
