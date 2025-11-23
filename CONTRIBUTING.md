# Contributing to Emergent Code

Thank you for your interest in contributing to Emergent Code! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/emergent-code.git
   cd emergent-code
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original/emergent-code.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv
- Git

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   make install-dev
   # or
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Optional: Install Python Code Harmonizer

For real LJPW analysis (optional):
```bash
# Clone the harmonizer to project root
git clone <harmonizer-repo-url> Python-Code-Harmonizer-main
```

See `HARMONIZER_SETUP.md` for detailed instructions.

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-level7-experiments`
- `fix/ci-timeout-issue`
- `docs/improve-readme`
- `refactor/simplify-composition-logic`

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
```

### Development Workflow

1. Make your changes
2. Run tests: `make test`
3. Run linting: `make lint`
4. Format code: `make format`
5. Validate changes: `make validate`

Or run all checks at once:
```bash
make check
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific experiment
make level1  # Or level2, level3, etc.

# Validate fractal proof
make validate

# Test harmonizer integration
make test-harmonizer
```

### Writing Tests

- Add tests for new features in the appropriate experiment file
- Ensure tests pass before submitting PR
- Aim for meaningful test coverage

## Code Style

### Python Style Guide

This project follows:
- **Black** for code formatting (line length: 100)
- **Ruff** for linting
- **mypy** for type checking (optional but encouraged)

### Running Code Style Tools

```bash
# Format code
make format

# Check linting
make lint

# Run all checks
make check
```

### Pre-commit Hooks

Pre-commit hooks automatically format and lint your code. They run on `git commit`.

To run manually:
```bash
pre-commit run --all-files
```

### LJPW Framework Conventions

When working with LJPW code:
- Single letters `L`, `J`, `P`, `W` are acceptable for LJPW profile variables
- Single letters `l`, `j`, `p`, `w` are acceptable in mock implementations
- Use descriptive names elsewhere
- Document LJPW profiles clearly in docstrings

## Commit Messages

### Format

```
type(scope): Brief description

Detailed explanation of the changes (if needed).

Fixes #123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```
feat(level7): Add ecosystem-level composition experiments

Implements Level 7 of the fractal composition hierarchy,
demonstrating composition at the ecosystem scale.

Fixes #45
```

```
fix(ci): Remove continue-on-error from lint checks

Lint checks should fail the build if code doesn't meet
quality standards. This ensures code quality.
```

## Pull Request Process

### Before Submitting

1. ✅ All tests pass (`make test`)
2. ✅ Code is formatted (`make format`)
3. ✅ Linting passes (`make lint`)
4. ✅ Documentation updated (if needed)
5. ✅ Commit messages follow convention
6. ✅ Branch is up to date with main

### Submitting

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a pull request on GitHub

3. Fill out the PR template:
   - **Title**: Clear, descriptive title
   - **Description**: What changes and why
   - **Testing**: How you tested the changes
   - **Related Issues**: Link to related issues

### PR Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How the changes were tested.

## Checklist
- [ ] Tests pass locally
- [ ] Code is formatted with black
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Commit messages follow convention

## Related Issues
Fixes #123
```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

### After Merge

1. Delete your branch:
   ```bash
   git branch -d feature/your-feature-name
   ```

2. Update your fork:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

## Questions?

If you have questions:
- Open an issue for discussion
- Check existing documentation
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Emergent Code! 🚀
