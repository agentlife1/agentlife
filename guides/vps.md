# AgentLife — VPS Install Guide
#
# What this guide does: Walks you through installing AgentLife on a
# rented cloud server (DigitalOcean, Hetzner, Linode, AWS EC2, etc.).
# A VPS is a good fit when you want your Life Ops persona running
# 24/7 but don't want a physical box at home.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run — copy-paste them into your SSH session.

Install AgentLife on a cloud VPS (DigitalOcean, Hetzner, Linode, AWS EC2, etc.).

## Recommended Specs

# What this does: A "droplet" / "instance" / "VPS" is a virtual server.
# Life Ops is a small-footprint app, so even the cheapest tier works
# for a single user. The RAM matters most if you enable many MCP
# servers (Puppeteer especially is hungry).

| Provider | Plan | Cost |
|----------|------|------|
| DigitalOcean | Basic Droplet ($6/mo) — 1GB RAM, 25GB SSD | ~$6/mo |
| Hetzner | CX22 (~€4/mo) — 2GB RAM, 40GB SSD | ~$4/mo |
| Oracle Cloud | Free Tier — 1GB RAM, 100GB (free) | $0 |

## Prerequisites

# What this does: Ubuntu LTS versions are the best-tested base for
# AgentLife. You'll need root SSH access to the VPS to do the
# initial setup.
- **Ubuntu 22.04 or 24.04** (recommended — other distros work but these have best support)
- **Python 3.10+**
- **SSH access** to your VPS

```bash
# What this does: SSH is a secure remote shell. The first command
# opens a remote terminal session on your VPS; the rest run on the
# VPS itself.
# SSH into your VPS first
ssh root@<your-vps-ip>

# What this does: apt update refreshes the package index; apt upgrade
# installs the latest versions of all currently installed packages.
# On a freshly-provisioned VPS this can take a couple of minutes.
# Update system
apt update && apt upgrade -y

# What this does: Installs Python 3, pip, the venv module, and curl
# from the apt repository.
# Install Python and tools
apt install -y python3 python3-pip python3-venv curl

# What this does: Prints the installed Python version. You should see
# something like "Python 3.10.x" or higher.
# Verify
python3 --version
```

## Option A: One-Liner Install

# What this does: Downloads and runs the official AgentLife install
# script. Works the same on a VPS as it does on a local box.
```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Option B: Manual Install

# What this does: Seven steps covering user creation, the install
# itself, auto-start, and (most importantly) secure access. The
# default VPS has its ports exposed to the public internet, so the
# "secure access" step is critical.

### Step 1: Create a Non-Root User

# What this does: Running things as root on a server is dangerous —
# any typo or compromised dependency gets unlimited access. We create
# a dedicated user, give it sudo for occasional admin tasks, and
# switch into that user for the rest of the install.
```bash
# What this does: adduser interactively creates a new user account.
adduser agentlife

# What this does: Adds the new user to the `sudo` group so they can
# run admin commands when needed. You'll be prompted for agentlife's
# password to elevate privileges.
usermod -aG sudo agentlife

# What this does: `su -` switches to the new user; the `-` flag
# simulates a fresh login so PATH and HOME get set properly.
su - agentlife
```

### Step 2: Install pipx

# What this does: pipx installs Python CLI tools in isolated
# environments so their dependencies can't conflict with each other.
# `--user` puts it in your home directory.
```bash
python3 -m pip install --user pipx

# What this does: Adds `~/.local/bin` to PATH so you can run pipx and
# the tools it installs without typing the full path.
python3 -m pipx ensurepath
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
# background process. It will keep running until you stop it.
```bash
hermes daemon
```

### Step 5: Install AgentLife

# What this does: Installs the AgentLife framework into the same Python
# environment, then runs `agentlife setup` which interactively configures
# your API keys, persona selection, and channels.
```bash
pip install agentlife
agentlife setup
```

### Step 6: Enable Auto-Start (Systemd)

# What this does: Creates a "user systemd service" so hermes starts
# automatically every time the VPS boots. Critical for a remote server
# — you don't want to have to SSH in every time the host restarts.
```bash
# What this does: Creates the directory systemd looks in for user-level
# service definitions.
mkdir -p ~/.config/systemd/user/

# What this does: Writes a small service file called `hermes.service`
# into that directory. The `<< 'EOF'` ... `EOF` is a bash "heredoc" —
# everything between the two EOF markers is written verbatim to the
# file.
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

# What this does: Tells systemd to re-read its config files (so it
# sees the new service file), then `enable --now` both enables the
# service to start on boot AND starts it right now.
systemctl --user daemon-reload
systemctl --user enable --now hermes.service
```

### Step 7: Secure Access

# What this does: By default, the Hermes dashboard listens on a port
# (9119) that's exposed to the public internet. That's risky. We
# recommend either wrapping it in an encrypted VPN (Tailscale) or
# putting it behind HTTPS via a reverse proxy (Caddy).
**Recommended: Use Tailscale** — creates an encrypted tunnel so Hermes isn't exposed to the public internet.

```bash
# What this does: Downloads and runs the Tailscale install script,
# then authenticates this VPS with your Tailscale account.
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# What this does: Prints your VPS's private 100.x.x.x tailnet IP.
# You'll use this IP from your laptop/phone to reach the dashboard.
# Find your VPS tailscale IP
tailscale ip -4
# → 100.x.x.x

# Access Hermes from your devices
# http://100.x.x.x:9119
```

# What this does: If you'd rather use a real public URL with HTTPS,
# Caddy is a one-line reverse proxy that auto-provisions a Let's
# Encrypt certificate. You DO need a domain pointed at the VPS for
# this to work.
**Alternative: Caddy reverse proxy with HTTPS**

```bash
# What this does: Installs Caddy (a small Go web server that's also
# a reverse proxy and ACME client) from the official Cloudsmith repo.
# Install Caddy
apt install -y debian-keyring debian-archive-keyring
curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/gpg.key | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install caddy

# What this does: Writes a Caddyfile that reverse-proxies
# your-domain.com to localhost:9119 (where Hermes listens). Caddy
# automatically provisions a Let's Encrypt HTTPS cert for free.
# Configure reverse proxy
cat > /etc/caddy/Caddyfile << 'EOF'
your-domain.com {
    reverse_proxy localhost:9119
}
EOF

# What this does: Restarts Caddy so it picks up the new config.
systemctl restart caddy
```

## Verify

# What this does: Runs a diagnostic that checks Python version, hermes
# installation, MCP dependencies, persona config, and channel
# connectivity. You should see all checks pass.
```bash
agentlife verify
```

## Next Steps

# What this does: Quick pointers once the install is up.
- Access your Hermes dashboard via Tailscale: `http://<vps-tailscale-ip>:9119`
- Set up Life Ops to track finances, calendar, and subscriptions

---

*Need help? Open an issue on GitHub or join the community Discord.*
