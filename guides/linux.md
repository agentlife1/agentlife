# AgentLife — Linux Install Guide
#
# What this guide does: Walks you through installing AgentLife on a Linux
# box (Ubuntu, Debian, Fedora, Arch, etc.). By the end, the `agentlife`
# CLI will be on your PATH and the `hermes` agent will be running as a
# background service that auto-starts on login.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run — copy-paste them into your terminal.

Install AgentLife on any Linux distribution (Ubuntu, Debian, Fedora, Arch, etc.).

## Prerequisites

# What this does: Sanity-checks that the three programs the installer
# depends on are already on your system. If any of them print "command
# not found", install them using the block below.
- **Python 3.10+** — check with `python3 --version`
- **pip** — check with `python3 -m pip --version`
- **curl** — for the one-liner installer

If missing:

```bash
# What this does: Installs Python 3, pip, the venv module, and curl from
# your distribution's package repository. `apt update` refreshes the
# package index so apt knows about the latest versions; `-y` auto-answers
# "are you sure?" prompts.
# Ubuntu / Debian
sudo apt update && sudo apt install -y python3 python3-pip python3-venv curl

# What this does: Same as above, but using DNF (Fedora's package manager).
# Fedora
sudo dnf install -y python3 python3-pip curl

# What this does: Same as above, but using Pacman (Arch's package manager).
# Arch
sudo pacman -S python python-pip curl
```

## Option A: One-Liner Install (Recommended)

# What this does: Downloads and runs the official AgentLife install
# script. The `| bash` part pipes the script directly into bash. The
# `sfSL` flags tell curl to fail silently on errors (-s), show nothing
# on success (-S), and follow redirects (-fL). The installer detects
# your platform, installs Hermes if needed, and launches `agentlife setup`.
```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

This detects your platform, installs Hermes if needed, and launches `agentlife setup`.

## Option B: Manual Install

# What this does: Five short steps that install everything by hand.
# Use this if the one-liner doesn't work for your environment (locked-down
# servers, air-gapped networks, custom Python versions, etc.).

### Step 1: Install pipx

# What this does: pipx installs Python CLI tools in isolated
# environments so their dependencies can't conflict with each other or
# with system Python. `--user` puts it in your home directory so you
# don't need root.
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
# process (a "daemon"). It will keep running until you stop it, listening
# for commands and running scheduled jobs.
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
# distro). `systemd` is the init system used by most modern Linux
# distributions.
Create a systemd user service so Hermes starts on boot:

```bash
# What this does: Creates the directory systemd looks in for user-level
# service definitions. The `-p` flag prevents an error if it already
# exists.
mkdir -p ~/.config/systemd/user/

# What this does: Writes a small service file called `hermes.service`
# into that directory. The `<< 'EOF'` ... `EOF` is a bash "heredoc" —
# everything between the two EOF markers is written verbatim to the
# file. The systemd unit tells Linux:
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

## Verify

# What this does: Runs a diagnostic that checks Python version, hermes
# installation, MCP dependencies, persona config, and channel
# connectivity. You should see all checks pass.
```bash
agentlife verify
```

Expected output: all checks pass.

---

*Need help? Open an issue on GitHub or join the community Discord.*
