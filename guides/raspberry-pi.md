# AgentLife — Raspberry Pi Install Guide

## Prerequisites

- Raspberry Pi 4 or 5 running Raspberry Pi OS (64-bit)
- Python 3.10+

## Step 1: Install Hermes Agent

Follow the [Hermes Agent install guide](https://hermes-agent.nousresearch.com/docs) for ARM Linux.

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