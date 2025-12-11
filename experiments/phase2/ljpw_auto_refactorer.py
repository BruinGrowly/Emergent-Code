"""
LJPW-Guided Automatic Code Refactorer

This tool automatically improves code toward autopoietic thresholds by:
1. Analyzing code for LJPW weaknesses
2. Applying targeted refactorings based on low dimensions
3. Generating improved code that moves toward L > 0.7, H > 0.6

Based on Phase 2 discoveries:
- Intent is measurable and improvable
- Balance emerges from genuine improvements
- Specific patterns increase specific dimensions

Refactoring Strategy:
- Low L → Add integration (logging, type hints, docstrings)
- Low J → Add validation (error handling, input checks)
- Low P → Simplify logic (extract functions, remove redundancy)
- Low W → Add structure (constants, abstractions, domain models)
"""

import re
from typing import Dict, List, Tuple


class LJPWRefactorer:
    """Automatic refactorer guided by LJPW principles."""

    def __init__(self):
        self.refactorings_applied = []

    def analyze_code_issues(self, code: str) -> Dict[str, List[str]]:
        """
        Static analysis to identify LJPW issues.

        Returns dict with issues categorized by dimension.
        """
        issues = {
            "love": [],
            "justice": [],
            "power": [],
            "wisdom": []
        }

        # Love issues (integration, documentation, observability)
        if not re.search(r'"""[\s\S]*?"""', code):  # No docstring
            issues["love"].append("Missing docstring (↓ Love: poor developer experience)")

        if not re.search(r':\s*\w+', code):  # No type hints
            issues["love"].append("Missing type hints (↓ Love: unclear interfaces)")

        if code.count('print') == 0 and code.count('log') == 0:
            issues["love"].append("No logging/observability (↓ Love: poor visibility)")

        # Justice issues (validation, error handling)
        if 'raise' not in code:
            issues["justice"].append("No error handling (↓ Justice: unsafe)")

        if not re.search(r'if.*(<|>|==|!=)', code):
            issues["justice"].append("No validation checks (↓ Justice: unguarded)")

        # Power issues (inefficiency, complexity)
        lines = code.split('\n')
        if len([l for l in lines if l.strip()]) > 50:
            issues["power"].append("Function too long (↓ Power: complex)")

        # Count nested blocks
        max_indent = max([len(l) - len(l.lstrip()) for l in lines if l.strip()])
        if max_indent > 12:  # More than 3 levels
            issues["power"].append("Too deeply nested (↓ Power: complex)")

        # Wisdom issues (structure, abstraction)
        # Check for magic numbers
        magic_numbers = re.findall(r'\b\d+\.?\d*\b', code)
        if len([n for n in magic_numbers if float(n) not in [0, 1]]) > 2:
            issues["wisdom"].append("Magic numbers present (↓ Wisdom: unclear intent)")

        # Check for repeated code
        code_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]
        if len(code_lines) != len(set(code_lines)):
            issues["wisdom"].append("Duplicated code (↓ Wisdom: should abstract)")

        # Check parameter count
        func_match = re.search(r'def\s+\w+\((.*?)\):', code)
        if func_match:
            params = [p.strip() for p in func_match.group(1).split(',') if p.strip()]
            if len(params) > 5:
                issues["wisdom"].append(f"{len(params)} parameters (↓ Wisdom: should use objects)")

        return issues

    def add_docstring(self, code: str) -> str:
        """Add docstring to function (↑ Love)."""
        # Find function definition
        match = re.search(r'(def\s+(\w+)\((.*?)\):)', code)
        if not match:
            return code

        func_line, func_name, params = match.groups()

        # Generate docstring based on function name
        docstring = f'''    """
    {func_name.replace('_', ' ').title()}.

    Refactored with LJPW guidance for improved quality.
    """
'''

        # Insert after function definition
        return code.replace(func_line, func_line + '\n' + docstring)

    def add_type_hints(self, code: str) -> str:
        """Add type hints to function (↑ Love: clarity)."""
        # Simple heuristic type hints
        code = re.sub(r'def\s+(\w+)\((.*?)\):',
                     lambda m: f'def {m.group(1)}({self._add_param_types(m.group(2))}) -> dict:',
                     code)
        return code

    def _add_param_types(self, params: str) -> str:
        """Add types to parameters based on names."""
        if not params.strip():
            return params

        typed_params = []
        for param in params.split(','):
            param = param.strip()
            if ':' in param:  # Already typed
                typed_params.append(param)
                continue

            # Heuristic typing based on common names
            if any(word in param for word in ['name', 'email', 'address', 'phone']):
                typed_params.append(f'{param}: str')
            elif any(word in param for word in ['age', 'count', 'quantity', 'id']):
                typed_params.append(f'{param}: int')
            elif any(word in param for word in ['price', 'total', 'discount', 'weight']):
                typed_params.append(f'{param}: float')
            elif any(word in param for word in ['user', 'data', 'config']):
                typed_params.append(f'{param}: dict')
            elif any(word in param for word in ['users', 'items', 'results']):
                typed_params.append(f'{param}: list')
            else:
                typed_params.append(param)

        return ', '.join(typed_params)

    def add_validation(self, code: str) -> str:
        """Add input validation (↑ Justice)."""
        # Find function definition and parameters
        match = re.search(r'def\s+\w+\((.*?)\):', code)
        if not match:
            return code

        params = [p.split(':')[0].strip() for p in match.group(1).split(',') if p.strip()]

        # Generate validation based on parameter types
        validations = []
        for param in params:
            if any(word in param for word in ['name', 'email']):
                validations.append(f'''    if not {param} or not {param}.strip():
        raise ValueError("{param.title()} is required")''')
            elif 'email' in param:
                validations.append(f'''    if "@" not in {param}:
        raise ValueError("Invalid email format")''')
            elif any(word in param for word in ['age', 'quantity', 'count']):
                validations.append(f'''    if {param} < 0:
        raise ValueError("{param.title()} cannot be negative")''')
            elif any(word in param for word in ['price', 'total']):
                validations.append(f'''    if {param} < 0:
        raise ValueError("{param.title()} cannot be negative")''')

        if validations:
            validation_block = '\n\n    # Validation (Justice)\n' + '\n'.join(validations) + '\n'
            # Insert after docstring or function def
            code = re.sub(r'(""".*?""")', lambda m: m.group(1) + validation_block, code, flags=re.DOTALL)
            if '"""' not in code:  # No docstring
                code = re.sub(r'(def\s+\w+\(.*?\):)', lambda m: m.group(1) + validation_block, code)

        return code

    def extract_constants(self, code: str) -> Tuple[str, str]:
        """Extract magic numbers to constants (↑ Wisdom)."""
        # Find magic numbers
        numbers = re.findall(r'\b(\d+\.?\d*)\b', code)
        magic_numbers = [n for n in numbers if float(n) not in [0, 1]]

        if not magic_numbers:
            return "", code

        # Generate constants
        constants = []
        for i, num in enumerate(set(magic_numbers)):
            const_name = f'CONSTANT_{i+1}'
            constants.append(f'{const_name} = {num}')
            code = code.replace(num, const_name, 1)

        return '\n'.join(constants) + '\n\n', code

    def add_logging(self, code: str) -> str:
        """Add logging for observability (↑ Love)."""
        # Find function name
        match = re.search(r'def\s+(\w+)\(', code)
        if not match:
            return code

        func_name = match.group(1)

        # Add logging before return
        log_statement = f'    print(f"[LOG] {func_name} completed successfully")'

        # Insert before last return
        lines = code.split('\n')
        for i in range(len(lines) - 1, -1, -1):
            if 'return' in lines[i]:
                lines.insert(i, log_statement)
                break

        return '\n'.join(lines)

    def refactor_code(self, code: str) -> Dict:
        """
        Automatically refactor code to improve LJPW.

        Returns:
            dict with 'refactored_code', 'improvements', 'issues_fixed'
        """
        original_code = code
        issues = self.analyze_code_issues(code)
        improvements = []

        # Apply refactorings based on issues
        constants_code = ""

        # Love improvements
        if any('docstring' in i for i in issues['love']):
            code = self.add_docstring(code)
            improvements.append("Added docstring (↑ Love)")

        if any('type hints' in i for i in issues['love']):
            code = self.add_type_hints(code)
            improvements.append("Added type hints (↑ Love)")

        if any('logging' in i for i in issues['love']):
            code = self.add_logging(code)
            improvements.append("Added logging (↑ Love)")

        # Justice improvements
        if issues['justice']:
            code = self.add_validation(code)
            improvements.append(f"Added validation ({len(issues['justice'])} checks) (↑ Justice)")

        # Wisdom improvements
        if any('magic' in i for i in issues['wisdom']):
            constants_code, code = self.extract_constants(code)
            improvements.append("Extracted constants (↑ Wisdom)")

        # Combine constants and code
        refactored = constants_code + code if constants_code else code

        return {
            "original": original_code,
            "refactored": refactored,
            "issues_found": issues,
            "improvements": improvements,
            "total_issues": sum(len(v) for v in issues.values()),
            "total_improvements": len(improvements)
        }


def demonstrate_auto_refactoring():
    """Demonstrate automatic refactoring on bad code."""

    print("╔" + "═" * 78 + "╗")
    print("║" + "LJPW-GUIDED AUTOMATIC CODE REFACTORER".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")

    refactorer = LJPWRefactorer()

    # Example: Bad code with multiple issues
    bad_code = '''def process_order(n, e, p, q):
    t = p * q
    d = t * 0.1
    f = t - d
    return f
'''

    print("ORIGINAL CODE (Low LJPW):")
    print("─" * 80)
    print(bad_code)

    # Analyze
    result = refactorer.refactor_code(bad_code)

    print("\nISSUES FOUND:")
    print("─" * 80)
    for dim, issues in result['issues_found'].items():
        if issues:
            print(f"\n{dim.upper()}:")
            for issue in issues:
                print(f"  ⚠️  {issue}")

    print(f"\nTotal issues: {result['total_issues']}")

    print("\n\nREFACTORED CODE (Improved LJPW):")
    print("─" * 80)
    print(result['refactored'])

    print("\nIMPROVEMENTS APPLIED:")
    print("─" * 80)
    for improvement in result['improvements']:
        print(f"  ✅ {improvement}")

    print(f"\nTotal improvements: {result['total_improvements']}")

    print("\n" + "=" * 80)
    print("KEY PRINCIPLES:")
    print("=" * 80)
    print()
    print("Low L (Love) → Add integration:")
    print("  - Docstrings (help developers)")
    print("  - Type hints (clarity)")
    print("  - Logging (observability)")
    print()
    print("Low J (Justice) → Add safety:")
    print("  - Input validation")
    print("  - Error handling")
    print("  - Boundary checks")
    print()
    print("Low W (Wisdom) → Add structure:")
    print("  - Extract constants")
    print("  - Create abstractions")
    print("  - Domain objects")
    print()
    print("This moves code toward autopoietic thresholds: L > 0.7, H > 0.6")
    print()


if __name__ == "__main__":
    demonstrate_auto_refactoring()
