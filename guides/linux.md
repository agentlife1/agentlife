# AgentLife — Linux Install Guide

## Prerequisites

- A Linux machine (Ubuntu 22.04+, Debian 12+, Fedora 38+, or similar)
- `curl` and `bash` available
- Python 3.10+

## Step 1: Install Hermes Agent

Follow the [Hermes Agent install guide](https://hermes-agent.nousresearch.com/docs) for your distro.

## Step 2: Install AgentLife

```bash
curl -sfSL https://agentlife.io/install.sh | bash
```

## Step 3: Configure

```bash
agentlife setup
```

Select your persona(s) and use cases. AgentLife will generate your Hermes config.

## Step 4: Verify

```bash
agentlife verify
```

---

*Need help? Open an issue on GitHub or join the community Discord.*