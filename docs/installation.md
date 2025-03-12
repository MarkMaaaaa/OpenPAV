# Installation Guide

## Requirements

### Hardware Requirements
- **CPU**: Minimum 4 cores (Intel i5 or higher recommended)
- **RAM**: At least 8GB (16GB recommended for simulations)
- **Storage**: Minimum 10GB free space
- **GPU** (Optional, for AI-based models): NVIDIA GPU with CUDA support (e.g., RTX 3060 or higher)

### Software Requirements
- **Operating System**: Ubuntu 20.04/22.04 or Windows 10/11
- **Python**: Version 3.8 or later
- **Git**: Installed and configured
- **SUMO** (Optional): Required for traffic simulation
- **VISSIM** (Optional): Required for advanced microscopic simulation
- **PyTorch** (Optional): Required for AI-based model testing

---

## Local Installation

### Step 1: Clone the Open-PAV Repository
Use Git to download the Open-PAV source code:

```bash
git clone https://github.com/MarkMaaaaa/OpenPAV.git
cd OpenPAV
```

### Step 2: Install Dependencies
Ensure Python and necessary packages are installed:
```bash
pip install -r requirements.txt
```

### Step 3: Basic Test Environment
Run a simple Python simulation to verify the installation:
```bash
import numpy as np
import matplotlib.pyplot as plt

# Simple vehicle motion simulation
t = np.linspace(0, 10, 100)
velocity = 2 * t  # Linear acceleration
position = 0.5 * 2 * t**2

plt.plot(t, position, label="Vehicle Position")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.legend()
plt.grid()
plt.show()
```

If the plot appears, your environment is ready.

## Optional Components

### Option 1: Install SUMO
For SUMO users, install it as follows:
**Ubuntu:**
```bash
sudo apt-get install sumo sumo-tools sumo-doc
```

**Windows:**
- Download from [SUMO Official Website](https://sumo.dlr.de)
- Add SUMO to system PATH

### Option 2: Install VISSIM
- VISSIM is a commercial tool, and a valid license is required.
- Install from **PTV Group Website**: [https://www.ptvgroup.com](https://www.ptvgroup.com)
- Configure the Python COM interface for integration.

### Option 3: Install PyTorch (Optional for AI-based Models)
For machine learning applications, install PyTorch:

**CPU Version:**
```bash
pip install torch torchvision torchaudio
```

**GPU Version (with CUDA):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---








