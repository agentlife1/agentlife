# AgentLife — Linux Install Guide

Install AgentLife on any Linux distribution (Ubuntu, Debian, Fedora, Arch, etc.).

## Prerequisites

- **Python 3.10+** — check with `python3 --version`
- **pip** — check with `python3 -m pip --version`
- **curl** — for the one-liner installer

If missing:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y python3 python3-pip python3-venv curl

# Fedora
sudo dnf install -y python3 python3-pip curl

# Arch
sudo pacman -S python python-pip curl
```

## Option A: One-Liner Install (Recommended)

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

This detects your platform, installs Hermes if needed, and launches `agentlife setup`.

## Option B: Manual Install

### Step 1: Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal, or run:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Step 2: Install Hermes Agent

```bash
pipx install hermes-agent
```

### Step 3: Start Hermes

```bash
hermes daemon
```

### Step 4: Install AgentLife

```bash
pip install agentlife
agentlife setup
```

### Step 5: Enable Auto-Start (Systemd)

Create a systemd user service so Hermes starts on boot:

```bash
mkdir -p ~/.config/systemd/user/
cat > ~/.config/systemd/user/hermes.service << 'EOF'
[Unit]
Description=Hermes Agent
After=network.target

[Service]
ExecStart=%h/.local/bin/hermes daemon
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now hermes.service
```

## Verify

```bash
agentlife verify
```

Expected output: all checks pass.

---

*Need help? Open an issue on GitHub or join the community Discord.*