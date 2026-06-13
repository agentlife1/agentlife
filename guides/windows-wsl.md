# AgentLife — Windows (WSL2) Install Guide

## Prerequisites

- Windows 10 22H2+ or Windows 11
- WSL2 with an Ubuntu or Debian distro installed
- Python 3.10+

## Step 1: Install Hermes Agent

Open your WSL terminal and follow the [Hermes Agent install guide](https://hermes-agent.nousresearch.com/docs) for Linux.

## Step 2: Install AgentLife

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Step 3: Configure

```bash
agentlife setup
```

Select your persona(s) and use cases.

## Step 4: Verify

```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*