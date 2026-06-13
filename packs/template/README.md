# Persona Pack Template

Use this template to create a new persona pack for AgentLife.

## Structure

```
packs/<persona-name>/
├── config.yaml           # Persona configuration (required)
├── skills/               # Hermes skills this persona provides
│   └── <persona>-skill.md
├── scripts/              # Cron scripts (shell or Python)
│   └── example-job.sh
├── helpers/              # Helper scripts (Python)
│   └── example-helper.py
└── use-cases/            # Tier 3 use cases within this persona
    └── example-use-case.yaml
```

## 1. Config YAML (Required)

Create `packs/<persona-name>/config.yaml`:

```yaml
persona: <persona-name>
version: 0.1.0
display_name: "Display Name"
description: "Brief description of what this persona does"
base: base  # Inherits from the Base Pack

hermes:
  model:
    provider: openrouter
    model: deepseek/deepseek-v4-flash

skills:
  directories:
    - skills/<persona-name>/

cron:
  - name: example-job
    schedule: "0 9 * * 1"
    script: packs/<persona-name>/scripts/example-job.sh
    description: "Weekly example job"

use_cases: []  # Reference use cases by directory name

channels:
  local:
    enabled: true
```

## 2. Skills

Create Hermes skill files in `packs/<persona-name>/skills/`:

```yaml
---
name: <persona-name>-skill-name
description: "What this skill does"
version: 0.1.0
author: "Your Name"
metadata:
  agentlife:
    persona: <persona-name>
    tier: 2
    cron: example-job
---

# Skill Title

Describe what the skill does, when to use it, and what output to expect.

## Manual Use

```
Natural language prompt the user would say to trigger this.
```

## Cron Integration

Describe what cron jobs use this skill.
```

## 3. Use Cases (Optional)

Create `packs/<persona-name>/use-cases/<use-case>.yaml`:

```yaml
use_case: <use-case-id>
persona: <persona-name>
version: 0.1.0

cron:
  - name: example-cron
    schedule: "0 9 * * *"
    script: packs/<persona-name>/scripts/example.sh

config:
  setting_one: value
  setting_two:
    - item1
    - item2
```

## 4. Validation

Before submitting, validate your pack:

```bash
cd /path/to/agentlife/framework
python3 packs/base/scripts/config-validate.py
```

Expected: `✅ All N configs valid`

## 5. Testing

Test your pack installs correctly:

```bash
pip install -e .
agentlife setup  # Your persona should appear in the list
agentlife verify  # All checks should pass
```

## Checklist

Before submitting a PR:

- [ ] `config.yaml` has all required fields (persona, version, display_name, base)
- [ ] Skills have valid Hermes YAML frontmatter
- [ ] All cron scripts are executable (`chmod +x`)
- [ ] `config-validate.py` passes with zero errors
- [ ] `agentlife setup` shows your persona as an option
- [ ] `agentlife verify` passes
- [ ] README explains what the persona does
- [ ] No secrets, API keys, or credentials in configs