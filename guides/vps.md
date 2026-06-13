# AgentLife — VPS Install Guide

Install AgentLife on a cloud VPS (DigitalOcean, Hetzner, Linode, AWS EC2, etc.).

## Recommended Specs

| Provider | Plan | Cost |
|----------|------|------|
| DigitalOcean | Basic Droplet ($6/mo) — 1GB RAM, 25GB SSD | ~$6/mo |
| Hetzner | CX22 (~€4/mo) — 2GB RAM, 40GB SSD | ~$4/mo |
| Oracle Cloud | Free Tier — 1GB RAM, 100GB (free) | $0 |

## Prerequisites

- **Ubuntu 22.04 or 24.04** (recommended — other distros work but these have best support)
- **Python 3.10+**
- **SSH access** to your VPS

```bash
# SSH into your VPS first
ssh root@<your-vps-ip>

# Update system
apt update && apt upgrade -y

# Install Python and tools
apt install -y python3 python3-pip python3-venv curl

# Verify
python3 --version
```

## Option A: One-Liner Install

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Option B: Manual Install

### Step 1: Create a Non-Root User

```bash
adduser agentlife
usermod -aG sudo agentlife
su - agentlife
```

### Step 2: Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
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

### Step 6: Enable Auto-Start (Systemd)

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

### Step 7: Secure Access

**Recommended: Use Tailscale** — creates an encrypted tunnel so Hermes isn't exposed to the public internet.

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Find your VPS tailscale IP
tailscale ip -4
# → 100.x.x.x

# Access Hermes from your devices
# http://100.x.x.x:9119
```

**Alternative: Caddy reverse proxy with HTTPS**

```bash
# Install Caddy
apt install -y debian-keyring debian-archive-keyring
curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/gpg.key | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install caddy

# Configure reverse proxy
cat > /etc/caddy/Caddyfile << 'EOF'
your-domain.com {
    reverse_proxy localhost:9119
}
EOF

systemctl restart caddy
```

## Verify

```bash
agentlife verify
```

## Next Steps

- Access your Hermes dashboard via Tailscale: `http://<vps-tailscale-ip>:9119`
- Set up Life Ops to track finances, calendar, and subscriptions

---

*Need help? Open an issue on GitHub or join the community Discord.*