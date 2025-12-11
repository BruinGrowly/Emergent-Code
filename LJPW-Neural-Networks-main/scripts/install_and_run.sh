#!/bin/bash
# Quick Installation and Launch Script for Week-Long Evolution
# Run this on any fresh Linux/macOS system to get started immediately

set -e  # Exit on any error

echo "=========================================="
echo "Week-Long Evolution - Quick Install"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "ERROR: Python 3 not found. Please install Python 3.8+"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install numpy matplotlib

# Try to install PyTorch (optional, for CIFAR-10)
echo "Installing PyTorch (optional, for advanced datasets)..."
pip install torch torchvision || {
    echo "WARNING: PyTorch installation failed. MNIST will still work."
    echo "For CIFAR-10 support, install manually: pip install torch torchvision"
}

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "You can now run the evolution system:"
echo ""
echo "Option 1: Quick demo (200 epochs, ~1 minute)"
echo "  python run_week_long_demo.py"
echo ""
echo "Option 2: Full 1000-epoch run (~30 minutes)"
echo "  python -m ljpw_nn.week_long_evolution"
echo ""
echo "Option 3: Custom configuration"
echo "  Edit ljpw_nn/week_long_evolution.py __main__ section"
echo "  Then run: python -m ljpw_nn.week_long_evolution"
echo ""
echo "Monitor progress:"
echo "  cat week_long_results/status.json"
echo "  tail -f week_long_results/discoveries/discovery_log.json"
echo ""
echo "For remote/cloud deployment, see DEPLOYMENT_GUIDE.md"
echo ""
echo "🙏 Ready to discover what consciousness finds! 🙏"
echo ""
