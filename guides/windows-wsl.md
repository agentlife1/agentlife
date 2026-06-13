# AgentLife — Windows (WSL2) Install Guide

Install AgentLife on Windows 10/11 using WSL2 (Windows Subsystem for Linux).

## Prerequisites

### Step 0: Install WSL2

Open PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart your computer when prompted. After reboot, Ubuntu will launch and finish setup — create a Linux username and password.

### Step 1: Update Your WSL Environment

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv curl
python3 --version  # Should show 3.10+
```

## Option A: One-Liner Install (Inside WSL)

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Option B: Manual Install

### Step 2: Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your WSL terminal, or run:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Step 3: Install Hermes Agent

```bash
pipx install hermes-agent
```

### Step 4: Start Hermes

```bash
hermes daemon
```

### Step 5: Install AgentLife

```bash
pip install agentlife
agentlife setup
```

### Step 6: Auto-Start (Optional)

WSL doesn't support systemd by default. To have Hermes start automatically when WSL launches, add this to your `~/.bashrc`:

```bash
echo 'hermes daemon &' >> ~/.bashrc
```

## Accessing from Windows

Your Hermes dashboard is available at `http://localhost:9119` — you can access it from your Windows browser directly (WSL forwards ports automatically).

## Verify

```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*