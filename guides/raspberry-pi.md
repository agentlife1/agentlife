# AgentLife — Raspberry Pi Install Guide
#
# What this guide does: Walks you through installing AgentLife on a
# Raspberry Pi 4 or 5 (the most common single-board computers people
# run personal AI agents on). The Pi is a low-power, always-on box
# perfect for hosting your Life Ops persona 24/7.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run — copy-paste them into the Pi's terminal (or SSH into it first).

Install AgentLife on a Raspberry Pi 4 or 5 running Raspberry Pi OS (64-bit).

## Prerequisites

# What this does: These are the hardware and OS requirements. Raspberry
# Pi 3 will technically run, but it's slow. You NEED 64-bit OS because
# many MCP servers and Python wheels only ship 64-bit builds now.
- **Raspberry Pi 4 or 5** (Pi 3 may work but is not recommended)
- **Raspberry Pi OS (64-bit)** — check with `uname -m` (should show `aarch64`)
- **Python 3.10+**

```bash
# What this does: Updates every package on the Pi to its latest
# version. On a freshly-flashed Pi this can take several minutes. `-y`
# auto-answers "are you sure?" prompts.
# Update system
sudo apt update && sudo apt upgrade -y

# What this does: Installs Python 3, pip, the venv module, and curl
# from the apt repository. These are the same prerequisites the Linux
# guide covers.
# Install Python and curl
sudo apt install -y python3 python3-pip python3-venv curl

# What this does: Prints the installed Python version. You should see
# something like "Python 3.11.x" or higher.
# Verify
python3 --version  # Should show 3.10+
```

## Option A: One-Liner Install (Recommended)

# What this does: Downloads and runs the official AgentLife install
# script. The installer auto-detects Raspberry Pi and applies the right
# configuration (aarch64 wheels, lower memory limits, etc.).
```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

The installer auto-detects Raspberry Pi and applies the right configuration.

## Option B: Manual Install

# What this does: Six steps that mirror the Linux manual install, plus
# an optional Step 6 for accessing the Pi from your other devices.

### Step 1: Install pipx

# What this does: pipx installs Python CLI tools in isolated
# environments so their dependencies can't conflict with each other or
# with system Python. `--user` puts it in your home directory.
```bash
python3 -m pip install --user pipx

# What this does: pipx ensurepath adds `~/.local/bin` to your PATH so
# you can run `pipx` and the tools it installs without typing the full
# path every time.
python3 -m pipx ensurepath
```

# What this does: pipx installs a "shim" for each tool in `~/.local/bin`.
# Your current shell doesn't know about that directory yet, so either
# open a new terminal window, or export PATH for this session only.
Close and reopen your terminal, or run:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Step 2: Install Hermes Agent

# What this does: pipx downloads the hermes-agent package, creates a
# dedicated virtualenv for it, and links the `hermes` command into
# `~/.local/bin`.
```bash
pipx install hermes-agent
```

### Step 3: Start Hermes

# What this does: Launches the hermes agent as a long-running background
# process. It will keep running until you stop it, listening for
# commands and running scheduled jobs.
```bash
hermes daemon
```

### Step 4: Install AgentLife

# What this does: Installs the AgentLife framework into the same Python
# environment, then runs `agentlife setup` which interactively configures
# your API keys, persona selection, and channels.
```bash
pip install agentlife
agentlife setup
```

### Step 5: Enable Auto-Start (Systemd)

# What this does: Creates a "user systemd service" so hermes starts
# automatically every time you log in (or on boot, depending on your
# Pi's configuration). systemd is the init system used by Raspberry Pi
# OS Bookworm and later.
```bash
# What this does: Creates the directory systemd looks in for user-level
# service definitions. The `-p` flag prevents an error if it already
# exists.
mkdir -p ~/.config/systemd/user/

# What this does: Writes a small service file called `hermes.service`
# into that directory. The `<< 'EOF'` ... `EOF` is a bash "heredoc" —
# everything between the two EOF markers is written verbatim to the
# file. The systemd unit tells the Pi:
#   - Wait for the network to be up before starting (`After=network.target`)
#   - Run the hermes daemon (`ExecStart=%h/.local/bin/hermes daemon`)
#   - Restart automatically if it crashes (`Restart=on-failure`)
#   - Restart after a 5-second pause (`RestartSec=5`)
#   - Start on login (`WantedBy=default.target`)
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

# What this does: Tells systemd to re-read its config files (so it sees
# the new service file), then `enable --now` both enables the service
# to start on boot AND starts it right now.
systemctl --user daemon-reload
systemctl --user enable --now hermes.service
```

### Step 6: Access from Other Devices (Optional)

# What this does: Tailscale is a "zero-config VPN" that creates an
# encrypted tunnel between your devices. It assigns each device a
# stable 100.x.x.x IP that you can reach from anywhere — without
# exposing your Pi to the public internet.
Install [Tailscale](https://tailscale.com/download) for secure remote access:

```bash
# What this does: Downloads and runs the official Tailscale install
# script, which adds the Tailscale apt repo and installs the daemon.
curl -fsSL https://tailscale.com/install.sh | sh

# What this does: Authenticates this Pi with your Tailscale account
# and brings up the WireGuard tunnel. It'll print a URL — open it in
# any browser to sign in.
sudo tailscale up
```

# What this does: Once Tailscale is up, the Pi gets a 100.x.x.x address
# on your private "tailnet". Open this URL from any device on the same
# tailnet to reach the Hermes dashboard.
Then access your Hermes dashboard from any device on your tailnet at:
`http://<raspberry-pi-tailscale-ip>:9119`

## Verify

# What this does: Runs a diagnostic that checks Python version, hermes
# installation, MCP dependencies, persona config, and channel
# connectivity. You should see all checks pass.
```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*
