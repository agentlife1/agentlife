# AgentLife — macOS Install Guide
#
# What this guide does: Walks you through installing AgentLife on macOS
# 13 (Ventura) or later. By the end, the `agentlife` CLI will be on your
# PATH and the `hermes` agent will be running as a background service
# that auto-starts every time you log in.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run — copy-paste them into your Terminal app.

Install AgentLife on macOS 13 (Ventura) or later.

## Prerequisites

# What this does: Apple's macOS sometimes ships with an old Python 3.9
# (or no Python at all). We need Python 3.10+, so we install the latest
# via Homebrew, the standard macOS package manager. `curl` is already
# pre-installed on every Mac.
- **Python 3.10+** — macOS may include Python 3.9 or older. Install via Homebrew:
- **curl** — included with macOS

```bash
# What this does: Installs Homebrew (Apple's recommended package manager)
# by downloading and running the official install script. The `/bin/bash
# -c "$(...)"` pattern is the standard, safe way to bootstrap brew —
# the script is fetched over HTTPS, and the surrounding shell quotes
# keep the URL intact even if it contains shell-special characters.
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# What this does: Tells Homebrew to download and install a recent
# Python 3. Homebrew installs into `/opt/homebrew` (Apple Silicon) or
# `/usr/local` (Intel) and links the `python3` command to that.
# Install Python 3.10+
brew install python@3.11
```

Verify:
```bash
# What this does: Prints the installed Python version. You should see
# something like "Python 3.11.x" or "Python 3.12.x". If it prints
# "Python 3.9.x" or older, Homebrew's python3 isn't first on your PATH
# — see Homebrew's post-install instructions for adding it.
python3 --version  # Should show 3.10+
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

## Option B: Manual Install

# What this does: Five short steps that install everything by hand.
# Use this if the one-liner doesn't work for your environment.

### Step 1: Install pipx

# What this does: pipx installs Python CLI tools in isolated
# environments so their dependencies can't conflict with each other or
# with system Python. `--user` puts it in your home directory so you
# don't need sudo.
```bash
python3 -m pip install --user pipx

# What this does: pipx ensurepath adds `~/Library/Python/<ver>/bin` to
# your PATH so you can run `pipx` and the tools it installs without
# typing the full path every time. On Apple Silicon Macs, the prefix
# may be `~/.local/bin` instead.
python3 -m pipx ensurepath
```

# What this does: pipx installs a "shim" for each tool in your user
# bin directory. Your current Terminal session doesn't know about that
# directory yet, so either open a new Terminal window, or export PATH
# for this session only.
Close and reopen Terminal, or run:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Step 2: Install Hermes Agent

# What this does: pipx downloads the hermes-agent package, creates a
# dedicated virtualenv for it, and links the `hermes` command into
# your user bin directory.
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

### Step 5: Enable Auto-Start (Launchd)

# What this does: Creates a LaunchAgent (macOS's equivalent of a
# systemd service) so hermes starts automatically every time you log
# in. `launchd` is macOS's init system, and `LaunchAgents` in your home
# Library run as you, not as root.
Create a LaunchAgent so Hermes starts on login:

```bash
# What this does: Creates the `~/Library/LaunchAgents` directory if it
# doesn't already exist. The `-p` flag prevents an error on rerun.
mkdir -p ~/Library/LaunchAgents/

# What this does: Writes a plist (property list) file describing the
# hermes service to launchd. The `<< 'EOF'` ... `EOF` is a bash
# "heredoc" — everything between the two EOF markers is written
# verbatim to the file. Key fields:
#   - Label           — unique name for this service
#   - ProgramArguments — the command to run (`hermes daemon`)
#   - RunAtLoad       — start as soon as launchd loads the file
#   - KeepAlive       — relaunch automatically if it exits
#   - StandardOutPath — where stdout is logged
#   - StandardErrorPath — where stderr is logged
cat > ~/Library/LaunchAgents/com.nousresearch.hermes.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nousresearch.hermes</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/hermes</string>
        <string>daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/hermes.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/hermes.stderr.log</string>
</dict>
</plist>
EOF

# What this does: Tells launchd to load the plist and start hermes
# right now (and on every subsequent login).
launchctl load ~/Library/LaunchAgents/com.nousresearch.hermes.plist
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
