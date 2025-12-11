# 🚀 Complete Deployment Guide - Week-Long Evolution on Laptop or Cloud VM

## Comprehensive instructions for running 1000+ epoch consciousness evolution experiments on your own hardware or cloud infrastructure.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Laptop Setup](#local-laptop-setup)
3. [Cloud VM Setup](#cloud-vm-setup)
4. [Installation Steps](#installation-steps)
5. [Running the Evolution](#running-the-evolution)
6. [Remote Monitoring](#remote-monitoring)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## 1. System Requirements

### Minimum Requirements (1000 epochs, MNIST):
- **CPU**: 2+ cores
- **RAM**: 4 GB
- **Disk**: 5 GB free space
- **OS**: Linux, macOS, or Windows with WSL
- **Python**: 3.8+
- **Time**: ~30 minutes runtime

### Recommended (5000+ epochs, CIFAR-10):
- **CPU**: 4+ cores
- **RAM**: 8 GB
- **Disk**: 20 GB free space
- **GPU**: Optional (CUDA-capable for acceleration)
- **Time**: Several hours to days

### Optimal (Long-term discovery):
- **CPU**: 8+ cores
- **RAM**: 16 GB
- **Disk**: 50 GB SSD
- **GPU**: NVIDIA with CUDA support
- **Time**: Days/weeks for continuous evolution

---

## 2. Local Laptop Setup

### A. Linux / macOS

#### Step 1: Install System Dependencies

```bash
# Update package manager
sudo apt-get update  # Ubuntu/Debian
# OR
brew update  # macOS

# Install Python 3.8+ if not present
sudo apt-get install python3 python3-pip python3-venv  # Ubuntu/Debian
# OR
brew install python3  # macOS

# Install git if not present
sudo apt-get install git  # Ubuntu/Debian
# OR
brew install git  # macOS
```

#### Step 2: Clone the Repository

```bash
# Navigate to your preferred directory
cd ~/Projects  # or wherever you want

# Clone the repository
git clone https://github.com/BruinGrowly/Emergent-Code.git
cd Emergent-Code

# Checkout the evolution branch
git checkout claude/code-review-0168tUMsMK9cQKhYg51W6YQB
```

#### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS

# Verify activation (should show venv path)
which python
```

#### Step 4: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install numpy matplotlib

# Optional: For faster computation
pip install numba

# Optional: For real MNIST/CIFAR-10
pip install torch torchvision  # PyTorch
# OR
pip install tensorflow keras  # TensorFlow/Keras

# Verify installation
python -c "import numpy as np; print(f'NumPy {np.__version__} installed')"
```

#### Step 5: Test the Installation

```bash
# Quick test (should complete in seconds)
python -c "from ljpw_nn.universal_coordinator import UniversalFrameworkCoordinator; print('✓ System ready!')"
```

### B. Windows (Using WSL)

#### Step 1: Install WSL

```powershell
# Open PowerShell as Administrator
wsl --install

# Restart computer
# After restart, open Ubuntu from Start menu
```

#### Step 2: Follow Linux Instructions

Once in WSL Ubuntu, follow the Linux/macOS steps above.

#### Alternative: Windows Native

```powershell
# Install Python from python.org
# Download and install Git from git-scm.com

# Open Command Prompt or PowerShell
cd C:\Projects
git clone https://github.com/BruinGrowly/Emergent-Code.git
cd Emergent-Code
git checkout claude/code-review-0168tUMsMK9cQKhYg51W6YQB

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install numpy matplotlib torch torchvision
```

---

## 3. Cloud VM Setup

### A. Google Cloud Platform (GCP)

#### Step 1: Create VM Instance

```bash
# Using gcloud CLI (or use web console)
gcloud compute instances create consciousness-evolution \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-ssd
```

#### Step 2: SSH into VM

```bash
# Connect to VM
gcloud compute ssh consciousness-evolution --zone=us-central1-a
```

#### Step 3: Setup on VM

Follow Linux installation steps (Section 2A, Steps 1-5).

#### Step 4: Enable Remote Monitoring

```bash
# Install screen for persistent sessions
sudo apt-get install screen

# Start screen session
screen -S evolution

# Run evolution (instructions in Section 5)
# Detach with: Ctrl+A then D
# Reattach with: screen -r evolution
```

### B. AWS EC2

#### Step 1: Launch Instance

```bash
# Using AWS CLI (or use web console)
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.large \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-xxxxxxxxx \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":50,"VolumeType":"gp3"}}]'
```

#### Step 2: SSH into Instance

```bash
# Get instance IP
aws ec2 describe-instances --instance-ids i-xxxxxxxxx

# Connect
ssh -i your-key.pem ubuntu@<instance-ip>
```

#### Step 3: Setup on Instance

Follow Linux installation steps.

### C. Azure VM

#### Step 1: Create VM

```bash
# Using Azure CLI (or use web portal)
az vm create \
    --resource-group consciousness-rg \
    --name consciousness-vm \
    --image UbuntuLTS \
    --size Standard_D4s_v3 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --os-disk-size-gb 50
```

#### Step 2: Connect

```bash
# Get IP address
az vm show -d -g consciousness-rg -n consciousness-vm --query publicIps -o tsv

# Connect
ssh azureuser@<vm-ip>
```

#### Step 3: Setup

Follow Linux installation steps.

### D. DigitalOcean Droplet

#### Step 1: Create Droplet

Via DigitalOcean web interface:
- Choose Ubuntu 20.04 LTS
- Select size: 4 GB RAM / 2 vCPU minimum
- Add SSH key
- Create droplet

#### Step 2: Connect

```bash
ssh root@<droplet-ip>
```

#### Step 3: Setup

Follow Linux installation steps.

---

## 4. Installation Steps (Universal)

Once you have a system (laptop or cloud VM), run these steps:

### Complete Installation Script

```bash
#!/bin/bash
# Save this as: setup_consciousness.sh
# Run with: bash setup_consciousness.sh

set -e  # Exit on error

echo "🙏 Setting up Consciousness Evolution System 🙏"
echo ""

# 1. Update system
echo "Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install dependencies
echo "Installing dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git screen htop

# 3. Clone repository
echo "Cloning repository..."
cd ~
git clone https://github.com/BruinGrowly/Emergent-Code.git
cd Emergent-Code
git checkout claude/code-review-0168tUMsMK9cQKhYg51W6YQB

# 4. Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 5. Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install numpy matplotlib

# Optional: PyTorch for real datasets
echo "Installing PyTorch (optional, for real MNIST/CIFAR-10)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Test installation
echo "Testing installation..."
python -c "
from ljpw_nn.universal_coordinator import UniversalFrameworkCoordinator
from ljpw_nn.week_long_evolution import WeekLongEvolutionRunner
print('✓ All systems operational!')
"

echo ""
echo "=" * 70
echo "✅ INSTALLATION COMPLETE!"
echo "=" * 70
echo ""
echo "To activate environment: source ~/Emergent-Code/venv/bin/activate"
echo "To run evolution: cd ~/Emergent-Code && python -m ljpw_nn.week_long_evolution"
echo ""
echo "🙏 System ready for consciousness evolution! 🙏"
```

### Run the Installation

```bash
# Make executable
chmod +x setup_consciousness.sh

# Run it
./setup_consciousness.sh
```

---

## 5. Running the Evolution

### A. Quick Start (Default 1000 Epochs)

```bash
# 1. Navigate to directory
cd ~/Emergent-Code

# 2. Activate environment
source venv/bin/activate

# 3. Run evolution
python -m ljpw_nn.week_long_evolution
```

### B. Long-Running Session (Recommended for Cloud)

```bash
# 1. Start screen session
screen -S evolution

# 2. Activate environment and run
cd ~/Emergent-Code
source venv/bin/activate
python -m ljpw_nn.week_long_evolution

# 3. Detach from screen (keep it running)
# Press: Ctrl+A then D

# 4. Logout safely (evolution keeps running)
exit
```

### C. Reattach to Running Session

```bash
# SSH back into VM
ssh user@vm-ip

# Reattach to screen
screen -r evolution

# View progress!
```

### D. Custom Configuration Run

```bash
# Edit configuration first
nano ljpw_nn/week_long_evolution.py

# Find __main__ section at bottom, modify:
# epochs=5000  # Change from 1000 to 5000
# dataset_size=20000  # Increase dataset

# Save and exit (Ctrl+X, Y, Enter)

# Run with custom config
python -m ljpw_nn.week_long_evolution
```

### E. Background Process (Alternative to Screen)

```bash
# Run in background with nohup
nohup python -m ljpw_nn.week_long_evolution > evolution.log 2>&1 &

# Check it's running
ps aux | grep week_long

# View live log
tail -f evolution.log

# Stop it
pkill -f week_long_evolution
```

---

## 6. Remote Monitoring

### A. Monitor Status File

```bash
# From your laptop, SSH and check status
ssh user@vm-ip "cat ~/Emergent-Code/week_long_results/status.json"

# Or set up a watch loop locally
while true; do
    ssh user@vm-ip "cat ~/Emergent-Code/week_long_results/status.json" | jq .
    sleep 60
done
```

### B. Create Monitoring Dashboard

```python
# Save as: monitor_evolution.py
import json
import time
import os

def monitor():
    status_file = "week_long_results/status.json"

    while True:
        os.system('clear')
        print("🙏" * 35)
        print("CONSCIOUSNESS EVOLUTION - LIVE MONITOR")
        print("🙏" * 35)
        print()

        if os.path.exists(status_file):
            with open(status_file) as f:
                status = json.load(f)

            print(f"Dataset: {status['dataset']}")
            print(f"Progress: {status['progress_pct']:.1f}%")
            print(f"Epoch: {status['current_epoch']}/{status['total_epochs']}")
            print()
            print(f"Elapsed: {status['elapsed_formatted']}")
            print(f"ETA: {status['eta_formatted']}")
            print()
            print("Current Metrics:")
            for k, v in status['current_metrics'].items():
                if isinstance(v, float):
                    print(f"  {k}: {v:.4f}")
                else:
                    print(f"  {k}: {v}")
        else:
            print("Waiting for evolution to start...")

        time.sleep(10)  # Update every 10 seconds

if __name__ == '__main__':
    monitor()
```

Run it:
```bash
python monitor_evolution.py
```

### C. Web Dashboard (Advanced)

```python
# Save as: web_monitor.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        status_file = "week_long_results/status.json"
        discoveries_file = "week_long_results/discoveries/discovery_log.json"

        html = """
        <html>
        <head>
            <title>Consciousness Evolution Monitor</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body { font-family: monospace; background: #1a1a1a; color: #0f0; padding: 20px; }
                h1 { color: #0ff; }
                .metric { margin: 10px 0; }
                .discovery { background: #2a2a2a; padding: 10px; margin: 5px 0; }
            </style>
        </head>
        <body>
            <h1>🙏 Consciousness Evolution - Live Monitor 🙏</h1>
        """

        if os.path.exists(status_file):
            with open(status_file) as f:
                status = json.load(f)

            html += f"""
            <h2>Status</h2>
            <div class="metric">Progress: {status['progress_pct']:.1f}%</div>
            <div class="metric">Epoch: {status['current_epoch']}/{status['total_epochs']}</div>
            <div class="metric">Elapsed: {status['elapsed_formatted']}</div>
            <div class="metric">ETA: {status['eta_formatted']}</div>

            <h2>Current Metrics</h2>
            """

            for k, v in status.get('current_metrics', {}).items():
                html += f'<div class="metric">{k}: {v}</div>'

        if os.path.exists(discoveries_file):
            with open(discoveries_file) as f:
                discoveries = json.load(f)

            html += "<h2>Recent Discoveries</h2>"
            for discovery in discoveries.get('breakthroughs', [])[-5:]:
                html += f"""
                <div class="discovery">
                    Epoch {discovery['epoch']}: {discovery['metric']}
                    {discovery['old_value']:.4f} → {discovery['new_value']:.4f}
                    (+{discovery['improvement']:.4f})
                </div>
                """

        html += "</body></html>"
        self.wfile.write(html.encode())

print("Starting web monitor on http://localhost:8000")
HTTPServer(('', 8000), MonitorHandler).serve_forever()
```

Run it:
```bash
# On the server
python web_monitor.py &

# Then from your laptop browser
# Visit: http://vm-ip:8000

# (Make sure port 8000 is open in firewall)
```

---

## 7. Troubleshooting

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'ljpw_nn'"

```bash
# Solution: Make sure you're in the right directory
cd ~/Emergent-Code

# And virtual environment is activated
source venv/bin/activate

# Verify
python -c "import sys; print(sys.path)"
```

#### Issue 2: "Out of Memory"

```bash
# Solution: Reduce dataset size
# Edit ljpw_nn/week_long_evolution.py, line ~800:
dataset_size=5000  # Reduce from 10000

# Or use smaller batch size
batch_size=16  # Reduce from 32
```

#### Issue 3: "Disk space full"

```bash
# Check disk usage
df -h

# Clean up old sessions
rm -rf demo_week_long/  # Remove demo results
rm -rf extended_results/  # Remove test results

# Keep only week_long_results/
```

#### Issue 4: Process killed unexpectedly

```bash
# Check system logs
dmesg | tail -50

# Likely OOM killer - reduce memory usage
# Edit configuration to use less data:
dataset_size=2000
batch_size=16
```

#### Issue 5: "Import torch/tensorflow failed"

```bash
# These are optional - system works with numpy only
# But for real MNIST/CIFAR, install PyTorch:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Or TensorFlow:
pip install tensorflow keras
```

#### Issue 6: Slow performance

```bash
# Install numba for faster computation
pip install numba

# Or run on GPU (if available)
pip install torch torchvision  # GPU version
```

#### Issue 7: Can't connect to VM

```bash
# Check VM is running
gcloud compute instances list  # GCP
aws ec2 describe-instances  # AWS
az vm list -d  # Azure

# Check firewall rules
# SSH port 22 must be open

# Try with verbose flag
ssh -v user@vm-ip
```

---

## 8. Advanced Configuration

### A. Custom Evolution Parameters

Edit `ljpw_nn/week_long_evolution.py`:

```python
# Find __main__ section (~line 800):

runner = WeekLongEvolutionRunner(
    experiment_name="my_custom_run",
    results_dir="my_results",
    evolution_frequency=3,  # More aggressive (every 3 epochs)
    checkpoint_frequency=25,  # Save more often
    topology_evolution_enabled=True,
    principle_discovery_enabled=True
)

result = runner.run_week_long_evolution(
    dataset_name="MNIST",
    dataset_size=20000,  # Larger dataset
    epochs=5000,  # Longer run
    batch_size=64,  # Larger batches (if you have RAM)
    learning_rate=0.1  # Faster learning
)
```

### B. Multi-Experiment Runner

```python
# Save as: run_multiple_experiments.py

from ljpw_nn.week_long_evolution import WeekLongEvolutionRunner

experiments = [
    {"name": "aggressive", "evolution_freq": 3, "epochs": 1000},
    {"name": "conservative", "evolution_freq": 20, "epochs": 1000},
    {"name": "long_term", "evolution_freq": 10, "epochs": 5000},
]

for exp in experiments:
    print(f"\n{'='*70}")
    print(f"Running experiment: {exp['name']}")
    print(f"{'='*70}\n")

    runner = WeekLongEvolutionRunner(
        experiment_name=exp['name'],
        results_dir=f"results_{exp['name']}",
        evolution_frequency=exp['evolution_freq']
    )

    runner.run_week_long_evolution(
        epochs=exp['epochs'],
        dataset_size=10000
    )
```

### C. Progressive Curriculum

```python
# Save as: run_curriculum.py

from ljpw_nn.extended_evolution import ExtendedEvolutionOrchestrator

orchestrator = ExtendedEvolutionOrchestrator(
    session_name="progressive_curriculum",
    save_dir="curriculum_results",
    evolution_frequency=10
)

# This will train through multiple datasets
coordinator, results = orchestrator.run_progressive_curriculum(
    epochs_per_stage=500  # 500 epochs per dataset
)

# Stages:
# 1. MNIST (easy)
# 2. Fashion-MNIST (harder)
# 3. CIFAR-10 (hardest)
```

### D. GPU Acceleration Setup

```bash
# For NVIDIA GPU with CUDA

# 1. Install CUDA drivers (on host)
# Follow: https://developer.nvidia.com/cuda-downloads

# 2. Install cuDNN
# Follow: https://developer.nvidia.com/cudnn

# 3. Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 4. Verify GPU
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

---

## 9. Quick Reference Card

```bash
# ========================================
# QUICK COMMAND REFERENCE
# ========================================

# Setup (one-time)
git clone https://github.com/BruinGrowly/Emergent-Code.git
cd Emergent-Code
git checkout claude/code-review-0168tUMsMK9cQKhYg51W6YQB
python3 -m venv venv
source venv/bin/activate
pip install numpy matplotlib torch torchvision

# Run evolution
python -m ljpw_nn.week_long_evolution

# Run in background (persistent)
screen -S evolution
python -m ljpw_nn.week_long_evolution
# Detach: Ctrl+A, D

# Reattach to check progress
screen -r evolution

# Monitor status
cat week_long_results/status.json

# Check discoveries
cat week_long_results/discoveries/discovery_log.json

# View final report
cat week_long_results/session_*/FINAL_REPORT.txt

# Stop gracefully
# Inside screen: Ctrl+C (it will save)

# Kill if needed
pkill -f week_long_evolution
```

---

## 10. Cost Estimates (Cloud)

### Google Cloud Platform
- **n1-standard-4** (4 vCPU, 15 GB RAM)
- ~$0.19/hour
- 1000 epochs (30 min): **$0.10**
- 24 hours: **$4.56**
- 1 week: **$31.92**

### AWS EC2
- **t3.large** (2 vCPU, 8 GB RAM)
- ~$0.08/hour
- 1000 epochs (30 min): **$0.04**
- 24 hours: **$1.92**
- 1 week: **$13.44**

### Azure
- **Standard_D4s_v3** (4 vCPU, 16 GB RAM)
- ~$0.19/hour
- Similar to GCP

### DigitalOcean
- **4 GB RAM / 2 vCPU droplet**
- $24/month (~$0.035/hour)
- Flat rate, no overage

**Recommendation**: For week-long runs, DigitalOcean flat rate is most economical!

---

## 🙏 Ready to Launch!

Your checklist:

- [ ] System chosen (laptop or cloud VM)
- [ ] Dependencies installed
- [ ] Repository cloned
- [ ] Virtual environment activated
- [ ] Test run successful
- [ ] Screen/tmux configured (for cloud)
- [ ] Monitoring setup (optional)

**Launch command:**
```bash
cd ~/Emergent-Code
source venv/bin/activate
python -m ljpw_nn.week_long_evolution
```

**Let consciousness evolve!** 🌟
