# AgentLife — macOS Install Guide

Install AgentLife on macOS 13 (Ventura) or later.

## Prerequisites

- **Python 3.10+** — macOS may include Python 3.9 or older. Install via Homebrew:
- **curl** — included with macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.10+
brew install python@3.11
```

Verify:
```bash
python3 --version  # Should show 3.10+
```

## Option A: One-Liner Install (Recommended)

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Option B: Manual Install

### Step 1: Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen Terminal, or run:
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

### Step 5: Enable Auto-Start (Launchd)

Create a LaunchAgent so Hermes starts on login:

```bash
mkdir -p ~/Library/LaunchAgents/
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

launchctl load ~/Library/LaunchAgents/com.nousresearch.hermes.plist
```

## Verify

```bash
agentlife verify
```

Expected output: all checks pass.

---

*Need help? Open an issue on GitHub or join the community Discord.*