---
name: base-system-health
description: "Daily system health check — Hermes status, disk space, uptime, config validity"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: base
    tier: 1
    cron: daily-system-health
---

# Base System Health

Run this skill to perform a routine health check of your Hermes Agent + AgentLife installation. Called automatically by the `daily-system-health` cron job.

## Checks Performed

1. **Hermes process** — is the daemon running?
2. **Config valid** — are all YAML configs parseable?
3. **Disk space** — is the drive >80% full?
4. **Uptime** — how long since last restart?
5. **Cron jobs** — are scheduled jobs running on time?

## Manual Use

```
Run the system health check and report any issues.
```

## Cron Integration

Configured automatically by the Base Pack. Runs daily at 6 AM. Results delivered to the configured output channel.