# AgentLife — Windows (WSL2) Install Guide
#
# What this guide does: Walks you through installing AgentLife on
# Windows 10 or 11 by using WSL2 (Windows Subsystem for Linux). WSL
# runs a real Linux kernel inside Windows, so you can install
# AgentLife as if you were on a Linux box, while still having full
# access to your Windows files and browser.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run. PowerShell and bash commands are kept in separate code blocks.

Install AgentLife on Windows 10/11 using WSL2 (Windows Subsystem for Linux).

## Prerequisites

### Step 0: Install WSL2

# What this does: This PowerShell command (run as Administrator)
# installs WSL and tells it to use Ubuntu 24.04 as the default Linux
# distribution. The first time you run it, Windows will also enable
# the Hyper-V / Virtual Machine Platform features it needs.
# WSL = Windows Subsystem for Linux: lets you run a real Linux
# environment directly inside Windows, no VM or dual-boot required.
Open PowerShell as Administrator and run:

```powershell
# What this does: -d specifies the Linux distribution to install.
# You can substitute Ubuntu-22.04, Debian, or any other distro from
# the Microsoft Store if you prefer.
wsl --install -d Ubuntu-24.04
```

# What this does: WSL needs to finish initializing its kernel and
# first-boot setup, which requires a full restart. After rebooting,
# Ubuntu will launch automatically and ask you to create a Linux
# username + password — that account is separate from your Windows
# account.
Restart your computer when prompted. After reboot, Ubuntu will launch and finish setup — create a Linux username and password.

### Step 1: Update Your WSL Environment

# What this does: Now we're inside the Linux side of WSL. These
# commands install Python, pip, and curl, then verify the version.
```bash
# What this does: apt update refreshes the package index; apt upgrade
# installs the latest versions of all installed packages. The first
# run on a fresh WSL distro can take a couple of minutes.
sudo apt update && sudo apt upgrade -y

# What this does: Installs Python 3, pip, the venv module, and curl
# from the apt repository.
sudo apt install -y python3 python3-pip python3-venv curl

# What this does: Prints the installed Python version. You should see
# something like "Python 3.10.x" or higher.
python3 --version  # Should show 3.10+
```

## Option A: One-Liner Install (Inside WSL)

# What this does: Same one-liner as the Linux guide, just running
# inside WSL this time. The installer doesn't care that it's WSL —
# it just sees a Debian/Ubuntu environment.
```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Option B: Manual Install

# What this does: Five steps that mirror the Linux manual install.
# Auto-start works a little differently on WSL (no systemd by
# default) — that's covered in Step 6.

### Step 2: Install pipx

# What this does: pipx installs Python CLI tools in isolated
# environments so their dependencies can't conflict with each other.
```bash
python3 -m pip install --user pipx

# What this does: pipx ensurepath adds `~/.local/bin` to your PATH so
# you can run `pipx` and the tools it installs without typing the full
# path every time.
python3 -m pipx ensurepath
```

# What this does: pipx installs a "shim" for each tool in `~/.local/bin`.
# Your current shell doesn't know about that directory yet, so either
# open a new WSL terminal window, or export PATH for this session only.
Close and reopen your WSL terminal, or run:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Step 3: Install Hermes Agent

# What this does: pipx downloads the hermes-agent package, creates a
# dedicated virtualenv for it, and links the `hermes` command into
# `~/.local/bin`.
```bash
pipx install hermes-agent
```

### Step 4: Start Hermes

# What this does: Launches the hermes agent as a long-running
# background process. It will keep running until you stop it or
# shut down WSL.
```bash
hermes daemon
```

### Step 5: Install AgentLife

# What this does: Installs the AgentLife framework into the same
# Python environment, then runs `agentlife setup` which interactively
# configures your API keys, persona selection, and channels.
```bash
pip install agentlife
agentlife setup
```

### Step 6: Auto-Start (Optional)

# What this does: WSL doesn't have systemd enabled by default, so the
# `systemctl` approach used in the Linux guide won't work. The
# simplest workaround is to append a one-liner to your `~/.bashrc`,
# which runs every time you open a new bash shell (including when
# WSL starts).
WSL doesn't support systemd by default. To have Hermes start automatically when WSL launches, add this to your `~/.bashrc`:

```bash
# What this does: `>>` APPENDS to ~/.bashrc (doesn't overwrite it).
# The `&` at the end backgrounds the process so it doesn't block
# your shell. Next time you open a WSL terminal, hermes will start
# itself in the background.
echo 'hermes daemon &' >> ~/.bashrc
```

## Accessing from Windows

# What this does: WSL automatically forwards network ports from
# Linux to Windows, so any port Hermes listens on (e.g. 9119 for the
# dashboard) is reachable from your Windows browser at localhost.
# No firewall or port-mapping config required.
Your Hermes dashboard is available at `http://localhost:9119` — you can access it from your Windows browser directly (WSL forwards ports automatically).

## Verify

# What this does: Runs a diagnostic that checks Python version, hermes
# installation, MCP dependencies, persona config, and channel
# connectivity. You should see all checks pass.
```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*
