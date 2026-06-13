# AgentLife — VPS Install Guide

## Prerequisites

- A VPS (DigitalOcean, Hetzner, Linode, etc.) running Ubuntu 22.04+
- SSH access to your VPS
- A domain or Tailscale network for secure access
- Python 3.10+

## Step 1: Install Hermes Agent

SSH into your VPS and follow the [Hermes Agent install guide](https://hermes-agent.nousresearch.com/docs) for Linux.

## Step 2: Install AgentLife

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Step 3: Configure

```bash
agentlife setup
```

Select your persona(s) and use cases.

## Step 4: Secure Access

Set up [Tailscale](https://tailscale.com) or a reverse proxy (Caddy, Nginx) for secure remote access.

## Step 5: Verify

```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*