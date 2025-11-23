#!/bin/bash
# Emergent Code - Quick Start Script
# This script helps you get up and running quickly

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Emergent Code - Quick Start Setup          ║${NC}"
echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}→${NC} Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo -e "${YELLOW}→${NC} Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}→${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Upgrade pip
echo ""
echo -e "${YELLOW}→${NC} Upgrading pip..."
pip install --upgrade pip -q
echo -e "${GREEN}✓${NC} pip upgraded"

# Install dependencies
echo ""
echo -e "${YELLOW}→${NC} Installing dependencies..."
pip install -r requirements.txt -q
echo -e "${GREEN}✓${NC} Production dependencies installed"

echo ""
read -p "Install development dependencies? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -r requirements-dev.txt -q
    echo -e "${GREEN}✓${NC} Development dependencies installed"
fi

# Install pre-commit hooks
echo ""
read -p "Install pre-commit hooks? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install pre-commit -q
    pre-commit install
    echo -e "${GREEN}✓${NC} Pre-commit hooks installed"
fi

# Run validation
echo ""
echo -e "${YELLOW}→${NC} Running validation tests..."
python3 validate_fractal_proof.py
echo ""
python3 test_harmonizer.py

# Summary
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Setup Complete! 🚀                          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "  1. Activate the virtual environment:"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo -e "  2. Run experiments:"
echo -e "     ${YELLOW}make level1${NC}  # Or level2, level3, etc."
echo -e "     ${YELLOW}make run-experiments${NC}  # Run all experiments"
echo ""
echo -e "  3. Run tests:"
echo -e "     ${YELLOW}make test${NC}"
echo ""
echo -e "  4. Format and lint code:"
echo -e "     ${YELLOW}make format${NC}  # Format code"
echo -e "     ${YELLOW}make lint${NC}    # Check linting"
echo -e "     ${YELLOW}make check${NC}   # Run all checks"
echo ""
echo -e "  5. View all available commands:"
echo -e "     ${YELLOW}make help${NC}"
echo ""
echo -e "${GREEN}Happy coding! ✨${NC}"
echo ""
