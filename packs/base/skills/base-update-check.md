---
name: base-update-check
description: "Check for new AgentLife pack versions and report updates available"
version: 0.1.0
author: Agentic Life
metadata:
  agentlife:
    persona: base
    tier: 1
    cron: pack-update-check
---

# Base Update Check

Checks for newer versions of installed persona packs. Called weekly by the `pack-update-check` cron job.

## What It Does

1. Queries the AgentLife GitHub repo for latest pack versions
2. Compares against locally installed versions
3. Reports available updates with changelog summaries

## Manual Use

```
Check for available AgentLife pack updates.
```

## Cron Integration

Configured automatically by the Base Pack. Runs weekly on Monday at 5 AM.