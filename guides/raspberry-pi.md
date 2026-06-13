# AgentLife — Raspberry Pi Install Guide

Install AgentLife on a Raspberry Pi 4 or 5 running Raspberry Pi OS (64-bit).

## Prerequisites

- **Raspberry Pi 4 or 5** (Pi 3 may work but is not recommended)
- **Raspberry Pi OS (64-bit)** — check with `uname -m` (should show `aarch64`)
- **Python 3.10+**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and curl
sudo apt install -y python3 python3-pip python3-venv curl

# Verify
python3 --version  # Should show 3.10+
```

## Option A: One-Liner Install (Recommended)

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

The installer auto-detects Raspberry Pi and applies the right configuration.

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

### Step 6: Access from Other Devices (Optional)

Install [Tailscale](https://tailscale.com/download) for secure remote access:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Then access your Hermes dashboard from any device on your tailnet at:
`http://<raspberry-pi-tailscale-ip>:9119`

## Verify

```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*