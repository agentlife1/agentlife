---
name: New Persona Pack —  Pull Request
about: Submit a new persona pack for AgentLife Framework
title: "feat(pack): <persona-name> persona pack"
labels: persona-pack
---

## Persona Pack: <!-- name -->

**Display Name:** <!-- how it appears in the setup UI -->
**Description:** <!-- one-line summary -->

### Checklist

**Config:**
- [ ] `config.yaml` has valid `persona`, `version`, `display_name`, `description`, `base: base`
- [ ] No hardcoded secrets, API keys, or credentials

**Skills:**
- [ ] At least 1 Hermes skill with valid YAML frontmatter
- [ ] Skills include manual-use prompts and cron integration docs

**Scripts:**
- [ ] All cron scripts are executable (`chmod +x`)
- [ ] Scripts use paths relative to framework root (`packs/<name>/scripts/`)
- [ ] Scripts handle errors gracefully (no silent failures)

**Validation:**
- [ ] `config-validate.py` passes: `✅ All N configs valid`
- [ ] `agentlife setup` shows the new persona
- [ ] `agentlife verify` passes all checks

**Documentation:**
- [ ] README explains who this persona is for and what use cases it enables

### Use Cases

<!-- List the use cases included in this pack -->

- [ ] <!-- use case 1 -->
- [ ] <!-- use case 2 -->

### Testing Notes

<!-- Describe how you tested this pack. What output did you see? -->

### Additional Context

<!-- Any relevant links, screenshots, or notes for reviewers -->